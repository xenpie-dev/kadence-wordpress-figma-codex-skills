# Formula Dependencies

Generated: 2026-07-06T18:35:44.753719+00:00

This document maps spreadsheet formula dependencies to the WordPress data sources that should feed the Drapery Builder implementation.

## WordPress Data Mapping

| Formula Concept | Spreadsheet Lookup Intent | WordPress Source |
| --- | --- | --- |
| Main fabric cost | Fabric Data / My Cost per Yard | `fabric` post type, ACF `my_cost_per_yard` |
| Main fabric client price | Cost times markup or client price per yard | `fabric` post type, ACF `client_price_per_yard` or `my_cost_per_yard` + `mark_up` |
| Fabric width | Fabric Data / Fabric Width | `fabric` post type, ACF `fabric_width` |
| Vertical repeat | Fabric Data / Vertical Repeat | `fabric` post type, ACF `vertical_repeat` |
| Fabric sample price | Fabric Data / Sample Price | `fabric` post type, ACF `sample_price` |
| Sheer cost/width/repeat/sample | Sheer Data equivalents | Same `fabric` model, filtered by fabric/use taxonomy or material type |
| Rod base price | Rod Selection / Client Price for 4 | `rod-selection` post type, ACF `client_price_for_4_foot` |
| Rod additional-foot price | Rod Selection / Client Price per additional Foot | `rod-selection` post type, ACF `client_price_per_additional_foot` |
| Lining choice | Lining dropdown/options | Builder options or product/ACF constants; not spreadsheet rows |
| Lining cost and markup | Lining data | Builder pricing config or ACF option fields |
| Interlining choice | Interlining dropdown/options | Builder options or ACF constants |
| Interlining cost and markup | Interlining data | Builder pricing config or ACF option fields |
| Drape style fullness | Fullness selector chart | Code constants keyed by drape style + material type |
| Drape style labor charge | Fullness selector chart / Labor Chg | Code constants or ACF option table keyed by drape style |
| Room/window dropdowns | Dropdown source list | Frontend constants or WordPress option fields |

## Formula Inputs Required

### Required User Inputs

- room location
- window location/sidemark
- rod setup
- rod/track purchase yes/no
- rod selection when purchasing hardware
- drape or sheer
- drape style
- fabric/sheer selection
- left extension
- window opening
- right extension
- finished height/length
- lining option
- bottom hem
- interlining option
- panel or pair
- panel placement for single panels

### Required Derived Constants

- overlap: `3.5`
- width/cut ease: `2`
- default return closest/single: `4`
- return farthest double rod: `6`
- lining/interlining width: `54`
- labor width divisor: `50`
- rod included length: `48`
- rod additional-foot divisor: `12`
- lining allowance for 4-inch hem: `9`
- lining allowance for 6-inch hem: `11`

### Style Constants

| Style | Drape Fullness | Sheer Fullness | Labor Charge |
| --- | ---: | ---: | ---: |
| Pinch Pleat | 2 | 2.5 | 37.5 |
| Euro Pleat | 2 | 2.5 | 37.5 |
| Inverted Box Pleat | 3 | 3 | 54.5 |
| Goblet Pleat | 3 | 3 | 49.5 |
| Grommet Top | 2 | 2 | 88.5 |
| Ripplefold 100% | 2.5 | 2.5 | 48.25 |
| Rod Pocket Top | 3 | 3 | 42 |

## External References Found

The raw formula inventory preserves external workbook references when present. The extractor found the following unique external reference tokens:

- None found in extracted formulas.

## Implementation Guidance

- Keep formula logic independent from spreadsheet rows.
- Fetch live catalog values from WordPress post types/ACF at runtime.
- Keep style/fullness/labor constants centralized so both pricing and summary/debug output use the same source.
- Preserve spreadsheet rounding behavior explicitly in code: `CEILING` for cut widths, cut length repeat counts, required yards, rod additional feet, and labor widths.
- Treat missing external workbook references as documentation gaps, not production blockers, because production data should come from WordPress.
