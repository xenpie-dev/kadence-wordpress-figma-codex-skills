# Davis Drapery AI Development Guidance

This folder preserves the reusable, credentials-free development guidance from the Davis Drapery WordPress project.

## Contents

- `OVERVIEW.md`: project architecture, Figma design system, WordPress/Kadence environment, Drapery Builder ownership, data model, pricing boundaries, source-of-truth decisions, risks, and QA matrix.
- `code-vs-new-spreadsheet-audit.md`: evidence-based comparison of the builder formula implementation with the newer spreadsheet model.
- `backup-policy/`: instructions that keep live child-theme backup snapshots immutable.
- `spreadsheet-formula-reference/`: compact formula flow, dependencies, mismatch flags, workbook index, and parity test cases for AI-assisted pricing work.

## Exclusions

The repository intentionally excludes raw `.xlsx` workbooks, the multi-megabyte generated formula inventory, theme PHP backup snapshots, working theme code, screenshots, and generated sync/audit artifacts. Retrieve those from the original private project workspace when a task genuinely requires them.

Treat all URLs, WordPress IDs, plugin versions, and observed implementation details as project-specific snapshots that must be rechecked before live changes.
