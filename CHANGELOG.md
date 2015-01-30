# phpunit changelog

## 0.2.0

### Bug Fixes

* Test result progress highlighting was not displayed properly
* Test result failures red background no longer matches trailing whitespace, previously the red background stretched the full width of the screen.

### New Features

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

* Initial import
