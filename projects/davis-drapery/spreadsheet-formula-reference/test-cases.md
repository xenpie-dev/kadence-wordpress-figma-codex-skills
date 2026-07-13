# Formula Test Cases

Generated: 2026-07-06T18:35:44.753719+00:00

These cases come from visible examples in the shared workbooks. They should be used as implementation parity checks, not as exhaustive business validation.

## Drapery Example A: Top Calculator Visible Case

Inputs:

| Field | Value |
| --- | ---: |
| Left extension | 12 |
| Window opening | 48 |
| Right extension | 6 |
| Total rod size | 66 |
| Return size | 4 |
| Overlap | 3.5 |
| Ease | 2 |
| Panels | 2 |
| Fullness | 2.5 |
| Side hems | 6 |
| Fabric width | 54 |
| Finished length | 72 |
| Double header | 8 |
| Double bottom hem | 4 |
| Vertical repeat | 32 |

Expected outputs:

| Output | Expected |
| --- | ---: |
| Rod size | 66 |
| Finished width | 83 |
| Cut width | 194 |
| Raw cut widths | 3.592592593 |
| Rounded cut widths | 4 |
| Cut length without repeats | 90 |
| Repeat count | 3 |
| Cut length | 96 |
| Paneled yardage | 10.66666667 |
| Overage multiplier | 1.07 |
| Required yards before final roundup | 11.41333333 |
| Required yards | 12 |
| Railroad yardage from cut inches | 5.388888889 |
| Railroad required yards before roundup | 5.766111111 |
| Railroad required yards | 6 |
| Lining widths | 4 |
| Lining cut length | 81 |
| Lining yards | 9 |
| Interlining widths | 4 |
| Interlining cut length | 81 |
| Interlining yards | 9 |
| Labor per width | 64 |
| Rounded labor widths | 4 |
| Labor price each treatment | 256 |
| Main fabric price | 171.6 |
| Lining fabric price | 90.00018 |
| Interlining fabric price | 102.000204 |
| Visible subtotal | 875.600384 |

Notes:

- The visible subtotal equals labor `512` plus main fabric `171.6`, lining `90.00018`, and interlining `102.000204`.
- Labor appears doubled in the top summary for this example, while the per-treatment labor section shows `256`.

## Drapery Example B: Formula Translation Case

Inputs:

| Field | Value |
| --- | ---: |
| Rod setup | Double Rod Set Farthest From Window 6in |
| Drape or sheer | Drape |
| Customer purchasing rod/track | Yes |
| Drape style | Pinch Pleat |
| Left extension | 12 |
| Window opening | 60 |
| Right extension | 12 |
| Height | 96 |
| Bottom hem | 4 |
| Panels | 2 |
| Return size | 6 |
| Overlap | 3.5 |
| Ease | 2 |
| Cost / yard | 39 |
| Sample price | 6 |
| Fabric width | 54 |
| Fullness | 2 |
| Side hems | 12 |
| Double header | 8 |
| Vertical repeat | 27 |

Expected outputs:

| Output | Expected |
| --- | ---: |
| Total rod size | 84 |
| Rod base pricing | 121.8 |
| Rod additional costs | 42 |
| Rod total | 327.6 |
| Finished width | 105 |
| Cut width | 201 |
| Cut widths paneled | 4 |
| Cut length repeat count | 5 |
| Cut length | 135 |
| Total yardage | 15 |
| Overage multiplier | 1.07 |
| Total required yards | 17 |

Notes:

- Rod total is larger than base plus additional cost, indicating treatment count or double-rod multiplication in the workbook. Preserve this behavior when translating to code.

## Pillow And Shade Notes

The shared workbooks include pillow and shade calculator areas, but this package is focused on Drapery Builder formulas. Keep pillow/shade examples as secondary references unless those features enter scope.
