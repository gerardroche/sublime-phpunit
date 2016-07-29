# gerardroche/sublime-phpunit

[![Author](https://img.shields.io/badge/author-@gerardroche-blue.svg?style=flat)](https://twitter.com/gerardroche) [![Source Code](https://img.shields.io/badge/source-GitHub-blue.svg?style=flat)](https://github.com/gerardroche/sublime-phpunit) [![License](https://img.shields.io/badge/license-BSD--3-blue.svg?style=flat)](https://raw.githubusercontent.com/gerardroche/sublime-phpunit/master/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat)](https://github.com/gerardroche/sublime-phpunit/stargazers)
[![Sublime version](https://img.shields.io/badge/sublime-v3-lightgrey.svg?style=flat)](http://sublimetext.com) [![Latest version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?maxAge=2592000?style=flat&label=release)](https://github.com/gerardroche/sublime-phpunit/tags) [![Downloads](https://img.shields.io/packagecontrol/dt/phpunitkit.svg?maxAge=2592000?style=flat)](https://packagecontrol.io/packages/phpunitkit)

PHPUnit support for Sublime Text.

![Screenshot](screenshot.png)

Works best with [PHP Grammar], [PHP Completions], [PHP Snippets], [PHPUnit Completions], and [PHPUnit Snippets].

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

* Run test suite
* Run test case
* Run test
* Run multiple tests
* Run test case for current class
* Rerun last test
* Jump to next or previous failure file line number
* Switch, split, and focus on test case and class under test
* Colour test results (including failure diffs)
* Composer installed PHPUnit aware

## Installation

The preferred method of installation is [Package Control]. Search for "phpunitkit".

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named `phpunitkit` in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunitkit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunitkit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunitkit`
3. The features listed above will be available the next time Sublime Text is started.

## Commands

* `PHPUnit: Run All Tests`
* `PHPUnit: Run Single Test`
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
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run tests
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Rerun last test run
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch test case / class under test
<kbd>F4</kbd> | <kbd>F4</kbd> | Goto to next test failure file line number
<kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Goto to previous test failure file line number

**Vintage/Vintageous** key bindings are disabled by default. See the [configuration](#configuration) section for how to enable them.

OS X / Windows / Linux | Description
-----------------------|------------
<kbd>,</kbd><kbd>t</kbd> | Run all tests
<kbd>,</kbd><kbd>r</kbd> | Run tests
<kbd>,</kbd><kbd>e</kbd> | Rerun last test run
<kbd>,</kbd><kbd>.</kbd> | Switch test case / class under test

## Configuration

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.color_scheme` | *Colour scheme to use for test results.* | `string|null` | `monokai`
`phpunit.composer` | *Enable/disable composer installed PHPUnit support. If a composer installed PHPUnit exists then it will be used command to run tests, otherwise assumes phpunit is available on the system path.* | `boolean` | `true`
`phpunit.keymaps` | *Enable/disable the default keymaps.* | `boolean` | `true`
`phpunit.options` | *Options to pass to PHPUnit when running tests.* | `dict` | `{}`
`phpunit.save_all_on_run` | *Enable/disable saving all dirty views before running tests.* | `boolean` | `true`
`phpunit.vi_keymaps` | *Enable/disable the default vi keymaps.* | `boolean` | `false`

The bundled `phpunit.color_scheme`'s are:

* `Packages/phpunitkit/color-schemes/monokai.hidden-tmTheme`
* `Packages/phpunitkit/color-schemes/monokai-extended-seti.hidden-tmTheme`
* `Packages/phpunitkit/color-schemes/solarized-dark.hidden-tmTheme`

**Example `phpunit.options`**

```
    "phpunit.options": {
        "no-coverage": true,
        "testdox": true,
        "verbose": true
    }
```

**Per-project settings**

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.options": {
            "no-coverage": true
        },
        "phpunit.save_all_on_run": false
    }
}
```

**User settings**

`Preferences > Settings - User`

```json
{
    "phpunit.options": {
        "no-coverage": true
    },
    "phpunit.save_all_on_run": false
}
```

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

[Package Control]: https://packagecontrol.io/search/phpunitkit
[PHP Completions]: https://packagecontrol.io/packages/PHP%20Completions%20Kit
[PHP Grammar]: https://packagecontrol.io/packages/php-grammar
[PHP Snippets]: https://packagecontrol.io/packages/php-snippets
[PHPUnit Completions]: https://github.com/gerardroche/sublime-phpunit-completions
[PHPUnit Snippets]: https://github.com/gerardroche/sublime-phpunit-snippets
[PHPUnit]: https://github.com/gerardroche/sublime-phpunit
