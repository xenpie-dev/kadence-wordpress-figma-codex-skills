# Validation

Run validation after every generated section and after the final page save.

## WordPress PHP Checks

```php
$post = get_post($post_id);
$blocks = parse_blocks($post->post_content);
$stable = serialize_blocks($blocks) === $post->post_content;

$counts = array();
$walk = function($blocks) use (&$walk, &$counts) {
  foreach ($blocks as $block) {
    $name = $block['blockName'] ?: 'raw';
    $counts[$name] = ($counts[$name] ?? 0) + 1;
    if (!empty($block['innerBlocks'])) $walk($block['innerBlocks']);
  }
};
$walk($blocks);

try {
  do_blocks($post->post_content);
  $render_ok = true;
  $render_error = null;
} catch (Throwable $e) {
  $render_ok = false;
  $render_error = $e->getMessage();
}

return array(
  'stable' => $stable,
  'block_counts' => $counts,
  'h1_count' => substr_count($post->post_content, '<h1'),
  'raw_count' => $counts['raw'] ?? 0,
  'core_html_count' => $counts['core/html'] ?? 0,
  'render_ok' => $render_ok,
  'render_error' => $render_error,
);
```

Expected:

- `stable` is true.
- `raw_count` is 0.
- `core_html_count` is 0 by default.
- Any `core/html` usage must be explicitly justified before implementation, must name the registered Kadence blocks that were considered first, and must be documented in the response after implementation.
- Headings match semantic expectations.
- Every paragraph Advanced Heading has `htmlTag:"p"` and saved `<p>`.
- Hero or section background images are stored in `kadence/rowlayout` attributes such as `bgImg`/`bgImgID`, not only in custom CSS.
- `do_blocks($post->post_content)` and `render_block($block)` succeed for dynamic Kadence blocks such as Modal, Row Layout, Column, and Image.

## Registry And Block-Choice Checks

Before writing content, run a live registry check on the target site with `WP_Block_Type_Registry` and list the native blocks selected for the implementation.

For common features, validation should reject custom HTML/CSS/JS substitutions when the native block is registered:

- Carousel or slider: expect `kadence/slider` and `kadence/slide`, or `kadence/advancedgallery` for image-only galleries.
- Table of contents: expect `kadence/tableofcontents` unless it cannot target the required headings after inspection.
- Icon or bullet list: expect `kadence/iconlist` and `kadence/listitem` unless the list must be represented as individually styled text blocks.
- Map: expect `kadence/googlemaps`.
- FAQ/expandable panels: expect `kadence/accordion`.
- Tabs: expect `kadence/tabs`.
- Counters: expect `kadence/countup`.
- Hero or section background image/overlay: expect native `kadence/rowlayout` background and overlay attributes such as `bgImg`, `bgImgID`, `overlay`, and `overlayOpacity`. Reject CSS-only `background-image: url(...)` or pseudo-element overlays unless the live Row Layout registry or same-site sample proves the native setting cannot represent the design.

## Front-End Checks

- Open the page in a browser.
- Check desktop and mobile viewport widths.
- Confirm `document.body.scrollWidth <= window.innerWidth + 1`.
- Confirm visible text does not include `unexpected or invalid content`.
- For Row Layout backgrounds, confirm the rendered row has the native Kadence background class/CSS (for example `kt-row-has-bg` or generated `.kb-row-layout-id...{background-image:...}`), and confirm scoped custom CSS does not duplicate the same image URL.
- For Modal blocks, click each trigger and measure the open modal's rendered rectangles. Confirm the trigger text, modal content, close button, images, headings, and paragraph blocks are present in the front-end DOM, not only in saved block comments.
- Check for text overflow inside buttons, headings, cards, and narrow columns.
- Check lazy images by scrolling to image sections or directly inspecting image `naturalWidth`.
- For sticky/sidebar behavior, confirm the native Kadence structure remains editable and CSS only adjusts positioning or spacing.
- For WPCode-backed CSS on MTI, confirm the active `wpcode_snippets` option cache contains the same scoped rules as the snippet post content.

For Figma-matched components, record target and live geometry in the same coordinate system:

```js
const container = document.querySelector('.kt-modal-container');
const c = container.getBoundingClientRect();
const relRect = (selector) => {
  const r = document.querySelector(selector).getBoundingClientRect();
  return { x: r.x - c.x, y: r.y - c.y, w: r.width, h: r.height };
};
```

Use this for modals, cards, and other spacing-sensitive work before claiming visual accuracy.

## Failure Response

If validation fails:

1. Do not add more sections.
2. Isolate the failing block by saving only that section to a scratch page or element.
3. Compare against a fresh Kadence-generated sample from the same site.
4. Fix the helper/reference pattern before regenerating more content.
