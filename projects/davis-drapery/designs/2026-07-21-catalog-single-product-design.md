# Catalog Single-Product Figma Layout Design

**Status:** Approved in conversation on 2026-07-21

**Design source:** Davis Drapery Figma file `JE7ALOmjVP2wwKpRlvmtdO`, frame `638:6425`

**Target environment:** WordPress 7.0, WooCommerce 10.9.4, Kadence Child theme on `wordpress-421525-4426215.cloudwaysapps.com`

## Goal

Rebuild the ordinary WooCommerce catalog-product content area to match Figma frame `638:6425` while preserving WooCommerce commerce behavior and leaving generated Drapery Builder products on their current data-specific template.

## Scope

The redesigned frame contains only:

- Product breadcrumb.
- Product gallery and thumbnails.
- Product title, wishlist control, rating and review count, price, short description, quantity, stock or validation messages, and Add to Cart controls.
- Details, Dimensions, Shipping Information, and Reviews tabs using live WooCommerce tab content.
- Three related-product cards.

The existing site header, footer, and every section outside this frame remain unchanged.

## Non-Goals

- Do not redesign generated Drapery Builder products.
- Do not change the Drapery Builder, its pricing formulas, or generated order metadata.
- Do not redesign product archives, cart, checkout, account pages, header, or footer.
- Do not hardcode the example Clear Curtain title, imagery, price, description, ratings, or related products from Figma.
- Do not replace WooCommerce cart, stock, nonce, variation, review, or related-product logic with custom equivalents.
- Do not install Tailwind or another frontend framework.

## Product Eligibility

The catalog layout applies only to ordinary WooCommerce catalog products.

Generated Drapery Builder products are excluded when either condition is true:

1. The product belongs to the `drapery-order` product category. This is the authoritative signal.
2. As a safety fallback, the product contains the generated-order metadata set, including values such as `room_location`, `window_location`, and `drape_style`.

Names and slugs are never used for classification. Words such as "curtain" or "drapery" in a normal catalog-product name do not exclude that product.

If classification is inconclusive or the WooCommerce product object is unavailable, rendering falls back to the current WooCommerce template.

Reference generated product used for verification:

`/product/custom-drapery-living-room-window-b-sheer-royal-batiste-white-royal-slub-black-36-12-grommet-pleat-drapery/` (product ID `6970`). It is a virtual simple product in `drapery-order` with generated room, window, drape, rod, fabric, lining, and dimension metadata and no normal product gallery.

## Architecture

Use a hybrid child-theme template rather than a hook-only rearrangement or full WooCommerce replacement.

### `wp-content/themes/kadence-child/woocommerce/single-product.php`

Retain the existing WooCommerce page wrapper and loop. After `the_post()`, route the current product through the eligibility helper:

- Generated Drapery Builder product: render the existing `content-single-product` path unchanged.
- Eligible catalog product: load the dedicated catalog single-product partial.

### `wp-content/themes/kadence-child/woocommerce/content-single-product-catalog.php`

Own only the markup inside Figma frame `638:6425`. Use the current global WooCommerce product object and WooCommerce template functions for commerce and product data. The partial must not contain hardcoded product copy, prices, IDs, or media URLs.

### `wp-content/themes/kadence-child/assets/css/single-product-catalog.css`

Contain the Figma-specific layout and responsive styling. Every selector must be scoped beneath a unique catalog-product wrapper so it cannot affect generated products, archives, cart, checkout, or account screens.

### `wp-content/themes/kadence-child/assets/js/single-product-catalog.js`

Provide only behavior that WooCommerce does not already provide: accessible quantity decrement and increment controls and any small state synchronization required by the custom markup. WooCommerce continues to own variation selection, stock validation, cart submission, tabs, and review handling.

### `wp-content/themes/kadence-child/functions.php`

Add the generated-product eligibility helper and conditionally enqueue the catalog CSS and JavaScript only for eligible catalog single-product requests.

## Desktop Layout

The catalog content is centered with a maximum width of `1410px`, matching the Figma frame.

1. Breadcrumb appears above the product area using 14px Instrument Sans semibold uppercase text, subtle gray for ancestors, and black for the current product.
2. Product area uses a `600px` gallery column, a one-pixel vertical divider, and a `700px` summary column at the Figma desktop width.
3. The main image is square with a two-pixel corner radius and appropriate object cropping. Thumbnails appear below with a maroon active border and accessible selection state.
4. Summary uses a 40px Cormorant Garamond medium uppercase title, existing wishlist state, live rating and review count, maroon current price, struck-through regular price when on sale, horizontal divider, description label and copy, then the bordered purchase panel.
5. Purchase panel contains quantity controls on the left and WooCommerce's native product-type-specific purchase form or button on the right. The panel grows vertically when variations, stock messages, or validation content require more space.
6. A full-width divider separates the main product area from the tabs.
7. Tabs preserve live WooCommerce content and current labels: Details, Dimensions, Shipping Information, and Reviews. The selected tab uses maroon text and underline.
8. Related Products shows a centered 40px Cormorant Garamond heading and at most three cards in one row. Each card uses a square product image, live product title, and live price.

## Dynamic Data Rules

- Gallery uses the product featured image and gallery attachment IDs. If none exist, render WooCommerce's placeholder behavior.
- Title, price HTML, stock state, purchasability, sale state, short description, rating, review count, tabs, and related products come from WooCommerce.
- Rating and review count render only when rating data is available under the site's WooCommerce settings.
- Sale styling renders only when WooCommerce returns both current and regular prices as a sale.
- Wishlist control renders only through the site's existing wishlist implementation; it must preserve its current login, add, remove, nonce, and notification behavior.
- Add to Cart uses WooCommerce's template for the active product type so simple, variable, grouped, and external catalog products remain supported.
- WooCommerce notices and form errors remain visible within the catalog wrapper.
- Related products use WooCommerce's related-product query and are limited to three; no placeholder cards are invented when fewer than three exist.

## Responsive Design

The provided Figma frame is desktop-only, so smaller breakpoints use an approved responsive interpretation.

### Tablet

- Stack gallery above summary.
- Convert the vertical divider to a horizontal divider.
- Allow the summary, descriptions, variation fields, and purchase panel to use the full container width.
- Use two related-product columns.

### Mobile

- Reduce outer spacing and use the mobile Davis Drapery typography scale.
- Keep imagery, controls, and buttons within the viewport.
- Stack purchase-panel content when needed and make the primary button easy to tap.
- Keep tabs on one horizontally scrollable row with a visible active state.
- Use one related-product column.
- Do not use fixed content heights that clip long titles, descriptions, variations, notices, or tab content.

## Accessibility

- Keep one product H1.
- Use semantic breadcrumb navigation and meaningful link text.
- Provide accessible labels for wishlist, thumbnails, quantity decrement, and quantity increment controls.
- Preserve keyboard access, focus visibility, native form semantics, disabled states, and WooCommerce error associations.
- Quantity controls must respect the input minimum, maximum, step, and disabled state.
- Tab behavior must retain WooCommerce keyboard and ARIA behavior; styling must not hide inactive panels in a way that breaks accessibility.
- Images use WooCommerce-provided alternative text and responsive image attributes.

## Failure Handling and Isolation

- Missing product object or ambiguous eligibility falls back to the current template.
- Missing images, ratings, sale prices, descriptions, tab panels, or related products use WooCommerce's natural empty/default behavior.
- Out-of-stock and non-purchasable products show WooCommerce's native status instead of a fabricated cart form.
- Catalog CSS and JavaScript load only when the eligibility helper returns true.
- The existing generated-product layout, detailed order specification, and current behaviors remain untouched.
- Use the already-enqueued Font Awesome heart and circular plus/minus glyphs only when they visually match the Figma icons; do not create replacement vector artwork.

## Implementation Safety

- Create dated backups of every live child-theme file before editing it.
- Validate PHP syntax before deploying each PHP file.
- Implement in small passes: routing and eligibility, markup/data mapping, styling, behavior, then responsive and regression QA.
- Clear relevant WordPress/WP Rocket caches after deployment and before visual comparison.
- Restore the dated backups immediately if a PHP error, blank page, or routing regression appears.

## Verification Matrix

### Eligible catalog products

- Normal product with featured image, gallery images, price, description, tabs, and related products.
- Missing product image.
- No ratings or reviews.
- Sale price with regular-price strike-through.
- Out-of-stock or non-purchasable product.
- Variable product, plus grouped or external products if representative products exist on the site.
- Fewer than three related products.

### Generated product regression

- Product ID `6970` stays on the current WooCommerce layout.
- Its `drapery-order` category, custom order Details content, `$487` price, and Add to Cart behavior remain intact.
- It does not load the catalog wrapper or catalog-only CSS and JavaScript.

### Interaction and visual QA

- PHP lint passes for every modified or created PHP file.
- Quantity decrement and increment honor min, max, and step.
- A representative eligible product successfully adds the selected quantity or variation to the cart.
- Wishlist add/remove and login-required behavior remain functional.
- Tabs, review form, thumbnails, and related links remain functional.
- Compare numerically and visually at the Figma desktop width, `1440px`, `768px`, and `390px`.
- Confirm expected container widths, column proportions, spacing, typography, borders, active states, and card sizing.
- Confirm no horizontal overflow, clipped text, duplicated headings, PHP warnings, browser console errors, or layout changes outside the catalog wrapper.

## Acceptance Criteria

1. Eligible catalog product content matches Figma frame `638:6425` closely at desktop width and follows the approved responsive behavior on tablet and mobile.
2. All visible product content is driven by WordPress and WooCommerce data.
3. WooCommerce stock, variation, validation, nonce, cart, review, and related-product behavior remains intact.
4. Generated `drapery-order` products retain their existing layout and detailed order data.
5. Header, footer, archives, cart, checkout, account pages, and Drapery Builder remain unchanged.
6. No catalog-only CSS or JavaScript loads on excluded generated products.
7. The verification matrix passes without PHP warnings, console errors, horizontal overflow, or clipped content.
