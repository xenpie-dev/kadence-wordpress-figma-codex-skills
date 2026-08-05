# Drapery Builder Settings and Workbook-Aligned Constants

## Goal

Make the existing WordPress **Drapery Builder Settings** page the single administrative source for every fixed business value used by the Drapery Builder calculations. The builder must read those settings for both the primary/farthest treatment and the closest-to-window treatment on a double rod.

The updated workbook is the default-value specification. The source reviewed for this design is the Google Drive workbook downloaded on 2026-08-04 as `audit_work/linked-2026-08-04.xlsx`, especially the `Updated Worksheet`, `Rod Selection`, `Lining Data`, and `Interlining Data` sheets.

This work does not turn product catalog records into global settings. Selected fabric width, repeat, cost, and markup and each rod's base/additional-foot price remain sourced from their existing catalog data. The settings page owns fixed construction, allowance, threshold, fullness, and labor/material-pricing rules that are currently embedded in the builder code.

## Access

- Retain the existing WordPress admin URL: `/wp-admin/admin.php?page=drapery-builder-settings`.
- Change the options-page capability from `edit_posts` to `manage_options`.
- Only administrators or another role deliberately granted `manage_options` may view or save these settings.
- Frontend visitors may consume the normalized values only through the builder calculation configuration; they cannot change them.

## Recommended architecture

Keep the existing ACF PRO options page and add a version-controlled local ACF field group for the workbook-aligned settings. Do not create another settings page. The registration and normalization code will live in a recoverable site settings module rather than being buried in the large builder template.

A small settings module will have three responsibilities:

1. Register the ACF fields and their workbook defaults.
2. Load, sanitize, validate, and normalize all saved values into one configuration array.
3. Enforce `manage_options` on the existing options page.

The large builder template will consume one normalized PHP configuration object encoded with `wp_json_encode`. Both calculation paths will use that same object. Individual `get_field()` calls and independent fallback literals must not be scattered through the JavaScript calculations.

If ACF is unavailable, a field has never been saved, or a stored value is invalid, the normalizer will supply the workbook default. That preserves a functional builder without silently reverting to the builder's old constants.

## Settings model and workbook defaults

### Construction and measurement

| Setting | Default | Workbook source | Use |
|---|---:|---|---|
| Rod included length | 48 in | `Updated Worksheet!D23` formula | Length covered by the selected rod's base price |
| Rod billing increment | 12 in | `Updated Worksheet!D23` formula | Increment used for additional-foot pricing |
| Farthest return | 6 in | `Updated Worksheet!D25` | Room-side treatment on a double rod |
| Closest/single return | 4 in | `Updated Worksheet!D25`, `D43`, `D45` | Single rod or wall-side treatment |
| Overlap | 3.5 in | `Updated Worksheet!D26`, `D46` | Shared by both treatment calculations |
| Cut ease | 2 in | `Updated Worksheet!D27`, `D47` | Shared value used in width and cut-length formulas |
| Single-panel side hems | 6 in | `Updated Worksheet!D33`, `D53` | Side-hem allowance for one panel |
| Pair side hems | 12 in | `Updated Worksheet!D33`, `D53` | Side-hem allowance for a pair |
| Double header | 8 in | `Updated Worksheet!D36`, `D56` | Cut-length header allowance |
| Railroad cutoff | 118 in | `Updated Worksheet!D40`, `D60` | Cut-length boundary for railroad calculation |
| Lining/interlining width | 54 in | `Updated Worksheet!D63`, `D66` | Standard lining width |
| Labor-width divisor | 50 in | `Updated Worksheet!D76`, `D84` | One-way or split-draw labor-width calculation |

One setting is used for overlap and one setting is used for cut ease. The duplicated drapery/sheer workbook cells do not become duplicate WordPress fields because their approved values and meaning are identical.

### Fabric overage tiers

The builder will use a validated, ordered table corresponding to `Updated Worksheet!D41` and `D61`:

| Finished length | Multiplier |
|---|---:|
| Less than 100 in | 1.07 |
| 100–119 in | 1.085 |
| 120–139 in | 1.10 |
| 140–159 in | 1.12 |
| 160 in or more | 1.14 |

The four breakpoints and five multipliers are administrator-editable. Breakpoints must remain strictly increasing and multipliers must be positive.

### Lining and interlining allowances

The lining and interlining cut-length allowance table corresponds to `Updated Worksheet!D64` and `D67`:

| Bottom hem | Added cut length |
|---|---:|
| 4 in | 9 in |
| 6 in | 11 in |
| 8 in | 13 in |
| 10 in | 15 in |
| 12 in | 17 in |

The five allowances are administrator-editable. The builder's selectable hem sizes are expected to map to this table. An unsupported value must not be silently assigned an unrelated allowance: the calculation returns a custom-quote state and does not display a numeric total.

### Labor pricing

| Setting | Default | Workbook source |
|---|---:|---|
| Lined labor add-on | $10.00 | `Updated Worksheet!D71` |
| Interlined labor add-on | $19.50 | `Updated Worksheet!D72` |
| Large-bottom-hem threshold | More than 4 in | `Updated Worksheet!D74`, `D82` |
| Large-bottom-hem charge | $9.00 per labor width | `Updated Worksheet!D74`, `D82` |

The corrected large-bottom-hem rule adds $9 to the per-width labor amount and then applies the labor-width count once. It must not multiply by the labor-width count before the final labor multiplication.

The extra-length table corresponds to `Updated Worksheet!D73` and `D81`:

| Finished length | Add-on per labor width |
|---|---:|
| Less than 110 in | $0.00 |
| 110–118 in | $22.00 |
| 119–190 in | $32.00 |
| 191–230 in | $55.50 |
| 231 in or more | Custom quote |

The four numeric breakpoints and four numeric add-ons are administrator-editable. The final custom-quote state is preserved rather than converted into an arbitrary price.

### Style fullness and base labor

The settings page will expose a fixed row for every style in `Updated Worksheet!H36:J42`. Each row has separate drape fullness, sheer fullness, and base labor fields:

| Style | Drape fullness | Sheer fullness | Base labor |
|---|---:|---:|---:|
| Pinch Pleat | 2.0 | 2.5 | $37.50 |
| Euro Pleat | 2.0 | 2.5 | $37.50 |
| Inverted Box Pleat | 3.0 | 3.0 | $54.50 |
| Goblet Pleat | 3.0 | 3.0 | $49.50 |
| Grommet Top | 2.0 | 2.0 | $88.50 |
| Ripplefold 100% | 2.5 | 2.5 | $48.25 |
| Rod Pocket Top | 3.0 | 3.0 | $42.00 |

The current ACF `base_pricing` option remains readable during migration as a backwards-compatible fallback for the Pinch Pleat and Euro Pleat $37.50 defaults. Once the new style fields exist, the style-specific fields are authoritative. The old field is hidden from the settings form after migration so administrators do not see two controls for the same concept; its saved option is not deleted.

### Fixed material pricing

The current builder has old inline lining and interlining values marked in code as needing a proper data source. Per the requirement that the builder read constants from Builder Settings, the following values become settings:

| Setting | Default | Workbook source |
|---|---:|---|
| Generic sample price | $6.00 | `Updated Worksheet!D30`, `D50` |
| Lining cost per yard | $8.00 | `Lining Data!C3:C6` |
| Lining markup | 1.70 | `Lining Data!D3:D6` |
| Lining sample price | $6.00 | `Lining Data!F3:F6` |
| Interlining cost per yard | $9.00 | `Interlining Data!D3` |
| Interlining markup | 1.70 | `Interlining Data!E3` |
| Interlining sample price | $8.00 | `Interlining Data!G3` |

These are global settings only while the builder offers the workbook's single-price lining/interlining choices. If lining or interlining later becomes a true item catalog with different prices per selection, selected item data should supersede these globals in a separate change.

### Values intentionally locked in code

The following are mathematical or control-flow mechanics, not business settings:

- 12 inches per foot and 36 inches per yard as unit conversions.
- `ceil`, `round up`, and `round to the next even width` operations.
- Panel count semantics: one panel versus a pair of two panels.
- No-rod, no-lining, and no-interlining zero behavior.
- Formula ordering and the selection of closest versus farthest treatment.

The 12-inch rod billing increment is still editable as a business rule even though its workbook default happens to equal one foot. The separate inches-per-foot conversion remains locked.

## Field presentation and validation

The ACF field group will be divided into clear tabs or accordions:

1. Construction
2. Overage
3. Lining and Interlining
4. Labor Tiers
5. Style Fullness and Labor
6. Material Pricing

All fields use numeric controls with units in the label or instructions. Currency supports cents; fullness and multipliers support at least three decimals where the workbook requires it.

Validation rules:

- Required numeric fields cannot be blank.
- Lengths, prices, and multipliers cannot be negative.
- Divisors, increments, widths, and multipliers must be greater than zero.
- Overage and extra-length breakpoints must be strictly increasing.
- Fullness values must be greater than zero.
- Runtime normalization repeats the safety checks even if data was stored before the validation hooks existed.
- A bad individual value falls back to its workbook default and must not corrupt the whole configuration.

## Builder data flow

1. WordPress loads option values through the settings module.
2. The module returns one complete normalized array with workbook defaults filled in.
3. The builder template emits that array once as JSON.
4. `DavisDraperyFormulaV2` receives the configuration and uses it in `overageMultiplier`, `bottomHemAllowance`, `extraLengthLabor`, `getStyleRule`, and `calculateTreatment`.
5. The primary/farthest and closest treatment calls use the same configuration. They differ only where the configuration or selected rod position requires different return sizes and selected material data.
6. Totals and the debug panel use the results of those configured calculations; they do not maintain a second set of legacy formulas.

This replaces the current mismatch where the primary path defaults to overlap 1.5, ease 6, and double header 14 while the closest path passes overlap 3.5, ease 2, and double header 8.

## Compatibility and migration

- Preserve the existing page slug and `options` storage scope.
- Register new ACF fields with stable field keys and option names so deployments are repeatable.
- Do not delete existing option data.
- Use the existing `base_pricing` value only as a migration fallback as described above.
- Seed all unsaved fields from workbook defaults through the normalizer; an administrator does not need to press Save before the builder remains functional.
- Refresh the local builder template from the current live copy before editing because the inspected live template differs from the local working copy.
- Keep the recoverable field-registration/settings module separate from the large template so the schema and defaults are reviewable and can be disabled independently.

## Error handling

- If ACF PRO is inactive, return the full workbook-default configuration.
- If an option is missing or malformed, substitute only that setting's default.
- If a tier table is unordered, reject the admin save and retain the previous valid settings.
- If the frontend receives no configuration object, the calculation helper uses the same workbook-default configuration embedded in its testable adapter, not the old legacy literals.
- Unsupported custom-quote tiers must not produce `NaN`, negative, or misleading numeric totals.

## Testing

Implementation follows test-driven development.

Automated tests will cover:

- Workbook defaults for every settings key.
- Administrator-only `manage_options` capability and the unchanged page slug.
- Missing, malformed, negative, zero-divisor, and unordered-tier handling.
- Style lookup for every workbook row.
- Overage boundary values at 99/100, 119/120, 139/140, and 159/160 inches.
- Extra-length boundary values at 109/110, 118/119, 190/191, and 230/231 inches.
- Hem allowances for 4, 6, 8, 10, and 12 inches.
- The corrected flat $9 large-bottom-hem add-on per width.
- A non-default injected configuration changes both primary and closest treatment results, proving both paths use Builder Settings.
- Lining cost $8 and interlining cost $9 with 1.70 markups.
- The updated workbook example reconciles to the expected calculation after all workbook-aligned constants are applied.
- No active builder calculation retains a duplicate hardcoded business constant or direct scattered ACF lookup.

Live verification will confirm:

- An administrator can load and save the settings page.
- A non-administrator is denied by the page capability.
- Saved changes alter the Drapery Builder total without a code deployment.
- Single-rod and double-rod primary/closest calculations both respond to shared overlap/ease changes.
- Refreshing the page preserves saved values and calculation behavior.
- Restoring the workbook defaults restores the expected workbook-aligned totals.

## Deployment and rollback

1. Back up the current live builder template and current option values.
2. Deploy the settings module/field group first; defaults keep existing calculations available.
3. Deploy the tested builder integration.
4. Run the live verification checklist with workbook defaults.
5. If rollback is required, restore the prior template and disable/remove the settings module. Saved options remain harmless and recoverable.

No workbook or product catalog data is modified by this feature.
