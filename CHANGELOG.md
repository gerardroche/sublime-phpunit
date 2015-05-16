# sublime-phpunit changelog

## 0.5.0-next

### Bug Fixes

* Fixed error when there is no active window and/or view
* Fixed test results not displaying colour when there are risky tests
* Keymaps now display the default "ctrl+..." keymaps in command palette. Previously they displayed the Vintage/Vintageous keymaps.

### New Features / Enhancements

* Running the last test command is now saved per window #19
* Added PHPUnit to the Tools Menu #15 #16
* New in command palette:
    - Added "PHPUnit: Show Test Results"
    - Added open "Preferences: PHPunit Settings - Default"
    - Added open "Preferences: PHPunit Settings - User"

### Changes

* Removed command `phpunit_command` #31
* Per-project settings are now accessed via prefix `phpunit.` in project definition settings. The old behaviour is deprecated and will be removed before the 1.0.0 beta releases.

`Project > Edit Project`

    ```json
    {
        "settings": {
            "phpunit.save_all_on_run": false
        }
    }
    ```

## 0.4.0

### New Features / Enhancements

* Added option to disable the default keymaps. To disable the keymaps set `"phpunit.enable_keymaps": false` the User Settings. Access this file from `Preferences > Settings - User` menu item. #30

## 0.3.0

### Bug Fixes

* Can't switch classes beginning with an underscore #22
* Running single test runs all tests with the same prefix #25
* Some minor test result progress syntax highlighting bugs

### New Features / Enhancements

* Added run multiple tests using multiple selection #5
* Added report test execution progress command palette toggles #24
    - TestDox format #2
    - TAP format #28
* Switching class-under-test/test-case now splits window into two views with both side-by-side *if* the current window only has one group.
* Vintage/Vintageous keymaps can now be enabled in the preferences. They are disabled by default. To enable set `"phpunit.enable_vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

## 0.2.0

### Bug Fixes

* Test result progress highlighting was not displayed properly
* Test result failures red background no longer matches trailing whitespace, previously the red background stretched the full width of the screen.

### New Features / Enhancements

* Composer installed PHPUnit support #13
* Saving all files on run can now be disabled. It can also be set on a per-project basis #12
* Added Command Palette commands #17
* Added Package Settings menu: `Preferences > Package Settings > PHPUnit` #14
* Added example Vintage/Vintageous keymaps in the default key bindings: `Preferences > Package Settings > PHPUnit > Key Bindings - Default` #10

### Changes

* Debug messages are now disabled by default. To enable debug messages set an environment variable to a non-blank value: `SUBLIME_PHPUNIT_DEBUG=yes`. To disable debug message set the variable to a blank value: `SUBLIME_PHPUNI_DEBUG=`. For example, on Linux Sublime Text can be opened at the Terminal with an exported environment variable: `export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text`. #6
* The last test run is now saved in memory for the current session, previously it was save to a file. #11
* Many refactorings including:
    - Test runner commands are now Window commands, previously they were Text commands. There is no need for these commands to be instantiated for every view.

## 0.1.0

* Initial import; PHPUnit support
