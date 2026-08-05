# Drapery Product Card Actions

## Goal

Replace WooCommerce's generic `Read more` action on drapery product cards with the action selected for that product in ACF, while matching the supplied Figma nodes.

## Data source and precedence

- `replace_drapery_button` (`field_66f41f60c722c`, label `Add Drapery Button`) selects the builder action.
- `add_email_custom_qoute` (`field_66f420305a209`, label `Add Email Custom Qoute`) selects the email action. The existing field name is intentionally preserved despite its spelling.
- When the builder field is true, render the builder action.
- Otherwise, when the email field is true, render the quote action.
- If neither field is true, retain WooCommerce's existing loop action as a safe fallback.
- If both fields are true, the builder action wins so a malformed editor state does not create duplicate calls to action.

All current products in the Drapery category have exactly one of these fields enabled.

## Rendering architecture

Use WooCommerce loop hooks in the Kadence child theme rather than copying `content-product.php` or modifying card markup with JavaScript. Remove the default loop add-to-cart/read-more callback only for products with one of the ACF actions, then render one semantic anchor in the existing `.product-action-wrap` location. Products without either flag continue through WooCommerce's default callback.

The behavior applies wherever WooCommerce renders these products through its standard product loop, including product-category archives and related-product grids. It does not alter single-product purchase controls.

## Action destinations

- Builder: `/drapery-builder/`
- Quote: `mailto:sales@davisdrapery.com`

## Figma styling

### Builder action (`1657:19253`)

- Text: `BUILD YOUR OWN DRAPERY`
- Instrument Sans, 14px, 600 weight, 14px line height
- Uppercase with 0.84px letter spacing
- Text color `#700202`
- 1px border `#B9B9B9`, 8px radius
- 20px horizontal and 16px vertical padding

### Quote action (`1657:19360`)

- Text: `Email us for a custom quote`
- Instrument Sans, 16px, 400 weight, 24px line height
- Text color `#700202`, underlined
- Regular envelope icon in the same color and size
- 10px icon-to-label gap

Styles are scoped to the new loop-action classes so Kadence's generic WooCommerce button rules do not alter the Figma appearance.

## Accessibility and safety

- Anchors remain keyboard-focusable and receive a visible focus state.
- The envelope icon is decorative and hidden from assistive technology; the link text supplies the accessible name.
- URLs, labels, and class attributes are escaped with WordPress helpers.
- ACF access is guarded so the product loop retains its default action if ACF is unavailable.

## Verification

Automated contract tests will cover field precedence, destinations, labels, fallback behavior, and required scoped styles. The change will then be checked on the live Drapery category and a related-products grid at desktop and mobile widths for correct action selection, dimensions, typography, focus behavior, clipping, and overflow.
