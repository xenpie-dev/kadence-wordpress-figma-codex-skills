# Implementation Checklist

Use this reference when translating a Figma or screenshot reference into a Kadence WordPress page.

## Design Extraction

- Prefer a node-specific Figma URL. It lets the agent extract frame metadata, inspect the exact node, and compare a precise screenshot.
- Use a supplied PNG/JPG screenshot as a valid fallback. Name it as the reference source in the final response.
- Capture the viewport or frame size before comparing spacing. A 390 px mobile frame and a 1440 px desktop frame can require different Kadence responsive values.
- For reusable typography utilities, inspect Figma text styles or the typography guide rows for desktop, tablet, and mobile before writing CSS.
- Record numeric measurements for the important elements:
  - section top and bottom padding
  - heading-to-copy gaps
  - paragraph-to-paragraph gaps
  - prior content to next heading gaps
  - column widths and gutters
  - image crop, focal point, and overlay opacity
  - for modals: outer frame size, content-frame x/y, each column x/y/width/height, close-button x/y/size, and variant-specific offsets
  - paragraph breaks and text block boundaries, not only combined copy text
- Triage guide artifacts before implementation. Ignore Figma layout grids, Dev Mode measurement/ruler overlays, selection outlines, and pink/red column guides unless they are real named/exportable layers or the user confirms they are part of the design.
- If a repeated line/column/ruler-like detail might be intentional brand artwork, verify against the layer tree, a clean screenshot with guides hidden, or explicit user direction before recreating it in Kadence or WPCode CSS.

## Native Kadence Mapping

- Section, hero, full-width band, editable section padding/margins/backgrounds/overlays: `kadence/rowlayout`
- Layout columns and editable column padding/margins: `kadence/column`
- H1/H2/H3/body copy: `kadence/advancedheading`
- CTA: `kadence/advancedbtn` with `kadence/singlebtn`
- Inline or standalone image: `kadence/image`
- Icon bullets: `kadence/iconlist` with `kadence/listitem`
- Table of contents: `kadence/tableofcontents`
- Repeating image cards: `kadence/imageoverlay`, `kadence/infobox`, or `kadence/image` plus headings
- Modal popup: `kadence/modal` with native Kadence inner blocks for image, heading, role, and paragraph content

For section or hero backgrounds, use Row Layout background attributes:

```json
{
  "bgImg": "https://example.com/wp-content/uploads/image.png",
  "bgImgID": 123,
  "bgImgSize": "cover",
  "bgImgPosition": "center center",
  "bgImgRepeat": "no-repeat",
  "overlay": "#FFFFFF",
  "overlayOpacity": 80
}
```

Do not duplicate the same background image URL in custom CSS when Row Layout owns the image. Do not put Row Layout or Column padding/margins, editable backgrounds, overlays, widths, alignment, text, images, buttons, icons, or lists in CSS when Kadence can own them. CSS may tune non-editable edge cases, responsive wrappers, and typography where native Kadence settings are insufficient.

## Live Comparison

Use browser measurements rather than visual memory. Useful checks include:

```js
const rect = (selector) => document.querySelector(selector).getBoundingClientRect();
const gap = (a, b) => Math.round(rect(b).top - rect(a).bottom);
const style = (selector) => getComputedStyle(document.querySelector(selector));
```

Measure at least one desktop viewport and one mobile viewport. For legal/content pages, prioritize:

- H1 line wrapping and hero height
- body wrapper width
- H2 to first paragraph gap
- paragraph to paragraph gap
- final paragraph to next H2 gap
- sidebar/table-of-contents behavior
- horizontal overflow

For Figma-matched modals and cards, also compare:

- modal content width and height
- content frame offset from the modal container
- left and right column x/y/width/height
- image rendered width/height and crop position
- name, role, paragraph, and close-button rectangles
- paragraph count when Figma uses deliberate blank-line breaks

If desktop uses absolute positioning or fixed image sizes, run a mobile check after every CSS pass and explicitly reset `top`, `left`, `width`, and `height` where needed.

## WordPress Validation

Before calling the work done:

- `parse_blocks($post->post_content)` returns the expected block tree.
- `serialize_blocks(parse_blocks($post->post_content)) === $post->post_content`.
- There are no raw blocks.
- There are no `core/html` blocks unless unavoidable and documented.
- The page has one H1.
- Native background rows render with Kadence background classes and generated background-image CSS.
- Custom CSS does not contain duplicate background image URLs for Kadence-owned Row Layout backgrounds.
- Custom CSS does not override Row Layout or Column padding/margins, editable backgrounds/overlays, or other values a normal editor should control in Kadence.
- The live page has no visible invalid-content warning.
- Dynamic Kadence blocks, especially `kadence/modal`, render successfully through `do_blocks` and have their expected front-end DOM after clicking/opening.
- WPCode-backed styling is present in both the snippet post content and the active `wpcode_snippets` option cache when snippets are edited programmatically.
- WPCode typography utility snippets are published, cached in the expected location, and present in a public page response with any required tablet/mobile media queries.

## Reporting

Report the design source used, the pages changed, and the key measured before/after targets. If exact Figma extraction was not possible because no node URL was provided, say that the screenshot was used as the Figma reference.
