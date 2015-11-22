# gerardroche/sublime-phpunit-test-runner

A plugin for Sublime Text.

Provides decent PHPUnit support.

**Sublime Text 3 only**

![Screenshot](screenshot.png)

## Overview

* [Features](#features)
* [Installation](#installation)
* [Commands](#commands)
* [Key Bindings](#key-bindings)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## Features

* Run all tests
* Run a single test case
* Run a single test case method
* Run specific test case methods
* Run the test case for current class under test
* Rerun the last test run
* Jump to next or previous failure file line number
* Switch, split, and focus on test case and class under test
* Test result output in colour (including failure diffs)
* Composer installed PHPUnit aware

## Installation

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named `phpunit` in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunit`
3. Restart Sublime Text to complete installation. The features listed above should now be available.

## Commands

* `PHPUnit: Run All Tests`
* `PHPUnit: Run Single Test` *(context dependent)*
* `PHPUnit: Run Last Test`
* `PHPUnit: Switch Test Case / Class Under Test`
* `PHPUnit: Toggle --tap option`
* `PHPUnit: Toggle --testdox option`
* `PHPUnit: Toggle --no-coverage option`
* `PHPUnit: Open HTML Code Coverage in Browser`

## Key Bindings

OS X | Windows / Linux | Description
-----|-----------------|------------
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run all tests
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run tests *(context dependent)*
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Rerun last test run
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch test case / class under test
<kbd>F4</kbd> | <kbd>F4</kbd> | Goto to next test failure file line number
<kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Goto to previous test failure file line number

Keymaps are enabled by default. To disable them set `"phpunit.keymaps": false` in User Settings. Access this file from `Preferences > Settings - User` menu item.

Vintage/Vintageous keymaps are disabled by default. To enable them set `"phpunit.vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

OS X / Windows / Linux | Description
-----------------------|------------
<kbd>,</kbd><kbd>t</kbd> | Run all tests
<kbd>,</kbd><kbd>r</kbd> | Run tests *(context dependent)*
<kbd>,</kbd><kbd>e</kbd> | Rerun last test run
<kbd>,</kbd><kbd>.</kbd> | Switch test case / class under test

## Configuration

### User settings

`Preferences > Settings - User`

```json
{
    "phpunit.save_all_on_run": false
}
```

### Per-project settings

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.save_all_on_run": false
    }
}
```

### Settings

**phpunit.color_scheme**

Type: `string|null`

Default: `Packages/phpunit/color-schemes/monokai.hidden-tmTheme`

The colour scheme to use for test results.

Set to null for no colour scheme.

The bundled schemes are:

* `Packages/phpunit/color-schemes/monokai.hidden-tmTheme`
* `Packages/phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme`
* `Packages/phpunit/color-schemes/solarized-dark.hidden-tmTheme`

**phpunit.development**

Type: `bool`

Default: `false`

Enables/disables plugin development helper utilities. For example, when enabled a "PHPUnit: Run All Plugin Tests" command is added to the command palette.

*Note: This setting does nothing when installed with Package Control.*

**phpunit.keymaps**

Type: `bool`

Default: `true`

**phpunit.options**

Type: `dict`

Default: `{}`

A default list of options to pass to PHPUnit.

```
    "phpunit.options": {
        "no-coverage": true,
        "testdox": true,
        "verbose": true
    }
```

**phpunit.save_all_on_run**

Type: `bool`

Default: `true`

**phpunit.vi_keymaps**

Type: `bool`

Default: `false`

## Contributing

Your issue reports and pull requests are always welcome.

**Debug messages**

Debug messages are disabled by default. To enable them set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=y`. To disable them set unset it or set it to a blank value e.g. `SUBLIME_PHPUNIT_DEBUG=`.

On Linux, for example, Sublime Text can be started at the Terminal with an exported environment variable.

```
$ export SUBLIME_PHPUNIT_DEBUG=y; ~/sublime_text_3/sublime_text
```

**Running the tests**

Enable plugin development mode. Set `phpunit.development` to `true` and run the command "PHPUnit: Run all Plugin Tests" using the command palette. See the configuration section for more details on configurations.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on [Sublime Text Ruby Tests](https://github.com/maltize/sublime-text-2-ruby-tests).

## License

Released under the [BSD 3-Clause License](LICENSE).
