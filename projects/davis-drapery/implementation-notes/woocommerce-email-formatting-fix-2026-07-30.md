# WooCommerce customer email formatting fix

Applied on July 30, 2026 to the live Davis Drapery WordPress site.

## Changes

- Changed the WooCommerce email header image setting from
  `DD-logo-med.png` to `DD-logo.png`.
- Added `wp-content/novamira-sandbox/davis-woocommerce-email-formatting.php`.
  The module replaces WooCommerce `tel:` anchors with their visible phone
  number text after the HTML email is rendered. Other email links are unchanged.
- Customer processing-order and completed-order emails remain enabled.

## Local source and test

- `wordpress-child-theme-working/davis-woocommerce-email-formatting.php`
- `wordpress-child-theme-working/tests/davis-woocommerce-email-formatting.test.js`

Run the contract test with:

```powershell
node wordpress-child-theme-working/tests/davis-woocommerce-email-formatting.test.js
```

## Verification

Order 7061 was rendered in memory without sending an email. The rendered
customer processing-order email contained the requested logo URL, contained no
`tel:` anchors after the formatting filter, and retained the visible billing
phone number.

## Recovery

The prior email setting is recorded on the server at:

`wp-content/novamira-sandbox/backups/woocommerce-email-formatting-before-20260730.json`

To roll back, disable or remove the formatting module and restore
`woocommerce_email_header_image` to the previous value recorded in the backup.
