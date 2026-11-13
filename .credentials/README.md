# .credentials/ — project secrets (git-ignored)

Everything in this folder **except this README and the `.example` file is ignored by git**
(see `.gitignore`). It never reaches GitHub.

## What goes here
- `credentials.yaml` — the real logins/keys for this project (copy from `credentials.example.yaml`)
- `gtm-container.json` — exported GTM container (may contain measurement IDs)
- Google service-account JSON, if the project uses one

## Rules (enforced by CLAUDE.md)
1. Claude may **read** a file here only when a task needs one specific secret, and must
   never copy a secret into chat, a commit, a Sheet, a Doc, or any file outside `.credentials/`.
2. Claude never writes a real secret into `credentials.yaml`; a human fills it in.
3. The tab `SEO Assets` in the Masterfile must only hold TRUE/FALSE + the account email,
   never a password. If Claude sees a password there, it flags it and does not copy it.

## Where real secrets should live long-term
A shared team password manager (1Password / Bitwarden), not this repo and not a Google Sheet.
This folder is a convenience for a running session, protected by `.gitignore`, not a vault.
