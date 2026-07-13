# Fast Style Tuning

Use this for MTI WordPress/Kadence fixes that only change scoped WPCode CSS or JS on already-rendered Kadence blocks: typography, line clamps, equal heights, small responsive overflow, browser polish, and micro-spacing that Kadence cannot express cleanly.

Do not use this shortcut for page content changes, native Kadence block attribute changes, editor-owned Row Layout/Column padding or margins, editable backgrounds/overlays, new sections, new assets, invalid-content repair, or anything that changes editable structure. Use the full implementation checklist for those.

Before adding CSS, verify the requested value cannot live in the relevant Row Layout, Column, Advanced Heading, Image, Button, Icon, or List block. If Kadence can own it, update the block attribute and remove or narrow any old CSS override instead of adding another rule.

## Target Workflow

1. Read `MEMORY.md` first. Reuse known page IDs, snippet IDs, node IDs, and marker names instead of rediscovering them.
2. Extract only the necessary Figma facts for the exact node: frame size, padding, text styles, colors, and key x/y/width/height values. A screenshot is optional unless visual ambiguity remains.
3. Run one bounded live-page probe that returns:
   - current URL and viewport width
   - target element selectors/classes
   - computed font, color, decoration, text-transform, margin, padding, display, and line-height
   - root-relative rectangles for the target text/image/button elements
   - horizontal overflow and invalid-content flags
   - whether the expected WPCode marker is present in the public HTML
4. Update the existing WPCode snippet named in memory when possible. Add a clear marker block. Update both the `wpcode` post content and the `wpcode_snippets` option cache in the same PHP call, then clear caches.
5. Verify with one fresh public render at the affected desktop width and one mobile overflow smoke check. Reuse the same measurement fields from step 3 so before/after comparison is direct.
6. Refresh the in-app browser tab when it is already on the affected page, then run one small read-only measurement there. Do not spend time on visual browsing when numeric checks answer the question.

## WPCode Update Pattern

Use this shape through `novamira/execute-php`; replace the IDs, marker, CSS, and optional cache-location assumptions.

```php
$snippet_id = 345;
$marker = 'START MTI example scoped fix';
$end_marker = 'END MTI example scoped fix';
$new_block = "/* $marker */\n...css...\n/* $end_marker */";

$post = get_post($snippet_id);
if (!$post) return array('updated' => false, 'error' => 'Snippet not found');

$code = $post->post_content;
$pattern = '#/\* ' . preg_quote($marker, '#') . ' \*/.*?/\* ' . preg_quote($end_marker, '#') . ' \*/#s';
$code = preg_match($pattern, $code)
  ? preg_replace($pattern, $new_block, $code, 1)
  : rtrim($code) . "\n\n" . $new_block . "\n";

$result = wp_update_post(array('ID' => $snippet_id, 'post_content' => $code), true);
if (is_wp_error($result)) return array('updated' => false, 'error' => $result->get_error_message());

$cache = get_option('wpcode_snippets', array());
$cache_updated = false;
if (is_array($cache)) {
  foreach ($cache as &$items) {
    if (!is_array($items)) continue;
    foreach ($items as &$item) {
      if ((int) ($item['id'] ?? 0) === $snippet_id) {
        $item['code'] = $code;
        $item['modified'] = current_time('mysql');
        $cache_updated = true;
      }
    }
    unset($item);
  }
  unset($items);
  if ($cache_updated) update_option('wpcode_snippets', $cache, false);
}

clean_post_cache($snippet_id);
wp_cache_delete('wpcode_snippets', 'options');
if (function_exists('rocket_clean_domain')) rocket_clean_domain();
if (function_exists('wp_cache_flush')) wp_cache_flush();

return array(
  'updated' => true,
  'post_has_marker' => strpos(get_post($snippet_id)->post_content, $marker) !== false,
  'cache_updated' => $cache_updated,
);
```

## Validation Budget

For CSS-only WPCode changes, do not list the block registry or re-parse the full page unless the page content changed, invalid-content warnings appear, or selectors imply the structure is not what memory says it is.

Required checks:

- snippet post has the marker
- `wpcode_snippets` cache has the marker
- public HTML has the marker after cache clear
- affected desktop viewport matches the Figma numeric targets
- mobile has no horizontal overflow or obvious clipped/overlapping text
- visible text does not include `unexpected or invalid content`

Escalate to the full checklist when any required check fails twice, when selectors are unstable, or when a native Kadence setting can own the requested change more cleanly than CSS.
