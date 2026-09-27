"""Stage published chapters and diagrams; never edit a source README."""
from pathlib import Path
import html
import json
import os
import re
import shutil
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / ".website-build" / "content"
NUMBERED = re.compile(r"^\d{2}-[a-z0-9-]+$")
ASSET_TYPES = {".html", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".css", ".js", ".json", ".txt", ".pdf"}
MODULE_NAMES = {"01-langchain": "LangChain", "02-mcp": "MCP", "03-langgraph": "LangGraph", "04-embeddings-vector-stores": "Embeddings and vector stores", "05-rag": "RAG", "06-agentic-rag": "Agentic RAG", "07-evals": "Evaluations", "08-observability-tracing": "Observability and tracing", "09-safety-pii-guardrails": "Safety, PII, and guardrails", "10-human-in-the-loop": "Human in the loop", "11-multi-agent-systems": "Multi-agent systems", "12-production-agentic-ai": "Production agentic AI"}

def read_title(path):
    text = path.read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip(), text
    return path.parent.name.replace("-", " ").title(), text

def write(relative, text):
    target = STAGE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")

def copy_diagrams(topic):
    folder = topic / "diagrams"
    if not folder.is_dir():
        return
    for source in sorted(folder.rglob("*")):
        if not source.is_file() or source.is_symlink():
            continue
        relative = source.relative_to(ROOT)
        if any(part.startswith(".") for part in relative.parts) or source.suffix.lower() not in ASSET_TYPES:
            continue
        destination = STAGE / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

def visual_guide(relative, title, spec):
    lines = [f"# {title} — Interactive diagrams", "", "Choose a diagram below. Use its controls to zoom, focus on a node, or follow a path.", "", f"[Read the chapter](README.md)", ""]
    for diagram in spec["diagrams"]:
        filename = diagram["file"]
        source = (ROOT / relative / filename).resolve()
        if not source.is_relative_to(ROOT / relative) or not source.is_file():
            raise ValueError(f"Missing diagram: {relative}/{filename}")
        safe_title = html.escape(diagram["title"], quote=True)
        safe_url = quote(filename, safe="/.-_")
        lines.extend([
            f"## {diagram['title']}", "", diagram["text"], "",
            f'<a href="{safe_url}" target="_blank" rel="noopener">Open this diagram full screen ↗</a>', "",
            '<p class="diagram-fallback">Open the full-screen view to explore this diagram on a smaller screen.</p>', "",
            f'<iframe class="diagram-frame" src="{safe_url}" title="{safe_title}" loading="lazy"></iframe>', "",
        ])
    lines.extend(["## About these diagrams", "", "These are conceptual illustrations. They do not call a model or report measured performance.", "", "Diagrams use [Archify](https://github.com/tt-a1i/archify). [Attribution and license](../../credits.md).", ""])
    return "\n".join(lines)

def on_config(config):
    if STAGE.is_symlink():
        raise ValueError("The generated content directory must not be a symlink")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copytree(ROOT / "website" / "assets", STAGE / "assets")
    write("README.md", (ROOT / "website" / "home.md").read_text(encoding="utf-8"))
    write("credits.md", (ROOT / "website" / "credits.md").read_text(encoding="utf-8"))
    shutil.copy2(ROOT / "website" / "ARCHIFY-LICENSE.txt", STAGE / "ARCHIFY-LICENSE.txt")
    specs = json.loads((ROOT / "website" / "visuals.json").read_text(encoding="utf-8"))
    nav = [{"Start here": "README.md"}]
    published_topics = set()
    for module in sorted(ROOT.iterdir()):
        if not module.is_dir() or module.is_symlink() or not NUMBERED.fullmatch(module.name):
            continue
        topics = [p for p in sorted(module.iterdir()) if p.is_dir() and not p.is_symlink() and NUMBERED.fullmatch(p.name) and (p / "README.md").is_file()]
        if not topics:
            continue
        module_name = MODULE_NAMES.get(module.name, module.name[3:].replace("-", " ").title())
        section = [{"Overview": f"{module.name}/README.md"}]
        overview = [f"# {module_name}", "", "Choose a chapter:", ""]
        for topic in topics:
            relative = topic.relative_to(ROOT).as_posix()
            title, content = read_title(topic / "README.md")
            overview.append(f"- [{title}]({topic.name}/README.md)")
            copy_diagrams(topic)
            if relative in specs:
                title = specs[relative]["title"]
                # Add this only to the generated website copy.
                content += '\n\n<div class="visual-link" markdown="1">\n\n[Explore the interactive diagrams](visual-guide.md)\n\n</div>\n'
                write(f"{relative}/visual-guide.md", visual_guide(relative, title, specs[relative]))
                section.append({title: [{"Explanation": f"{relative}/README.md"}, {"Interactive diagrams": f"{relative}/visual-guide.md"}]})
            else:
                section.append({title: f"{relative}/README.md"})
            write(f"{relative}/README.md", content)
            published_topics.add(relative)
        write(f"{module.name}/README.md", "\n".join(overview) + "\n")
        nav.append({module_name: section})
    missing = set(specs) - published_topics
    if missing:
        raise ValueError("Diagram configuration has no chapter README: " + ", ".join(sorted(missing)))
    nav.append({"Credits": "credits.md"})
    config["nav"] = nav
    site_url = os.environ.get("SITE_URL", "").strip()
    if site_url:
        config["site_url"] = site_url.rstrip("/") + "/"
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        config["repo_url"] = f"https://github.com/{repo}"
        config["repo_name"] = repo
        config["edit_uri"] = ""
    config["watch"].extend([str(ROOT / "website")] + [str(p) for p in ROOT.iterdir() if p.is_dir() and not p.is_symlink() and NUMBERED.fullmatch(p.name)])
    return config
