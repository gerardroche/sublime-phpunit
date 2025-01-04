# Changelog

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## 3.19.4 - 2025-01-04

### Fixed

- Fix path to the osx_iterm executable [#130](https://github.com/gerardroche/sublime-phpunit/pull/130) @devinfd

## 3.19.3 - 2024-04-01

### Fixed

- Fix ''NoneType' object is not iterable'

## 3.19.2 - 2024-02-06

### Fixed

- `PHPUnit: Test Switch` ("switchables") doesn't work in some cases

## 3.19.1 - 2024-01-23

### Fixed

- Tmux strategy `phpunit.tmux_clear_scrollback` setting is not working correctly

## 3.19.0 - 2024-01-22

### Added

- Tmux strategy - Runs test in a tmux pane [#119](https://github.com/gerardroche/sublime-phpunit/issues/119)

### Fixed

- Syntax fixes

## 3.18.2 - 2023-11-12

### Fixed

- Fix debug mode should be disabled by default
- Fix result output footer edge-cases

## 3.18.1 - 2023-08-16

### Deprecated

* The deprecated strategy `basic` should be replaced with `sublime`.

## 3.18.0 - 2023-08-06

### Added

* [#126](https://github.com/gerardroche/sublime-phpunit/issues/126): New "powershell" strategy to run tests in the PowerShell command-line shell (Windows)
* [#92](https://github.com/gerardroche/sublime-phpunit/issues/92): New "cmd" strategy to run tests in the cmd.exe command-line (Windows)
* [#125](https://github.com/gerardroche/sublime-phpunit/issues/125): New "Toggle Run Test On Save" command palette

## 3.17.1 - 2023-08-04

### Fixed

* [#92](https://github.com/gerardroche/sublime-phpunit/issues/92): Allow "external" strategy for custom strategies using `prepend_cmd`

## 3.17.0 - 2023-08-04

### Added

* [#121](https://github.com/gerardroche/sublime-phpunit/issues/121): Run tests from the side bar menu
* [#122](https://github.com/gerardroche/sublime-phpunit/issues/122): Run tests from the context menu

### Deprecated

* The deprecated on-post-save "run_test_file" event, use on-post-save "phpunit_test_file" event instead.

## 3.16.0 - 2023-08-02

### Added

* [#99](https://github.com/gerardroche/sublime-phpunit/issues/99): New support for running tests via Docker
* [#118](https://github.com/gerardroche/sublime-phpunit/issues/118): New support for running tests on a remote server via SSH
* [#120](https://github.com/gerardroche/sublime-phpunit/issues/120): New strategy: `xterm` - Sends test commands to xterm terminal.
* New Command: Changelog

## 3.15.0 - 2023-07-24

### Added

* New Command: "PHPUnit: Toggle --cache-result" - Write test results to cache file
* New Command: "PHPUnit: Toggle --do-not-cache-result" - Do not write test results to cache file
* New Command: "PHPUnit: Toggle --globals-backup" - Backup and restore `$GLOBALS` for each test
* New Command: "PHPUnit: Toggle --no-logging" - Ignore logging configured in the XML configuration file
* New Command: "PHPUnit: Toggle --path-coverage" - Report path coverage in addition to line coverage
* New Command: "PHPUnit: Toggle --process-isolation" - Run each test in a separate PHP process
* New Command: "PHPUnit: Toggle --static-backup" - Backup and restore static properties for each test
* New Command: "PHPUnit: Toggle --teamcity" - Replace default progress and result output with TeamCity format

### Fixed

* Session options, e.g. toggled options, should be cleared on restart
* Session options loading edge-case issues
* Toggle options edge-case issues
* `phpunit.debug` should be documented in preferences
* Disable white-space characters in results output #117
* Disable indent guides in results output #116

## 3.14.0 - 2023-07-22

### Added

* New Command: "PHPUnit: Toggle --display-incomplete" - Display details for incomplete tests
* New Command: "PHPUnit: Toggle --display-skipped" - Display details for skipped tests
* New Command: "PHPUnit: Toggle --display-deprecations" - Display details for deprecations triggered by tests
* New Command: "PHPUnit: Toggle --display-errors" - Display details for errors triggered by tests
* New Command: "PHPUnit: Toggle --display-notices" - Display details for notices triggered by tests
* New Command: "PHPUnit: Toggle --display-warnings" - Display details for warnings triggered by tests
* New Command: "PHPUnit: Toggle --fail-on-skipped" - Signal failure using shell exit code when a test was skipped
* New Command: "PHPUnit: Toggle --fail-on-notice" - Signal failure using shell exit code when a notice was triggered
* New Command: "PHPUnit: Toggle --fail-on-incomplete" - Signal failure using shell exit code when a test was marked incomplete
* New Command: "PHPUnit: Toggle --fail-on-deprecation" - Signal failure using shell exit code when a deprecation was triggered
* New Command: "PHPUnit: Toggle --no-output" - Disable all output
* New Command: "PHPUnit: Toggle --no-progress" - Disable output of test execution progress
* New Command: "PHPUnit: Toggle --no-results" - Disable output of test results
* New Command: "PHPUnit: Toggle --order-by=depends" - Run tests in order: depends
* New Command: "PHPUnit: Toggle --order-by=size" - Run tests in order: size
* New Command: "PHPUnit: Toggle --stop-on-deprecation" - Stop after first test that triggered a deprecation
* New Command: "PHPUnit: Toggle --stop-on-notice" - Stop after first test that triggered a notice

### Changed

* Renamed command captions "PHPUnit: Toggle Option ..." → "PHPUnit: Toggle ..."

### Fixed

* Fixed various tests results colour output issues (PHPUnit, Pest)
* Fixed `--orderby=` toggle commands doesn't work
* Fixed command captions "PHPUnit: Set Option ..." → "PHPUnit: Toggle ..."

## 3.13.0 - 2023-05-15

### Changed

* [#83](https://github.com/gerardroche/sublime-phpunit/issues/83): Autocommand test file on save renamed `phpunit_test_file` to `run_test_file`

## 3.12.3 - 2023-04-19

### Fixed

* [#115](https://github.com/gerardroche/sublime-phpunit/issues/115): Test nearest, tests whole pest file

## 3.12.2 - 2023-04-18

### Fixed

* [#103](https://github.com/gerardroche/sublime-phpunit/issues/103): Some Pest exec output colors not correct
* [#102](https://github.com/gerardroche/sublime-phpunit/issues/102): Some Artisan exec output colors not correct

## 3.12.1 - 2023-04-17

### Fixed

* [#114](https://github.com/gerardroche/sublime-phpunit/issues/114): Test nearest and file is missing for Pest

## 3.12.0 - 2023-04-16

### Added

* [#69](https://github.com/gerardroche/sublime-phpunit/issues/69): Support for PHPUnit output font size: `phpunit.font_size`
* [#111](https://github.com/gerardroche/sublime-phpunit/issues/111): Support for [ParaTest](https://github.com/paratestphp/paratest)
* [#110](https://github.com/gerardroche/sublime-phpunit/issues/110): View settings side-by-side

### Changed

* [#69](https://github.com/gerardroche/sublime-phpunit/issues/69): Renamed setting `phpunit.text_ui_result_font_size` to `phpunit.font_size`

### Fixed

* [#113](https://github.com/gerardroche/sublime-phpunit/issues/113): Color is missing in strategies like Kitty for Artisan and Pest test runners
* [#112](https://github.com/gerardroche/sublime-phpunit/issues/112): Don't show build panel when using strategies like Kitty

## 3.11.2 - 2023-04-15

### Fixed

* [#103](https://github.com/gerardroche/sublime-phpunit/issues/103): Build output syntax

## 3.11.1 - 2023-04-15

### Fixed

* [#103](https://github.com/gerardroche/sublime-phpunit/issues/104): Artisan and Pest color output

## 3.11.0 - 2023-04-15

* [#104](https://github.com/gerardroche/sublime-phpunit/issues/104): [Kitty](https://github.com/kovidgoyal/kitty) execution strategy

## 3.10.1 - 2023-04-13

### Fixed

* [#103](https://github.com/gerardroche/sublime-phpunit/issues/103): Only use the Artisan runner if enabled and it exists
* [#102](https://github.com/gerardroche/sublime-phpunit/issues/102): Only use the Pest runner if enabled and it exists

## 3.10.0 - 2023-04-13

### Added

* [#102](https://github.com/gerardroche/sublime-phpunit/issues/102): Support for Artisan: `artisan test`

## 3.9.0 - 2023-04-13

### Added

* [#103](https://github.com/gerardroche/sublime-phpunit/issues/103): Support for Pest

### Changed

* [#109](https://github.com/gerardroche/sublime-phpunit/issues/109): env and cmd information in now only displayed in debug mode

## 3.8.0 - 2023-04-09

### Added

* [#108](https://github.com/gerardroche/sublime-phpunit/issues/108): Allow `phpunit.executable` to be set as `list`
* [#107](https://github.com/gerardroche/sublime-phpunit/issues/107): Support PHPUnit 10 dist file name `phpunit.dist.xml`

## 3.7.0 - 2023-04-07

### Added

* [#105](https://github.com/gerardroche/sublime-phpunit/issues/105): `phpunit.prepend_cmd` option

### Fixed

* [#105](https://github.com/gerardroche/sublime-phpunit/issues/105): Support for syntax updates in build `>=` 4134

## 3.6.3 - 2022-07-06

### Fixed

* [#101](https://github.com/gerardroche/sublime-phpunit/issues/101): Remaining arguments are lost when running on iterm (OSX)

## 3.6.2 - 2022-07-06

### Fixed

* Switching misses matching switchable and displays overlay

## 3.6.1 - 2021-12-14

### Fixed

* Switching should go straight to file when only one result

## 3.6.0 - 2020-05-05

### Added

* [#98](https://github.com/gerardroche/sublime-phpunit/issues/98): Add `phpunit.executable` setting to set custom phpunit path

## 3.5.1 - 2020-01-24

### Fixed

* `.php-version` files should accept minor version formats e.g. 7.4

## 3.5.0 - 2020-01-22

### Added

* Support for ST4

## 3.4.0 - 2019-11-13

### Added

* [#83](https://github.com/gerardroche/sublime-phpunit/issues/83): Auto-run tests on save

## 3.3.0 - 2019-10-17

* [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=default
* [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=defects
* [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=duration
* [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=no-depends
* [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=random
* [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=reverse
* New command: PHPUnit: Toggle Option --stop-on-warning
* New command: PHPUnit: Toggle Option --stop-on-defect
* New command: PHPUnit: Toggle Option --fail-on-warning
* New command: PHPUnit: Toggle Option --fail-on-risky
* New command: PHPUnit: Toggle Option --disallow-resource-usage
* New command: PHPUnit: Toggle Option --dont-report-useless-tests
* New command: PHPUnit: Toggle Option --reverse-list
* New command: PHPUnit: Toggle Option --disable-coverage-ignore

## 3.2.2 - 2019-08-29

### Fixed

* Various trivial issues

## 3.2.1 - 2019-03-19

### Fixed

* [#89](https://github.com/gerardroche/sublime-phpunit/issues/89): "Test Last" is broken

## 3.2.0 - 2019-03-19

### Added

* [#86](https://github.com/gerardroche/sublime-phpunit/issues/86): Support running tests in iTerm
* [#81](https://github.com/gerardroche/sublime-phpunit/issues/81): Command to run a full test suite

## 3.1.1 - 2019-02-05

### Fixed

* Minor fixes

## 3.1.0 - 2018-12-23

### Added

* [#9](https://github.com/gerardroche/sublime-phpunit/issues/9): Use goto anything when more than one possible switchable

### Fixed

* Tests results panel should not show rulers

## 3.0.0 - 2018-03-06

### Changed

* Renamed plugin from "phpunitkit" to "PHPUnitKit"

  If you manually installed the package then you will need to rename the folder where you installed it from "phpunitkit" to "PHPUnitKit".

### Deprecated

* Color schemes (color schemes are auto generated based on the active color scheme)
* Command `phpunit_switch_file`, use `phpunit_test_switch` instead
* Command `phpunit_open_code_coverage`, use `phpunit_test_coverage` instead

## 2.5.0 - 2018-03-03

### Added

* [#78](https://github.com/gerardroche/sublime-phpunit/issues/78): Add support for PHPUnit Pretty Result Printer

## 2.4.6 - 2017-12-08

### Fixed

* [#76](https://github.com/gerardroche/sublime-phpunit/issues/76): Testing nearest doesn't always work

## 2.4.5 - 2017-12-05

### Fixed

* [#76](https://github.com/gerardroche/sublime-phpunit/issues/76): Testing nearest doesn't always work

## 2.4.4 - 2017-11-23

### Fixed

* Workaround [Base ApplicationCommand registered in application_command_classes](https://github.com/SublimeTextIssues/Core/issues/2044)

## 2.4.3 - 2017-11-20

### Fixed

* [#75](https://github.com/gerardroche/sublime-phpunit/issues/75): Test results colors don't work

## 2.4.2 - 2017-11-19

### Fixed

* Support for new Sublime Text color scheme format

## 2.4.1 - 2017-08-23

### Fixed

* [#70](https://github.com/gerardroche/sublime-phpunit/issues/70): Tests results don't have colors anymore

## 2.4.0 - 2017-08-23

### Added

* [#69](https://github.com/gerardroche/sublime-phpunit/issues/69): Can I adjust the font size of the test result panel

## 2.3.0 - 2017-08-23

### Added

* Improved color scheme support for test results
* `:TestSwitch` now positions cursor at the row of the class definition

### Removed

* The default key bindings have been removed, instead add your preferred key bindings:

  **Menu → Preferences → Key Bindings**

  ```json
  [
      { "keys": ["ctrl+shift+a"], "command": "phpunit_test_suite" },
      { "keys": ["ctrl+shift+f"], "command": "phpunit_test_file" },
      { "keys": ["ctrl+shift+n"], "command": "phpunit_test_nearest" },
      { "keys": ["ctrl+shift+l"], "command": "phpunit_test_last" },
      { "keys": ["ctrl+shift+v"], "command": "phpunit_test_visit" },
      { "keys": ["ctrl+shift+s"], "command": "phpunit_test_switch" },
      { "keys": ["ctrl+shift+c"], "command": "phpunit_test_cancel" },
      { "keys": ["ctrl+shift+r"], "command": "phpunit_test_results" },
  ]
  ```

  The following key bindings remain the same:

  Key | Description
  --- | -----------
  `F4` | Jump to Next Failure
  `Shift+F4` | Jump to Previous Failure

## 2.2.2 - 2017-08-11

### Fixed

* [#66](https://github.com/gerardroche/sublime-phpunit/issues/66): PHPUnit: 'NoneType' object has no attribute 'items'

## 2.2.1 - 2017-06-13

### Fixed

* TypeError: object of type 'NoneType' has no len()

## 2.2.0 - 2017-06-13

### Added

* [#38](https://github.com/gerardroche/sublime-phpunit/issues/38): Command "PHPUnit: Test Visit" (phpunit_test_visit) Open the last run test in the current window (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests)
* Command "phpunit_test_cancel" for cancelling tests
* Command "phpunit_test_results" for opening the test results panel

### Changed

* Renamed command "PHPUnit: Cancel Test" to "PHPUnit: Test Cancel"
* Renamed command "PHPUnit: Show Results" to "PHPUnit: Test Results"
* Renamed command "PHPUnit: Open Code Coverage" to "PHPUnit: Test Coverage"
* Renamed command "PHPUnit: Switch File" to "PHPUnit: Test Switch"

### Deprecated

* The command "phpunit_open_code_coverage" is deprecated and will be removed in v3.0.0; use "phpunit_test_coverage" instead
* The command "phpunit_switch_file" is deprecated and will be removed in v3.0.0; use "phpunit_test_switch" instead

## 2.1.0 - 2017-05-17

### Added

* New syntax definition format for test results panel
* Test File command will now also run the test case for current file

### Deprecated

* Colour schemes are deprecated and will be removed in v3.0.0

### Fixed

* All status messages should be prefixed with "PHPUnit: "
* No status messages in some edge cases

## 2.0.3 - 2017-04-19

### Fixed

* [#63](https://github.com/gerardroche/sublime-phpunit/issues/63): Switches to wrong test

## 2.0.2 - 2017-04-13

### Fixed

* [#59](https://github.com/gerardroche/sublime-phpunit/issues/59): Error when trying to run PHPUnit with a PHP executable (Windows)
* Error when trying to run a global install of PHPUnit with a PHP executable
* Errors when some paths contained characters like spaces
* Environment variables now work in path settings like "phpunit.php_executable" and "phpunit.php_versions_path"
* Project PHP version file (.php-version) version number not working for some version numbers
* Jump to next/previous error didn't work in some cases where file paths contained characters like spaces
* Running tests now terminates any currently running tests before running tests
* .php-version file version is no longer overridden by the default executable 'phpunit.php_executable'

## 2.0.1 - 2017-03-29

### Fixed

* [#58](https://github.com/gerardroche/sublime-phpunit/issues/58): Error when ~/.phpenv/versions path doesn't exist

## 2.0.0 - 2017-03-24

### Added

* [#56](https://github.com/gerardroche/sublime-phpunit/issues/56): Support for .php-version file to specify PHP version to use for running PHPUnit
* [#55](https://github.com/gerardroche/sublime-phpunit/issues/55): Use different PHP executable
* [#53](https://github.com/gerardroche/sublime-phpunit/issues/53): Vi keymaps are now enabled by default
* [#52](https://github.com/gerardroche/sublime-phpunit/issues/52): Test File command

### Changed

* [#42](https://github.com/gerardroche/sublime-phpunit/issues/42): Commands

    Old name | new name
    -------- | --------
    Run All Tests | Test Suite
    Run Last Test | Test Last
    Run Single | Test Nearest
    Switch Test Case / Class Under Test | Switch File
    Open HTML Code Coverage in Browser | open Code Coverage
    Cancel Test Run | Cancel Test
    Show Test Results | Show Results

* [#54](https://github.com/gerardroche/sublime-phpunit/issues/54): Vim keymaps

    Old keymap | New keymap | Description
    ---------- | ---------- | -----------
    `,t` | `,a` | Test All
    `,r` | `,t` | Test Single
    `,e` | `,l` | Test Last

* settings

    Old setting | new setting
    ----------- | -----------
    `phpunit.keymaps.vi` | `phpunit.vi_keymaps`

### Fixed

* [#57](https://github.com/gerardroche/sublime-phpunit/issues/57): Find next / previous failure keymaps (Windows)

## 1.2.1 - 2017-02-27

### Fixed

* Open settings command file path

## 1.2.0 - 2017-02-02

### Changed

* Minor refactoring

### Fixed

* Minor fixes

## 1.1.0 - 2016-09-21

### Added

* [#39](https://github.com/gerardroche/sublime-phpunit/issues/39): Command Palette Command-Line Option toggles

### Deprecated

* Deprecated [#41](https://github.com/gerardroche/sublime-phpunit/issues/41): The `phpunit.vi_keymaps` configuration setting. Use `phpunit.keymaps.vi` instead.

## 1.0.3 - 2016-09-21

### Fixed

* [#46](https://github.com/gerardroche/sublime-phpunit/issues/46): (Windows) Cannot run single test from class under test

## 1.0.2 - 2016-09-20

### Fixed

* [#40](https://github.com/gerardroche/sublime-phpunit/issues/40): Cannot specify short Command-Line Options

## 1.0.1 - 2016-09-20

### Fixed

* [#43](https://github.com/gerardroche/sublime-phpunit/issues/43): (Windows) Cannot run Composer installed PHPUnit

## 1.0.0 - 2016-09-19

### Fixed

* README

## 1.0.0-beta2 - 2016-08-11

### Fixed

* README

## 1.0.0-beta1 - 2016-07-29

### Fixed

* README

## 0.15.1 - 2016-06-08

### Fixed

* README

## 0.15.0 - 2016-06-03

### Changed

* plugin name from "php_phpunit" to "phpunitkit". The plugin was renamed because the last name was rejected by the Package Control channel.
  - If you previously installed manually then remove the installation and install via Package Control. Search for phpunitkit.
  - If you prefer to keep your manual installation then rename or move your installation to "phpunitkit".

## 0.14.1 - 2016-05-16

### Fixed

* [#35](https://github.com/gerardroche/sublime-phpunit/issues/35): Cannot run "Run Single Test" with the latest build of Sublime Text (build 3114)

## 0.14.0 - 2016-05-15

### Added

* Now available on Package Control

### Changed

* Renamed package from "phpunit" to "php_phpunit". This was needed in order to provide the plugin via Package Control. If you are having issues then either remove your existing plugin installation and install via Package Control, making sure to install the plugin by me, PHP PHPUnit (gerardroche), or rename your existing installation to "phpunit".

## 0.13.0 - 2016-01-29

### Added

* [#34](https://github.com/gerardroche/sublime-phpunit/issues/34): Option to disable composer support (phpunit.composer). Defaults to true.

## 0.12.0 - 2016-01-12

### Changed

* switch file command caption is now "PHPUnit: Switch Test Case / Class Under Test"

## 0.11.0 - 2015-11-13

### Added

* CHANGELOG link to package settings menu
* Toggle No Coverage "--no-coverage" command
* "phpunit.options" setting to allow configuring a default list of options for PHPUnit to use

## 0.10.1 - 2015-09-30

### Fixed

* incorrect file path to settings when opening from the command palette

## 0.10.0 - 2015-09-30

### Added

* "phpunit.development" setting to enable/disable plugin development utilities

### Changed

* settings are no longer loaded from a plugin specific settings file i.e. phpunit.sublime-settings

    There is, in my opinion, a bad practice of each and every plugin having its
    own settings file. This plugin no longer does this. All plugin settings are prefixed with the name of the plugin followed by a period i.e. "phpunit.".

    Settings are loaded in this order:

    1) Project Specific

    Example: Menu → Project → Edit Project

    ```
    {
        "settings": {
            "phpunit.save_all_on_run": true
        }
    }
    ```

    2) User

    Example: Menu → Preferences → Settings - User

    ```
    {
        "phpunit.save_all_on_run": true
    }
    ```

* "save_all_on_run" now only save files that exist on disk and have dirty buffers

    The reason for this change:

    When saving a file that doesn't exist on disk Sublime Text prompts with a "Save file" dialog, meanwhile the tests would run in the background anyways. We could prevent the tests from running until the user finishes handling the dialogs. If there is a desire for this please open an issue.

* renamed setting "phpunit.enable_keymaps" to "phpunit.keymaps"
* renamed setting "phpunit.enable_vi_keymaps" to "phpunit.keymaps"
* To enable vi keymaps both "phpunit.keymaps" and "phpunit.vi_keymaps" need to be set to true, previously only the vi_keymaps needed to be set to true

## 0.9.0 - 2015-07-06

### Added

* "Open HTML Code Coverage in Browser" command #23
* Switch and put class and test-case side-by-side #8

## 0.8.0 - 2015-06-18

### Added

* Configurable color schemes #7
* Colour scheme "Packages/phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme" #21
* Colour scheme "Packages/phpunit/color-schemes/solarized-dark.hidden-tmTheme" #21

### Fixed

* Command palette captions are now capitalised
* Goto next/last failure now matches all files/line-numbers in stack traces

## 0.7.0 - 2015-06-11

### Added

* License link to package settings menu

### Removed

* Several deprecated behaviours

## 0.6.0 - 2015-05-27

### Added

* "PHPUnit: Cancel Test Run" to command palette
* ST3 Requirements check. Now raises a runtime exception if trying to load in < Sublime Text 3

## 0.5.0 - 2015-05-16

### Added

* "PHPUnit.." to "Tools" main menu #15 #16
* "PHPUnit: Show Test Results" command
* "Open "Preferences: PHPunit Settings - Default" command
* "Open "Preferences: PHPunit Settings - User" command
* Running the last test command is now saved per window #19

### Deprecated

* Per-project settings are now accessed via prefix "phpunit." in project definition settings. The old behaviour is deprecated and will be removed before the 1.0.0 beta releases.

### Removed

* "phpunit" command #31

### Fixed

* Keymaps now display the default `ctrl+...` keymaps in command palette. Previously the Vintage/Vintageous keymaps were displayed.
* error when there is no active window and/or view
* test results not displaying colour when there are risky tests

## 0.4.0 - 2015-05-03

### Added

* option to disable the default keymaps. To disable the keymaps set `"phpunit.enable_keymaps": false` the User Settings. Access this file from `Preferences → Settings - User` menu item. #30

## 0.3.0 - 2015-02-04

### Added

* Can now run multiple test methods using a multiple selection #5
* command palette toggle - report test progress TestDox format #24 #2
* command palette toggle - report test progress TAP format #24 #28
* Switching class-under-test/test-case now splits window into two views with both side-by-side *if* the current window only has one group.
* Vintage/Vintageous keymaps can now be enabled in the preferences. They are disabled by default. To enable set `"phpunit.enable_vi_keymaps": true` in the User Settings. Access this file from `Preferences → Settings - User` menu item.

### Fixed

* Can't switch classes beginning with an underscore #22
* Running single test runs all tests with the same prefix #25
* Some minor test result progress syntax highlighting bugs

## 0.2.0 - 2015-01-21

### Added

* Composer installed PHPUnit support #13
* Saving all files on run can now be disabled. It can also be set on a per-project basis #12
* Command Palette commands #17
* Package Settings menu "Preferences → Package Settings → PHPUnit" #14
* Example Vintage/Vintageous keymaps in the default key bindings: "Preferences → Package Settings → PHPUnit → Key Bindings - Default" #10

### Changed

* Debug messages are now disabled by default. To enable debug messages set an environment variable to a non-blank value: `SUBLIME_PHPUNIT_DEBUG=yes`. To disable debug message set the variable to a blank value: `SUBLIME_PHPUNI_DEBUG=`. For example, on Linux Sublime Text can be opened at the Terminal with an exported environment variable: `export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text`. #6
* The last test run is now saved in memory for the current session, previously it was save to a file. #11
* Many refactorings including test runner commands are now Window commands, previously they were Text commands. There is no need for these commands to be instantiated for every view.

### Fixed

* Test result progress highlighting was not displayed properly
* Test result failures red background no longer matches trailing whitespace, previously the red background stretched the full width of the screen.

### 0.1.0 - 2015-01-07

* Initial import; PHPUnit support
