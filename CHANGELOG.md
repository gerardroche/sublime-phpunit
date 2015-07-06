# sublime-phpunit changelog

## 0.9.0 (upcoming)

* Added: "Open HTML Code Coverage in Browser" command #23
* Added: Switch and put class and test-case side-by-side #8

## 0.8.0

* Added: Configurable color schemes #7
* Added: Colour scheme "Packages/phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme" #21
* Added: Colour scheme "Packages/phpunit/color-schemes/solarized-dark.hidden-tmTheme" #21
* Fixed: Command palette captions are now capitalised
* Fixed: Goto next/last failure now matches all files/line-numbers in stack traces

## 0.7.0

* Removed: Several deprecated behaviours
* Added: License link to package settings menu

## 0.6.0

* Added: "PHPUnit: Cancel Test Run" to command palette
* Added: ST3 Requirements check. Now raises a runtime exception if trying to load in < Sublime Text 3

## 0.5.0

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

## 0.4.0

* Added: option to disable the default keymaps. To disable the keymaps set `"phpunit.enable_keymaps": false` the User Settings. Access this file from `Preferences > Settings - User` menu item. #30

## 0.3.0

* Fixed: Can't switch classes beginning with an underscore #22
* Fixed: Running single test runs all tests with the same prefix #25
* Fixed: Some minor test result progress syntax highlighting bugs
* Added: Can now run multiple test methods using a multiple selection #5
* Added: command palette toggle - report test progress TestDox format #24 #2
* Added: command palette toggle - report test progress TAP format #24 #28
* Added: Switching class-under-test/test-case now splits window into two views with both side-by-side *if* the current window only has one group.
* Added: Vintage/Vintageous keymaps can now be enabled in the preferences. They are disabled by default. To enable set `"phpunit.enable_vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

## 0.2.0

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

## 0.1.0

* Initial import; PHPUnit support
