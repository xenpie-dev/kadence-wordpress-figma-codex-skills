# Drapery Builder Formula Map

Generated: 2026-07-06T18:35:44.753719+00:00

This package captures formula logic only. Spreadsheet lookup rows are not treated as production data because the live site should read fabric, rod, lining, interlining, and product option data from WordPress post types and ACF fields.

Important: on the `Updated Worksheet` tab, the actual formula/value cells in column `C` sometimes disagree with the prose in column `D` (`Formula Translation`). Exact row-level flags are documented in `formula-translation-mismatch-flags.md`. When they conflict, treat column `C` as stronger evidence unless the business confirms the prose is the intended correction.

## Source Workbooks

| Workbook | Role | Sheets | Formula cells |
| --- | --- | --- | --- |
| davis-drapery-dev-copy-v1.xlsx | Shared main Drapery Builder calculator workbook. | 16 | 1811 |
| 20260210-master-1a-computerized-form.xlsx | Shared companion workbook containing formula translation and calculator variants. | 16 | 1811 |

## Calculation Flow

### 1. User Inputs

Core inputs observed in the Formula Translation sheet and calculator areas:

- room location and window sidemark
- rod setup and rod/track purchase choice
- drape or sheer
- drape style
- fabric or sheer selection
- left extension, window opening, right extension
- finished length / drapery height
- lining option, bottom hem, interlining option
- panel or pair, with placement for single panels

### 2. Rod Size And Rod Pricing

- `total_rod_size = left_extension + window_opening + right_extension`
- If the customer is not buying a rod/track, rod pricing is `0`.
- Otherwise, rod base pricing comes from the selected `rod-selection` post field equivalent to `client_price_for_4_foot`.
- Additional rod cost is based on inches over 48:
  - `additional_feet = CEILING((total_rod_size - 48) / 12)`
  - `rod_additional_cost = additional_feet * client_price_per_additional_foot`
- The Formula Translation area shows an example with total rod size `84`, base price `121.8`, additional cost `42`, and rod total `327.6`. This implies double-treatment multiplication may be applied in the total, so implementation should preserve the workbook's treatment-count behavior.

### 3. Return Size

- Closest-to-window or single rod return: `4`.
- Double rod farthest from window / room side return: `6`.
- The calculator also notes custom returns should be treated as an override or manual quote path.

### 4. Finished Width

Formula translation:

```text
finished_width = total_rod_size + (return_size * panels) + (overlap * panels) + ease
```

Observed constants:

- overlap: `3.5`
- ease: `2`
- panels: `1` for panel, `2` for pair

### 5. Fullness And Cut Width

Fullness is selected by material type and drape style. Observed selector values:

- Pinch Pleat: Drape `2`, Sheer `2.5`, Labor `37.5`
- Euro Pleat: Drape `2`, Sheer `2.5`, Labor `37.5`
- Inverted Box Pleat: Drape `3`, Sheer `3`, Labor `54.5`
- Goblet Pleat: Drape `3`, Sheer `3`, Labor `49.5`
- Grommet Top: Drape `2`, Sheer `2`, Labor `88.5`
- Ripplefold 100%: Drape `2.5`, Sheer `2.5`, Labor `48.25`
- Rod Pocket Top: Drape `3`, Sheer `3`, Labor `42`

Cut width formula:

```text
cut_width = (total_rod_size * fullness)
  + side_hems
  + (return_size * panels)
  + (overlap * panels)
  + ease
```

In `Updated Worksheet!C34` and `Updated Worksheet!C54`, side hems are added once because `C33`/`C53` already encode panel vs pair (`6` for panel, `12` for pair). Do not multiply side hems by panel count a second time.

Observed side hem rule:

- panel: `6`
- pair: `12`

Cut widths/panels:

```text
cut_widths = CEILING(cut_width / fabric_width)
```

### 6. Cut Length And Repeat Rounding

Inputs:

- finished length / height
- double header
- bottom hem doubled
- ease
- vertical repeat from fabric or sheer data

Formula translation:

```text
cut_length_repeat_count = CEILING((height + double_header + (bottom_hem * 2) + ease) / vertical_repeat)
cut_length = vertical_repeat * cut_length_repeat_count
```

If there is no repeat, the workbook guidance uses repeat value `1`.

### 7. Yardage And Overage

Paneled method:

```text
total_yardage = (cut_length * cut_widths) / 36
```

Railroad method:

```text
if cut_length < 118:
    total_yardage = cut_width / 36
else:
    total_yardage = (cut_length * cut_widths) / 36
```

The prose in column `D` phrases this as sheer plus cut length under `118`, but the actual formulas in `Updated Worksheet!C40` and `Updated Worksheet!C60` check cut length only. If the business wants the sheer/wide-goods condition enforced, treat that as a product-rule correction rather than a direct spreadsheet parity implementation.

Overage multiplier by finished length:

- `< 100`: `1.07`
- `100-119`: `1.085`
- `120-139`: `1.10`
- `140-159`: `1.12`
- `160+`: `1.14`

Required yards:

```text
total_required_yards = CEILING(total_yardage * overage_multiplier)
```

Some older calculator notes mention rounding to nearest quarter or third yard, but the Formula Translation area says round up to the nearest whole number. Treat whole-yard round-up as the implementation default unless a later business rule overrides it.

### 8. Lining And Interlining Yardage

Both calculators use a 54-inch material width:

```text
lining_widths = CEILING(cut_width / 54)
lining_cut_length = finished_length + lining_length_allowance
lining_yards = (lining_widths * lining_cut_length) / 36
```

Observed allowance notes:

- 4-inch bottom hem: `9` inches allowance
- 6-inch bottom hem: `11` inches allowance
- general note: bottom hem plus 1-inch top seam plus 2-inch allowance

Interlining follows the same width/cut-length/yards pattern.

### 9. Labor Pricing

Labor price per width is assembled from:

- base style labor charge
- lining add-on
- interlining add-on
- extra length
- bottom trim/banding
- large bottom hems
- side trim/banding specialty labor

Column `D` contains stale labor notes in a few places. In the actual `Updated Worksheet` formulas, style base labor uses `XLOOKUP` by style (`C71`, `C79`), lined/interlined add-ons are static values in `C72`/`C73`, and large bottom hem add-ons use `9 * labor_widths` (`C75`, `C83`).

Observed example:

```text
unlined 37.5 + lined 7 + interlined 19.5 + extra_length 0 + large_bottom_hem 0 = 64
```

Drape labor:

```text
labor_widths = cut_width / 50
pair_labor_widths = round up to an even whole number
panel_labor_widths = round up to a whole number
drape_labor_price = labor_widths_rounded * total_price_per_width
```

### 10. Fabric, Lining, And Interlining Price

Main fabric:

```text
fabric_price_per_yard = fabric_cost_per_yard * fabric_markup
fabric_price = fabric_price_per_yard * total_required_yards
```

Observed example:

```text
11 * 1.3 = 14.3
14.3 * 12 = 171.6
```

Lining:

```text
lining_price_per_yard = lining_cost_per_yard * lining_markup
lining_fabric_price = lining_price_per_yard * lining_yards
```

Interlining follows the same cost * markup * yards pattern.

### 11. Total/Subtotal Assembly

The calculator subtotal combines, per treatment:

- labor
- specialty labor items
- main fabric
- lining
- interlining
- bottom banding fabric
- side trim fabric
- side banding fabric
- bottom trim fabric
- rod/track where applicable
- sample/freight/additional product charges where applicable

Observed top calculator example:

```text
labor 512
main fabric 171.6
lining 90.00018
interlining 102.000204
subtotal 875.600384
```

This equals labor + main fabric + lining + interlining for the visible example.

## Extraction Notes

- Exact formulas and cached values are in `formulas.json`.
- Inputs that are lookup-driven should be mapped to WordPress data, not copied from spreadsheet lookup rows.
- Any formulas with external workbook references are preserved in JSON under `dependencies.external_refs`.
