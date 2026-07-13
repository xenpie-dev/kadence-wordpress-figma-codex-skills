# Kadence Markup Patterns

Use these patterns as the minimum safe saved markup. Prefer inspecting a fresh block from the same site for new block types.

## Advanced Heading

Required consistency:

- Comment block name: `wp:kadence/advancedheading`
- Attribute `uniqueID`: used in saved class `kt-adv-heading{uniqueID}`
- Attribute `htmlTag`: must equal the saved HTML tag
- Saved class: `kt-adv-heading{uniqueID} ... wp-block-kadence-advancedheading`
- Saved attribute: `data-kb-block="kb-adv-heading{uniqueID}"`

Example paragraph:

```html
<!-- wp:kadence/advancedheading {"uniqueID":"46_74f58d-51","htmlTag":"p","className":"mti-copy"} -->
<p class="kt-adv-heading46_74f58d-51 mti-copy wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading46_74f58d-51">Vehicle Diagnostics &amp; Inspection</p>
<!-- /wp:kadence/advancedheading -->
```

Example link paragraph:

```html
<!-- wp:kadence/advancedheading {"uniqueID":"46_74f58d-51","htmlTag":"p","className":"mti-footer-link-text"} -->
<p class="kt-adv-heading46_74f58d-51 mti-footer-link-text wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading46_74f58d-51"><a href="https://example.com/services/">Vehicle Diagnostics &amp; Inspection</a></p>
<!-- /wp:kadence/advancedheading -->
```

## Image

```html
<!-- wp:kadence/image {"id":44,"width":124,"height":124,"sizeSlug":"full","uniqueID":"mtiFooterLogoKb","className":"mti-footer-logo-block"} -->
<figure class="wp-block-kadence-image kb-imagemtiFooterLogoKb size-full is-resized mti-footer-logo-block"><img src="https://example.com/logo.png" alt="Manufacturing Technologies, Inc." class="kb-img wp-image-44" width="124" height="124"/></figure>
<!-- /wp:kadence/image -->
```

Use `is-resized` only when width or height is present.

## Row Layout And Column

Observed site pattern:

```html
<!-- wp:kadence/rowlayout {"uniqueID":"mtiSectionKb","columns":2,"colLayout":"equal","htmlTag":"section","inheritMaxWidth":true,"kbVersion":2,"className":"mti-section"} -->
<!-- wp:kadence/column {"uniqueID":"mtiSectionCol1Kb","kbVersion":2,"className":"inner-column-1 mti-section-copy"} -->
<div class="wp-block-kadence-column kadence-columnmtiSectionCol1Kb inner-column-1 mti-section-copy"><div class="kt-inside-inner-col">
...
</div></div>
<!-- /wp:kadence/column -->
<!-- /wp:kadence/rowlayout -->
```

After generating row/column markup, validate on the target site. Kadence may add row wrapper HTML in the editor/frontend depending on version, so use existing site output whenever possible.

## Row Layout Background Image And Overlay

Use native `kadence/rowlayout` attributes for hero and section backgrounds instead of inlining `background-image` in CSS. This keeps the background editable in Kadence and lets Kadence generate the front-end `kt-row-has-bg` and `.kt-row-layout-overlay` CSS.

Simple editable hero background:

```html
<!-- wp:kadence/rowlayout {"uniqueID":"mtiLegalHeroRowKb","columns":1,"colLayout":"equal","htmlTag":"section","inheritMaxWidth":true,"kbVersion":2,"bgImg":"https://example.com/hero.png","bgImgID":70,"bgImgSize":"cover","bgImgPosition":"center 38%","bgImgAttachment":"scroll","bgImgRepeat":"no-repeat","overlay":"#FFFFFF","overlayOpacity":78,"className":"mti-legal-hero"} -->
<!-- wp:kadence/column {"id":1,"uniqueID":"mtiLegalHeroColKb","kbVersion":2,"className":"inner-column-1 mti-legal-hero-col"} -->
<div class="wp-block-kadence-column kadence-columnmtiLegalHeroColKb inner-column-1 mti-legal-hero-col"><div class="kt-inside-inner-col">
...
</div></div>
<!-- /wp:kadence/column -->
<!-- /wp:kadence/rowlayout -->
```

Use custom CSS for layout tuning only, such as `min-height`, padding, row width, typography, or responsive spacing. Do not duplicate the same image URL in CSS. For gradient overlays, first inspect a fresh generated Row Layout sample from the same site; do not guess fragile opacity or gradient attributes.

## Advanced Button

Use `kadence/advancedbtn` with one or more `kadence/singlebtn` children. If the exact saved HTML is unknown for the site, create one sample in the editor or inspect an existing button before mass generation.

Core idea:

```html
<!-- wp:kadence/advancedbtn {"uniqueID":"mtiButtonsKb","btnCount":1,"className":"mti-button-row"} -->
<div class="wp-block-kadence-advancedbtn kb-buttons-wrap kb-btnsmtiButtonsKb mti-button-row">
<!-- wp:kadence/singlebtn {"uniqueID":"mtiButton1Kb","text":"Request a Consultation","link":"https://example.com/contact/"} /-->
</div>
<!-- /wp:kadence/advancedbtn -->
```

If this self-closing `singlebtn` does not validate on the target site, inspect a generated button and update the helper script before proceeding.

## Kadence Modal

Use `kadence/modal` for popup interactions when it is registered. Keep both the visible trigger and popup content in the Modal block, and place editable Kadence blocks inside the modal content.

Practical rules:

- Inspect a same-site Modal sample before hand-writing one; Kadence Modal is dynamic and renders through a callback.
- Validate with `parse_blocks`, `serialize_blocks`, and `do_blocks`. Structural validity does not prove the front-end DOM matches the saved markup.
- Inspect the rendered modal DOM in a browser before writing CSS selectors. Kadence can flatten, add, or alter wrappers and classes for inner Row Layout/Column blocks.
- Use stable `uniqueID`-derived rendered classes such as `.kadence-column{uniqueID}` or `kt-adv-heading{uniqueID}` after confirming they exist on the front end.
- Keep modal bios, paragraphs, names, roles, and images editable as `kadence/advancedheading` and `kadence/image`; use scoped CSS only for measured positioning, crop, trigger styling, and responsive polish.
- If Figma provides a precomposed modal art asset that already combines background, overlay, and cutout, let `kadence/image` own that asset rather than reconstructing the same composite with pseudo-elements.
- Map intentional Figma paragraph breaks to separate Advanced Heading paragraph blocks. This keeps spacing editable and prevents one long paragraph from hiding line-break mismatches.
- For responsive overrides after absolute desktop positioning, reset `position`, `top`, `left`, `width`, and `height`; do not assume `height:auto` overrides a more specific desktop selector.

For MTI WPCode CSS, keep modal rules scoped with `.page-id-116` and the modal-specific class such as `.mti-about-kb-bio-modal-tony`. When updating a WPCode snippet through PHP, update the `wpcode_snippets` option cache as well as the snippet post.
