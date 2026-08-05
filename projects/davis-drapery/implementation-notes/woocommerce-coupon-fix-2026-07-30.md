# WooCommerce Coupon Fix — 2026-07-30

## Request

- Allow only one coupon code per cart/order.
- Correct `fixprod10`, which deducted $10 once per product instead of $10 once from the cart.
- Keep the discount correct when cart items are removed.

## Root cause

Coupon ID `5154` (`fixprod10`) used WooCommerce's `fixed_product` discount type. WooCommerce applies that type's amount to every eligible item, so five eligible products produced a $50 discount.

## Live implementation

- Changed `fixprod10` from `fixed_product` to `fixed_cart`.
- Kept its amount at `$10`.
- Enabled WooCommerce's individual-use setting on `fixprod10`.
- Added `wp-content/novamira-sandbox/davis-woocommerce-coupon-guard.php`:
  - hides the coupon entry field after the first coupon is applied;
  - rejects a different second coupon on the server;
  - permits revalidation of the already-applied coupon during cart recalculation;
  - restores the coupon field after the applied coupon is removed.

The recoverable local source is `wordpress-child-theme-working/davis-woocommerce-coupon-guard.php`.

## Verification

An isolated live WooCommerce cart containing multiple products confirmed:

- `fixprod10` applies successfully;
- the total discount remains exactly `$10` with multiple products;
- removing a product changes the cart subtotal while the coupon stays exactly `$10`;
- a second coupon is rejected and the applied-coupon count remains one;
- removing `fixprod10` changes the discount to `$0` and re-enables coupon entry.

The complete local Node contract suite also passes.

## Rollback

- The original coupon configuration is recorded at `wp-content/novamira-sandbox/backups/fixprod10-before-cart-discount-20260730.json` on the server.
- Disable or remove `wp-content/novamira-sandbox/davis-woocommerce-coupon-guard.php` to remove the one-coupon behavior.
- Restore `fixprod10` to `fixed_product` and turn off individual-use only if the former per-product behavior is intentionally required.
