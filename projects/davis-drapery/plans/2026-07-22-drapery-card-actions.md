# Drapery Product Card Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace WooCommerce `Read more` links with the ACF-selected Drapery Builder or custom-quote action and match the approved Figma components.

**Architecture:** Extend the existing catalog integration in the Kadence child theme. A `woocommerce_loop_add_to_cart_link` filter will preserve Kadence's product-card wrapper while replacing only the anchor for field-enabled products; a dedicated stylesheet will own the Figma action styles on archive and related-product loops.

**Tech Stack:** WordPress 7.0.2, WooCommerce 10.9.4, Kadence Child, ACF Pro, PHP 8.3, CSS, Node.js contract tests.

## Global Constraints

- `replace_drapery_button` is the builder field and has precedence over `add_email_custom_qoute`.
- Builder destination is `/drapery-builder/`; quote destination is `mailto:sales@davisdrapery.com`.
- Products with neither field retain WooCommerce's existing loop action.
- Builder styling must match Figma node `1657:19253`: `#700202`, 14px/600 Instrument Sans, 14px line height, 0.84px tracking, 20px by 16px padding, `#B9B9B9` border, 8px radius.
- Quote styling must match Figma node `1657:19360`: `#700202`, 16px/400 Instrument Sans, 24px line height, underline, 10px icon gap.
- The behavior applies to standard WooCommerce archives and related-product loops, not single-product purchase controls.
- Preserve the existing misspelled ACF field name `add_email_custom_qoute`.

---

## File Structure

- Modify `wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php`: choose and render the loop action; enqueue its stylesheet.
- Create `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/catalog-card-actions.css`: scoped archive/related card action presentation.
- Modify `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/single-product-catalog.css`: stop hiding related-product action wrappers so the approved loop action can render.
- Modify `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`: regression contracts for field precedence, destinations, hook registration, styles, and related-card visibility.

### Task 1: Add the ACF-driven loop action with contract coverage

**Files:**
- Modify: `wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs`
- Modify: `wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php`
- Create: `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/catalog-card-actions.css`
- Modify: `wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/single-product-catalog.css`

**Interfaces:**
- Consumes: `davis_catalog_product_has_drapery_button( WC_Product|int|null ): bool` and `davis_is_quote_only_catalog_product( WC_Product|int|null ): bool`.
- Produces: `davis_catalog_loop_action_markup( string $html, WC_Product $product, array $args ): string` registered on `woocommerce_loop_add_to_cart_link` with three accepted arguments.
- Produces: the classes `.davis-catalog-card-action`, `--builder`, `--quote`, and `__icon`.

- [ ] **Step 1: Write the failing contract assertions**

Add the new stylesheet read and the following assertions to `catalog-single-product-contract.test.cjs`:

```js
const cardActionsCss = read('assets/css/catalog-card-actions.css');

assert.match(helper, /function davis_catalog_loop_action_markup\s*\(/);
assert.match(helper, /woocommerce_loop_add_to_cart_link',\s*'davis_catalog_loop_action_markup',\s*20,\s*3/);
assert.match(helper, /davis_catalog_product_has_drapery_button\(\s*\$product\s*\)[\s\S]*davis_is_quote_only_catalog_product\(\s*\$product\s*\)/);
assert.match(helper, /home_url\(\s*'\/drapery-builder\/'\s*\)/);
assert.match(helper, /mailto:sales@davisdrapery\.com/);
assert.match(helper, /return \$html;/);
assert.match(helper, /catalog-card-actions\.css/);
assert.doesNotMatch(css, /\.davis-catalog-product\s+\.related\.products\s+\.product-action-wrap[\s\S]*display:\s*none\s*!important;/);
assert.match(cardActionsCss, /\.davis-catalog-card-action--builder\s*\{[^}]*border:\s*1px\s+solid\s+#b9b9b9;[^}]*border-radius:\s*8px;[^}]*padding:\s*16px\s+20px;/is);
assert.match(cardActionsCss, /font-size:\s*14px;[^}]*font-weight:\s*600;[^}]*letter-spacing:\s*0\.84px;[^}]*line-height:\s*14px;/is);
assert.match(cardActionsCss, /\.davis-catalog-card-action--quote\s*\{[^}]*font-size:\s*16px;[^}]*font-weight:\s*400;[^}]*gap:\s*10px;[^}]*line-height:\s*24px;[^}]*text-decoration:\s*underline;/is);
assert.match(cardActionsCss, /:focus-visible/);
```

- [ ] **Step 2: Run the contract test and verify RED**

Run from the `catalog-single-product` worktree:

```powershell
node wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
```

Expected: FAIL because `assets/css/catalog-card-actions.css` does not exist and the loop filter is not registered.

- [ ] **Step 3: Add the minimal PHP loop filter and enqueue**

Append this focused integration to `inc/catalog-single-product.php`:

```php
/**
 * Replace the default WooCommerce card action when an ACF action is selected.
 *
 * @param string     $html    Default WooCommerce action markup.
 * @param WC_Product $product Current loop product.
 * @param array      $args    Loop action arguments.
 * @return string
 */
function davis_catalog_loop_action_markup( $html, $product, $args ) {
	if ( ! $product instanceof WC_Product ) {
		return $html;
	}

	if ( davis_catalog_product_has_drapery_button( $product ) ) {
		return sprintf(
			'<a class="davis-catalog-card-action davis-catalog-card-action--builder" href="%1$s">%2$s</a>',
			esc_url( home_url( '/drapery-builder/' ) ),
			esc_html__( 'Build Your Own Drapery', 'kadence-child' )
		);
	}

	if ( davis_is_quote_only_catalog_product( $product ) ) {
		return sprintf(
			'<a class="davis-catalog-card-action davis-catalog-card-action--quote" href="%1$s"><span class="davis-catalog-card-action__icon fa-regular fa-envelope" aria-hidden="true"></span><span>%2$s</span></a>',
			esc_attr( 'mailto:sales@davisdrapery.com' ),
			esc_html__( 'Email us for a custom quote', 'kadence-child' )
		);
	}

	return $html;
}
add_filter( 'woocommerce_loop_add_to_cart_link', 'davis_catalog_loop_action_markup', 20, 3 );

/**
 * Load Figma-matched card actions anywhere WooCommerce renders product loops.
 *
 * @return void
 */
function davis_enqueue_catalog_card_action_assets() {
	$is_product_surface =
		( function_exists( 'is_shop' ) && is_shop() ) ||
		( function_exists( 'is_product_taxonomy' ) && is_product_taxonomy() ) ||
		( function_exists( 'is_product' ) && is_product() );

	if ( ! $is_product_surface ) {
		return;
	}

	$css_path = get_stylesheet_directory() . '/assets/css/catalog-card-actions.css';
	wp_enqueue_style(
		'davis-catalog-card-actions',
		get_stylesheet_directory_uri() . '/assets/css/catalog-card-actions.css',
		array( 'kadence-child' ),
		file_exists( $css_path ) ? (string) filemtime( $css_path ) : null
	);
}
add_action( 'wp_enqueue_scripts', 'davis_enqueue_catalog_card_action_assets', 35 );
```

- [ ] **Step 4: Add the scoped Figma CSS and expose related actions**

Create `assets/css/catalog-card-actions.css`:

```css
.woocommerce .product-action-wrap .davis-catalog-card-action {
	box-sizing: border-box;
	color: #700202;
	font-family: "Instrument Sans", sans-serif;
	margin: 0;
}

.woocommerce .product-action-wrap .davis-catalog-card-action--builder {
	align-items: center;
	background: transparent;
	border: 1px solid #b9b9b9;
	border-radius: 8px;
	display: inline-flex;
	font-size: 14px;
	font-weight: 600;
	justify-content: center;
	letter-spacing: 0.84px;
	line-height: 14px;
	padding: 16px 20px;
	text-align: center;
	text-transform: uppercase;
}

.woocommerce .product-action-wrap .davis-catalog-card-action--quote {
	align-items: center;
	display: inline-flex;
	font-size: 16px;
	font-weight: 400;
	gap: 10px;
	line-height: 24px;
	text-decoration: underline;
	text-underline-position: from-font;
}

.woocommerce .product-action-wrap .davis-catalog-card-action__icon {
	font-size: 16px;
	line-height: 1;
	text-decoration: none;
}

.woocommerce .product-action-wrap .davis-catalog-card-action--builder:hover {
	background: #700202;
	color: #fff;
}

.woocommerce .product-action-wrap .davis-catalog-card-action--quote:hover {
	color: #700202;
	text-decoration-thickness: 2px;
}

.woocommerce .product-action-wrap .davis-catalog-card-action:focus-visible {
	outline: 2px solid #700202;
	outline-offset: 3px;
}

.davis-catalog-product .related.products .product-action-wrap {
	display: flex !important;
	justify-content: center;
	margin-top: 12px;
}

.davis-catalog-product .related.products ul.products li.product {
	height: auto;
	min-height: 421px;
}
```

Remove the rule that sets `.davis-catalog-product .related.products .product-action-wrap` to `display: none !important` from `single-product-catalog.css`.

- [ ] **Step 5: Run the contract test and verify GREEN**

```powershell
node wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
```

Expected: `catalog single-product contracts passed` with exit code 0.

- [ ] **Step 6: Check PHP and diff hygiene**

```powershell
php -l wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php
git diff --check
```

Expected: PHP reports no syntax errors and `git diff --check` produces no output.

- [ ] **Step 7: Commit the tested implementation**

```powershell
git add wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/catalog-card-actions.css wordpress-child-theme-working/catalog-single-product/kadence-child/assets/css/single-product-catalog.css wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
git commit -m "feat: add ACF-driven drapery card actions"
```

### Task 2: Deploy and verify the live WooCommerce loops

**Files:**
- Deploy: `wp-content/themes/kadence-child/inc/catalog-single-product.php`
- Deploy: `wp-content/themes/kadence-child/assets/css/catalog-card-actions.css`
- Deploy: `wp-content/themes/kadence-child/assets/css/single-product-catalog.css`

**Interfaces:**
- Consumes: the tested files from Task 1.
- Produces: live archive and related-product card actions selected from the two ACF fields.

- [ ] **Step 1: Back up the three live targets**

Read each live file before writing and preserve timestamped copies under the existing local `sync-artifacts` directory. The new CSS target may not exist; record that state instead of fabricating a backup.

- [ ] **Step 2: Deploy the tested files**

Use the WordPress file abilities to write the exact tested local bytes to the three child-theme targets. Do not edit `wordpress-child-theme-php-backup`; it is reference-only.

- [ ] **Step 3: Clear WordPress/Kadence page caches**

Call `rocket_clean_domain()` when available and `wp_cache_flush()` in the loaded WordPress environment. Expected: both calls complete without warnings.

- [ ] **Step 4: Verify server integration before visual QA**

Run a read-only WordPress check that confirms:

```php
return array(
	'filter_priority' => has_filter( 'woocommerce_loop_add_to_cart_link', 'davis_catalog_loop_action_markup' ),
	'css_exists'      => file_exists( get_stylesheet_directory() . '/assets/css/catalog-card-actions.css' ),
	'box_action'      => davis_catalog_product_has_drapery_button( 3500 ),
	'clear_action'    => davis_is_quote_only_catalog_product( 3502 ),
);
```

Expected: priority `20`; CSS, box builder action, and clear-curtain quote action are all `true`.

- [ ] **Step 5: Verify the Drapery archive in the browser**

On `/product-category/drapery/`, inspect at least:

- Product 3500: `BUILD YOUR OWN DRAPERY`, `/drapery-builder/`, 14px/600, 0.84px tracking, 1px `#B9B9B9` border, 8px radius, 16px/20px padding.
- Product 3502: envelope plus `Email us for a custom quote`, `mailto:sales@davisdrapery.com`, 16px/400, 24px line height, 10px gap, underline.
- No field-enabled card retains `READ MORE`.

Expected: no clipping, overlap, horizontal overflow, or card-width expansion at desktop and a mobile viewport.

- [ ] **Step 6: Verify a related-products loop**

Open a standard catalog product with related drapery items. Confirm actions are visible, selected from the same ACF fields, centered, and contained by auto-height cards; confirm single-product purchase controls are unchanged.

- [ ] **Step 7: Run final local verification**

```powershell
node wordpress-child-theme-working/catalog-single-product/tests/catalog-single-product-contract.test.cjs
php -l wordpress-child-theme-working/catalog-single-product/kadence-child/inc/catalog-single-product.php
git status --short
```

Expected: contract passes, PHP syntax passes, and status contains no uncommitted files from this feature.
