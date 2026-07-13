# Formula Translation Mismatch Flags

Source workbook: `source/davis-drapery-dev-copy-v1.xlsx`

Source sheet: `Updated Worksheet`

This file flags rows where the `Formula Translation` text in column `D` appears stale, incomplete, reversed, or inconsistent with the actual formula/value in column `C`. For implementation, treat the formula/value cell in column `C` as stronger evidence than the prose in column `D` unless the business confirms otherwise.

Columns:

- `Type cell`: column `A`
- `Field cell`: column `B`
- `Formula/value cell`: column `C`
- `Translation cell`: column `D`

| Type cell | Field cell | Formula/value cell | Translation cell | Severity | Flag |
| --- | --- | --- | --- | --- | --- |
| `A22` | `B22` | `C22` | `D22` | High | `D22` says to check whether `C7` says "No Rod", but `C22` checks `C6="No"` before looking up `C7` in `Rod Selection`. |
| `A23` | `B23` | `C23` | `D23` | High | `D23` says to check whether `C7` says "No Rod", but `C23` checks `C6="No"` before calculating additional rod cost. |
| `A24` | `B24` | `C24` | `D24` | High | `D24` is blank. `C24` is important: `=IF(C4="Single Rod 4in Return",SUM(C22:C23),2*SUM(C22:C23))`, so non-single-rod cases double rod base plus additional cost. |
| `A29` | `B29` | `C29` | `D29` | Medium | `D29` describes `C5` as "No" vs "Yes", but `C29` checks `C5="Drape"` and otherwise uses sheer data. |
| `A30` | `B30` | `C30` | `D30` | Medium | `D30` describes a fabric/sheer sample price lookup, but `C30` is a static value `6`. |
| `A31` | `B31` | `C31` | `D31` | Medium | `D31` describes `C5` as "No" vs "Yes", but `C31` checks `C5="Drape"` and otherwise uses sheer data. |
| `A34` | `B34` | `C34` | `D34` | High | `D34` says `(Side Hems*Panels)`, but `C34` adds `C33` once: `=(C21*C32)+(C33)+(C25*C20)+(C26*C20)+C27`. `C33` already encodes panel vs pair as `6` or `12`. |
| `A37` | `B37` | `C37` | `D37` | Medium | `D37` describes `C5` as "No" vs "Yes", but `C37` checks `C5="Drape"` and otherwise uses sheer data. |
| `A40` | `B40` | `C40` | `D40` | High | `D40` says the railroad method depends on sheer selection plus cut length under `118`, but `C40` only checks `C39<118`: `=IF((C39<118),C34/36,(C39*C35)/36)`. |
| `A45` | `B45` | `C45` | `D45` | High | Second-treatment return logic is reversed in the translation. `C45` returns `4` when `C4` is "Double Rod Set Farthest From Window 6in", otherwise `6`; `D45` says the opposite. |
| `A49` | `B49` | `C49` | `D49` | Medium | `D49` repeats the stale `C5` "No" vs "Yes" wording, but `C49` checks `C44="Drape"` for the second treatment. |
| `A50` | `B50` | `C50` | `D50` | Medium | `D50` describes a fabric/sheer sample price lookup, but `C50` is a static value `6`. |
| `A51` | `B51` | `C51` | `D51` | Medium | `D51` repeats the stale `C5` "No" vs "Yes" wording, but `C51` checks `C44="Drape"` for the second treatment. |
| `A52` | `B52` | `C52` | `D52` | Medium | `D52` says selectors are `C5` and `C9`, but the array formula in `C52` uses `C44` and `C9`: `=IFERROR(INDEX(H36:I42,MATCH(C9,G36:G42,0),MATCH(C44,H35:I35,0)),"")`. |
| `A54` | `B54` | `C54` | `D54` | High | `D54` says `(Side Hems*Panels)`, but `C54` adds `C53` once: `=(C21*C52)+(C53)+(C45*C20)+(C46*C20)+C47`. `C53` already encodes panel vs pair. |
| `A57` | `B57` | `C57` | `D57` | Medium | `D57` repeats the stale `C5` "No" vs "Yes" wording, but `C57` checks `C44="Drape"` for the second treatment. |
| `A60` | `B60` | `C60` | `D60` | High | `D60` says the railroad method depends on sheer selection plus cut length under `118`, but `C60` only checks `C59<118`: `=IF((C59<118),C54/36,(C59*C55)/36)`. |
| `A64` | `B64` | `C64` | `D64` | Low | `C64` returns `"CUSTOM"` for bottom hem sizes outside `4,6,8,10,12`; `D64` does not mention that fallback. |
| `A66` | `B66` | `C66` | `D66` | High | `D66` says "If No Lining", but `C66` checks `C18="No Interlining"`. |
| `A67` | `B67` | `C67` | `D67` | High | `D67` says "If No Lining", but `C67` checks `C18="No Interlining"`. It also has a `"CUSTOM"` bottom-hem fallback not mentioned in `D67`. |
| `A70` | `B70` | `C70` | `D70` | Medium | `D70` says rod base plus additional costs. `C70` is `=C24`, and `C24` may double rod costs depending on `C4`. |
| `A71` | `B71` | `C71` | `D71` | Medium | `D71` says static labor pricing, but `C71` is an array formula using `XLOOKUP` by drape style `C9`: `=XLOOKUP("*"&C9&"*",$G$35:$G$42,$J$35:$J$42,"",2)`. |
| `A72` | `B72` | `C72` | `D72` | High | `D72` says add `10.00` if selected "yes", but `C72` is a static `10` with no condition against the lining choice `C16`. |
| `A73` | `B73` | `C73` | `D73` | High | `D73` says add `19.50` if selected "yes", but `C73` is a static `19.5` with no condition against interlining choice `C18`. |
| `A74` | `B74` | `C74` | `D74` | Low | `D74` refers to `C14`, but `C74` uses height cell `C15`. |
| `A75` | `B75` | `C75` | `D75` | High | `D75` says large bottom hems add `$5.00`, but `C75` is `=IF(C17>4,9*C77,0)`. |
| `A77` | `B77` | `C77` | `D77` | Low | `D77` says closest even number, but `C77` uses Excel `EVEN(C34/50)`, which rounds up/away from zero to the next even integer. |
| `A79` | `B79` | `C79` | `D79` | Medium | `D79` says static labor pricing, but `C79` is an array formula using `XLOOKUP` by drape style `C9`. |
| `A82` | `B82` | `C82` | `D82` | Low | `D82` refers to `C14`, but `C82` uses height cell `C15`. |
| `A83` | `B83` | `C83` | `D83` | High | `D83` says large bottom hems add `$5.00`, but `C83` is `=IF(C17>4,9*C85,0)`. |
| `A85` | `B85` | `C85` | `D85` | Low | `D85` says closest even number, but `C85` uses Excel `EVEN(C54/50)`, which rounds up/away from zero to the next even integer. |
| `A87` | `B87` | `C87` | `D87` | Medium | `D87` repeats the stale `C5` "No" vs "Yes" wording inherited from `D29`; `C87` simply references `C29`. |
| `A88` | `B88` | `C88` | `D88` | Medium | `D88` describes `C5` as "No" vs "Yes", but `C88` checks `C5="Drape"` and otherwise uses sheer data. |
| `A90` | `B90` | `C90` | `D90` | Low | `D90` says main fabric cost per yard times required yards, but `C90` uses price per yard `C89` times required yards `C42`. |
| `A92` | `B92` | `C92` | `D92` | Medium | `D92` is blank. The row is "Sheer Fabric Markup", but `C92` checks first-treatment selector `C5` rather than second-treatment selector `C44`. This may be intentional fallback behavior, but it should be reviewed. |
| `A95` | `B95` | `C95` | `D95` | High | `D95` says Fabric Data and "Markup", but `C95` looks up lining cost per yard from `Lining Data`: `=VLOOKUP(C16,'Lining Data'!B:C,2,FALSE)`. |
| `A96` | `B96` | `C96` | `D96` | High | `D96` says "My Cost per Yard", but `C96` looks up lining markup from `Lining Data`: `=VLOOKUP(C16,'Lining Data'!B:D,3,FALSE)`. |
| `A103` | `B103` | `C103` | `D103` | High | `D103` omits sheer labor and sheer fabric components. `C103` totals `C70+C78+C86+C90+C94+C98+C102`, so it includes both drape and sheer labor/fabric price cells. |

## Highest-Risk Implementation Flags

These are the flags most likely to affect live Drapery Builder pricing if copied incorrectly:

- `C24/D24`: rod total doubles non-single-rod cases.
- `C34/D34` and `C54/D54`: side hems are not multiplied by panel count in the formula because `C33`/`C53` already encode panel vs pair.
- `C40/D40` and `C60/D60`: railroad method formula checks only cut length under `118`, not material type.
- `C45/D45`: second-treatment return size translation is reversed.
- `C66/D66` and `C67/D67`: interlining no-charge logic checks `No Interlining`, not `No Lining`.
- `C72/D72` and `C73/D73`: lined/interlined labor add-ons are static in the sheet formulas, despite conditional wording in column `D`.
- `C75/D75` and `C83/D83`: large bottom hem add-on uses `9 * labor_widths`, not `$5`.
- `C95/D95` and `C96/D96`: lining cost and markup translations are swapped/stale.
- `C103/D103`: total price includes both drape and sheer components in the formula.
