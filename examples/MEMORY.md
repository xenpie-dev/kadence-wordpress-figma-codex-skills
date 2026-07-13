# MTI Project Memory Example

This example shows the small, credentials-free context file referenced by `AGENTS.md`. Keep the real project copy current with site decisions and reusable implementation facts.

## Active Site

- Working site: https://wordpress-339840-6492082.cloudwaysapps.com/

## Design Source

- Figma file: `OrK4KyQfdoR0WZBwxYQFxu` / MTI

## Durable Decisions

- Use native Kadence blocks as the editable source of truth whenever Kadence can represent the design.
- Keep Row Layout and Column spacing, backgrounds, overlays, widths, and alignment in Kadence block attributes.
- Keep text, images, buttons, icons, and lists editable in their corresponding blocks.
- Use WPCode only for narrowly scoped behavior or visual details Kadence cannot express cleanly.
- When moving a value from CSS into a Kadence block, remove or narrow the old CSS override in the same change.
- Record credentials-free page IDs, snippet IDs, Figma node IDs, stable marker names, plugin-version assumptions, and verification requirements that will save future agents from rediscovery.
- Preserve exact legal or regulated source copy unless the user explicitly authorizes editing it.
