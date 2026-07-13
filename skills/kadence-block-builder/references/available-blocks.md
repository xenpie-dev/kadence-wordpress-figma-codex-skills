# Available Kadence Blocks

Source: MTI staging site, WordPress block registry, Kadence Blocks 3.7.6 and Kadence Blocks Pro 2.8.16.

This file is a snapshot. Always check the current live registry with `WP_Block_Type_Registry` before choosing blocks or writing content.

Use native Kadence blocks before custom HTML, `core/html`, custom JavaScript, or generic columns styled into another widget. If the feature exists below and is registered on the live site, use it as the structural block.

## Page-Building Core

- `kadence/rowlayout` - Row Layout. Use for every major section and for editable section background images, colors, and overlays before custom CSS.
- `kadence/column` - Section/column. Use only inside Row Layout unless inspecting site output shows another valid pattern.
- `kadence/advancedheading` - Advanced Text. Use for all headings, paragraphs, labels, links, and small text.
- `kadence/advancedbtn` - Advanced Button wrapper.
- `kadence/singlebtn` - Single button child inside `kadence/advancedbtn`.
- `kadence/image` - Advanced Image.
- `kadence/spacer` - Spacer / Divider.
- `kadence/icon` - Icon wrapper.
- `kadence/single-icon` - Single Icon child inside `kadence/icon`.
- `kadence/iconlist` and `kadence/listitem` - Editable icon lists.
- `kadence/tableofcontents` - Editable/generated table of contents. Use for TOC patterns before manual linked text.
- `kadence/slider` and `kadence/slide` - Editable slider/carousel. Use for sliders before columns plus custom drag/scroll JavaScript.

## Useful For MTI Pages

- `kadence/countup` - Animated stat numbers.
- `kadence/googlemaps` - Editable Google Maps embeds.
- `kadence/advancedgallery` - Image galleries or logo galleries.
- `kadence/infobox` - Icon/text cards when a simple card is needed.
- `kadence/imageoverlay` - Image cards with overlay copy.
- `kadence/splitcontent` - Two-panel media/content layouts.
- `kadence/accordion` - FAQ or expandable content.
- `kadence/tabs` - Tabbed service/category content.
- `kadence/testimonials` and `kadence/testimonial` - Testimonials.
- `kadence/query` plus query child blocks - Dynamic post/case-study listings.

## Registered But Usually Not First Choice For Static Pages

- Advanced forms: `kadence/advanced-form` and its field children.
- Legacy form: `kadence/form`.
- Header builder blocks: `kadence/header`, `kadence/header-column`, `kadence/header-container-desktop`, `kadence/header-container-tablet`, `kadence/header-row`, `kadence/header-section`, `kadence/off-canvas`, `kadence/off-canvas-trigger`.
- Dynamic content: `kadence/dynamichtml`, `kadence/dynamiclist`, `kadence/repeater`, `kadence/repeatertemplate`.
- Navigation/search: `kadence/navigation`, `kadence/navigation-link`, `kadence/search`.
- Media/special: `kadence/lottie`, `kadence/modal`, `kadence/slider`, `kadence/slide`, `kadence/vector`, `kadence/videopopup`.
- Tables: `kadence/table`, `kadence/table-row`, `kadence/table-data`.
- Post grids: `kadence/postgrid`, `kadence/posts`, `kadence/portfoliogrid`.
- Miscellaneous: `kadence/countdown`, `kadence/progress-bar`, `kadence/show-more`, `kadence/userinfo`, `kadence/identity`.

## Native Block Selection Examples

- Slider/carousel: use `kadence/slider` with `kadence/slide`; for image-only carousels, consider `kadence/advancedgallery`.
- Hero or section background image: use `kadence/rowlayout` background attributes such as `bgImg`, `bgImgID`, `bgImgSize`, `bgImgPosition`, and overlay attributes such as `overlay` and `overlayOpacity`; use CSS only for spacing or responsive tuning.
- Table of contents: use `kadence/tableofcontents`; only use manual TOC links if the native block cannot target the required headings after registry and markup inspection.
- Bulleted or icon lists: use `kadence/iconlist` with `kadence/listitem`; use styled Advanced Heading items only when the design requires text blocks that Icon List cannot represent.
- Image service cards: use `kadence/imageoverlay`, `kadence/infobox`, or `kadence/image` plus text blocks depending on editability needs.
- Counters/statistics: use `kadence/countup`.
- Maps: use `kadence/googlemaps`.
- FAQs: use `kadence/accordion`.
- Tabbed service/category panels: use `kadence/tabs`.

## Complete Block Name List

`kadence/accordion`, `kadence/advanced-form`, `kadence/advanced-form-accept`, `kadence/advanced-form-captcha`, `kadence/advanced-form-checkbox`, `kadence/advanced-form-date`, `kadence/advanced-form-email`, `kadence/advanced-form-file`, `kadence/advanced-form-hidden`, `kadence/advanced-form-number`, `kadence/advanced-form-radio`, `kadence/advanced-form-select`, `kadence/advanced-form-submit`, `kadence/advanced-form-telephone`, `kadence/advanced-form-text`, `kadence/advanced-form-textarea`, `kadence/advanced-form-time`, `kadence/advancedbtn`, `kadence/advancedgallery`, `kadence/advancedheading`, `kadence/column`, `kadence/countdown`, `kadence/countup`, `kadence/dynamichtml`, `kadence/dynamiclist`, `kadence/form`, `kadence/googlemaps`, `kadence/header`, `kadence/header-column`, `kadence/header-container-desktop`, `kadence/header-container-tablet`, `kadence/header-row`, `kadence/header-section`, `kadence/icon`, `kadence/iconlist`, `kadence/identity`, `kadence/image`, `kadence/imageoverlay`, `kadence/infobox`, `kadence/listitem`, `kadence/lottie`, `kadence/modal`, `kadence/navigation`, `kadence/navigation-link`, `kadence/off-canvas`, `kadence/off-canvas-trigger`, `kadence/portfoliogrid`, `kadence/postgrid`, `kadence/posts`, `kadence/progress-bar`, `kadence/query`, `kadence/query-card`, `kadence/query-filter`, `kadence/query-filter-buttons`, `kadence/query-filter-checkbox`, `kadence/query-filter-date`, `kadence/query-filter-range`, `kadence/query-filter-rating`, `kadence/query-filter-reset`, `kadence/query-filter-search`, `kadence/query-filter-woo-attribute`, `kadence/query-noresults`, `kadence/query-pagination`, `kadence/query-result-count`, `kadence/query-sort`, `kadence/repeater`, `kadence/repeatertemplate`, `kadence/rowlayout`, `kadence/search`, `kadence/show-more`, `kadence/single-icon`, `kadence/singlebtn`, `kadence/slide`, `kadence/slider`, `kadence/spacer`, `kadence/splitcontent`, `kadence/table`, `kadence/table-data`, `kadence/table-row`, `kadence/tableofcontents`, `kadence/tabs`, `kadence/testimonial`, `kadence/testimonials`, `kadence/userinfo`, `kadence/vector`, `kadence/videopopup`.
