# Code Vs New Spreadsheet Audit

Audit date: 2026-07-09  
Spreadsheet: `[20260210] MASTER_1A Computerized Form (DSM/EA Copy).xlsx`  
Drive file ID: `1WPt3mVA25UVfpUalrhStB5DUr-ytP-Am`  
Drive modified time: `2026-07-08T18:25:35.274Z`  
Code audited: `wordpress-child-theme-working/fabric-selection-v2.php`

## Verdict

The Drapery V2 code is aligned with the new spreadsheet for the audited pricing logic. I found no code-vs-spreadsheet formula mismatch in rod totals, return sizes, finished/cut widths, yardage, lining/interlining quantities, fabric pricing, labor pricing, or final double-rod total assembly.

The two important caveats are:

1. Local Excel recalculation returned `#NAME?` for `Updated Worksheet!D70` and `Updated Worksheet!D78` because those cells use `XLOOKUP`. The workbook's saved cached values are valid, so I treated this as a local Excel compatibility/recalculation caveat rather than a formula mismatch.
2. `Updated Worksheet!D103` is labeled `Total Price (For Single Rod)`, but while the workbook input `D4` is still set to double rod, `D103` is really the current farthest/drape-only subtotal with the current double-rod component values. The code also supports a true single-rod scenario when the single-rod input is selected.

## Confirmed Matches

| Area | Spreadsheet evidence | Code evidence | Result |
| --- | --- | --- | --- |
| Rod size and rod total | `Updated Worksheet!D21=84`, `D22=121.8`, `D23=42`, `D24=327.6`; formula `D24=IF(D4="Single Rod 4in Return",SUM(D22:D23),2*SUM(D22:D23))` | `fabric-selection-v2.php:3807-3809` calculates additional rod cost and doubles non-single rod totals | Match |
| Return size | `Updated Worksheet!D25=6` for farthest/drape; `D45=4` for closest/sheer | Primary call passes `returnSize: rodSetup` at `fabric-selection-v2.php:4344-4358`; closest call passes `returnSize: 4` at `fabric-selection-v2.php:4397-4399` | Match |
| Finished/cut width | `D28=105`, `D34=201`, `D35=4`; closest `D48=101`, `D54=239`, `D55=3` | Helper formulas at `fabric-selection-v2.php:3811-3814` | Match |
| Yardage | Drape `D39=135`, `D40=15`, `D42=17`; sheer `D59=114`, `D60=6.6388888889`, `D62=8` | Helper and tests use the same short-cut-length yardage branch and whole-yard roundup | Match |
| Lining/interlining | `D63:D68` gives lining yards `12` and interlining yards `0` for the current workbook selection | Helper returns lining/interlining quantities and prices into integration at `fabric-selection-v2.php:4383-4390` | Match |
| Labor | Cached `D70=37.5`, `D75=67`, `D77=402`; cached `D78=37.5`, `D83=37.5`, `D85=225` | Style labor lookup in helper plus combined primary/closest labor at `fabric-selection-v2.php:4380-4382` and `4423` | Match |
| Fabric pricing | `D89=861.9`, `D93=156`, `D97=142.8`, `D101=0` | Primary fabric assigned at `fabric-selection-v2.php:4378-4379`; closest fabric added at `4422` | Match |
| Double-rod total | `Updated Worksheet!D102` cached value `2115.3`; formula `D69+D77+D85+D89+D93+D97+D101` | Closest labor/fabric are added before final total; total assembled at `fabric-selection-v2.php:4426` | Match |
| Current D103 subtotal | `Updated Worksheet!D103` cached value `1734.3`; formula `D69+D77+D89+D97+D101` | Equivalent current-workbook subtotal excluding closest/sheer labor and fabric | Match |

## Comparison Results

The temporary comparator executed the formula helper directly from `fabric-selection-v2.php` and passed all 21 metrics.

| Scenario | Expected | Code result | Status |
| --- | ---: | ---: | --- |
| Top visible subtotal, `Worksheet!L4/M4` | `875.600384` | `875.600384` | Pass |
| Formula Translation rod total, `Updated Worksheet!D24` | `327.6` | `327.6` | Pass |
| Formula Translation drape labor, `D77` | `402` | `402` | Pass |
| Formula Translation sheer labor, `D85` | `225` | `225` | Pass |
| Formula Translation drape fabric, `D89` | `861.9` | `861.9` | Pass |
| Formula Translation sheer fabric, `D93` | `156` | `156` | Pass |
| Formula Translation lining, `D97` | `142.8` | `142.8` | Pass |
| Double-rod total, `D102` | `2115.3` | `2115.3` | Pass |
| Current-workbook D103 subtotal | `1734.3` | `1734.3` | Pass |

The comparator also calculated a true single-rod scenario using single-rod input behavior. That result is `1436.5`. This is lower than the current workbook's `D103=1734.3` because the workbook is still set to the double-rod input in `D4`.

## Recalculation Caveat

After saving a recalculated workbook through local Excel, these `Updated Worksheet` cells showed `#NAME?`:

| Cell | Label | Formula | Source cached value | Recalculated value |
| --- | --- | --- | ---: | --- |
| `D70` | Base Pricing (unlined) | `XLOOKUP("*"&D9&"*", $G$35:$G$42,$J$35:$J$42, "", 2)` | `37.5` | `#NAME?` |
| `D75` | Total Labor Price per Width | `D70+D71+D72+D73+D74` | `67` | `#NAME?` |
| `D77` | Drape Labor Price | `D75*D76` | `402` | `#NAME?` |
| `D78` | Base Pricing (unlined) | `XLOOKUP("*"&D9&"*", $G$35:$G$42,$J$35:$J$42, "", 2)` | `37.5` | `#NAME?` |
| `D83` | Total Labor Price per Width | `D78+D79+D80+D81+D82` | `37.5` | `#NAME?` |
| `D85` | Sheer Labor Price | `D83*D84` | `225` | `#NAME?` |
| `D102` | Total Price (For Double Rod) | `D69+D77+D85+D89+D93+D97+D101` | `2115.3` | `#NAME?` |
| `D103` | Total Price (For Single Rod) | `D69+D77+D89+D97+D101` | `1734.3` | `#NAME?` |

This does not indicate the V2 code is wrong. It indicates this local Excel runtime did not evaluate the workbook's `XLOOKUP` formulas. If the spreadsheet must be safely recalculated in older Excel runtimes, replace those `XLOOKUP` formulas with an older-compatible lookup pattern.

## Verification

- Downloaded the raw `.xlsx` from Drive and saved it as a scratch source workbook.
- Recalculated a scratch copy through local Excel.
- Extracted cached and recalculated values from `Worksheet` and `Updated Worksheet`.
- Ran the code comparator: all 21 metrics passed.
- Ran existing focused test: `drapery-formula-v2.test.js passed`.

## Recommendation

No formula code change is needed for Drapery V2 based on this workbook comparison.

Recommended cleanup, if desired later:

- Rename or annotate the `Updated Worksheet!D103` label so it is clear it is only a true single-rod total after the workbook input `D4` is switched to single rod.
- Consider replacing `XLOOKUP` in `D70` and `D78` if the workbook needs compatibility with older/local Excel runtimes.
- Keep `wordpress-child-theme-working/tests/drapery-formula-v2.test.js` as the parity guard for future formula edits.
