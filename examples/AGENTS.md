# MTI Project Guidelines

- Read `MEMORY.md` for current site context before making MTI website changes.
- Working site: `https://wordpress-339840-6492082.cloudwaysapps.com/`.
- Design source: Figma file `OrK4KyQfdoR0WZBwxYQFxu` / MTI.

## WordPress And Kadence

- Prefer native Kadence blocks as the editable source of truth.
- Use `kadence/rowlayout` for sections and editable backgrounds.
- Use `kadence/column` for layout, `kadence/advancedheading` for text, `kadence/image` for images, and Kadence button/icon/list blocks when available.
- Do not replace editable images, text, icons, spacing, or layout with CSS pseudo-elements, custom HTML, or hard-coded markup when a Kadence block can own it.
- Put editable layout and visual values in Kadence block attributes/settings whenever possible. Row/column padding, margins, section backgrounds, overlays, widths, alignment, text, images, buttons, icons, and lists should be editable in Gutenberg/Kadence instead of hidden in WPCode CSS.
- Before adding WPCode CSS for a page or section, check whether the same value can live in the relevant Row Layout, Column, Advanced Heading, Image, Button, Icon, or List block. Avoid CSS that overrides or stacks with values a normal editor can change visually.
- When moving an existing visual value from CSS into Kadence block attributes, remove or narrow the old CSS override so the visual editor remains the source of truth.
- Use WPCode CSS only for visual details Kadence cannot express cleanly, such as exact ruler ticks, responsive polish, or small section-specific overrides.
- Keep any unavoidable WPCode CSS scoped to the affected page/section and named clearly.
