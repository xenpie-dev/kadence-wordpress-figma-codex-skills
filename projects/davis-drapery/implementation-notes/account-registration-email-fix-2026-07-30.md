# Account registration activation email fix

Date: 2026-07-30

## Cause

Gravity Forms form 2 (`Register`) correctly created pending User Registration
records, but its customer activation notification was disabled. The notification
was also attached to the `form_submission` event even though its message uses the
`{activation_url}` merge tag. That merge tag must be rendered for the User
Registration pending-activation event.

## Live change

Notification ID `66215849833d5` was updated as follows:

- Enabled: yes
- Event: `gfur_user_activation` (`User is pending activation`)
- Recipient: `{Email:9}` only
- Activation merge tag: retained
- Subject: `Activate Your Account on Davis Drapery`

The form confirmation already tells the registrant to check their email, so no
copy change was required after the notification was repaired.

All three User Registration feeds remain enabled with manual pending activation.
Their conditional routing was verified:

- General Consumer -> `general_consumer`
- Interior Designer -> `interior_designer`
- Wholesaler -> `wholesaler`

## Verification

The activation message rendered a valid URL on the connected WordPress host for
the current pending registration. The repaired notification was resent once for
entry 102. Gravity Forms returned the notification ID and WordPress fired
`wp_mail_succeeded` for the masked Gmail recipient.

This confirms that WordPress handed the message to its mail transport; it does
not by itself prove inbox placement.

## Mail transport follow-up

WP Mail SMTP is installed but currently selects the PHP `mail` transport. No
SMTP host, username, password, Mailgun domain, or Mailgun API key is configured.

Current public DNS observations for the forced From domain (`getdsm.com`):

- SPF: `v=spf1 include:mailgun.org ~all`
- DMARC: quarantine policy
- MX: Google Workspace

The SPF record authorizes Mailgun, not the current PHP-mail origin. Configure WP
Mail SMTP with the site's Mailgun domain and private API key, or choose another
authenticated provider and update SPF/DKIM before treating delivery as reliable.

## Backup and rollback

The pre-change export is stored on the WordPress server at:

`wp-content/novamira-sandbox/backups/register-form-2-before-email-fix-20260730.json`

Only the notification changed. A targeted rollback can restore the notification
from that export, or set it back to disabled with event `form_submission` and its
previous recipient value. The User Registration feed rows did not change.

After rollback, reload form 2 and verify the notification values directly rather
than relying only on a successful API response.
