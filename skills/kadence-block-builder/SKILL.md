---
name: kadence-block-builder
description: Generate, convert, audit, and validate WordPress pages or templates as editable Kadence Blocks. Use whenever working on a WordPress site that uses Kadence/Kadence Blocks, including pages, Kadence Elements, headers, footers, landing pages, sliders/carousels, table-of-contents layouts, or converting custom HTML into native Kadence Row Layout, Column, Advanced Heading, Advanced Button, Image, Icon List, Table of Contents, Slider/Slide, Count Up, Google Maps, or related blocks without invalid block warnings.
---

# Kadence Block Builder

## Core Rule

Build Kadence pages as native Kadence blocks first. Do not use generic HTML, `core/html`, or custom DOM as the default implementation path.

Use scoped CSS only for visual tuning after the editable Kadence structure is correct. Do not use CSS or JavaScript to compensate for a missing native Kadence block. For example, use `kadence/slider` + `kadence/slide` for a carousel/slider, `kadence/tableofcontents` for a table of contents, and `kadence/iconlist` + `kadence/listitem` for bullet/icon lists before considering custom markup.

Treat Kadence block attributes as the source of truth for values a normal editor should be able to change in the visual editor. Put row/column padding, margins, section backgrounds, overlays, widths, alignment, text, images, buttons, icons, and lists in Kadence block settings whenever the block supports them. Do not hide those same editable values in WPCode CSS where they can override or stack with editor settings.

Use native Row Layout spacing, background, and overlay settings for editable section layout. For hero or band sections, set `kadence/rowlayout` attributes such as `padding`, `tabletPadding`, `mobilePadding`, `margin`, `bgImg`, `bgImgID`, `bgImgSize`, `bgImgPosition`, `bgImgRepeat`, `overlay`, and `overlayOpacity` instead of putting padding, `background: url(...)`, pseudo-element overlays, or image overlays in custom CSS. CSS may tune non-editable edge cases after the native Row Layout owns the primary spacing, image, or color.

Custom HTML is an exception that must be justified before implementation. It is allowed only when the live block registry confirms no native Kadence block can represent the required feature cleanly.

## Fast Path Exception

For small scoped WPCode typography, card-height, line-clamp, or responsive polish fixes where no Kadence block content or attributes will change, do not spend time on registry discovery or full block-generation checks. Do not use this fast path for Row Layout or Column padding, margins, editable backgrounds, or other values Kadence can expose to normal editors. Verify the rendered selectors, update the existing WPCode snippet and active `wpcode_snippets` cache together, then browser-check the affected desktop viewport plus mobile overflow. Return to the full workflow below as soon as content, structure, native block attributes, media ownership, editor-owned spacing/backgrounds, or invalid-content warnings are involved.

## Workflow

1. Inspect the target site before generating:
   - Always list registered `kadence/*` blocks with `WP_Block_Type_Registry` for the current site before selecting blocks. Treat bundled block references as a snapshot, not a substitute for the live registry.
   - Inspect existing Kadence block markup from the same site when available.
   - For dynamic Kadence blocks with a `render_callback` such as `kadence/modal`, inspect both saved block markup and the rendered front-end DOM. A block can parse and serialize cleanly while Kadence changes wrappers, classes, or inner layout at render time.
   - Inspect Row Layout and Column spacing/background attributes on existing sections before writing custom padding, margin, or background CSS.
   - Confirm Kadence Blocks and Kadence Blocks Pro versions if behavior matters.
2. List the native Kadence blocks to use before implementing. Include alternatives considered when a feature could be represented in multiple ways.
3. Select the smallest Kadence block set that fits the page:
   - Sections and editable section backgrounds: `kadence/rowlayout`
   - Layout columns: `kadence/column`
   - Text: `kadence/advancedheading`
   - Buttons: `kadence/advancedbtn` containing `kadence/singlebtn`
   - Images: `kadence/image`
   - Icons: `kadence/icon` containing `kadence/single-icon`
   - Lists: `kadence/iconlist` containing `kadence/listitem`
   - Table of contents: `kadence/tableofcontents`
   - Sliders/carousels: `kadence/slider` containing `kadence/slide`
   - Image cards: `kadence/imageoverlay`, `kadence/infobox`, or `kadence/image` with headings
   - Galleries/carousels of images: `kadence/advancedgallery`
   - Modal popups and bio overlays: `kadence/modal` containing native Kadence inner blocks
   - Stats: `kadence/countup` or Advanced Heading pairs only when Count Up is not appropriate
   - Maps: `kadence/googlemaps` when the map must be editable
4. Generate one section at a time.
5. Save the section/page.
6. Validate after every save:
   - `parse_blocks($post->post_content)`
   - `serialize_blocks(parse_blocks(...)) === $post->post_content`
   - no raw blocks
   - no `core/html` blocks unless explicitly justified in the response and unavoidable after registry review
   - `do_blocks($post->post_content)` renders without exceptions, especially after dynamic blocks or WPCode changes
   - no editor/front-end text containing `unexpected or invalid content`
7. Browser-check desktop and mobile after structural validation passes. For Figma-matched work, measure rendered element rectangles rather than relying on visual inspection alone.

## Generation Rules

- Use `scripts/kadence_blocks.py` for fragile blocks before hand-writing markup.
- Give every Kadence block a stable, unique `uniqueID`.
- Ensure saved HTML classes match the `uniqueID`.
- For `kadence/advancedheading`, the `htmlTag` attribute must match the saved HTML tag exactly.
- For paragraph/body text, use `htmlTag: "p"` and save a `<p>`.
- For headings, use the correct semantic tag: one page H1, section H2s, card H3s.
- Preserve `data-kb-block="kb-adv-heading{uniqueID}"` on Advanced Heading saved HTML.
- For section spacing, background images, colors, or overlays, use native `kadence/rowlayout` attributes first. Do not place padding, margins, background image URLs, colors, or overlays in CSS when Row Layout can own them.
- When converting existing CSS-owned values into Kadence block attributes, remove or narrow the old CSS override in the same change so the visual editor and front end do not have competing sources of truth.
- Avoid `core/group`, `core/heading`, `core/button`, and custom HTML when the user asked for a Kadence page.
- Use `core/html` only for assets that Kadence cannot represent cleanly, such as exact inline SVG snippets; document why it is used and which registered Kadence blocks were considered first.
- Do not build a carousel, slider, table of contents, gallery, accordion, tabs, icon list, testimonial set, map, or counter by using generic columns plus custom JavaScript/CSS when a native Kadence block for that pattern is registered.
- For `kadence/modal`, keep the trigger and modal content in the Modal block, and use native Kadence blocks inside the modal for images, headings, and paragraph text. Split deliberate Figma paragraph breaks into separate editable `kadence/advancedheading` paragraph blocks instead of one long paragraph with CSS spacing.
- When scoped CSS targets a dynamic Kadence block, target stable page/section classes and rendered `uniqueID` classes verified in the browser. Do not assume a saved wrapper class exists on the front end until measured.

## References

- Read `references/available-blocks.md` after checking the live registry when deciding which Kadence blocks are available on the MTI staging site.
- Read `references/patterns.md` before generating block markup.
- Read `references/validation.md` before writing to WordPress or when an invalid-content warning appears.

## Site Notes

The MTI staging site currently uses Kadence Child theme with Kadence Blocks 3.7.6, Kadence Blocks Pro 2.8.16, Kadence Theme Kit Pro 1.2.4, and Kadence Slider 2.3.7 active. Re-check versions on future sites before assuming identical markup.

For the MTI staging site, store unavoidable shared or scoped CSS, JavaScript, and PHP snippets in WPCode at `https://wordpress-339840-6492082.cloudwaysapps.com/wp-admin/admin.php?page=wpcode`, using a separate snippet for each purpose/type. Do not add new CSS to Appearance/Customizer Additional CSS, the `custom_css` post, block-level inline CSS, theme files, or ad hoc script/PHP injection unless the user explicitly requests that storage location.

For MTI page work, do not store editable Row Layout or Column padding/margins, section background colors/images/overlays, or block-owned text/media/button/icon/list values in WPCode when Kadence can own them. Normal editors should be able to open the visual editor, adjust the block, and see the front end follow that setting without hunting through CSS.

When editing WPCode snippets programmatically on MTI, update both the snippet post content and the active `wpcode_snippets` option cache, then clear caches. Otherwise the saved snippet can differ from the CSS served on the public page.
