# phpunitkit changelog

## Unreleased

* Fixed [#40](https://github.com/gerardroche/sublime-phpunit/issues/40): Cannot specify short Command-Line Options

## [1.0.1]

* Fixed [#43](https://github.com/gerardroche/sublime-phpunit/issues/43): Cannot run Composer installed PHPUnit on Windows

## [1.0.0]

* README cleanup for 1.0.0 release

## [1.0.0-beta2]

* README cleanup for 1.0.0 release

## [1.0.0-beta1]

* README cleanup for 1.0.0 release

## [0.15.1]

* Fixed: README typos

## [0.15.0]

* Changed: plugin name from "php_phpunit" to "phpunitkit". The plugin was renamed because the last name was rejected by the Package Control channel.
  - If you previously installed manually then remove the installation and install via Package Control. Search for phpunitkit.
  - If you prefer to keep your manual installation then rename or move your installation to "phpunitkit".

## [0.14.1]

* Fixed [#35](https://github.com/gerardroche/sublime-phpunit/issues/35): Cannot run "Run Single Test" with the latest build of Sublime Text (build 3114)

## [0.14.0]

* Added: Now available on Package Control
* Changed: Renamed package from "phpunit" to "php_phpunit". This was needed in order to provide the plugin via Package Control. If you are having issues then either remove your existing plugin installation and install via Package Control, making sure to install the plugin by me, PHP PHPUnit (gerardroche), or rename your existing installation to "phpunit".

## [0.13.0]

* Added [#34](https://github.com/gerardroche/sublime-phpunit/issues/34): Option to disable composer support (phpunit.composer). Defaults to true.

## [0.12.0]

* Changed: switch file command caption is now "PHPUnit: Switch Test Case / Class Under Test"
* Refactorings

## [0.11.0]

* Added: CHANGELOG link to package settings menu
* Added: Toggle No Coverage "--no-coverage" command
* Added: "phpunit.options" setting to allow configuring a default list of options for PHPUnit to use

## [0.10.1]

* Fixed: incorrect file path to settings when opening from the command palette

## [0.10.0]

* Added: "phpunit.development" setting to enable/disable plugin development utilities
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
* Minor refactorings
* Minor fixes

## [0.9.0]

* Added: "Open HTML Code Coverage in Browser" command #23
* Added: Switch and put class and test-case side-by-side #8

## [0.8.0]

* Added: Configurable color schemes #7
* Added: Colour scheme "Packages/phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme" #21
* Added: Colour scheme "Packages/phpunit/color-schemes/solarized-dark.hidden-tmTheme" #21
* Fixed: Command palette captions are now capitalised
* Fixed: Goto next/last failure now matches all files/line-numbers in stack traces

## [0.7.0]

* Removed: Several deprecated behaviours
* Added: License link to package settings menu

## [0.6.0]

* Added: "PHPUnit: Cancel Test Run" to command palette
* Added: ST3 Requirements check. Now raises a runtime exception if trying to load in < Sublime Text 3

## [0.5.0]

* Added: "PHPUnit.." to "Tools" main menu #15 #16
* Added: "PHPUnit: Show Test Results" command
* Added: "Open "Preferences: PHPunit Settings - Default" command
* Added: "Open "Preferences: PHPunit Settings - User" command
* Added: Running the last test command is now saved per window #19
* Fixed: Keymaps now display the default `ctrl+...` keymaps in command palette. Previously the Vintage/Vintageous keymaps were displayed.
* Fixed: error when there is no active window and/or view
* Fixed: test results not displaying colour when there are risky tests
* Removed: "phpunit" command #31
* Deprecated: Per-project settings are now accessed via prefix "phpunit." in project definition settings. The old behaviour is deprecated and will be removed before the 1.0.0 beta releases.

## [0.4.0]

* Added: option to disable the default keymaps. To disable the keymaps set `"phpunit.enable_keymaps": false` the User Settings. Access this file from `Preferences > Settings - User` menu item. #30

## [0.3.0]

* Fixed: Can't switch classes beginning with an underscore #22
* Fixed: Running single test runs all tests with the same prefix #25
* Fixed: Some minor test result progress syntax highlighting bugs
* Added: Can now run multiple test methods using a multiple selection #5
* Added: command palette toggle - report test progress TestDox format #24 #2
* Added: command palette toggle - report test progress TAP format #24 #28
* Added: Switching class-under-test/test-case now splits window into two views with both side-by-side *if* the current window only has one group.
* Added: Vintage/Vintageous keymaps can now be enabled in the preferences. They are disabled by default. To enable set `"phpunit.enable_vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

## [0.2.0]

* Added: Composer installed PHPUnit support #13
* Added: Saving all files on run can now be disabled. It can also be set on a per-project basis #12
* Added: Command Palette commands #17
* Added: Package Settings menu "Preferences > Package Settings > PHPUnit" #14
* Added: Example Vintage/Vintageous keymaps in the default key bindings: "Preferences > Package Settings > PHPUnit > Key Bindings - Default" #10
* Fixed: Test result progress highlighting was not displayed properly
* Fixed: Test result failures red background no longer matches trailing whitespace, previously the red background stretched the full width of the screen.
* Changed: Debug messages are now disabled by default. To enable debug messages set an environment variable to a non-blank value: `SUBLIME_PHPUNIT_DEBUG=yes`. To disable debug message set the variable to a blank value: `SUBLIME_PHPUNI_DEBUG=`. For example, on Linux Sublime Text can be opened at the Terminal with an exported environment variable: `export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text`. #6
* Changed: The last test run is now saved in memory for the current session, previously it was save to a file. #11
* Changed: Many refactorings including test runner commands are now Window commands, previously they were Text commands. There is no need for these commands to be instantiated for every view.

### 0.1.0

* Initial import; PHPUnit support

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
