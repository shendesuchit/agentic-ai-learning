# Open the starter and make your first checkpoint

These instructions assume Windows, VS Code, and GitHub Desktop. Work from the
repository's main folder—the one containing this file and `pyproject.toml`.
You do not need an API key for this setup or for orientation.

## 1. Extract the ZIP

Right-click the downloaded ZIP and choose **Extract All**. Open the extracted
`agentic-ai-learning` folder. Keep this as the source copy for the next step.
Do not work from inside the ZIP preview.

## 2. Create your local repository in GitHub Desktop

For a new repository:

1. Sign in to GitHub Desktop. Choose **File → New repository**.
2. Use `agentic-ai-learning` as the name and, for example, `C:\Learning` as
   the local parent path. Desktop will create `C:\Learning\agentic-ai-learning`.
3. Leave README initialization unchecked, and choose **None** for Git ignore
   and License. The starter already supplies its README and ignore rules.
4. Create the repository. Copy all the **contents** of the extracted starter
   folder into the new repository folder, including `.vscode`, `.gitignore`,
   `.env.example`, and `.python-version`. Keep the `.git` folder Desktop created.

Check that `README.md` is directly inside `C:\Learning\agentic-ai-learning`.
There should not be another `agentic-ai-learning` folder nested inside it.
The ZIP deliberately has no Git history; commits should belong to your account.

If you already created this repository on GitHub, clone it in Desktop instead
and copy the starter contents into that clone. Review any existing files before
replacing them. Do not create a second remote repository for the same work.

## 3. Open the repository in VS Code

Use **File → Open Folder** in VS Code and choose the new repository folder.
Install the recommended Microsoft Python and Pylance extensions when prompted.
You can also find them in Extensions. The recommendations are included in
`.vscode/extensions.json`; they do not install themselves.

For a direct Desktop shortcut, set **File → Options → Integrations → External
editor** to Visual Studio Code, then use **Repository → Open in Visual Studio Code**.

## 4. Prepare Python

Open a PowerShell terminal in VS Code. If uv is not installed, run:

```powershell
winget install --id=astral-sh.uv -e
```

Restart VS Code after installation so its terminal sees the updated PATH.
If WinGet is unavailable, use the official uv installation guide linked below.
Then run these commands from the repository root:

```powershell
uv --version
uv python install 3.11
uv sync
uv run python --version
```

The last command should report Python 3.11.x. `uv sync` creates `.venv` using
the committed `uv.lock`; `.venv` is ignored. Provider SDKs are optional, so a
plain `uv sync` does not install them. Do not run `uv init`: this project is
already configured.

Press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and select the
interpreter in this repository's `.venv`. If necessary, browse to
`.venv\Scripts\python.exe`. The included settings point to `.venv`, but a
previously selected interpreter may need to be changed manually.

We will normally run experiments with `uv run` from the repository root.
There is no need to activate a PowerShell environment script for those commands.

## 5. Environment variables, when needed

The example file lists supported provider key names with empty values. Copy it
once, then fill only the key for the provider you will use:

```powershell
Copy-Item .env.example .env
```

Do not repeat this copy over a populated `.env`. The real `.env` is ignored by
Git. Keep only empty values and explanatory comments in `.env.example`.
The experiment command uses `uv run --env-file .env` to load your selected key;
ordinary Python execution does not load `.env` automatically.

## 6. Save the foundation checkpoint

In GitHub Desktop, review the **Changes** tab. Confirm that `.env` and `.venv`
are absent. Include `uv.lock` if you have completed the environment setup.

Use this commit summary:

```text
chore: establish agentic ai learning foundation
```

Commit to `main` (check the selected branch name). If this is a new local
repository, choose **Publish repository** and choose its visibility. If it was
cloned from GitHub, choose **Push origin**. Publishing creates the remote;
committing saves a local checkpoint; pushing uploads subsequent commits.

Desktop may already have created an initial commit. That is fine: this commit
records the learning starter. No topic is complete simply because its folder exists.

## 7. Begin learning

Open [Orientation](01-langchain/00-orientation/README.md). After studying it,
answer the questions in your own words before marking its checklist complete.
Use the [module page](01-langchain/README.md) to record progress.

## If something does not work

| What you see | What to check |
|---|---|
| `uv` is not recognized | Restart VS Code; confirm uv installation completed. |
| Python cannot be downloaded | Check network access, then retry `uv python install 3.11`. |
| VS Code uses a different Python | Select this repository's `.venv` interpreter. |
| Desktop shows no files | Confirm VS Code and Desktop point to the same folder. |
| Desktop says the extracted folder is not a repository | Use step 2; a ZIP has no `.git` history. |
| PowerShell blocks `Activate.ps1` | Use `uv run`; activation is unnecessary for this workflow. |

## Repository validation

Run the [validator](scripts/validate.py) from the repository root before a
topic checkpoint. It never installs dependencies or calls providers.

FAST and STANDARD use the root uv learning environment. These commands preserve
its installed packages and avoid network access by uv or lockfile changes:

```powershell
uv --no-cache --offline --no-python-downloads run --no-sync python -B scripts/validate.py fast
uv --no-cache --offline --no-python-downloads run --no-sync python -B scripts/validate.py standard
```

FULL uses the dedicated Python 3.11 website environment instead:

```powershell
.\website\.venv\Scripts\python.exe -B scripts/validate.py full
```

Keep website packages separate so they cannot conflict with learning dependencies
or be removed by a learning-environment synchronization. No activation is needed;
Git and uv must remain on PATH. Plain `uv run` may synchronize the root environment
before validation, so use the no-sync commands above.

One-time website provisioning, when explicitly requested:

```powershell
.\.venv\Scripts\python.exe -B -m venv website/.venv
.\website\.venv\Scripts\python.exe -m pip install -r website/requirements.txt
```

The root interpreter must be Python 3.11. Creation does not install website
packages into the root environment. The existing `.venv/` Git ignore rule covers
`website/.venv`; no new dependency file or lockfile is needed.

- **FAST:** Git state (pending edits are allowed), Python version, TOML parsing,
  tracked Python syntax, forbidden credential/environment filenames, and generated
  output conventions. The validator checks itself even before it is staged.
- **STANDARD:** FAST plus offline `uv lock --check`, conservative redacted secret
  scanning of tracked working-copy and staged text, required website files,
  diagram JSON/HTML, navigation inventory, and advisory progress checks.
- **FULL:** STANDARD plus the existing strict `website/build.py build` and checks
  for expected generated pages and diagrams. Request this mode explicitly: it
  regenerates `.website-build/content` and `.website-build/site`. It never deploys.

FAST and STANDARD do not write repository files or synchronize the environment.
The uv check can use operating-system temporary storage. FULL preserves the
existing website pip/`website/requirements.txt` setup and requires those pinned
packages to be installed in the interpreter running the validator. Missing
prerequisites fail with a diagnostic; nothing is installed automatically.

PASS or WARN-only runs exit 0; any FAIL exits nonzero. Provider experiments are
reported as SKIP and do not fail validation. The offline experiment allowlist is
currently empty; new entries require an explicit review for provider calls,
network access, and file writes. uv's offline flag does not sandbox Python code.

Checks primarily cover tracked files, including staged additions. Stage new topic
files yourself before final validation; unstaged new topic files are not validated.
Working-copy syntax and website checks do not prove a partially staged commit is
valid. Source hashes and Git state are compared before and after each run.

Secrets are never printed, and real `.env` files are never read. Suspected secrets
fail pending human review; diagnostics show only location and never the value.
This is a conservative text scan, not a comprehensive security audit. Subprocess
output is withheld because tools can print sensitive information.

Static website checks cover this repository's current conventions, not arbitrary
YAML or Markdown. FULL delegates configuration, plugin, and rendered Markdown-link
validation to MkDocs; external URLs and interactive diagram behavior are not
tested. Progress warnings cannot establish learner understanding. Do not fix
unrelated findings automatically or treat validation as permission to commit,
push, dispatch a workflow, or publish.

## Official setup references

- [GitHub Desktop: create a repository](https://docs.github.com/en/desktop/overview/creating-your-first-repository-using-github-desktop)
- [GitHub Desktop: add an existing local Git repository](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop)
- [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- [uv project workflow](https://docs.astral.sh/uv/guides/projects/)
- [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)

Setup references checked on 26 September 2026. Menu wording may vary slightly
between versions.
