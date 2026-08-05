# Catalog Single-Product Figma Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Figma frame `638:6425` for ordinary WooCommerce catalog products while preserving the existing generated Drapery Builder product template.

**Architecture:** The child theme's existing `woocommerce/single-product.php` remains the page router. It sends generated `drapery-order` products to the current WooCommerce `content-single-product` template and eligible catalog products to a focused custom partial; a small include loaded by `functions.php` owns eligibility, conditional assets, and the related-product limit.

**Tech Stack:** WordPress 7.0, WooCommerce 10.9.4, Kadence Child, PHP 8.3, CSS, vanilla JavaScript, existing Font Awesome, Node.js contract tests, Novamira WordPress connector, in-app browser QA.

## Global Constraints

- Match Davis Drapery Figma frame `638:6425`; do not implement content outside that frame.
- Apply the redesign only to ordinary catalog products.
- Treat `product_cat=drapery-order` as the authoritative generated-product exclusion, with `room_location`, `window_location`, and `drape_style` together as the metadata fallback.
- Never classify products by title or slug words.
- Preserve native WooCommerce product-type, stock, validation, nonce, cart, variation, review, gallery, and related-product behavior.
- Preserve the existing header, footer, Drapery Builder, archives, cart, checkout, account pages, and generated product layout.
- Do not hardcode example Figma product copy, IDs, prices, ratings, or imagery.
- Do not install Tailwind or another frontend framework.
- Scope every catalog style and behavior beneath `.davis-catalog-product`.
- Back up every live file before editing and lint PHP on the server before activating new PHP.

## File Map

- Create local/deploy: `wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php` — eligibility helper, request helper, conditional assets, related-product limit.
- Create local/deploy: `wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/content-single-product-catalog.php` — Figma frame markup using WooCommerce data/functions.
- Create local/deploy: `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/single-product-catalog.css` — scoped desktop/tablet/mobile layout.
- Create local/deploy: `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/js/single-product-catalog.js` — accessible quantity controls and wishlist ARIA synchronization.
- Create local/deploy: `wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/single-product.php` — conditional router based on the live template.
- Create test: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs` — static contract and isolation tests.
- Modify live: `wp-content/themes/kadence-child/functions.php` — one `require_once` for the focused include.
- Deploy the matching local files under `wp-content/themes/kadence-child/`.

---

### Task 1: Establish the deployment package and failing contracts

**Files:**
- Create: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`
- Create: `wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/single-product.php`

**Interfaces:**
- Consumes: the live `single-product.php` read through `novamira/read-file`.
- Produces: a local deploy package with the same relative paths as the live child theme and a Node contract test that every later task must satisfy.

- [ ] **Step 1: Create dated live backups before any mutation**

Use `novamira/execute-php` with this exact code and verify every `copy()` result is `true`:

```php
$root = get_stylesheet_directory();
$stamp = gmdate('Ymd-His');
$targets = array(
    $root . '/functions.php',
    $root . '/woocommerce/single-product.php',
);
$results = array();
foreach ($targets as $target) {
    $backup = $target . '.bak-' . $stamp . '-catalog-single-product';
    $results[$target] = array('backup' => $backup, 'copied' => copy($target, $backup));
}
return $results;
```

- [ ] **Step 2: Write the failing contract test**

```js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..', 'kadence-child');
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');

const helper = read('inc/catalog-single-product.php');
const router = read('woocommerce/single-product.php');
const partial = read('woocommerce/content-single-product-catalog.php');
const css = read('assets/css/single-product-catalog.css');
const js = read('assets/js/single-product-catalog.js');

assert.match(helper, /function davis_is_generated_drapery_order_product\s*\(/);
assert.match(helper, /has_term\(\s*'drapery-order'/);
assert.match(helper, /room_location/);
assert.match(helper, /window_location/);
assert.match(helper, /drape_style/);
assert.match(helper, /function davis_is_catalog_product_request\s*\(/);
assert.match(helper, /single-product-catalog\.css/);
assert.match(helper, /single-product-catalog\.js/);
assert.match(helper, /posts_per_page.*3/s);

assert.match(router, /davis_is_generated_drapery_order_product/);
assert.match(router, /content-single-product-catalog\.php/);
assert.match(router, /wc_get_template_part\(\s*'content',\s*'single-product'\s*\)/);

assert.match(partial, /class="davis-catalog-product/);
assert.match(partial, /woocommerce_show_product_images\(\)/);
assert.match(partial, /woocommerce_template_single_add_to_cart\(\)/);
assert.match(partial, /woocommerce_output_product_data_tabs\(\)/);
assert.match(partial, /woocommerce_output_related_products\(\)/);
assert.doesNotMatch(partial, /Clear Curtain|\$57\.00|Grommet Drapery/);

for (const selector of css.matchAll(/(^|})\s*([^@][^{]+)\{/gm)) {
  const list = selector[2].trim();
  if (list.startsWith('from') || list.startsWith('to')) continue;
  assert.ok(
    list.split(',').every((item) => item.trim().startsWith('.davis-catalog-product')),
    `Unscoped selector: ${list}`
  );
}

assert.match(js, /davis-qty-minus/);
assert.match(js, /davis-qty-plus/);
assert.match(js, /aria-pressed/);
console.log('catalog single-product contracts passed');
```

- [ ] **Step 3: Run the contract and verify it fails before implementation**

Run:

```powershell
node wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
```

Expected: failure with `ENOENT` for `inc/catalog-single-product.php`.

- [ ] **Step 4: Copy the exact live router into the local deploy package**

Read `wp-content/themes/kadence-child/woocommerce/single-product.php` with `novamira/read-file`, then create the matching local file with identical content. Do not source the router from the dated reference backup because the live file is authoritative.

- [ ] **Step 5: Commit the failing test and baseline router**

```powershell
git add wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/single-product.php
git commit -m "test: define catalog product template contracts"
```

---

### Task 2: Implement generated-product detection and request-scoped integration

**Files:**
- Create: `wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php`
- Test: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`

**Interfaces:**
- Produces: `davis_is_generated_drapery_order_product($product = null): bool` and `davis_is_catalog_product_request(): bool`.
- Produces: handles `davis-catalog-single-product` and `davis-catalog-single-product-js` only on eligible requests.
- Produces: `davis_catalog_related_product_args(array $args): array` limiting eligible related products to three columns/cards.

- [ ] **Step 1: Create the focused integration include**

```php
<?php
defined('ABSPATH') || exit;

function davis_is_generated_drapery_order_product($product = null) {
    if (is_numeric($product)) {
        $product = wc_get_product((int) $product);
    }

    if (!$product instanceof WC_Product) {
        $global_product = isset($GLOBALS['product']) ? $GLOBALS['product'] : null;
        $product = $global_product instanceof WC_Product ? $global_product : null;
    }

    if (!$product instanceof WC_Product) {
        return true;
    }

    $product_id = $product->get_id();
    if (has_term('drapery-order', 'product_cat', $product_id)) {
        return true;
    }

    foreach (array('room_location', 'window_location', 'drape_style') as $meta_key) {
        $value = get_post_meta($product_id, $meta_key, true);
        if ($value === '' || $value === null) {
            return false;
        }
    }

    return true;
}

function davis_is_catalog_product_request() {
    if (!function_exists('is_product') || !is_product()) {
        return false;
    }

    $product = wc_get_product(get_queried_object_id());
    return $product instanceof WC_Product && !davis_is_generated_drapery_order_product($product);
}

function davis_enqueue_catalog_single_product_assets() {
    if (!davis_is_catalog_product_request()) {
        return;
    }

    $css_path = get_stylesheet_directory() . '/assets/css/single-product-catalog.css';
    $js_path  = get_stylesheet_directory() . '/assets/js/single-product-catalog.js';

    wp_enqueue_style(
        'davis-catalog-single-product',
        get_stylesheet_directory_uri() . '/assets/css/single-product-catalog.css',
        array('kadence-child'),
        file_exists($css_path) ? (string) filemtime($css_path) : null
    );

    wp_enqueue_script(
        'davis-catalog-single-product-js',
        get_stylesheet_directory_uri() . '/assets/js/single-product-catalog.js',
        array(),
        file_exists($js_path) ? (string) filemtime($js_path) : null,
        true
    );
}
add_action('wp_enqueue_scripts', 'davis_enqueue_catalog_single_product_assets', 30);

function davis_catalog_related_product_args($args) {
    if (!davis_is_catalog_product_request()) {
        return $args;
    }

    $args['posts_per_page'] = 3;
    $args['columns'] = 3;
    return $args;
}
add_filter('woocommerce_output_related_products_args', 'davis_catalog_related_product_args');
```

- [ ] **Step 2: Run a server-side PHP lint against a temporary text copy**

Upload the file content as `wp-content/novamira-sandbox/catalog-single-product-lint.txt`, then run this code with `novamira/execute-php`:

```php
$file = ABSPATH . 'wp-content/novamira-sandbox/catalog-single-product-lint.txt';
$command = escapeshellarg(PHP_BINARY) . ' -l ' . escapeshellarg($file) . ' 2>&1';
$output = array();
$status = 1;
exec($command, $output, $status);
return array('status' => $status, 'output' => $output);
```

Expected: status `0` and `No syntax errors detected`.

- [ ] **Step 3: Add the include to the end of live `functions.php` only after the lint passes**

Append exactly:

```php

/** Catalog single-product Figma layout integration. */
require_once get_stylesheet_directory() . '/inc/catalog-single-product.php';
```

- [ ] **Step 4: Verify classification on WordPress**

Use `novamira/execute-php`:

```php
return array(
    'generated_6970' => davis_is_generated_drapery_order_product(wc_get_product(6970)),
    'catalog_3502'   => davis_is_generated_drapery_order_product(wc_get_product(3502)),
);
```

Expected: `generated_6970=true`; `catalog_3502=false`.

- [ ] **Step 5: Commit the eligibility integration**

```powershell
git add wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php
git commit -m "feat: classify catalog and generated drapery products"
```

---

### Task 3: Route catalog products and render the WooCommerce-backed Figma frame

**Files:**
- Modify: `wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/single-product.php`
- Create: `wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/content-single-product-catalog.php`
- Test: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`

**Interfaces:**
- Consumes: `davis_is_generated_drapery_order_product()` from Task 2.
- Produces: `.davis-catalog-product` as the single scope root for all catalog CSS/JS.
- Preserves: WooCommerce native gallery, add-to-cart templates, tabs, reviews, and related-product query.

- [ ] **Step 1: Replace only the loop body in the local router**

```php
<?php while (have_posts()) : ?>
    <?php
    the_post();
    $davis_product = wc_get_product(get_the_ID());

    if (
        $davis_product instanceof WC_Product &&
        function_exists('davis_is_generated_drapery_order_product') &&
        !davis_is_generated_drapery_order_product($davis_product)
    ) {
        wc_get_template('content-single-product-catalog.php');
    } else {
        wc_get_template_part('content', 'single-product');
    }
    ?>
<?php endwhile; ?>
```

Leave the live file's header, `get_header('shop')`, before/after main-content hooks, sidebar hook, and `get_footer('shop')` unchanged.

- [ ] **Step 2: Create the complete catalog partial**

```php
<?php
defined('ABSPATH') || exit;

global $product;

if (!$product instanceof WC_Product) {
    return;
}

do_action('woocommerce_before_single_product');

if (post_password_required()) {
    echo get_the_password_form(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
    return;
}

$product_id      = $product->get_id();
$rating_count    = $product->get_rating_count();
$average_rating  = $product->get_average_rating();
$is_wishlisted   = function_exists('is_product_in_wishlizt') && is_product_in_wishlizt($product_id);
$wishlist_action = $is_wishlisted ? 'remove' : 'add';
$wishlist_label  = $is_wishlisted ? __('Remove from wishlist', 'kadence-child') : __('Add to wishlist', 'kadence-child');
?>

<article id="product-<?php the_ID(); ?>" <?php wc_product_class('davis-catalog-product', $product); ?>>
    <div class="davis-catalog-product__inner">
        <div class="davis-catalog-product__breadcrumb">
            <?php
            woocommerce_breadcrumb(array(
                'delimiter'   => '<span class="davis-catalog-product__crumb-separator" aria-hidden="true">›</span>',
                'wrap_before' => '<nav class="woocommerce-breadcrumb" aria-label="' . esc_attr__('Product breadcrumb', 'kadence-child') . '">',
                'wrap_after'  => '</nav>',
            ));
            ?>
        </div>

        <div class="davis-catalog-product__main">
            <section class="davis-catalog-product__gallery" aria-label="<?php echo esc_attr__('Product gallery', 'kadence-child'); ?>">
                <?php woocommerce_show_product_images(); ?>
            </section>

            <div class="davis-catalog-product__vertical-rule" aria-hidden="true"></div>

            <section class="davis-catalog-product__summary summary entry-summary">
                <div class="davis-catalog-product__heading-row">
                    <div class="davis-catalog-product__heading-copy">
                        <?php woocommerce_template_single_title(); ?>

                        <?php if ($rating_count > 0 && wc_review_ratings_enabled()) : ?>
                            <div class="davis-catalog-product__rating">
                                <?php echo wc_get_rating_html($average_rating, $rating_count); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
                                <a href="#reviews" class="davis-catalog-product__review-link">
                                    <?php echo esc_html(number_format_i18n($average_rating) . ' (' . sprintf(_n('%s review', '%s reviews', $rating_count, 'kadence-child'), number_format_i18n($rating_count)) . ')'); ?>
                                </a>
                            </div>
                        <?php endif; ?>

                        <?php woocommerce_template_single_price(); ?>
                    </div>

                    <button
                        type="button"
                        class="wishlizt-heart davis-catalog-product__wishlist<?php echo $is_wishlisted ? ' active' : ''; ?>"
                        data-product-id="<?php echo esc_attr($product_id); ?>"
                        data-action="<?php echo esc_attr($wishlist_action); ?>"
                        aria-label="<?php echo esc_attr($wishlist_label); ?>"
                        aria-pressed="<?php echo $is_wishlisted ? 'true' : 'false'; ?>"
                        title="<?php echo esc_attr($wishlist_label); ?>"
                    >
                        <i class="<?php echo $is_wishlisted ? 'fas' : 'far'; ?> fa-heart heart-icon" aria-hidden="true"></i>
                    </button>
                </div>

                <div class="davis-catalog-product__summary-rule" aria-hidden="true"></div>

                <div class="davis-catalog-product__description">
                    <p class="davis-catalog-product__eyebrow"><?php esc_html_e('Description', 'kadence-child'); ?></p>
                    <?php woocommerce_template_single_excerpt(); ?>
                </div>

                <div class="davis-catalog-product__purchase">
                    <?php woocommerce_template_single_add_to_cart(); ?>
                </div>
            </section>
        </div>

        <div class="davis-catalog-product__section-rule" aria-hidden="true"></div>

        <section class="davis-catalog-product__tabs">
            <?php woocommerce_output_product_data_tabs(); ?>
        </section>

        <section class="davis-catalog-product__related">
            <?php woocommerce_output_related_products(); ?>
        </section>
    </div>
</article>

<?php do_action('woocommerce_after_single_product'); ?>
```

- [ ] **Step 3: Run the contract test**

Run:

```powershell
node wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
```

Expected: it progresses past router/partial assertions and fails only because CSS/JS are not yet present.

- [ ] **Step 4: Lint both PHP files on the server using the temporary-text lint command from Task 2**

Expected: status `0` for each file.

- [ ] **Step 5: Commit the router and partial**

```powershell
git add wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/single-product.php wordpress-child-theme-working/catalog-single-product/kadence-child/woocommerce/content-single-product-catalog.php
git commit -m "feat: render catalog products with Figma structure"
```

---

### Task 4: Implement the scoped Figma styling and responsive layout

**Files:**
- Create: `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/single-product-catalog.css`
- Test: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`

**Interfaces:**
- Consumes: `.davis-catalog-product` markup from Task 3.
- Produces: `1410px` desktop composition, stacked tablet layout, horizontally scrollable mobile tabs, and 3/2/1 related-product grid.

- [ ] **Step 1: Add the complete scoped stylesheet**

Create the stylesheet with these rules and no selector outside `.davis-catalog-product`:

```css
.davis-catalog-product { --davis-maroon:#700202; --davis-heading:#0d0d0d; --davis-copy:#000; --davis-subtle:#5c5c5e; --davis-line:#9f9f9f; --davis-border:#b9b9b9; background:#fff; color:var(--davis-copy); width:100%; }
.davis-catalog-product .davis-catalog-product__inner { box-sizing:border-box; margin:0 auto; max-width:1920px; padding:76px clamp(24px,13.28125vw,255px) 122px; }
.davis-catalog-product .davis-catalog-product__breadcrumb { margin:0 auto 45px; max-width:1410px; }
.davis-catalog-product .woocommerce-breadcrumb { align-items:center; color:var(--davis-subtle); display:flex; flex-wrap:wrap; font-family:"Instrument Sans",sans-serif; font-size:14px; font-weight:600; gap:10px; letter-spacing:.84px; line-height:1.5; margin:0; text-transform:uppercase; }
.davis-catalog-product .woocommerce-breadcrumb a { color:var(--davis-subtle); text-decoration:none; }
.davis-catalog-product .davis-catalog-product__crumb-separator { color:var(--davis-line); }
.davis-catalog-product .davis-catalog-product__main { align-items:start; display:grid; gap:55px; grid-template-columns:minmax(0,600px) 1px minmax(0,700px); margin:0 auto 45px; max-width:1410px; }
.davis-catalog-product .davis-catalog-product__vertical-rule { align-self:stretch; background:var(--davis-line); min-height:757px; opacity:.55; }
.davis-catalog-product .davis-catalog-product__gallery .woocommerce-product-gallery { float:none; margin:0; width:100%; }
.davis-catalog-product .davis-catalog-product__gallery .woocommerce-product-gallery__wrapper { margin:0; }
.davis-catalog-product .davis-catalog-product__gallery .woocommerce-product-gallery__image > a { aspect-ratio:1; display:block; overflow:hidden; border-radius:2px; }
.davis-catalog-product .davis-catalog-product__gallery .woocommerce-product-gallery__image img { height:100%; object-fit:cover; width:100%; }
.davis-catalog-product .davis-catalog-product__gallery .flex-control-thumbs { display:flex; gap:20px; margin:20px 0 0; overflow-x:auto; padding:0; }
.davis-catalog-product .davis-catalog-product__gallery .flex-control-thumbs li { flex:0 0 136px; list-style:none; width:136px; }
.davis-catalog-product .davis-catalog-product__gallery .flex-control-thumbs img { aspect-ratio:1; border:3px solid transparent; border-radius:2px; object-fit:cover; width:100%; }
.davis-catalog-product .davis-catalog-product__gallery .flex-control-thumbs img.flex-active { border-color:var(--davis-maroon); }
.davis-catalog-product .davis-catalog-product__summary { float:none; margin:32px 0 0; width:100%; }
.davis-catalog-product .davis-catalog-product__heading-row { align-items:flex-start; display:flex; gap:24px; justify-content:space-between; }
.davis-catalog-product .product_title { color:var(--davis-heading); font-family:"Cormorant Garamond",serif; font-size:40px; font-weight:500; line-height:1.1; margin:0 0 10px; text-transform:uppercase; }
.davis-catalog-product .davis-catalog-product__wishlist { appearance:none; background:transparent; border:0; color:var(--davis-maroon); cursor:pointer; flex:0 0 auto; font-size:32px; line-height:1; margin:4px 0 0; padding:4px; }
.davis-catalog-product .davis-catalog-product__wishlist:focus-visible { outline:2px solid var(--davis-maroon); outline-offset:4px; }
.davis-catalog-product .davis-catalog-product__rating { align-items:center; display:flex; flex-wrap:wrap; gap:15px; margin:0 0 6px; }
.davis-catalog-product .star-rating { color:#f2b300; margin:0; }
.davis-catalog-product .davis-catalog-product__review-link { color:#3e3e3e; font-family:"Instrument Sans",sans-serif; font-size:14px; line-height:1.5; text-decoration:none; }
.davis-catalog-product .price { align-items:baseline; color:var(--davis-maroon); display:flex; flex-wrap:wrap; font-family:"Instrument Sans",sans-serif; font-size:32px; font-weight:600; gap:10px; line-height:1.5; margin:0; }
.davis-catalog-product .price del { color:var(--davis-heading); font-size:20px; font-weight:400; opacity:1; }
.davis-catalog-product .price ins { background:transparent; color:inherit; text-decoration:none; }
.davis-catalog-product .davis-catalog-product__summary-rule { background:var(--davis-line); height:1px; margin:24px 0; opacity:.55; width:100%; }
.davis-catalog-product .davis-catalog-product__description { font-family:"Instrument Sans",sans-serif; font-size:16px; line-height:1.5; }
.davis-catalog-product .davis-catalog-product__eyebrow { color:var(--davis-heading); font-size:14px; font-weight:600; letter-spacing:.84px; line-height:1.4; margin:0 0 10px; text-transform:uppercase; }
.davis-catalog-product .woocommerce-product-details__short-description { margin:0 0 20px; }
.davis-catalog-product .davis-catalog-product__purchase { border:1px solid var(--davis-border); margin-top:20px; padding:20px; }
.davis-catalog-product .davis-catalog-product__purchase form.cart { align-items:center; display:flex; flex-wrap:wrap; gap:15px; justify-content:space-between; margin:0; width:100%; }
.davis-catalog-product .davis-catalog-product__purchase .quantity { align-items:center; border:1px solid var(--davis-line); border-radius:8px; display:flex; min-height:56px; overflow:hidden; }
.davis-catalog-product .davis-catalog-product__purchase .qty { appearance:textfield; border:0; box-shadow:none; font-family:"Instrument Sans",sans-serif; height:54px; margin:0; padding:0; text-align:center; width:48px; }
.davis-catalog-product .davis-catalog-product__purchase .qty::-webkit-inner-spin-button { appearance:none; margin:0; }
.davis-catalog-product .davis-qty-minus,.davis-catalog-product .davis-qty-plus { align-items:center; background:#fff; border:0; color:var(--davis-heading); cursor:pointer; display:flex; font-size:18px; height:54px; justify-content:center; padding:0; width:40px; }
.davis-catalog-product .single_add_to_cart_button,.davis-catalog-product .button { background:var(--davis-maroon); border:1px solid var(--davis-maroon); border-radius:8px; color:#fff; font-family:"Instrument Sans",sans-serif; font-size:14px; font-weight:600; letter-spacing:.84px; line-height:1; min-height:54px; padding:20px 28px; text-transform:uppercase; }
.davis-catalog-product .davis-catalog-product__section-rule { background:var(--davis-line); height:1px; margin:0 auto; max-width:1410px; opacity:.55; }
.davis-catalog-product .davis-catalog-product__tabs { margin:0 auto; max-width:1410px; padding:20px 50px 50px; }
.davis-catalog-product .woocommerce-tabs ul.tabs { border:0; display:flex; gap:20px; margin:0 0 30px; overflow-x:auto; padding:0; }
.davis-catalog-product .woocommerce-tabs ul.tabs::before,.davis-catalog-product .woocommerce-tabs ul.tabs::after { display:none; }
.davis-catalog-product .woocommerce-tabs ul.tabs li { background:transparent; border:0; border-radius:0; flex:0 0 auto; margin:0; padding:0 20px 0 0; position:relative; }
.davis-catalog-product .woocommerce-tabs ul.tabs li:not(:last-child)::after { background:var(--davis-line); content:""; height:32px; position:absolute; right:0; top:0; width:1px; }
.davis-catalog-product .woocommerce-tabs ul.tabs li a { border-bottom:1px solid transparent; color:#000; font-family:"Instrument Sans",sans-serif; font-size:20px; font-weight:400; line-height:1.5; padding:0 0 2px; text-transform:uppercase; white-space:nowrap; }
.davis-catalog-product .woocommerce-tabs ul.tabs li.active a { border-color:var(--davis-maroon); color:var(--davis-maroon); font-weight:600; }
.davis-catalog-product .woocommerce-Tabs-panel { font-family:"Instrument Sans",sans-serif; font-size:16px; line-height:1.5; margin:0; max-width:700px; }
.davis-catalog-product .davis-catalog-product__related { margin:0 auto; max-width:1410px; }
.davis-catalog-product .related.products > h2 { color:var(--davis-heading); font-family:"Cormorant Garamond",serif; font-size:40px; font-weight:500; line-height:1.1; margin:0 0 45px; text-align:center; text-transform:uppercase; }
.davis-catalog-product .related.products ul.products { display:grid; gap:20px; grid-template-columns:repeat(3,minmax(0,1fr)); margin:0 auto; max-width:1030px; }
.davis-catalog-product .related.products ul.products li.product { background:#f8f8f8; float:none; margin:0; padding:16px; text-align:center; width:auto; }
.davis-catalog-product .related.products ul.products li.product img { aspect-ratio:1; margin:0 0 16px; object-fit:cover; width:100%; }
.davis-catalog-product .related.products .woocommerce-loop-product__title { color:var(--davis-heading); font-family:"Instrument Sans",sans-serif; font-size:16px; font-weight:400; line-height:1.5; padding:0; }
.davis-catalog-product .related.products .price { display:block; font-size:20px; line-height:1.5; }
.davis-catalog-product .related.products .button { display:none; }
.davis-catalog-product .woocommerce-error,.davis-catalog-product .woocommerce-info,.davis-catalog-product .woocommerce-message { width:100%; }
@media (max-width:1100px) { .davis-catalog-product .davis-catalog-product__inner { padding:56px 40px 88px; } .davis-catalog-product .davis-catalog-product__main { grid-template-columns:1fr; } .davis-catalog-product .davis-catalog-product__vertical-rule { height:1px; min-height:1px; } .davis-catalog-product .davis-catalog-product__gallery,.davis-catalog-product .davis-catalog-product__summary { margin-left:auto; margin-right:auto; max-width:700px; } .davis-catalog-product .related.products ul.products { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:600px) { .davis-catalog-product .davis-catalog-product__inner { padding:32px 20px 64px; } .davis-catalog-product .davis-catalog-product__breadcrumb { margin-bottom:30px; } .davis-catalog-product .davis-catalog-product__main { gap:30px; margin-bottom:30px; } .davis-catalog-product .product_title { font-size:30px; } .davis-catalog-product .price { font-size:24px; } .davis-catalog-product .davis-catalog-product__purchase form.cart { align-items:stretch; flex-direction:column; } .davis-catalog-product .davis-catalog-product__purchase .quantity,.davis-catalog-product .single_add_to_cart_button { width:100%; } .davis-catalog-product .davis-catalog-product__tabs { padding:20px 0 40px; } .davis-catalog-product .woocommerce-tabs ul.tabs { gap:14px; } .davis-catalog-product .woocommerce-tabs ul.tabs li a { font-size:16px; } .davis-catalog-product .related.products > h2 { font-size:30px; } .davis-catalog-product .related.products ul.products { grid-template-columns:1fr; } }
```

- [ ] **Step 2: Run the contract test**

Expected: it fails only because the JavaScript file does not yet exist.

- [ ] **Step 3: Commit the stylesheet**

```powershell
git add wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/single-product-catalog.css
git commit -m "style: match catalog products to Figma layout"
```

---

### Task 5: Add accessible quantity controls and wishlist state synchronization

**Files:**
- Create: `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/js/single-product-catalog.js`
- Test: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`

**Interfaces:**
- Consumes: native WooCommerce `.quantity input.qty` fields.
- Produces: `.davis-qty-minus` and `.davis-qty-plus` buttons that update the native input and dispatch `change`.
- Consumes: existing `.wishlizt-heart` AJAX script.
- Produces: synchronized wishlist `aria-label` and `aria-pressed` values after the existing script changes `data-action` or `.active`.

- [ ] **Step 1: Create the complete JavaScript file**

```js
(() => {
  'use strict';

  const root = document.querySelector('.davis-catalog-product');
  if (!root) return;

  const parseNumber = (value, fallback) => {
    const parsed = Number.parseFloat(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  const decorateQuantity = (quantity) => {
    const input = quantity.querySelector('input.qty');
    if (!input || quantity.querySelector('.davis-qty-minus')) return;

    const makeButton = (className, label, iconClass) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = className;
      button.setAttribute('aria-label', label);
      button.innerHTML = `<i class="${iconClass}" aria-hidden="true"></i>`;
      return button;
    };

    const minus = makeButton('davis-qty-minus', 'Decrease quantity', 'far fa-circle-minus');
    const plus = makeButton('davis-qty-plus', 'Increase quantity', 'far fa-circle-plus');
    quantity.insertBefore(minus, input);
    quantity.appendChild(plus);

    const updateDisabledState = () => {
      const min = parseNumber(input.min, 0);
      const max = input.max === '' ? Number.POSITIVE_INFINITY : parseNumber(input.max, Number.POSITIVE_INFINITY);
      const current = parseNumber(input.value, min);
      minus.disabled = input.disabled || current <= min;
      plus.disabled = input.disabled || current >= max;
    };

    const changeBy = (direction) => {
      const min = parseNumber(input.min, 0);
      const max = input.max === '' ? Number.POSITIVE_INFINITY : parseNumber(input.max, Number.POSITIVE_INFINITY);
      const step = parseNumber(input.step, 1);
      const current = parseNumber(input.value, min);
      const next = clamp(current + direction * step, min, max);
      input.value = String(Number(next.toFixed(6)));
      input.dispatchEvent(new Event('change', { bubbles: true }));
      updateDisabledState();
    };

    minus.addEventListener('click', () => changeBy(-1));
    plus.addEventListener('click', () => changeBy(1));
    input.addEventListener('change', updateDisabledState);
    updateDisabledState();
  };

  root.querySelectorAll('.quantity').forEach(decorateQuantity);

  const quantityObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (!(node instanceof Element)) return;
        if (node.matches('.quantity')) decorateQuantity(node);
        node.querySelectorAll?.('.quantity').forEach(decorateQuantity);
      });
    });
  });
  quantityObserver.observe(root, { childList: true, subtree: true });

  const wishlist = root.querySelector('.wishlizt-heart');
  if (wishlist) {
    const syncWishlist = () => {
      const active = wishlist.classList.contains('active') || wishlist.dataset.action === 'remove';
      wishlist.setAttribute('aria-pressed', active ? 'true' : 'false');
      wishlist.setAttribute('aria-label', active ? 'Remove from wishlist' : 'Add to wishlist');
    };
    new MutationObserver(syncWishlist).observe(wishlist, { attributes: true, attributeFilter: ['class', 'data-action'] });
    syncWishlist();
  }
})();
```

- [ ] **Step 2: Validate JavaScript syntax**

Run:

```powershell
node --check wordpress-child-theme-working/catalog-single-product/kadence-child/assets/js/single-product-catalog.js
```

Expected: exit code `0` with no output.

- [ ] **Step 3: Run the complete contract test**

Run:

```powershell
node wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
```

Expected: `catalog single-product contracts passed`.

- [ ] **Step 4: Commit the behavior**

```powershell
git add wordpress-child-theme-working/catalog-single-product/kadence-child/assets/js/single-product-catalog.js wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
git commit -m "feat: add accessible catalog quantity controls"
```

---

### Task 6: Deploy in dependency order and validate the live site

**Files:**
- Deploy: `wp-content/themes/kadence-child/inc/catalog-single-product.php`
- Deploy: `wp-content/themes/kadence-child/woocommerce/content-single-product-catalog.php`
- Deploy: `wp-content/themes/kadence-child/assets/css/single-product-catalog.css`
- Deploy: `wp-content/themes/kadence-child/assets/js/single-product-catalog.js`
- Modify live: `wp-content/themes/kadence-child/woocommerce/single-product.php`
- Modify live: `wp-content/themes/kadence-child/functions.php`

**Interfaces:**
- Consumes: all local deploy-package files from Tasks 2–5.
- Produces: the live catalog layout with generated-product fallback and rollback backups.

- [ ] **Step 1: Deploy non-routing files first**

Upload the new include and partial with `novamira/create-upload-link`. Write the CSS and JavaScript with `novamira/write-file`. Read each deployed file back and compare its byte length and SHA-256 digest with the local source.

- [ ] **Step 2: Lint deployed PHP files before routing to them**

Run the PHP lint command from Task 2 against:

```text
wp-content/themes/kadence-child/inc/catalog-single-product.php
wp-content/themes/kadence-child/woocommerce/content-single-product-catalog.php
wp-content/themes/kadence-child/woocommerce/single-product.php
wp-content/themes/kadence-child/functions.php
```

Expected: status `0` and `No syntax errors detected` for every file.

- [ ] **Step 3: Activate the include, then activate the router**

Use `novamira/edit-file` for the one `functions.php` include insertion and for the exact live router loop replacement. Re-read both files after editing and verify the expected unique markers occur once.

- [ ] **Step 4: Clear WordPress/WP Rocket caches**

Use the site's supported WP Rocket cache purge command or API. Do not change WP Rocket settings.

- [ ] **Step 5: Verify generated product regression before catalog QA**

Open product ID `6970` and verify:

```text
No .davis-catalog-product wrapper
No single-product-catalog.css request
No single-product-catalog.js request
Title still starts with Custom Drapery:
Price remains $487
Details still contains Room, Window Location, Drape Style, rods, fabrics, lining, and dimensions
```

- [ ] **Step 6: Verify an eligible catalog product at four widths**

At Figma desktop width, `1440px`, `768px`, and `390px`, verify:

```text
Exactly one .davis-catalog-product wrapper and one H1
Maximum desktop content width is 1410px
Desktop gallery/divider/summary relationship matches 600px / 1px / 700px intent
Tablet gallery stacks above summary and related products use two columns
Mobile controls remain within 390px, tabs scroll horizontally, and related products use one column
No horizontal document overflow
No clipped title, description, notices, variation fields, tab content, or related-card text
```

- [ ] **Step 7: Verify interactions without purchasing**

Use a fresh browser cart session:

```text
Quantity minus stops at min
Quantity plus stops at max when max is present
Quantity change is reflected in the native input
Wishlist control is keyboard-focusable and its aria-pressed state follows add/remove
Gallery thumbnail changes the main image when multiple images exist
Each available tab opens its native WooCommerce panel
One representative eligible product adds to cart successfully
Generated product 6970 retains its current Add to Cart behavior
```

- [ ] **Step 8: Check server/browser errors and rollback on failure**

Confirm no PHP warnings/fatals and no new browser console errors. If a blank page, PHP parse error, routing regression, or broken Add to Cart occurs, restore `functions.php` and `woocommerce/single-product.php` from the dated Task 1 backups before continuing.

- [ ] **Step 9: Commit final deployment records**

```powershell
git add wordpress-child-theme-working/catalog-single-product docs/superpowers/plans/2026-07-21-catalog-single-product-figma.md
git commit -m "feat: implement catalog product Figma layout"
```

## Completion Evidence

Record in the final handoff:

- Backup filenames.
- PHP lint results.
- Contract-test and `node --check` results.
- Product IDs/URLs used for eligible and generated-product verification.
- Desktop/tablet/mobile measured widths and overflow results.
- Add-to-cart and wishlist outcomes.
- Any unavailable edge-case product types that could not be exercised.
