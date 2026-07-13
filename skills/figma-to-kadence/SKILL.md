---
name: figma-to-kadence
description: Use when Codex needs to implement, tune, or audit WordPress/Kadence pages from Figma, screenshots, or Figma typography specs; compare live spacing, typography, imagery, or responsive behavior; create reusable WPCode-backed typography utility classes; or convert designs into native Kadence blocks while avoiding inline CSS for features Kadence supports.
---

# Figma to Kadence

## Core Rule

Use this skill to coordinate design extraction, WordPress/Kadence implementation, and live browser QA. This skill does not replace `kadence-block-builder`; load and follow that skill before writing or validating Kadence block content.

Prefer native Kadence block attributes over custom CSS. Editable values a normal WordPress editor should change visually, including Row Layout/Column padding and margins, section backgrounds, overlays, widths, alignment, text, images, buttons, icons, and lists, belong in Kadence settings instead of WPCode CSS. In particular, use Row Layout spacing, background image, and overlay settings for section/hero backgrounds instead of placing padding, `background-image` URLs, pseudo-element overlays, or image overlays in inline/shared CSS.

For the MTI staging site, put unavoidable shared or scoped CSS, JavaScript, and PHP snippets in WPCode at `https://wordpress-339840-6492082.cloudwaysapps.com/wp-admin/admin.php?page=wpcode`, using a separate snippet for each purpose/type. Do not add new CSS to Appearance/Customizer Additional CSS, the `custom_css` post, block-level inline CSS, theme files, or ad hoc script/PHP injection unless the user explicitly asks for that location.

## Fast Path: Scoped Style Tuning

For small typography, card height, line clamp, or responsive polish fixes where the Kadence structure is already correct and only WPCode CSS/JS will change, use `references/fast-style-tuning.md` instead of the full implementation checklist. Keep the fast path narrow: use it only for rendered-selector tuning, not for page content edits, native block attribute edits, editor-owned Row Layout/Column spacing or backgrounds, new sections, new assets, or invalid-content repair.

## Workflow

1. Establish the design source.
   - If the user provides a Figma URL with a file and node, load the Figma usage skill before any Figma tool call, then extract design context and a screenshot for the exact node.
   - If the user provides only a screenshot or cropped image, inspect the image directly and state that the screenshot is the design reference.
   - If the user provides only a live URL and says to match Figma, ask for the node-specific Figma URL only when exact extraction is required and not otherwise available.
2. Capture measurable design details.
   - Record frame size, desktop/mobile breakpoint assumptions, section widths, row/column gaps, vertical spacing callouts, typography, colors, image crop/position, and overlays.
   - For spacing-sensitive work, measure actual distances from the Figma node or screenshot rather than relying on visual impression alone.
   - Classify guide-like artifacts before implementing them. Treat Figma layout grids, Dev Mode measurement/ruler overlays, selection outlines, and pink/red column guides as non-page aids unless they are actual named/exportable layers or the user explicitly confirms they are intended artwork.
   - Do not recreate guide artifacts as Kadence backgrounds or WPCode CSS. If a mark could be either a guide or a visual motif, verify it against the layer tree, a clean screenshot with guides hidden, or the user's direction before implementing it.
   - For modal/card nodes, record the outer frame size, content frame position, column x/y/width/height, close-button position, paragraph breaks, and any variant-specific offsets.
3. Inspect the live WordPress page.
   - Open the target URL in a browser at relevant desktop and mobile widths.
   - Measure current rendered gaps, container widths, font sizes, line heights, image positions, and overflow.
   - Inspect the WordPress page content and registered Kadence blocks before changing markup.
4. Map the design to native Kadence.
   - Use `kadence/rowlayout` for sections, full-width bands, container width, padding, margins, background image, background color, and overlay.
   - Use `kadence/column` for layout columns, editable column padding, and margins.
   - Use `kadence/advancedheading` for headings and paragraph text.
   - Use `kadence/image`, `kadence/advancedbtn`, `kadence/iconlist`, `kadence/tableofcontents`, and other native blocks when they match the design need.
   - Use scoped CSS only for tuning that Kadence cannot express cleanly, such as shared legal-page gap rules or responsive edge-case fixes.
5. Implement in small passes.
   - Update structure first, then visual attributes, then small CSS adjustments if needed.
   - When moving a visual value from WPCode CSS into Kadence attributes, remove or narrow the old CSS rule in the same pass so editor settings do not stack with CSS overrides.
   - Keep editable Kadence block markup stable and avoid raw blocks or `core/html` unless no native block can represent the requirement.
   - For spacing and background images, set Row Layout attributes such as `padding`, `tabletPadding`, `mobilePadding`, `margin`, `bgImg`, `bgImgID`, `bgImgSize`, `bgImgPosition`, `bgImgRepeat`, `overlay`, and `overlayOpacity`.
6. Validate WordPress content.
   - Confirm `parse_blocks` and `serialize_blocks(parse_blocks(...))` are stable.
   - Confirm expected Kadence block counts, one H1 per page, no raw blocks, and no `core/html` blocks unless explicitly justified.
   - Confirm the editor/front end does not show invalid-content warnings.
7. Compare live site to the design.
   - Browser-check desktop and mobile after each meaningful pass.
   - Measure key design targets numerically: heading-to-copy gaps, paragraph-to-paragraph gaps, section spacing, container width, hero height, image background behavior, modal frame size, modal column geometry, and close-button position.
   - Confirm no horizontal overflow, clipped text, orphaned button text, or unintended layout shifts.

## Figma Typography Utility CSS Flow

Use this flow when the user asks for callable Figma typography CSS classes, responsive font utilities, or a WPCode font snippet.

1. Read project memory first on MTI work, then inspect the exact Figma typography node or local text styles. Do not guess font sizes, weights, line heights, letter spacing, or responsive values.
2. Extract desktop, tablet, and mobile typography rows separately when the Figma guide includes breakpoint columns. If the responsive rows match desktop, still add explicit media-query blocks and note that Figma currently matches values across breakpoints.
3. Convert Figma style names to kebab-case utility selectors, for example `Big Body Bold` -> `.big-body-bold`. Add practical aliases when the design name is ambiguous, such as `.small-body` plus `.small-body-regular`, or `.xtra-small-body`, `.xs-body`, and `.extra-small-body`.
4. Keep utility declarations focused: `font-family`, `font-size`, `font-style`, `font-weight`, `line-height`, `letter-spacing`, and `text-transform`. Use `Artific Trial` body fallbacks from MTI memory unless the Figma row specifies another family.
5. Store shared utility CSS in the requested WPCode CSS snippet. When editing WPCode programmatically on MTI, update the snippet through `WPCode_Snippet`, keep it published/site-wide, rebuild `wpcode_snippets`, and clear caches.
6. Verify the saved snippet post content, the active WPCode cache entry, and a public page response all contain the expected classes and responsive media blocks before reporting completion.

## References

Read `references/fast-style-tuning.md` for MTI scoped WPCode typography/spacing/card polish where existing Kadence blocks remain unchanged.
Read `references/implementation-checklist.md` before structural page updates, native Kadence block changes, new sections/assets, or broader Figma-to-Kadence audits. It contains the measurement checklist, native Kadence mapping reminders, and final QA contract.
