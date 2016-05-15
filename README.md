# gerardroche/sublime-phpunit

A plugin for Sublime Text 3.

Provides decent PHPUnit support.

![Screenshot](screenshot.png)

**The plugin was recently renamed to "php_phpunit" and is now available on Package Control. So if you are having issues, then either remove your existing installtion and install via Package Control, making sure to install the phpunit package by me *PHP PHPUnit (gerardroche/sublime-phpunit)*, or rename your existing installation to "php_phpunit".**

For best results use with [PHP Grammar](https://github.com/gerardroche/sublime-php-grammar), [PHP Completions](https://packagecontrol.io/packages/PHP%20Completions%20Kit), and [PHP Snippets](https://packagecontrol.io/packages/php-snippets).

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

### Package Control installation

This is the preferred method of installation is via [Package Control](https://packagecontrol.io).

Search for "PHP PHPUnit" by me (gerardroche/sublime-phpunit).

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named `php_phpunit` in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/php_phpunit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/php_phpunit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/php_phpunit`
3. The features listed above will be available the next time Sublime Text is started.

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

**Vintage/Vintageous** key bindings are disabled by default. See the configuration for details on how to enable them.

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

The colour scheme to use for test results.

Type: `string|null`

Default: `Packages/php_phpunit/color-schemes/monokai.hidden-tmTheme`

The bundled schemes are:
* `Packages/php_phpunit/color-schemes/monokai.hidden-tmTheme`
* `Packages/php_phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme`
* `Packages/php_phpunit/color-schemes/solarized-dark.hidden-tmTheme`

Set to null for no colour scheme.

**phpunit.composer**

Enable/disable composer installed PHPUnit support.

Type: `bool`

Default: `true`

For example, if composer installed PHPUnit exists then it used as the command to run PHPUnit, otherwise defaults to the command "phpunit".

**phpunit.development**

Enable/disable the plugin development helpers.

Type: `bool`

Default: `false`

For example, when enabled a "PHPUnit: Run All Plugin Tests" command is added to the command palette.

*Note: This setting does nothing when installed using Package Control because plugin development helpers are excluded from the production build of the plugin.*

**phpunit.keymaps**

Enable/disable the default keymaps.

Type: `bool`

Default: `true`

**phpunit.options**

Default options to pass to PHPUnit.

Type: `dict`

Default: `{}`

Example

```
"phpunit.options": {
    "no-coverage": true,
    "testdox": true,
    "verbose": true
}
```

**phpunit.save_all_on_run**

Enable/disable saving all dirty views before running tests.

Type: `bool`

Default: `true`

**phpunit.vi_keymaps**

Enable/disable the default vi keymaps.

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

Enable plugin development mode (set `phpunit.development` to `true`) and run the "PHPUnit: Run all Plugin Tests" command from the command palette. See the configuration section for more details on configurations.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on [Sublime Text Ruby Tests](https://github.com/maltize/sublime-text-2-ruby-tests).

## License

Released under the [BSD 3-Clause License](LICENSE).
