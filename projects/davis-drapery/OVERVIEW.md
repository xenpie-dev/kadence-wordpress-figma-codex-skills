# Davis Drapery Project Overview

This file captures project memory that should help with future feature development.
It is based on inspection of the Figma design file and the live WordPress staging page:

- Figma: https://www.figma.com/design/JE7ALOmjVP2wwKpRlvmtdO/Davis-Drapery?m=dev
- Drapery Builder: https://wordpress-421525-4426215.cloudwaysapps.com/drapery-builder/

## Big Picture

Davis Drapery & Interiors is a refined interiors/ecommerce site for custom drapery, fabrics, rods/tracks, samples, and related account/cart workflows.

The Figma file is primarily a brand and component guide, not a complete set of page mockups. The live Drapery Builder is a custom WordPress/WooCommerce configurator, not a normal editable Gutenberg page.

## Design System Understanding

The Figma file has two top-level pages:

- `Thumbnail`: cover art with the Davis Drapery logo.
- `Guide`: brand assets, colors, typography, buttons, forms, social image cards, and an account sidebar component.

Figma does not currently show complete website page layouts such as homepage, product listing, product detail, cart, checkout, or the full drapery-builder flow. Treat it as the visual foundation/component library unless a more specific Figma node is provided.

### Brand

- Brand name: Davis Drapery & Interiors.
- Logo: maroon stylized "D" mark plus black serif wordmark.
- Favicon: maroon stylized "D" mark in a white rounded square.
- Visual tone: restrained luxury/interiors, mostly neutral with deep maroon accents.

### Colors

Primary colors:

- Black: `#000000`
- White: `#FFFFFF`
- Maroon: `#700202`

Text colors:

- `#0D0D0D`
- `#222222`
- `#5C5C5E`

Background/line/border colors:

- Lines on dark background: `#3E3E3E`
- Lines on white background: `#9F9F9F`
- Border: `#B9B9B9`

### Typography

Heading font: `Cormorant Garamond`

Body/UI font: `Instrument Sans`

Desktop scale:

- H1: 76px, line-height 1.1em
- H2: 54px, line-height 1.1em
- H3: 40px, line-height 1.1em
- H4: 20px, line-height 1.1em
- Testimonial text: 38px, line-height 1.3em
- Big body text: 20px, line-height 1.6em
- Body text: 16px, line-height 1.5em
- Body small: 14px, line-height 1.5em
- Button text: 14px, line-height 1.0em, uppercase, 6% letter spacing

Tablet scale:

- H1: 62px
- H2: 48px
- H3: 32px
- H4: 20px
- Testimonial text: 30px
- Big body text: 16px
- Body text: 16px
- Body small: 14px
- Button text: 14px uppercase, 6% letter spacing

Mobile scale:

- H1: 38px
- H2: 30px
- H3: 22px
- H4: 20px
- Testimonial text: 24px
- Big body text: 16px
- Body text: 16px
- Body small: 14px
- Button text: 14px uppercase, 6% letter spacing

### Figma Components

The guide includes:

- Buttons: filled, ghost, icon-left, icon-right, icon-only, hover, disabled, dark-background variants.
- Pagination and badges.
- Forms: default, completed, typing, password, dropdown, error, textarea, search, checkboxes, radio buttons, switches.
- My Account sidebar variants: Orders, Wishlist, Addresses, Payment Methods, Account Details, Log Out.
- Social/website image cards.

## Live WordPress Site Context

Observed environment from the WordPress connector:

- WordPress 7.0
- PHP 8.3.31
- Active theme: `Kadence Child` with parent `Kadence`
- Active plugins include WooCommerce, ACF PRO, Kadence Blocks, Kadence Blocks Pro, Kadence Theme Kit Pro, WPCode Lite, Gravity Forms, Filter Everything PRO, WooPayments, Stripe, Square, WP Rocket, Novamira.

Important: the local workspace currently does not contain the WordPress codebase. The real implementation lives on the connected WordPress server. Use the `novamira_wordpress_421525` connector for source inspection and edits unless a local copy is later added.

## Sitewide Footer And Dynamic Credits

- The sitewide footer is the published Kadence Element `Main Footer`, post ID `37`.
- Its copyright credit is the `kadence/advancedheading` block with unique ID `37_7e11b0-4b`.
- The saved credit uses `© [davis_current_year] Davis Drapery & Interiors. All Rights Reserved.` instead of a hardcoded year.
- The `[davis_current_year]` shortcode and targeted Kadence render filter are maintained in `wp-content/novamira-sandbox/davis-dynamic-footer-year.php` on the connected WordPress server. They render the WordPress site year from `wp_date('Y')`.
- When creating or auditing footer credits, copyright notices, or similar year-based credits, never leave a four-digit year hardcoded. Reuse the site's dynamic year mechanism, or add an equivalent server-rendered mechanism when none exists.
- After changing the footer or its dynamic-year implementation, clear WP Rocket and the object cache, then verify both the saved token and the rendered current year on a public page.

## Local Child Theme PHP Backup

A read-only backup snapshot of the live Kadence child theme PHP files exists at:

- `wordpress-child-theme-php-backup/kadence-child-php-20260706-190101/`

The backup was copied from `wp-content/themes/kadence-child` on the connected WordPress server and contains 25 PHP files plus `BACKUP-MANIFEST.json`. It is for reference/recovery only. Do not edit files inside `wordpress-child-theme-php-backup/`; use the WordPress connector or a separate working copy for implementation changes.

## Drapery Builder Page Ownership

Live page:

- URL: `/drapery-builder/`
- WordPress page title: `Drapery Builder`
- Page ID: `1003`
- Page status: `publish`
- Saved `post_content`: empty
- Page template meta: `fabric-selection-v2.php`

This means the page is not built from editable page blocks. The visible builder is owned by the child theme template and related child-theme code.

Primary implementation files on the server:

- `wp-content/themes/kadence-child/fabric-selection-v2.php`
  - Current main page template.
  - Contains the form markup.
  - Contains a large inline JavaScript block for wizard navigation, validation, fabric filtering, order summary, and pricing.
  - Also contains some inline CSS at the top.
- `wp-content/themes/kadence-child/assets/css/fabric-style.css`
  - Main builder styling file.
  - Loaded publicly on the Drapery Builder page.
- `wp-content/themes/kadence-child/functions.php`
  - Registers the page template.
  - Adds the "Build Your Own Drapery" button on product pages.
  - Defines helper functions such as `get_rod_selections()`.
  - Handles AJAX endpoints for fabrics, rod selections, wishlist, and pricing settings.
  - Handles custom form submission and WooCommerce product/cart creation.
- `wp-content/themes/kadence-child/assets/js/simple-drapery-pricing.js`
  - Exists on disk but was not loaded on the public Drapery Builder page during inspection.

Observed loaded custom asset on `/drapery-builder/`:

- CSS: `wp-content/themes/kadence-child/assets/css/fabric-style.css?ver=1.0.0`
- No custom drapery JS file was loaded by URL during inspection; the active builder logic appears to be inline inside `fabric-selection.php`.

Important caveat: `functions.php` references `drapery-pricing-config.js`, `drapery-pricing-fixes.js`, and `drapery-dynamic-pricing.js`, but those files were not present in `assets/js` and were not loaded on the live page. Do not assume that referenced pricing-script system is active.

## Drapery Builder User Flow

The wizard is a multi-step configurator:

1. Room Location
   - Room selection defaults include Living Room, Kitchen, Dining Room, Study, Master Bedroom, Bedroom 2, Guest Bedroom, Custom.
   - Window location options: A through F.
2. Measurements
   - Left Extension
   - Window Opening
   - Right Extension
   - Rod Size = left extension + window opening + right extension.
   - Drapery height, capped at 230 inches in the UI with call-us messaging above 230/231 inches.
3. Drape Style
   - Pinch Pleat Drape
   - Euro Pleat
   - Grommet Pleat
   - Goblet Pleat
   - Ripple Fold
   - Rod Pocket Top
   - Bottom hem size: 4, 6, 8, 10, 12 inches.
4. Panel or Pair
   - Panel or Pair.
   - Panel placement for single panel: Left, Center, Right.
5. Rod Setup
   - Mount type: Wall Mount or Ceiling Mount.
   - Rod purchase: no rod/track or include rod/track.
   - Rod style selection from `rod-selection` posts.
   - Rod setup: Single Rod or Double Rod.
6. Material
   - Drapery or Sheer.
   - Fabric selection with filtering.
   - Fabric sample/info modal available.
6.1/7. Lining
   - With Lining or No Lining.
   - Lining options.
   - With Interlining or No Interlining.
   - Interlining option.
7. Material, for double-rod scenarios
   - Additional fabric/material selection for the other rod/layer.
8. Order Summary
   - Displays chosen room, location, style, panel/pair, rod, material/fabric, lining, interlining, finished dimensions, and calculation debug details.
9. Sticky bottom bar
   - Warns not to refresh.
   - Shows total price.
   - Add to cart is hidden until the flow is sufficiently complete.

Browser-confirmed behavior:

- Step visibility is enforced; hidden fields cannot be interacted with until the relevant step is active.
- After selecting window location and advancing, Step 2 becomes active.
- With measurements 4, 60, and 4, `rod_size` updates to `68.00`.
- Advancing from Step 2 reaches Step 3 Drape Style.
- No horizontal overflow was observed on desktop width 1440 or mobile width 390 during the quick inspection.

## Data Model

Observed custom post types relevant to the builder:

- `fabric`
  - Label: Fabrics
  - Public UI
  - Observed count: 109 published
  - Taxonomies: `color-way-option`, `light-allowance`, `pattern`, `room-location`, `use`
- `rod-selection`
  - Label: Rod Selections
  - Public UI
  - Observed count: 9 published
  - Taxonomy: `color`
- `drapery-order`
  - Label: Drapery Orders
  - Public UI
  - Observed count: 22 published
- WooCommerce `product`
  - Observed count: 98 published, 1 draft

### ACF Field Groups

Relevant ACF groups observed:

- `Drapery Builder Fields`
  - Location: options page `drapery-builder-settings`
  - Field: `base_pricing`
  - Observed value: `37.50`
- `Fabric`
  - Location: post type `fabric`
  - Fields include `short_description`, `content`, `fabric_material`, `fabric_width`, `client_price_per_yard`, `mark_up`, `vertical_repeat`, `my_cost_per_yard`, `sku`, `fabric_image`, `inner_fabric_image`, `replace_drapery_button`, `add_build_drapery_button`, `sample_price`, `color`, `vendor`, `flame_scale`.
- `Rod Selections`
  - Location: post type `rod-selection`
  - Fields include `sku`, `my_cost_for_4`, `my_cost_per_each_additional_ft`, `markup`, `client_price_for_4_foot`, `client_price_per_additional_foot`.
- `Drapery Orders`
  - Location: post type `drapery-order`
  - Fields include `price`, `room_location`, `window_location`, `fabric_selection`, `rod_setup`, `inner_fabric`, `outer_fabric`.
- `Products`
  - Location: post type `product`
  - Fields include drapery metadata such as room, window, drape style, bottom hem, panel option, rod setup, rod selection, rod size, material type, fabric selection, lining, interlining, finished width/length, closest/farthest fields, and fabric image URLs.

Observed fabric sample fields can have money strings such as `$15.00`, so pricing code must normalize numeric strings safely.

## Pricing Understanding And Limits

The template includes calculation variables named to match an Excel/spreadsheet model, including:

- Basic measurements: Rod Size `C21`, Finished Length `C15`, Panel or Pair `C20`, Rod Setup Return `C25`.
- Fabric calculations: Fabric Width `C31`, X Fullness `C32`, Side Hems `C33`, Cut Width `C34`, Cut Width Paneled `C35`, Vertical Repeat, Cut Length `C37`.
- Yardage: Total Yardage `C38`, Total Required Yards `C40`, Overage Multiplier `C41`.
- Lining: Lining Width `C43`, Lining Cut Length `C44`, Lining Yards Required `C45`.
- Pricing: Rod Total Cost `C49`, Drape Style Value `C50`, Total Labor Per Width `C55`, Drape One Way/Split `C56`, Drape Labor Price `C57`, Cost Per Yard `C58`, Mark Up `C59`, Main Fabric Price/Yard `C60`, Fabric Price `C61`, Lining Cost/Yard `C62`, Lining Markup `C63`, Lining Price/Yard `C64`, Lining Fabric Price `C65`, Interlining Price/Yard `C66`, Interlining Fabric Price `C67`.

Observed high-level behavior:

- Rod size is calculated client-side from left extension, window opening, and right extension.
- The active total price is calculated client-side in the inline template JavaScript, then written to hidden fields for submission.
- Double-rod behavior uses a stored main fabric price while the second material step is being configured.
- Debug output exists on the order-summary step for comparing calculation variables to the Excel model.

Important limit: I can read and modify the current formulas, but I cannot verify commercial correctness without the source spreadsheet/specification. Any pricing feature should be tested against known expected examples.

## Spreadsheet Formula Reference

A formula-only spreadsheet reference package has been created locally at:

- `spreadsheet-ai-copy/`

This package is intended to support Drapery Builder pricing and measurement feature work. It preserves formula logic, cached/example values, workbook structure, named ranges, validations, external references, and test cases from the shared Excel-backed Google Sheets files.

Important files:

- `spreadsheet-ai-copy/formula-map.md`
  - Human-readable Drapery Builder formula flow.
- `spreadsheet-ai-copy/formula-dependencies.md`
  - Maps spreadsheet lookup intent to WordPress post types and ACF fields.
- `spreadsheet-ai-copy/formulas.json`
  - Machine-readable formula inventory with cells, exact formulas, cached values, and dependencies.
- `spreadsheet-ai-copy/formula-translation-mismatch-flags.md`
  - Flags rows where `Updated Worksheet` column `D` formula translation appears stale or inconsistent with column `C`.
- `spreadsheet-ai-copy/test-cases.md`
  - Spreadsheet-derived example inputs and expected outputs.
- `spreadsheet-ai-copy/workbook-index.md`
  - Workbook/sheet inventory and formula counts.
- `spreadsheet-ai-copy/source/`
  - Raw copied `.xlsx` source workbooks.

The reference intentionally does not treat spreadsheet lookup rows as production data. Fabric, rod, lining, interlining, and option data should come from WordPress post types/ACF where possible. Use the spreadsheet package for formula behavior, rounding, constants, dependencies, and parity test cases.

## WooCommerce And Cart Behavior

The custom form submission path is handled in `functions.php` by `handle_custom_order_form_submission()` on `template_redirect`.

Observed behavior from source:

- The form posts selected builder data back through the page/cart flow.
- The handler sanitizes posted fields.
- It creates a WooCommerce product/custom order representation with metadata.
- It adds the created product to the WooCommerce cart.
- On success it redirects to the cart page.

Important: because the page creates products/cart items from posted hidden fields, changes to frontend field names or pricing hidden fields can break cart/order metadata. Any feature touching form names, hidden fields, or summary values must verify add-to-cart end to end.

## Known Issues And Risks

Observed live console/page issues during browser inspection:

- 404 or aborted load for `wp-content/themes/kadence/js/ajax-login.js?ver=1.0`.
- Console error: `.fabric-filter-container not found.`
- JavaScript page error: `accountAddress_phoneFields.inputmask is not a function`.

Implementation risks:

- `fabric-selection.php` is large and mixes PHP, HTML, CSS, and inline JavaScript. Small changes can have wide effects.
- There are likely legacy or dead code paths:
  - `simple-drapery-pricing.js` exists but is not loaded publicly.
  - `functions.php` references pricing JS files that do not exist in `assets/js`.
- The page is template-driven, not block-driven. Editing page content in Gutenberg will not affect the builder UI.
- The Figma file does not provide a full drapery-builder screen design, so visual updates must be inferred from the design-system guide unless a new design is supplied.
- Pricing depends on multiple data sources: ACF option values, fabric post fields, rod-selection fields, frontend selections, and hidden fields.

## Feature Development Guidance

Before changing the builder:

1. Confirm the live owner of the behavior.
   - Most builder flow/pricing is in `fabric-selection-v2.php`.
   - Most styles are in `fabric-style.css`.
   - Data helpers, AJAX, wishlist, and submission are in `functions.php`.
2. Avoid editing page ID `1003` post content for builder changes; it is empty and the template owns the UI.
3. Check whether a proposed change is visual, data-model, pricing, or cart/order behavior.
4. For visual changes, compare against the Figma design guide:
   - Cormorant Garamond headings.
   - Instrument Sans body/UI.
   - Deep maroon `#700202`.
   - Restrained grayscale palette.
   - Buttons should be uppercase 14px with letter spacing where appropriate.
5. For pricing changes, get or reconstruct expected spreadsheet cases first.
6. For cart/order changes, test at least one successful add-to-cart path.
7. For double-rod changes, test closest and farthest material paths separately.
8. For mobile changes, inspect at 390px or similar and confirm no horizontal overflow.

Suggested QA matrix for builder features:

- Guest user and logged-in user.
- Single rod and double rod.
- No rod purchase and include rod/track.
- Panel and Pair.
- Each drape style, especially Ripple Fold because it has different labor/fullness behavior.
- Drapery material and Sheer material.
- With Lining and No Lining.
- With Interlining and No Interlining.
- Single panel placement: Left, Center, Right.
- Fabric sample modal and add sample to cart.
- Final Add to Cart and cart metadata.

## Source Of Truth By Topic

- Brand colors, typography, buttons, form states: Figma guide.
- Actual drapery-builder layout and DOM: `fabric-selection-v2.php`.
- The V2 template is assigned to both page ID `1003` (`/drapery-builder/`) and page ID `6996` (`/drapery-builder-2/`).
- Builder CSS: `assets/css/fabric-style.css`.
- Fabric data: `fabric` posts and ACF fields.
- Rod data: `rod-selection` posts and ACF fields.
- Base builder pricing option: ACF option `base_pricing`.
- Order/cart metadata: WooCommerce product meta and `drapery-order` records.
- Page content: not useful for this builder, because page ID `1003` has empty `post_content`.

## Drapery Builder V2 Template

- Original live builder page: `/drapery-builder/`, page ID `1003`, currently assigned to `fabric-selection-v2.php`.
- Formula staging builder page: `/drapery-builder-2/`, page ID `6996`, template `fabric-selection-v2.php`.
- The V2 template was created as a separate child-theme template and is now also active on the main builder page.
- Local working copy: `wordpress-child-theme-working/fabric-selection-v2.php`.
- Live child-theme target: `wp-content/themes/kadence-child/fabric-selection-v2.php`.
- Formula helper marker in V2: `DAVIS_DRAPERY_FORMULA_V2_START` / `DAVIS_DRAPERY_FORMULA_V2_END`.
- Local focused test: `wordpress-child-theme-working/tests/drapery-formula-v2.test.js`.
- Backup reference only: `wordpress-child-theme-php-backup/kadence-child-php-20260706-190101/`; do not edit backup PHP files.
- Current V2 formula choices:
  - Rod total doubles non-single rod purchases.
  - Width formulas use 1.5 inch overlap per panel plus 6 inch width ease.
  - Cut length uses 14 inch double header and `Math.ceil` repeat rounding.
  - Live V2 yardage uses the corrected short-cut-length branch: if cut length is under 118 inches, yardage is cut width divided by 36; otherwise cut length times cut widths divided by 36.
  - Lining/interlining cut length add-ons are mapped by bottom hem, including 2/4 inch hems adding 9 inches.
  - Large bottom hem labor uses 9 times rounded labor widths.
  - Fabric, rod, lining, and interlining lookup data should come from WordPress post types/ACF, not copied spreadsheet tables.

## Drapery Builder Finial Style

- Step 5 includes a `finial_style` dropdown with the five approved values from the computerized form.
- `None (Contract Track)` is the default.
- The value is shown in both single- and double-rod order summaries.
- The value is stored on the generated WooCommerce product, shown as cart item data, copied to the order line item, and shown in the generated product description.
- The WooCommerce integration is maintained in `wordpress-child-theme-working/drapery-finial-style.php` and deployed as the recoverable Novamira sandbox module `davis-drapery-finial-style.php`.

## Drapery Builder Mobile Layout

- At widths up to 768px, the builder uses the full available width with 16px outer gutters.
- The inline 65% form width is overridden only on mobile; desktop keeps the original two-column form/image layout.
- The responsive override is maintained in `wordpress-child-theme-working/fabric-mobile-layout.css` and loaded with file-modified cache versioning by `drapery-finial-style.php`.

## Material-Aware Colorways

- The Colorways dropdowns are derived from the fabrics available for the currently selected material instead of listing every global taxonomy term.
- Drapery shows the 25 unique values from the spreadsheet's `Fabric Data` sheet. The former zero-result Drapery choices (`Creamy White`, `Gold`, `Green`, `Linen`, and `White`) are no longer shown there.
- Singular/plural duplicates are standardized in the builder: `Grey` includes both `Grey` and `Greys` assignments, while `Tan` includes both `Tan` and `Tans` assignments.
- Sheer retains its eight valid values from `Sheer Data`, including the five labels that do not belong to Drapery.
- The behavior applies independently to the main and farthest fabric selectors and is maintained in `wordpress-child-theme-working/drapery-colorways.js`.

## Final Notes For Future Agents

Do not assume the design guide equals a finished page design. It defines the brand system.

Do not assume a local repository contains the WordPress source. In this workspace, the code was inspected through the WordPress connector on the live staging site.

Do not claim pricing is correct from code inspection alone. Verify against expected spreadsheet outputs.

Do not rely on `simple-drapery-pricing.js` unless you first confirm it is enqueued or intentionally wire it in. The active public page currently uses inline template JavaScript instead.
