# PHPUNITKIT CHANGELOG

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## [3.6.0] - 2020-05-05

### Added

* Added [#98](https://github.com/gerardroche/sublime-phpunit/issues/98): Add `phpunit.executable` setting to set custom phpunit path

## [3.5.1] - 2020-01-24

* Fixed: `.php-version` files should accept minor version formats e.g. 7.4

## [3.5.0] - 2020-01-22

* Added: Support for ST4

## [3.4.0] - 2019-11-13

* Added [#83](https://github.com/gerardroche/sublime-phpunit/issues/83): Auto-run tests on save

## [3.3.0] - 2019-10-17

* Added [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=default
* Added [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=defects
* Added [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=duration
* Added [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=no-depends
* Added [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=random
* Added [#29](https://github.com/gerardroche/sublime-phpunit/issues/29): New Command: PHPUnit: Set Option --order-by=reverse
* Added: New command: PHPUnit: Toggle Option --stop-on-warning
* Added: New command: PHPUnit: Toggle Option --stop-on-defect
* Added: New command: PHPUnit: Toggle Option --fail-on-warning
* Added: New command: PHPUnit: Toggle Option --fail-on-risky
* Added: New command: PHPUnit: Toggle Option --disallow-resource-usage
* Added: New command: PHPUnit: Toggle Option --dont-report-useless-tests
* Added: New command: PHPUnit: Toggle Option --reverse-list
* Added: New command: PHPUnit: Toggle Option --disable-coverage-ignore

## [3.2.2] - 2019-08-29

* Fixed: Various trivial issues

## [3.2.1] - 2019-03-19

* Fixed [#89](https://github.com/gerardroche/sublime-phpunit/issues/89): "Test Last" is broken

## [3.2.0] - 2019-03-19

### Added

* Added [#86](https://github.com/gerardroche/sublime-phpunit/issues/86): Support running tests in iTerm
* Added [#81](https://github.com/gerardroche/sublime-phpunit/issues/81): Command to run a full test suite

## [3.1.1] - 2019-02-05

* Trivial fixes

## [3.1.0] - 2018-12-23

### Added

* Added [#9](https://github.com/gerardroche/sublime-phpunit/issues/9): Use goto anything when more than one possible switchable

### Fixed

* Fixed: Tests results panel should not show rulers

## [3.0.0] - 2018-03-06

### Changed

* Changed: Renamed plugin from "phpunitkit" to "PHPUnitKit"

  If you manually installed the package then you will need to rename the folder where you installed it from "phpunitkit" to "PHPUnitKit".

### Removed

* Removed: Deprecated color schemes (color schemes are auto generated based on the active color scheme)
* Removed: Deprecated command `phpunit_switch_file`, use `phpunit_test_switch` instead
* Removed: Deprecated command `phpunit_open_code_coverage`, use `phpunit_test_coverage` instead

## [2.5.0] - 2018-03-03

### Added

* Added [#78](https://github.com/gerardroche/sublime-phpunit/issues/78): Add support for PHPUnit Pretty Result Printer

## [2.4.6] - 2017-12-08

### Fixed

* Fixed [#76](https://github.com/gerardroche/sublime-phpunit/issues/76): Testing nearest doesn't always work

## [2.4.5] - 2017-12-05

### Fixed

* Fixed [#76](https://github.com/gerardroche/sublime-phpunit/issues/76): Testing nearest doesn't always work

## [2.4.4] - 2017-11-23

### Fixed

* Fixed: Workaround [Base ApplicationCommand registered in application_command_classes](https://github.com/SublimeTextIssues/Core/issues/2044)

## [2.4.3] - 2017-11-20

### Fixed

* Fixed [#75](https://github.com/gerardroche/sublime-phpunit/issues/75): Test results colors don't work

## [2.4.2] - 2017-11-19

### Fixed

* Fixed: Support for new Sublime Text color scheme format

## [2.4.1] - 2017-08-23

### Fixed

* Fixed [#70](https://github.com/gerardroche/sublime-phpunit/issues/70): Tests results don't have colors anymore

## [2.4.0] - 2017-08-23

### Added

* Added [#69](https://github.com/gerardroche/sublime-phpunit/issues/69): Can I adjust the font size of the test result panel

## [2.3.0] - 2017-08-23

### Added

* Added: Improved color scheme support for test results
* Added: `:TestSwitch` now positions cursor at the row of the class definition

### Removed

* The default key bindings have been removed, instead add your preferred key bindings:

  `Menu > Preferences > Key Bindings`

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

## [2.2.2] - 2017-08-11

### Fixed

* Fixed [#66](https://github.com/gerardroche/sublime-phpunit/issues/66): PHPUnit: 'NoneType' object has no attribute 'items'

## [2.2.1] - 2017-06-13

### Fixed

* Fixed: TypeError: object of type 'NoneType' has no len()

## [2.2.0] - 2017-06-13

### Added

* Added [#38](https://github.com/gerardroche/sublime-phpunit/issues/38): Command "PHPUnit: Test Visit" (phpunit_test_visit) Open the last run test in the current window (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests)
* Added: Command "phpunit_test_cancel" for cancelling tests
* Added: Command "phpunit_test_results" for opening the test results panel

### Changed

* Renamed: Command "PHPUnit: Cancel Test" to "PHPUnit: Test Cancel"
* Renamed: Command "PHPUnit: Show Results" to "PHPUnit: Test Results"
* Renamed: Command "PHPUnit: Open Code Coverage" to "PHPUnit: Test Coverage"
* Renamed: Command "PHPUnit: Switch File" to "PHPUnit: Test Switch"

### Deprecated

* The command "phpunit_open_code_coverage" is deprecated and will be removed in v3.0.0; use "phpunit_test_coverage" instead
* The command "phpunit_switch_file" is deprecated and will be removed in v3.0.0; use "phpunit_test_switch" instead

## [2.1.0] - 2017-05-17

### Added

* Added: New syntax definition format for test results panel
* Added: Test File command will now also run the test case for current file

### Deprecated

* Deprecated: Colour schemes are deprecated and will be removed in v3.0.0

### Fixed

* Fixed: .travis.yml is not needed in release package
* Fixed: All status messages should be prefixed with "PHPUnit: "
* Fixed: No status messages in some edge cases

## [2.0.3] - 2017-04-19

### Fixed

* Fixed [#63](https://github.com/gerardroche/sublime-phpunit/issues/63): Switches to wrong test

## [2.0.2] - 2017-04-13

### Fixed

* Fixed [#59](https://github.com/gerardroche/sublime-phpunit/issues/59): Error when trying to run PHPUnit with a PHP executable (Windows)
* Fixed: Error when trying to run a global install of PHPUnit with a PHP executable
* Fixed: Errors when some paths contained characters like spaces
* Fixed: Environment variables now work in path settings like "phpunit.php_executable" and "phpunit.php_versions_path"
* Fixed: Project PHP version file (.php-version) version number not working for some version numbers
* Fixed: Jump to next/previous error didn't work in some cases where file paths contained characters like spaces
* Fixed: Running tests now terminates any currently running tests before running tests
* Fixed: .php-version file version is no longer overridden by the default executable 'phpunit.php_executable'

## [2.0.1] - 2017-03-29

### Fixed

* Fixed [#58](https://github.com/gerardroche/sublime-phpunit/issues/58): Error when ~/.phpenv/versions path doesn't exist

## [2.0.0] - 2017-03-24

### Added

* Added [#56](https://github.com/gerardroche/sublime-phpunit/issues/56): Support for .php-version file to specify PHP version to use for running PHPUnit
* Added [#55](https://github.com/gerardroche/sublime-phpunit/issues/55): Use different PHP executable
* Added [#53](https://github.com/gerardroche/sublime-phpunit/issues/53): Vi keymaps are now enabled by default
* Added [#52](https://github.com/gerardroche/sublime-phpunit/issues/52): Test File command

### Changed

* Changed [#42](https://github.com/gerardroche/sublime-phpunit/issues/42): Commands

    Old name | new name
    -------- | --------
    Run All Tests | Test Suite
    Run Last Test | Test Last
    Run Single | Test Nearest
    Switch Test Case / Class Under Test | Switch File
    Open HTML Code Coverage in Browser | open Code Coverage
    Cancel Test Run | Cancel Test
    Show Test Results | Show Results

* Changed [#54](https://github.com/gerardroche/sublime-phpunit/issues/54): Vim keymaps

    Old keymap | New keymap | Description
    ---------- | ---------- | -----------
    `,t` | `,a` | Test All
    `,r` | `,t` | Test Single
    `,e` | `,l` | Test Last

* Changed: settings

    Old setting | new setting
    ----------- | -----------
    `phpunit.keymaps.vi` | `phpunit.vi_keymaps`

### Fixed

* Fixed [#57](https://github.com/gerardroche/sublime-phpunit/issues/57): Find next / previous failure keymaps (Windows)

## [1.2.1] - 2017-02-27

### Fixed

* Fixed: Open settings command file path

## [1.2.0] - 2017-02-02

### Changed

* Minor refactoring

### Fixed

* Minor fixes

## [1.1.0] - 2016-09-21

### Added

* Added [#39](https://github.com/gerardroche/sublime-phpunit/issues/39): Command Palette Command-Line Option toggles

### Deprecated

* Deprecated [#41](https://github.com/gerardroche/sublime-phpunit/issues/41): The `phpunit.vi_keymaps` configuration setting. Use `phpunit.keymaps.vi` instead.

## [1.0.3] - 2016-09-21

### Fixed

* Fixed [#46](https://github.com/gerardroche/sublime-phpunit/issues/46): (Windows) Cannot run single test from class under test

## [1.0.2] - 2016-09-20

### Fixed

* Fixed [#40](https://github.com/gerardroche/sublime-phpunit/issues/40): Cannot specify short Command-Line Options

## [1.0.1] - 2016-09-20

### Fixed

* Fixed [#43](https://github.com/gerardroche/sublime-phpunit/issues/43): (Windows) Cannot run Composer installed PHPUnit

## [1.0.0] - 2016-09-19

### Fixed

* Fixed: README

## [1.0.0-beta2] - 2016-08-11

### Fixed

* Fixed: README

## [1.0.0-beta1] - 2016-07-29

### Fixed

* Fixed: README

## [0.15.1] - 2016-06-08

### Fixed

* Fixed: README

## [0.15.0] - 2016-06-03

### Changed

* Changed: plugin name from "php_phpunit" to "phpunitkit". The plugin was renamed because the last name was rejected by the Package Control channel.
  - If you previously installed manually then remove the installation and install via Package Control. Search for phpunitkit.
  - If you prefer to keep your manual installation then rename or move your installation to "phpunitkit".

## [0.14.1] - 2016-05-16

### Fixed

* Fixed [#35](https://github.com/gerardroche/sublime-phpunit/issues/35): Cannot run "Run Single Test" with the latest build of Sublime Text (build 3114)

## [0.14.0] - 2016-05-15

### Added

* Added: Now available on Package Control

### Changed

* Changed: Renamed package from "phpunit" to "php_phpunit". This was needed in order to provide the plugin via Package Control. If you are having issues then either remove your existing plugin installation and install via Package Control, making sure to install the plugin by me, PHP PHPUnit (gerardroche), or rename your existing installation to "phpunit".

## [0.13.0] - 2016-01-29

### Added

* Added [#34](https://github.com/gerardroche/sublime-phpunit/issues/34): Option to disable composer support (phpunit.composer). Defaults to true.

## [0.12.0] - 2016-01-12

### Changed

* Changed: switch file command caption is now "PHPUnit: Switch Test Case / Class Under Test"

## [0.11.0] - 2015-11-13

### Added

* Added: CHANGELOG link to package settings menu
* Added: Toggle No Coverage "--no-coverage" command
* Added: "phpunit.options" setting to allow configuring a default list of options for PHPUnit to use

## [0.10.1] - 2015-09-30

### Fixed

* Fixed: incorrect file path to settings when opening from the command palette

## [0.10.0] - 2015-09-30

### Added

* Added: "phpunit.development" setting to enable/disable plugin development utilities

### Changed

* Changed: settings are no longer loaded from a plugin specific settings file i.e. phpunit.sublime-settings

    There is, in my opinion, a bad practice of each and every plugin having its
    own settings file. This plugin no longer does this. All plugin settings are prefixed with the name of the plugin followed by a period i.e. "phpunit.".

    Settings are loaded in this order:

    1) Project Specific

    Example: Menu > Project > Edit Project

    ```
    {
        "settings": {
            "phpunit.save_all_on_run": true
        }
    }
    ```

    2) User

    Example: Menu > Preferences > Settings - User

    ```
    {
        "phpunit.save_all_on_run": true
    }
    ```

* Changed: "save_all_on_run" now only save files that exist on disk and have dirty buffers

    The reason for this change:

    When saving a file that doesn't exist on disk Sublime Text prompts with a "Save file" dialog, meanwhile the tests would run in the background anyways. We could prevent the tests from running until the user finishes handling the dialogs. If there is a desire for this please open an issue.

* Changed: renamed setting "phpunit.enable_keymaps" to "phpunit.keymaps"
* Changed: renamed setting "phpunit.enable_vi_keymaps" to "phpunit.keymaps"
* Changed: To enable vi keymaps both "phpunit.keymaps" and "phpunit.vi_keymaps" need to be set to true, previously only the vi_keymaps needed to be set to true

## [0.9.0] - 2015-07-06

### Added

* Added: "Open HTML Code Coverage in Browser" command #23
* Added: Switch and put class and test-case side-by-side #8

## [0.8.0] - 2015-06-18

### Added

* Added: Configurable color schemes #7
* Added: Colour scheme "Packages/phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme" #21
* Added: Colour scheme "Packages/phpunit/color-schemes/solarized-dark.hidden-tmTheme" #21

### Fixed

* Fixed: Command palette captions are now capitalised
* Fixed: Goto next/last failure now matches all files/line-numbers in stack traces

## [0.7.0] - 2015-06-11

### Added

* Added: License link to package settings menu

### Removed

* Removed: Several deprecated behaviours

## [0.6.0] - 2015-05-27

### Added

* Added: "PHPUnit: Cancel Test Run" to command palette
* Added: ST3 Requirements check. Now raises a runtime exception if trying to load in < Sublime Text 3

## [0.5.0] - 2015-05-16

### Added

* Added: "PHPUnit.." to "Tools" main menu #15 #16
* Added: "PHPUnit: Show Test Results" command
* Added: "Open "Preferences: PHPunit Settings - Default" command
* Added: "Open "Preferences: PHPunit Settings - User" command
* Added: Running the last test command is now saved per window #19

### Deprecated

* Deprecated: Per-project settings are now accessed via prefix "phpunit." in project definition settings. The old behaviour is deprecated and will be removed before the 1.0.0 beta releases.

### Removed

* Removed: "phpunit" command #31

### Fixed

* Fixed: Keymaps now display the default `ctrl+...` keymaps in command palette. Previously the Vintage/Vintageous keymaps were displayed.
* Fixed: error when there is no active window and/or view
* Fixed: test results not displaying colour when there are risky tests

## [0.4.0] - 2015-05-03

### Added

* Added: option to disable the default keymaps. To disable the keymaps set `"phpunit.enable_keymaps": false` the User Settings. Access this file from `Preferences > Settings - User` menu item. #30

## [0.3.0] - 2015-02-04

### Added

* Added: Can now run multiple test methods using a multiple selection #5
* Added: command palette toggle - report test progress TestDox format #24 #2
* Added: command palette toggle - report test progress TAP format #24 #28
* Added: Switching class-under-test/test-case now splits window into two views with both side-by-side *if* the current window only has one group.
* Added: Vintage/Vintageous keymaps can now be enabled in the preferences. They are disabled by default. To enable set `"phpunit.enable_vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

### Fixed

* Fixed: Can't switch classes beginning with an underscore #22
* Fixed: Running single test runs all tests with the same prefix #25
* Fixed: Some minor test result progress syntax highlighting bugs

## [0.2.0] - 2015-01-21

### Added

* Added: Composer installed PHPUnit support #13
* Added: Saving all files on run can now be disabled. It can also be set on a per-project basis #12
* Added: Command Palette commands #17
* Added: Package Settings menu "Preferences > Package Settings > PHPUnit" #14
* Added: Example Vintage/Vintageous keymaps in the default key bindings: "Preferences > Package Settings > PHPUnit > Key Bindings - Default" #10

### Changed

* Changed: Debug messages are now disabled by default. To enable debug messages set an environment variable to a non-blank value: `SUBLIME_PHPUNIT_DEBUG=yes`. To disable debug message set the variable to a blank value: `SUBLIME_PHPUNI_DEBUG=`. For example, on Linux Sublime Text can be opened at the Terminal with an exported environment variable: `export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text`. #6
* Changed: The last test run is now saved in memory for the current session, previously it was save to a file. #11
* Changed: Many refactorings including test runner commands are now Window commands, previously they were Text commands. There is no need for these commands to be instantiated for every view.

### Fixed

* Fixed: Test result progress highlighting was not displayed properly
* Fixed: Test result failures red background no longer matches trailing whitespace, previously the red background stretched the full width of the screen.

### 0.1.0 - 2015-01-07

* Initial import; PHPUnit support

[3.6.0]: https://github.com/gerardroche/sublime-phpunit/compare/3.5.1...3.6.0
[3.5.1]: https://github.com/gerardroche/sublime-phpunit/compare/3.5.0...3.5.1
[3.5.0]: https://github.com/gerardroche/sublime-phpunit/compare/3.4.0...3.5.0
[3.4.0]: https://github.com/gerardroche/sublime-phpunit/compare/3.3.0...3.4.0
[3.3.0]: https://github.com/gerardroche/sublime-phpunit/compare/3.2.2...3.3.0
[3.2.2]: https://github.com/gerardroche/sublime-phpunit/compare/3.2.1...3.2.2
[3.2.1]: https://github.com/gerardroche/sublime-phpunit/compare/3.2.0...3.2.1
[3.2.0]: https://github.com/gerardroche/sublime-phpunit/compare/3.1.1...3.2.0
[3.1.1]: https://github.com/gerardroche/sublime-phpunit/compare/3.1.0...3.1.1
[3.1.0]: https://github.com/gerardroche/sublime-phpunit/compare/3.0.0...3.1.0
[3.0.0]: https://github.com/gerardroche/sublime-phpunit/compare/2.5.0...3.0.0
[2.5.0]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.6...2.5.0
[2.4.6]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.5...2.4.6
[2.4.5]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.4...2.4.5
[2.4.4]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.3...2.4.4
[2.4.3]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.2...2.4.3
[2.4.2]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.1...2.4.2
[2.4.1]: https://github.com/gerardroche/sublime-phpunit/compare/2.4.0...2.4.1
[2.4.0]: https://github.com/gerardroche/sublime-phpunit/compare/2.3.0...2.4.0
[2.3.0]: https://github.com/gerardroche/sublime-phpunit/compare/2.2.2...2.3.0
[2.2.2]: https://github.com/gerardroche/sublime-phpunit/compare/2.2.1...2.2.2
[2.2.1]: https://github.com/gerardroche/sublime-phpunit/compare/2.2.0...2.2.1
[2.2.0]: https://github.com/gerardroche/sublime-phpunit/compare/2.1.0...2.2.0
[2.1.0]: https://github.com/gerardroche/sublime-phpunit/compare/2.0.3...2.1.0
[2.0.3]: https://github.com/gerardroche/sublime-phpunit/compare/2.0.2...2.0.3
[2.0.2]: https://github.com/gerardroche/sublime-phpunit/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/gerardroche/sublime-phpunit/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/gerardroche/sublime-phpunit/compare/1.2.1...2.0.0
[1.2.1]: https://github.com/gerardroche/sublime-phpunit/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/gerardroche/sublime-phpunit/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/gerardroche/sublime-phpunit/compare/1.0.3...1.1.0
[1.0.3]: https://github.com/gerardroche/sublime-phpunit/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/gerardroche/sublime-phpunit/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/gerardroche/sublime-phpunit/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/gerardroche/sublime-phpunit/compare/1.0.0-beta2...1.0.0
[1.0.0-beta2]: https://github.com/gerardroche/sublime-phpunit/compare/1.0.0-beta1...1.0.0-beta2
[1.0.0-beta1]: https://github.com/gerardroche/sublime-phpunit/compare/0.15.1...1.0.0-beta1
[0.15.1]: https://github.com/gerardroche/sublime-phpunit/compare/0.15.0...0.15.0
[0.15.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.14.1...0.15.0
[0.14.1]: https://github.com/gerardroche/sublime-phpunit/compare/0.14.0...0.14.1
[0.14.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.13.0...0.14.0
[0.13.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.12.0...0.13.0
[0.12.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.11.0...0.12.0
[0.11.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.10.1...0.11.0
[0.10.1]: https://github.com/gerardroche/sublime-phpunit/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.9.0...0.10.0
[0.9.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.8.0...0.9.0
[0.8.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.6.0...0.7.0
[0.6.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/gerardroche/sublime-phpunit/compare/0.1.0...0.2.0
