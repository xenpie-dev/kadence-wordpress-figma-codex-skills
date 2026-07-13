# kadence-wordpress-figma-codex-skills

Reusable Codex skills and AI guidance for translating Figma designs into editable WordPress pages built with native Kadence Blocks.

## Included skills

- `figma-to-kadence`: coordinates design extraction, native Kadence implementation, scoped WPCode fallback styling, and responsive browser QA.
- `kadence-block-builder`: generates, converts, audits, and validates editable Kadence block markup, with a small Python helper for fragile block structures.

The `examples/AGENTS.md` file shows how a project can enforce the central rule: editable content and visual values belong in Kadence block settings whenever Kadence can represent them.

## Project guidance examples

- `projects/davis-drapery/`: AI-ready context for a template-driven Kadence child-theme configurator, including Figma design-system facts, WordPress ownership boundaries, feature-development guidance, spreadsheet formula references, QA risks, and backup-snapshot safety rules.

## Core principles

- Use `kadence/rowlayout` for sections, spacing, backgrounds, and overlays.
- Use `kadence/column`, `kadence/advancedheading`, `kadence/image`, and native Kadence button, icon, list, slider, table-of-contents, counter, map, and query blocks when available.
- Keep editor-owned text, images, layout, spacing, colors, backgrounds, and overlays in block attributes.
- Use scoped WPCode CSS or JavaScript only for details Kadence cannot express cleanly.
- Remove or narrow older CSS rules when their values move into Kadence settings.
- Validate Gutenberg parsing/serialization and check desktop and mobile output after meaningful changes.

## Install

Copy either skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\figma-to-kadence "$HOME\.codex\skills\figma-to-kadence"
Copy-Item -Recurse .\skills\kadence-block-builder "$HOME\.codex\skills\kadence-block-builder"
```

Restart Codex or begin a new task so the skills catalog refreshes.

## Use

Invoke the skills directly when needed:

```text
Use $figma-to-kadence to implement this Figma section as native Kadence blocks.
Use $kadence-block-builder to audit this WordPress block markup for invalid or non-editable content.
```

`figma-to-kadence` requires `kadence-block-builder` for Kadence block generation and validation work.

## Project-specific notes

These skills originated in the MTI WordPress project. Some references intentionally retain MTI staging-site examples, page conventions, WPCode workflow details, and observed Kadence versions. Re-check the target site's registered blocks, plugin versions, IDs, selectors, and snippet storage before applying those details elsewhere.

No credentials, WordPress exports, screenshots, or captured production HTML are included.
