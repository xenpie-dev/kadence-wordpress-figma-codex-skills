# Drapery Builder Settings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the admin-only Drapery Builder Settings page the runtime source for every fixed workbook-aligned business constant used by both Drapery Builder treatment calculations.

**Architecture:** Store the canonical workbook defaults in one JSON file. A recoverable WordPress sandbox module registers and validates the ACF fields, normalizes saved options over those defaults, restricts the existing page to `manage_options`, and injects the normalized configuration before a footer JavaScript adapter. The adapter replaces `window.DavisDraperyFormulaV2` after the legacy inline helper is declared but before `DOMContentLoaded`, so both the primary/farthest and closest treatment paths use the same settings without editing the live PHP page template.

**Tech Stack:** WordPress 7.0.2, PHP 8.3.31, ACF PRO 6.8.6, browser JavaScript, Node.js contract/unit tests, Novamira WordPress sandbox deployment.

## Global Constraints

- Keep the existing admin slug `/wp-admin/admin.php?page=drapery-builder-settings`.
- Require `manage_options` for both menu visibility and direct access.
- Use the 2026-08-04 linked workbook as the default-value specification.
- Keep catalog-owned fabric and rod attributes in their existing data sources.
- Keep 12 inches per foot, 36 inches per yard, rounding, ceiling, and even-width mechanics locked in code.
- Store field definitions, defaults, and normalization outside the large page template.
- Both primary/farthest and closest treatment calculations must consume one normalized configuration.
- Missing or invalid individual options fall back to workbook defaults.
- Ordered tier breakpoints must be strictly increasing.
- Preserve the old `base_pricing` option as a migration fallback; do not delete it.
- An unsupported hem or extra-length tier returns a custom-quote state, never a misleading numeric total.
- Use test-driven development: observe each new test fail before adding the production behavior.
- Do not modify or overwrite unrelated files in the currently dirty/untracked workspace.
- Deploy generated PHP only through `wp-content/novamira-sandbox/`; use the sandbox disable/enable recovery path.

## File map

- Create `wordpress-child-theme-working/davis-drapery-builder-settings.defaults.json`: single canonical workbook-default configuration consumed by PHP and tests.
- Create `wordpress-child-theme-working/davis-drapery-builder-settings.php`: recoverable sandbox module; ACF schema, option normalization, access control, validation, and frontend asset/config injection.
- Create `wordpress-child-theme-working/davis-drapery-builder-settings.js`: settings-driven replacement for `window.DavisDraperyFormulaV2`.
- Create `wordpress-child-theme-working/tests/drapery-builder-settings-defaults.test.js`: exact workbook-default contract.
- Create `wordpress-child-theme-working/tests/drapery-builder-settings-php.test.js`: PHP source contract for ACF, access, normalization, migration, and enqueue behavior.
- Create `wordpress-child-theme-working/tests/drapery-builder-settings-formula.test.js`: pure JavaScript formula and boundary tests.
- Modify `wordpress-child-theme-working/tests/drapery-formula-v2.test.js`: load the settings adapter after the legacy helper and reconcile the updated workbook example.
- Do not modify `wordpress-child-theme-working/fabric-selection-v2.php`; the live and local copies currently differ, and the adapter boundary avoids overwriting either version.

---

### Task 1: Canonical workbook defaults

**Files:**
- Create: `wordpress-child-theme-working/davis-drapery-builder-settings.defaults.json`
- Create: `wordpress-child-theme-working/tests/drapery-builder-settings-defaults.test.js`

**Interfaces:**
- Consumes: Values verified from `Updated Worksheet!D23:D84`, `Updated Worksheet!H36:J42`, `Lining Data!C3:F6`, and `Interlining Data!D3:G3`.
- Produces: A JSON object with `measurements`, `overageTiers`, `hemAllowances`, `labor`, and `materials` keys.

- [ ] **Step 1: Write the failing defaults test**

Create `tests/drapery-builder-settings-defaults.test.js` with this complete contract:

```js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const defaultsPath = path.join(__dirname, '..', 'davis-drapery-builder-settings.defaults.json');
assert.equal(fs.existsSync(defaultsPath), true, 'defaults JSON must exist');
const actual = JSON.parse(fs.readFileSync(defaultsPath, 'utf8'));

const expected = {
  measurements: {
    rodIncludedLength: 48,
    rodBillingIncrement: 12,
    farthestReturn: 6,
    closestReturn: 4,
    overlap: 3.5,
    cutEase: 2,
    singleSideHems: 6,
    pairSideHems: 12,
    doubleHeader: 8,
    railroadCutoff: 118,
    liningWidth: 54,
    laborWidthDivisor: 50
  },
  overageTiers: [
    { maxExclusive: 100, multiplier: 1.07 },
    { maxExclusive: 120, multiplier: 1.085 },
    { maxExclusive: 140, multiplier: 1.1 },
    { maxExclusive: 160, multiplier: 1.12 },
    { maxExclusive: null, multiplier: 1.14 }
  ],
  hemAllowances: { '4': 9, '6': 11, '8': 13, '10': 15, '12': 17 },
  labor: {
    linedAddon: 10,
    interlinedAddon: 19.5,
    largeHemThreshold: 4,
    largeHemAddon: 9,
    extraLengthTiers: [
      { maxExclusive: 110, addon: 0 },
      { maxExclusive: 119, addon: 22 },
      { maxExclusive: 191, addon: 32 },
      { maxExclusive: 231, addon: 55.5 },
      { maxExclusive: null, customQuote: true }
    ],
    styles: {
      pinchPleat: { drapeFullness: 2, sheerFullness: 2.5, baseLabor: 37.5 },
      euroPleat: { drapeFullness: 2, sheerFullness: 2.5, baseLabor: 37.5 },
      invertedBoxPleat: { drapeFullness: 3, sheerFullness: 3, baseLabor: 54.5 },
      gobletPleat: { drapeFullness: 3, sheerFullness: 3, baseLabor: 49.5 },
      grommetTop: { drapeFullness: 2, sheerFullness: 2, baseLabor: 88.5 },
      ripplefold100: { drapeFullness: 2.5, sheerFullness: 2.5, baseLabor: 48.25 },
      rodPocketTop: { drapeFullness: 3, sheerFullness: 3, baseLabor: 42 }
    }
  },
  materials: {
    samplePrice: 6,
    liningCostPerYard: 8,
    liningMarkup: 1.7,
    liningSamplePrice: 6,
    interliningCostPerYard: 9,
    interliningMarkup: 1.7,
    interliningSamplePrice: 8
  }
};

assert.deepEqual(actual, expected);
assert.equal('inchesPerFoot' in actual, false);
assert.equal('inchesPerYard' in actual, false);
console.log('Drapery Builder workbook defaults contract passed.');
```

- [ ] **Step 2: Run the test and verify the red state**

Run:

```powershell
node tests/drapery-builder-settings-defaults.test.js
```

Expected: FAIL because `davis-drapery-builder-settings.defaults.json` does not exist.

- [ ] **Step 3: Add the exact defaults JSON**

Create `davis-drapery-builder-settings.defaults.json` with the exact `expected` object above as valid JSON. Do not add comments or duplicate conversion constants.

- [ ] **Step 4: Run the defaults test and JSON parser**

Run:

```powershell
node tests/drapery-builder-settings-defaults.test.js
node -e "JSON.parse(require('fs').readFileSync('davis-drapery-builder-settings.defaults.json','utf8')); console.log('valid JSON')"
```

Expected: both commands PASS.

- [ ] **Step 5: Commit the defaults contract**

```powershell
git add wordpress-child-theme-working/davis-drapery-builder-settings.defaults.json wordpress-child-theme-working/tests/drapery-builder-settings-defaults.test.js
git commit -m "test: define drapery builder workbook defaults"
```

### Task 2: Runtime settings loader and frontend configuration

**Files:**
- Create: `wordpress-child-theme-working/davis-drapery-builder-settings.php`
- Create: `wordpress-child-theme-working/tests/drapery-builder-settings-php.test.js`

**Interfaces:**
- Consumes: `davis-drapery-builder-settings.defaults.json` from Task 1 and ACF option values stored under `option`.
- Produces:
  - `davis_drapery_builder_defaults(): array`
  - `davis_drapery_builder_field_schema(): array<string,array>`
  - `davis_drapery_builder_settings(): array`
  - Frontend global `window.DavisDraperyBuilderSettings`
  - Script handle `davis-drapery-builder-settings`

- [ ] **Step 1: Write the failing PHP module contract**

Create `tests/drapery-builder-settings-php.test.js`:

```js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const modulePath = path.join(__dirname, '..', 'davis-drapery-builder-settings.php');
assert.equal(fs.existsSync(modulePath), true, 'settings PHP module must exist');
const php = fs.readFileSync(modulePath, 'utf8');

for (const functionName of [
  'davis_drapery_builder_defaults',
  'davis_drapery_builder_field_schema',
  'davis_drapery_builder_settings',
  'davis_drapery_builder_enqueue_settings'
]) {
  assert.match(php, new RegExp(`function\\s+${functionName}\\s*\\(`));
}

assert.match(php, /davis-drapery-builder-settings\.defaults\.json/);
assert.match(php, /get_field\(\s*\$option_name,\s*'option',\s*false\s*\)/);
assert.match(php, /get_field\(\s*'base_pricing',\s*'option',\s*false\s*\)/);
assert.match(php, /is_page_template\(\s*'fabric-selection-v2\.php'\s*\)/);
assert.match(php, /wp_enqueue_script\(\s*'davis-drapery-builder-settings'/);
assert.match(php, /wp_add_inline_script\(\s*'davis-drapery-builder-settings'/);
assert.match(php, /window\.DavisDraperyBuilderSettings/);
assert.match(php, /wp_json_encode\(\s*davis_drapery_builder_settings\(\)/);

for (const optionName of [
  'dd_overlap',
  'dd_cut_ease',
  'dd_overage_breakpoint_1',
  'dd_hem_12_allowance',
  'dd_extra_length_addon_4',
  'dd_style_ripplefold_100_labor',
  'dd_interlining_cost_per_yard'
]) {
  assert.ok(php.includes(`'${optionName}'`), `missing ${optionName}`);
}

console.log('Drapery Builder PHP runtime contract passed.');
```

- [ ] **Step 2: Run the contract and verify the red state**

Run:

```powershell
node tests/drapery-builder-settings-php.test.js
```

Expected: FAIL because the PHP module does not exist.

- [ ] **Step 3: Implement the defaults loader and schema metadata**

Start `davis-drapery-builder-settings.php` with a standard plugin header, `defined( 'ABSPATH' ) || exit;`, and these exact function boundaries:

```php
function davis_drapery_builder_defaults() {
    static $defaults = null;
    if ( null !== $defaults ) {
        return $defaults;
    }

    $path = __DIR__ . '/davis-drapery-builder-settings.defaults.json';
    $json = is_readable( $path ) ? file_get_contents( $path ) : '';
    $data = json_decode( $json, true );
    $defaults = is_array( $data ) ? $data : array();
    return $defaults;
}
```

Implement `davis_drapery_builder_field_schema()` as the one flat field registry. Every element must contain `path`, `label`, `section`, `min`, and `step`. Use these exact option-name/path groups:

```php
$paths = array(
    'dd_rod_included_length'             => array( 'measurements', 'rodIncludedLength' ),
    'dd_rod_billing_increment'           => array( 'measurements', 'rodBillingIncrement' ),
    'dd_farthest_return'                 => array( 'measurements', 'farthestReturn' ),
    'dd_closest_return'                  => array( 'measurements', 'closestReturn' ),
    'dd_overlap'                         => array( 'measurements', 'overlap' ),
    'dd_cut_ease'                        => array( 'measurements', 'cutEase' ),
    'dd_single_side_hems'                => array( 'measurements', 'singleSideHems' ),
    'dd_pair_side_hems'                  => array( 'measurements', 'pairSideHems' ),
    'dd_double_header'                   => array( 'measurements', 'doubleHeader' ),
    'dd_railroad_cutoff'                 => array( 'measurements', 'railroadCutoff' ),
    'dd_lining_width'                    => array( 'measurements', 'liningWidth' ),
    'dd_labor_width_divisor'             => array( 'measurements', 'laborWidthDivisor' ),
    'dd_overage_breakpoint_1'            => array( 'overageTiers', 0, 'maxExclusive' ),
    'dd_overage_multiplier_1'            => array( 'overageTiers', 0, 'multiplier' ),
    'dd_overage_breakpoint_2'            => array( 'overageTiers', 1, 'maxExclusive' ),
    'dd_overage_multiplier_2'            => array( 'overageTiers', 1, 'multiplier' ),
    'dd_overage_breakpoint_3'            => array( 'overageTiers', 2, 'maxExclusive' ),
    'dd_overage_multiplier_3'            => array( 'overageTiers', 2, 'multiplier' ),
    'dd_overage_breakpoint_4'            => array( 'overageTiers', 3, 'maxExclusive' ),
    'dd_overage_multiplier_4'            => array( 'overageTiers', 3, 'multiplier' ),
    'dd_overage_multiplier_5'            => array( 'overageTiers', 4, 'multiplier' ),
    'dd_hem_4_allowance'                 => array( 'hemAllowances', '4' ),
    'dd_hem_6_allowance'                 => array( 'hemAllowances', '6' ),
    'dd_hem_8_allowance'                 => array( 'hemAllowances', '8' ),
    'dd_hem_10_allowance'                => array( 'hemAllowances', '10' ),
    'dd_hem_12_allowance'                => array( 'hemAllowances', '12' ),
    'dd_lined_labor_addon'               => array( 'labor', 'linedAddon' ),
    'dd_interlined_labor_addon'          => array( 'labor', 'interlinedAddon' ),
    'dd_large_hem_threshold'             => array( 'labor', 'largeHemThreshold' ),
    'dd_large_hem_addon'                 => array( 'labor', 'largeHemAddon' ),
    'dd_extra_length_breakpoint_1'       => array( 'labor', 'extraLengthTiers', 0, 'maxExclusive' ),
    'dd_extra_length_addon_1'            => array( 'labor', 'extraLengthTiers', 0, 'addon' ),
    'dd_extra_length_breakpoint_2'       => array( 'labor', 'extraLengthTiers', 1, 'maxExclusive' ),
    'dd_extra_length_addon_2'            => array( 'labor', 'extraLengthTiers', 1, 'addon' ),
    'dd_extra_length_breakpoint_3'       => array( 'labor', 'extraLengthTiers', 2, 'maxExclusive' ),
    'dd_extra_length_addon_3'            => array( 'labor', 'extraLengthTiers', 2, 'addon' ),
    'dd_extra_length_breakpoint_4'       => array( 'labor', 'extraLengthTiers', 3, 'maxExclusive' ),
    'dd_extra_length_addon_4'            => array( 'labor', 'extraLengthTiers', 3, 'addon' ),
    'dd_style_pinch_pleat_drape_fullness'=> array( 'labor', 'styles', 'pinchPleat', 'drapeFullness' ),
    'dd_style_pinch_pleat_sheer_fullness'=> array( 'labor', 'styles', 'pinchPleat', 'sheerFullness' ),
    'dd_style_pinch_pleat_labor'         => array( 'labor', 'styles', 'pinchPleat', 'baseLabor' ),
    'dd_style_euro_pleat_drape_fullness' => array( 'labor', 'styles', 'euroPleat', 'drapeFullness' ),
    'dd_style_euro_pleat_sheer_fullness' => array( 'labor', 'styles', 'euroPleat', 'sheerFullness' ),
    'dd_style_euro_pleat_labor'          => array( 'labor', 'styles', 'euroPleat', 'baseLabor' ),
    'dd_style_inverted_box_drape_fullness'=>array( 'labor', 'styles', 'invertedBoxPleat', 'drapeFullness' ),
    'dd_style_inverted_box_sheer_fullness'=>array( 'labor', 'styles', 'invertedBoxPleat', 'sheerFullness' ),
    'dd_style_inverted_box_labor'        => array( 'labor', 'styles', 'invertedBoxPleat', 'baseLabor' ),
    'dd_style_goblet_drape_fullness'     => array( 'labor', 'styles', 'gobletPleat', 'drapeFullness' ),
    'dd_style_goblet_sheer_fullness'     => array( 'labor', 'styles', 'gobletPleat', 'sheerFullness' ),
    'dd_style_goblet_labor'              => array( 'labor', 'styles', 'gobletPleat', 'baseLabor' ),
    'dd_style_grommet_drape_fullness'    => array( 'labor', 'styles', 'grommetTop', 'drapeFullness' ),
    'dd_style_grommet_sheer_fullness'    => array( 'labor', 'styles', 'grommetTop', 'sheerFullness' ),
    'dd_style_grommet_labor'             => array( 'labor', 'styles', 'grommetTop', 'baseLabor' ),
    'dd_style_ripplefold_100_drape_fullness'=>array( 'labor', 'styles', 'ripplefold100', 'drapeFullness' ),
    'dd_style_ripplefold_100_sheer_fullness'=>array( 'labor', 'styles', 'ripplefold100', 'sheerFullness' ),
    'dd_style_ripplefold_100_labor'      => array( 'labor', 'styles', 'ripplefold100', 'baseLabor' ),
    'dd_style_rod_pocket_drape_fullness' => array( 'labor', 'styles', 'rodPocketTop', 'drapeFullness' ),
    'dd_style_rod_pocket_sheer_fullness' => array( 'labor', 'styles', 'rodPocketTop', 'sheerFullness' ),
    'dd_style_rod_pocket_labor'          => array( 'labor', 'styles', 'rodPocketTop', 'baseLabor' ),
    'dd_sample_price'                    => array( 'materials', 'samplePrice' ),
    'dd_lining_cost_per_yard'            => array( 'materials', 'liningCostPerYard' ),
    'dd_lining_markup'                   => array( 'materials', 'liningMarkup' ),
    'dd_lining_sample_price'             => array( 'materials', 'liningSamplePrice' ),
    'dd_interlining_cost_per_yard'       => array( 'materials', 'interliningCostPerYard' ),
    'dd_interlining_markup'              => array( 'materials', 'interliningMarkup' ),
    'dd_interlining_sample_price'        => array( 'materials', 'interliningSamplePrice' ),
);
```

Assign schema metadata using these exact rules:

- `construction`: the first 12 measurement options, labeled in order `Rod Included Length`, `Rod Billing Increment`, `Farthest Return`, `Closest / Single Return`, `Overlap`, `Cut Ease`, `Single-Panel Side Hems`, `Pair Side Hems`, `Double Header`, `Railroad Cutoff`, `Lining / Interlining Width`, and `Labor-Width Divisor`; cite `Updated Worksheet!D23`, `D25:D27`, `D33`, `D36`, `D40`, `D53`, `D56`, `D60`, `D63`, `D66`, `D76`, or `D84` as applicable.
- `overage`: all nine overage options; label breakpoints `Overage Breakpoint 1` through `4` and multipliers `Overage Multiplier 1` through `5`; cite `Updated Worksheet!D41,D61`.
- `lining`: all five hem allowances; label them `4-inch Hem Added Cut Length` through `12-inch Hem Added Cut Length`; cite `Updated Worksheet!D64,D67`.
- `labor`: lined/interlined/large-hem fields plus eight extra-length fields; use labels `Lined Labor Add-on`, `Interlined Labor Add-on`, `Large-Hem Threshold`, `Large-Hem Add-on`, `Extra-Length Breakpoint 1` through `4`, and `Extra-Length Add-on 1` through `4`; cite `Updated Worksheet!D71:D74,D81:D82`.
- `styles`: all 21 style fields; for each of Pinch Pleat, Euro Pleat, Inverted Box Pleat, Goblet Pleat, Grommet Top, Ripplefold 100%, and Rod Pocket Top, create `<Style> Drape Fullness`, `<Style> Sheer Fullness`, and `<Style> Base Labor`; cite `Updated Worksheet!H36:J42`.
- `materials`: all seven material fields; label them `Generic Sample Price`, `Lining Cost per Yard`, `Lining Markup`, `Lining Sample Price`, `Interlining Cost per Yard`, `Interlining Markup`, and `Interlining Sample Price`; cite `Updated Worksheet!D30,D50`, `Lining Data!C3:F6`, or `Interlining Data!D3:G3`.

Use `min => 0.001` for divisors, widths, increments, multipliers, and fullness; use `min => 0` for prices, returns, allowances, and add-ons. Use `step => 0.001` for multipliers/fullness and `step => 0.01` for currency; other lengths use `step => 0.1`.

- [ ] **Step 4: Implement safe nested lookup and assignment**

Add these interfaces and use them only with trusted schema paths:

```php
function davis_drapery_builder_get_path( array $data, array $path ) {
    $cursor = $data;
    foreach ( $path as $key ) {
        if ( ! is_array( $cursor ) || ! array_key_exists( $key, $cursor ) ) {
            return null;
        }
        $cursor = $cursor[ $key ];
    }
    return $cursor;
}

function davis_drapery_builder_set_path( array &$data, array $path, $value ) {
    $cursor =& $data;
    foreach ( $path as $index => $key ) {
        if ( $index === count( $path ) - 1 ) {
            $cursor[ $key ] = $value;
            return;
        }
        if ( ! isset( $cursor[ $key ] ) || ! is_array( $cursor[ $key ] ) ) {
            $cursor[ $key ] = array();
        }
        $cursor =& $cursor[ $key ];
    }
}

function davis_drapery_builder_valid_number( $value, $min, $strictly_positive = false ) {
    if ( ! is_numeric( $value ) ) {
        return false;
    }
    $number = (float) $value;
    if ( ! is_finite( $number ) ) {
        return false;
    }
    return $strictly_positive ? $number > $min : $number >= $min;
}
```

`davis_drapery_builder_settings()` must:

1. Start with `davis_drapery_builder_defaults()`.
2. Read each schema option with `get_field( $option_name, 'option', false )` only when ACF is available.
3. Normalize numeric strings to floats.
4. Reject non-numeric, non-finite, below-minimum, zero-when-positive, or missing values individually.
5. Use `base_pricing` for unsaved Pinch Pleat and Euro Pleat labor only when it is numeric and non-negative.
6. After overlays, reset the whole overage or extra-length breakpoint array to its default if its breakpoints are not strictly increasing.
7. Return the complete nested object.

- [ ] **Step 5: Enqueue the normalized settings before the adapter**

Implement:

```php
function davis_drapery_builder_enqueue_settings() {
    if ( ! is_page_template( 'fabric-selection-v2.php' ) ) {
        return;
    }

    $script_path = __DIR__ . '/davis-drapery-builder-settings.js';
    $script_url  = content_url( '/novamira-sandbox/davis-drapery-builder-settings.js' );
    wp_enqueue_script(
        'davis-drapery-builder-settings',
        $script_url,
        array(),
        is_readable( $script_path ) ? (string) filemtime( $script_path ) : null,
        true
    );
    wp_add_inline_script(
        'davis-drapery-builder-settings',
        'window.DavisDraperyBuilderSettings = ' . wp_json_encode( davis_drapery_builder_settings() ) . ';',
        'before'
    );
}
add_action( 'wp_enqueue_scripts', 'davis_drapery_builder_enqueue_settings', 100 );
```

Priority 100 and footer loading are required: the legacy inline helper must be declared first, then the adapter replaces it before `DOMContentLoaded` calculations run.

- [ ] **Step 6: Run the runtime contract**

Run:

```powershell
node tests/drapery-builder-settings-php.test.js
```

Expected: PASS.

- [ ] **Step 7: Commit the runtime loader**

```powershell
git add wordpress-child-theme-working/davis-drapery-builder-settings.php wordpress-child-theme-working/tests/drapery-builder-settings-php.test.js
git commit -m "feat: load normalized drapery builder settings"
```

### Task 3: ACF fields, validation, and administrator-only access

**Files:**
- Modify: `wordpress-child-theme-working/davis-drapery-builder-settings.php`
- Modify: `wordpress-child-theme-working/tests/drapery-builder-settings-php.test.js`

**Interfaces:**
- Consumes: `davis_drapery_builder_field_schema()` and `davis_drapery_builder_settings()` from Task 2.
- Produces:
  - Local field group `group_ddbs_workbook_constants`
  - Stable field keys `field_ddbs_<option-name-without-dd_>`
  - `davis_drapery_builder_register_fields(): void`
  - `davis_drapery_builder_validate_save(): void`
  - `davis_drapery_builder_guard_settings_page(): void`

- [ ] **Step 1: Extend the contract with failing access and ACF assertions**

Append:

```js
for (const required of [
  "acf_add_local_field_group",
  "group_ddbs_workbook_constants",
  "'options_page'",
  "'drapery-builder-settings'",
  "'manage_options'",
  "acf_add_validation_error",
  "current_user_can( 'manage_options' )",
  "remove_menu_page( 'drapery-builder-settings' )",
  "field_68ecf0bb3c179"
]) {
  assert.ok(php.includes(required), `missing ACF/access contract: ${required}`);
}
assert.match(php, /add_action\(\s*'acf\/init',\s*'davis_drapery_builder_register_fields'/);
assert.match(php, /add_action\(\s*'acf\/validate_save_post',\s*'davis_drapery_builder_validate_save'/);
assert.match(php, /add_action\(\s*'admin_init',\s*'davis_drapery_builder_guard_settings_page'/);
assert.match(php, /add_action\(\s*'admin_menu',[^;]+999/);
```

- [ ] **Step 2: Run the test and verify it fails on the missing hooks**

Run `node tests/drapery-builder-settings-php.test.js`.

Expected: FAIL on the first missing ACF/access assertion.

- [ ] **Step 3: Register the local ACF field group**

At `acf/init`, map schema sections into tabs in this order:

```php
$sections = array(
    'construction' => 'Construction',
    'overage'      => 'Overage',
    'lining'       => 'Lining and Interlining',
    'labor'        => 'Labor Tiers',
    'styles'       => 'Style Fullness and Labor',
    'materials'    => 'Material Pricing',
);
```

For each section, add an ACF `tab` field, followed by the section's `number` fields. Derive a stable key with `field_ddbs_` plus the option name after `dd_`. Set `name`, `label`, `default_value`, `min`, `step`, `required => 1`, `wrapper.width => 33`, and instructions containing the unit and workbook cell/range named in the design spec.

Register:

```php
acf_add_local_field_group( array(
    'key'      => 'group_ddbs_workbook_constants',
    'title'    => 'Construction & Pricing Constants',
    'fields'   => $fields,
    'location' => array(
        array(
            array(
                'param'    => 'options_page',
                'operator' => '==',
                'value'    => 'drapery-builder-settings',
            ),
        ),
    ),
    'active'   => true,
) );
```

- [ ] **Step 4: Validate ordered tiers on save**

Implement `davis_drapery_builder_validate_save()` to run only when `$_GET['page'] === 'drapery-builder-settings'`. Read submitted values from `$_POST['acf']` using the stable field keys, normalize with `wp_unslash`, and validate:

```php
$overage = array( 100, 120, 140, 160 ); // replaced by submitted values
$lengths = array( 110, 119, 191, 231 ); // replaced by submitted values
```

If any adjacent value is not strictly larger, call `acf_add_validation_error()` on the first invalid field with exactly:

- `Overage breakpoints must be strictly increasing.`
- `Extra-length breakpoints must be strictly increasing.`

ACF field `min`, `required`, and numeric validation cover the individual values; runtime normalization remains the second safety layer.

- [ ] **Step 5: Enforce administrator-only access in code**

Implement both controls:

```php
function davis_drapery_builder_guard_settings_page() {
    $page = isset( $_GET['page'] ) ? sanitize_key( wp_unslash( $_GET['page'] ) ) : '';
    if ( 'drapery-builder-settings' === $page && ! current_user_can( 'manage_options' ) ) {
        wp_die(
            esc_html__( 'You are not allowed to manage Drapery Builder settings.', 'davis-drapery' ),
            esc_html__( 'Access denied', 'davis-drapery' ),
            array( 'response' => 403 )
        );
    }
}

function davis_drapery_builder_hide_settings_menu() {
    if ( ! current_user_can( 'manage_options' ) ) {
        remove_menu_page( 'drapery-builder-settings' );
    }
}
```

Hook `admin_init` and `admin_menu` at priority 999. During live deployment, also update the ACF UI options-page record capability to `manage_options`; the code guard remains defense in depth.

- [ ] **Step 6: Hide the legacy Base Pricing control without deleting its option**

Add `acf/prepare_field/key=field_68ecf0bb3c179` and return `false` only while the current admin page is `drapery-builder-settings`. Do not call `delete_field()`, `delete_option()`, or mutate `base_pricing`.

- [ ] **Step 7: Run the PHP source contract**

Run `node tests/drapery-builder-settings-php.test.js`.

Expected: PASS.

- [ ] **Step 8: Commit the ACF admin UI**

```powershell
git add wordpress-child-theme-working/davis-drapery-builder-settings.php wordpress-child-theme-working/tests/drapery-builder-settings-php.test.js
git commit -m "feat: add admin-only drapery pricing fields"
```

### Task 4: Settings-driven formula adapter

**Files:**
- Create: `wordpress-child-theme-working/davis-drapery-builder-settings.js`
- Create: `wordpress-child-theme-working/tests/drapery-builder-settings-formula.test.js`

**Interfaces:**
- Consumes: `window.DavisDraperyBuilderSettings` with the exact Task 1 JSON shape.
- Produces: `window.DavisDraperyFormulaV2` with methods `toNumber`, `roundEvenUp`, `overageMultiplier`, `bottomHemAllowance`, `extraLengthLabor`, `getStyleRule`, and `calculateTreatment`.
- `calculateTreatment(input)` returns the existing result keys plus `requiresCustomQuote` and `customQuoteReason`.

- [ ] **Step 1: Write failing boundary and override tests**

Create a VM test that loads the defaults JSON, assigns it to `sandbox.window.DavisDraperyBuilderSettings`, evaluates `davis-drapery-builder-settings.js`, and asserts:

```js
assert.equal(formula.overageMultiplier(99), 1.07);
assert.equal(formula.overageMultiplier(100), 1.085);
assert.equal(formula.overageMultiplier(119), 1.085);
assert.equal(formula.overageMultiplier(120), 1.1);
assert.equal(formula.overageMultiplier(139), 1.1);
assert.equal(formula.overageMultiplier(140), 1.12);
assert.equal(formula.overageMultiplier(159), 1.12);
assert.equal(formula.overageMultiplier(160), 1.14);

assert.equal(formula.extraLengthLabor(109).addon, 0);
assert.equal(formula.extraLengthLabor(110).addon, 22);
assert.equal(formula.extraLengthLabor(118).addon, 22);
assert.equal(formula.extraLengthLabor(119).addon, 32);
assert.equal(formula.extraLengthLabor(190).addon, 32);
assert.equal(formula.extraLengthLabor(191).addon, 55.5);
assert.equal(formula.extraLengthLabor(230).addon, 55.5);
assert.equal(formula.extraLengthLabor(231).customQuote, true);

assert.equal(formula.bottomHemAllowance(4).allowance, 9);
assert.equal(formula.bottomHemAllowance(12).allowance, 17);
assert.equal(formula.bottomHemAllowance(5).customQuote, true);

assert.deepEqual(
  JSON.parse(JSON.stringify(formula.getStyleRule('Ripple Fold', 'sheer'))),
  { fullness: 2.5, drapeFullness: 2.5, sheerFullness: 2.5, labor: 48.25 }
);

const elements = {
  drapery_height: { value: '231' },
  bottom_hem_size: { value: '4' },
  total_price: { textContent: '$1,234.00' },
  total_price_field: { value: '1234' }
};
sandbox.window.document = {
  getElementById: (id) => elements[id] || null
};
assert.equal(formula.applyCustomQuoteUi(), true);
assert.equal(elements.total_price.textContent, 'Custom quote required');
assert.equal(elements.total_price_field.value, '');
```

Add a cloned configuration changing `overlap` to 10, `cutEase` to 4, `largeHemAddon` to 20, and Pinch Pleat labor to 60. Evaluate the adapter again and assert `finishedWidth`, `cutWidth`, and labor change without passing those values through `input`.

- [ ] **Step 2: Run the formula test and verify the red state**

Run `node tests/drapery-builder-settings-formula.test.js`.

Expected: FAIL because the adapter file does not exist.

- [ ] **Step 3: Implement configuration access and tier functions**

Wrap the file in an IIFE receiving `window`. Capture `window.DavisDraperyBuilderSettings` once and implement:

```js
function toNumber(value, fallback = 0) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function firstTier(value, tiers, valueKey) {
  for (const tier of tiers) {
    if (tier.maxExclusive === null || value < tier.maxExclusive) return tier[valueKey];
  }
  return undefined;
}
```

`overageMultiplier()` reads `settings.overageTiers`. `bottomHemAllowance()` returns `{ allowance, customQuote }`. `extraLengthLabor()` returns `{ addon, customQuote }`. Unknown hems and the final 231+ tier set `customQuote: true`.

- [ ] **Step 4: Implement exact style aliases**

Map input labels in this order:

```js
[
  [/euro/, 'euroPleat'],
  [/pinch/, 'pinchPleat'],
  [/inverted|box/, 'invertedBoxPleat'],
  [/goblet/, 'gobletPleat'],
  [/grommet/, 'grommetTop'],
  [/ripple/, 'ripplefold100'],
  [/rod pocket/, 'rodPocketTop']
]
```

Fall back to `pinchPleat`. Return the same `getStyleRule()` object shape used by the page template.

- [ ] **Step 5: Implement the configured calculation**

Port the current `calculateTreatment()` result shape, replacing every business literal with settings:

- Rod base coverage and increment from `measurements.rodIncludedLength` and `rodBillingIncrement`.
- Map legacy input return `6` to `farthestReturn`; all other valid builder return inputs map to `closestReturn`.
- Overlap, width ease, length ease, side hems, double header, railroad cutoff, lining width, and labor width divisor from `measurements`.
- Overage, hem allowances, extra-length, style base labor, and large-hem rules from the matching settings groups.
- Lining/interlining costs and markups from `materials`, not from the old input amounts.
- Preserve catalog inputs: fabric width, repeat, fabric cost/markup, rod base price, and rod additional-foot price.
- Preserve the workbook's current primary-treatment labor behavior: if the input object contains `liningOption`, add configured `linedAddon` and `interlinedAddon`; the closest treatment has neither input and receives neither add-on.
- Implement large hem as `largeHemAddon` in `totalLaborPerWidth`, then multiply the final per-width total by `laborWidths` exactly once.
- Use `Math.max(0, Math.ceil((rodSize - includedLength) / increment))` so rods below the included length cannot create a negative surcharge.
- When a custom-quote state occurs, return `requiresCustomQuote: true`, a stable reason (`unsupported_hem` or `extra_length`), and `null` for affected numeric price totals.

Also export `applyCustomQuoteUi()` on the formula object. It must inspect `#drapery_height` and `#bottom_hem_size`; when the height is in the final custom tier or the hem is absent from `settings.hemAllowances`, set `#total_price` to `Custom quote required`, clear `#total_price_field`, and return `true`. Otherwise return `false` without changing the displayed total. Register it on `DOMContentLoaded` and schedule it with `setTimeout(applyCustomQuoteUi, 0)` after `input` and `change` events so it runs after the legacy price renderer. This prevents `Number(null)` in the template from leaving a visible `$0.00` custom quote.

- [ ] **Step 6: Run syntax and formula tests**

```powershell
node --check davis-drapery-builder-settings.js
node tests/drapery-builder-settings-formula.test.js
```

Expected: PASS.

- [ ] **Step 7: Commit the adapter**

```powershell
git add wordpress-child-theme-working/davis-drapery-builder-settings.js wordpress-child-theme-working/tests/drapery-builder-settings-formula.test.js
git commit -m "feat: calculate drapery prices from builder settings"
```

### Task 5: End-to-end workbook reconciliation and legacy override

**Files:**
- Modify: `wordpress-child-theme-working/tests/drapery-formula-v2.test.js`
- Modify: `wordpress-child-theme-working/tests/drapery-builder-settings-formula.test.js`

**Interfaces:**
- Consumes: The legacy helper markers in `fabric-selection-v2.php`, the Task 1 defaults, and the Task 4 adapter.
- Produces: Proof that footer evaluation replaces the legacy helper and that the updated workbook's D105 total is reproduced.

- [ ] **Step 1: Add the failing updated-workbook scenario**

In a fresh VM sandbox:

1. Evaluate the helper block extracted from `fabric-selection-v2.php`.
2. Save `const legacyFormula = sandbox.window.DavisDraperyFormulaV2`.
3. Assign the defaults to `sandbox.window.DavisDraperyBuilderSettings`.
4. Evaluate `davis-drapery-builder-settings.js`.
5. Assert the formula object changed: `assert.notEqual(formula, legacyFormula)`.

Calculate the primary treatment with:

```js
const primary = formula.calculateTreatment({
  rodSize: 84,
  returnSize: 6,
  panels: 2,
  fullness: formula.getStyleRule('Pinch Pleat', 'drape').fullness,
  fabricWidth: 54,
  finishedLength: 112,
  bottomHem: 4,
  verticalRepeat: 27,
  costPerYard: 39,
  markup: 1.3,
  rodBasePrice: 365.316,
  rodAdditionalFootPrice: 39.2,
  purchaseRod: true,
  isSingleRod: false,
  liningOption: 'no_lining',
  interliningOption: 'no_interlining',
  yardageMethod: 'railroad-if-short'
});
```

Calculate the closest treatment with:

```js
const closest = formula.calculateTreatment({
  rodSize: 84,
  returnSize: 4,
  panels: 2,
  fullness: formula.getStyleRule('Pinch Pleat', 'sheer').fullness,
  fabricWidth: 118,
  finishedLength: 112,
  bottomHem: 4,
  verticalRepeat: 1,
  costPerYard: 15,
  markup: 1.3,
  purchaseRod: false,
  yardageMethod: 'railroad-if-short'
});
```

Assert the workbook intermediates and total:

```js
assert.equal(primary.rod.total, 965.832);
assert.equal(primary.laborWidths, 6);
assert.equal(primary.laborPrice, 534);
assert.equal(primary.fabricPrice, 861.9);
assert.equal(closest.laborWidths, 6);
assert.equal(closest.laborPrice, 357);
assert.equal(closest.fabricPrice, 234);
close(primary.rod.total + primary.laborPrice + primary.fabricPrice + closest.laborPrice + closest.fabricPrice, 2952.732);
```

- [ ] **Step 2: Run the reconciliation test and observe failure before integration adjustments**

Run `node tests/drapery-formula-v2.test.js`.

Expected: FAIL until the test loads the new adapter and the adapter matches every workbook intermediate.

- [ ] **Step 3: Remove obsolete source-literal assertions**

Delete assertions that treat these template literals as authoritative:

- `const lined = 10;`
- `overlap: 3.5`
- `widthEase: 2`
- `doubleHeader: 8`
- `lengthEase: 2`

Replace them with assertions that the PHP module enqueues the adapter at priority 100 and that the adapter reads those values from `window.DavisDraperyBuilderSettings`. Keep unrelated debug-panel and minimum-input assertions.

- [ ] **Step 4: Add a two-path settings mutation proof**

Clone the defaults, set overlap to `10`, rerun both calculations, and assert both `primary.finishedWidth` and `closest.finishedWidth` increase by `13` for a pair: `(10 - 3.5) * 2`.

- [ ] **Step 5: Run both formula suites**

```powershell
node tests/drapery-builder-settings-formula.test.js
node tests/drapery-formula-v2.test.js
```

Expected: PASS with the total `2952.732`.

- [ ] **Step 6: Commit workbook reconciliation**

```powershell
git add wordpress-child-theme-working/tests/drapery-formula-v2.test.js wordpress-child-theme-working/tests/drapery-builder-settings-formula.test.js
git commit -m "test: reconcile builder settings with updated workbook"
```

### Task 6: Full local regression and release review

**Files:**
- Modify only if a test exposes a defect: the three new settings files and their tests.

**Interfaces:**
- Consumes: All local modules and tests.
- Produces: A locally verified release set containing exactly three production files and four settings-related tests.

- [ ] **Step 1: Run every existing child-theme test**

From `wordpress-child-theme-working`:

```powershell
Get-ChildItem tests -Filter *.test.js | Sort-Object Name | ForEach-Object { node $_.FullName; if ($LASTEXITCODE -ne 0) { throw "Failed: $($_.Name)" } }
```

Expected: all tests PASS, including colorways, finials, mobile layout, coupons, email formatting, the legacy formula suite, and the three new settings suites.

- [ ] **Step 2: Run static checks and forbidden-literal review**

```powershell
node --check davis-drapery-builder-settings.js
node -e "JSON.parse(require('fs').readFileSync('davis-drapery-builder-settings.defaults.json','utf8')); console.log('valid JSON')"
rg -n "1\.15|1\.20|overlap, 1\.5|ease === undefined \? 6|doubleHeader, 14|lining_cost_per_yard = 7|interlining_fabric_cost_per_yard = 7" davis-drapery-builder-settings.*
```

Expected: syntax/JSON checks PASS and `rg` returns no matches in the new active adapter/module/defaults.

- [ ] **Step 3: Review staged scope**

```powershell
git status --short
git diff --check
git diff --stat HEAD~4..HEAD
```

Confirm no unrelated untracked workspace files are staged and no template file is changed.

- [ ] **Step 4: Commit any test-driven repair, or record no-op**

If a defect required a change, commit only the affected settings files and tests:

```powershell
git add wordpress-child-theme-working/davis-drapery-builder-settings.defaults.json wordpress-child-theme-working/davis-drapery-builder-settings.php wordpress-child-theme-working/davis-drapery-builder-settings.js wordpress-child-theme-working/tests/drapery-builder-settings-defaults.test.js wordpress-child-theme-working/tests/drapery-builder-settings-php.test.js wordpress-child-theme-working/tests/drapery-builder-settings-formula.test.js wordpress-child-theme-working/tests/drapery-formula-v2.test.js
git commit -m "fix: complete drapery builder settings verification"
```

If no repair was necessary, do not create an empty commit.

### Task 7: Reversible live deployment and capability migration

**Files:**
- Deploy local `wordpress-child-theme-working/davis-drapery-builder-settings.defaults.json` to `wp-content/novamira-sandbox/davis-drapery-builder-settings.defaults.json`.
- Deploy local `wordpress-child-theme-working/davis-drapery-builder-settings.js` to `wp-content/novamira-sandbox/davis-drapery-builder-settings.js`.
- Deploy local `wordpress-child-theme-working/davis-drapery-builder-settings.php` initially as `wp-content/novamira-sandbox/davis-drapery-builder-settings.php.disabled`.
- Do not overwrite `wp-content/themes/kadence-child/fabric-selection-v2.php`.

**Interfaces:**
- Consumes: Verified local release files and current live ACF options-page post ID 6974.
- Produces: Active admin settings fields, `manage_options` page access, and configured frontend calculations.

- [ ] **Step 1: Capture the live pre-deployment state**

Using read-only WordPress abilities:

- Read `wp-content/themes/kadence-child/fabric-selection-v2.php` metadata/hash and confirm the `DAVIS_DRAPERY_FORMULA_V2` markers and `DOMContentLoaded` calculation listeners still exist.
- Read the sandbox directory and `.crashed` state.
- Execute read-only PHP returning post 6974's `post_content`, the existing `base_pricing` option, and any options whose names start with `options_dd_`.
- Record the page's current capability and the returned option values in the task log; do not print unrelated WordPress options.

Expected: capability is `edit_posts`, `base_pricing` is `37.50`, and no new settings are required to exist.

- [ ] **Step 2: Upload the three files without activating PHP**

Use `novamira/write-file` with UTF-8 overwrite mode for the JSON and JavaScript. Write PHP to the `.php.disabled` path in the sandbox. Read all three back and compare SHA-256 hashes with the local files.

Expected: byte-for-byte matches and no sandbox crash marker.

- [ ] **Step 3: Update the ACF UI options-page capability safely**

Use `novamira/execute-php` with code that:

1. Loads post ID 6974.
2. `maybe_unserialize()`s `post_content`.
3. Verifies the resulting array has the expected page/menu slug `drapery-builder-settings`.
4. Saves the original serialized content in a uniquely named backup option such as `davis_ddbs_options_page_backup_20260804` only if that backup does not already exist.
5. Sets only `capability` to `manage_options`.
6. Calls `wp_update_post()` and returns the updated capability and post ID.

Abort without writing if the post ID, post type, slug, or serialized shape differs from the captured baseline.

- [ ] **Step 4: Activate the sandbox module**

Use `novamira/enable-file` on `wp-content/novamira-sandbox/davis-drapery-builder-settings.php.disabled`.

Immediately call the connector again. If safe mode or `.crashed` appears, disable the module, inspect the crash record, fix locally with a failing regression test, redeploy the disabled file, and only then clear `.crashed` and re-enable.

- [ ] **Step 5: Verify PHP runtime and ACF registration**

Use read-only `novamira/execute-php` calls to return only:

- `function_exists( 'davis_drapery_builder_settings' )`.
- `davis_drapery_builder_settings()`.
- `acf_get_field_group( 'group_ddbs_workbook_constants' )` title/location/active status.
- The field count and the exact field names.
- Post 6974's capability.

Expected: functions exist; normalized values equal the defaults; the group is active on `drapery-builder-settings`; capability is `manage_options`; every schema field is present.

- [ ] **Step 6: Verify the admin page**

Open `/wp-admin/admin.php?page=drapery-builder-settings` as the authenticated administrator and confirm:

- Six tabs render.
- Workbook defaults appear with correct units and decimals.
- The legacy Base Pricing field is hidden.
- Saving unchanged defaults succeeds.
- Changing overlap to a temporary test value, saving, and reloading persists the value.
- Restore overlap to `3.5` before continuing.

Do not use or create a non-admin account. Confirm non-admin protection from the stored `manage_options` capability plus the module's menu/direct-access guards.

- [ ] **Step 7: Verify the live builder calculation**

Fetch or open `/drapery-builder/` and confirm:

- The page contains `window.DavisDraperyBuilderSettings` before the adapter script.
- The adapter loads from `/wp-content/novamira-sandbox/davis-drapery-builder-settings.js`.
- Console inspection shows the configured helper replaced the legacy object.
- The updated workbook example produces primary rod `965.832`, primary labor `534`, primary fabric `861.9`, closest labor `357`, closest fabric `234`, and combined total `2952.732`.
- Temporarily changing overlap in Builder Settings changes both primary and closest finished widths; restoring `3.5` restores the workbook totals.
- Single-rod and double-rod flows show no `NaN`, negative surcharge, or JavaScript errors.

- [ ] **Step 8: Execute the rollback check without deleting saved data**

Document the tested rollback commands:

1. `novamira/disable-file` for the PHP module.
2. Restore post 6974's original `post_content` from `davis_ddbs_options_page_backup_20260804` if capability rollback is required.
3. Leave `options_dd_*` values in place; they are inert when the module is disabled.

Do not perform the rollback after successful verification. Keep the backup option until the user accepts the live result.

- [ ] **Step 9: Final evidence review**

Re-run the complete local test command from Task 6 and capture fresh live runtime/config results. Report the exact files deployed, live defaults, workbook reconciliation total, access capability, and rollback path. Do not claim completion from earlier test output.

## Reference documentation

- ACF Options Page UI and capability setting: `https://www.advancedcustomfields.com/resources/options-page/`
- ACF code-registered options pages and location rules: `https://www.advancedcustomfields.com/resources/acf_add_options_page/`
- Loading option values with `get_field( $name, 'option' )`: `https://www.advancedcustomfields.com/resources/get-values-from-an-options-page/`
