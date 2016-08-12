# gerardroche/sublime-phpunit

[![Author](https://img.shields.io/badge/author-@gerardroche-blue.svg?style=flat)](https://twitter.com/gerardroche) [![Source Code](https://img.shields.io/badge/source-GitHub-blue.svg?style=flat)](https://github.com/gerardroche/sublime-phpunit) [![License](https://img.shields.io/badge/license-BSD--3-blue.svg?style=flat)](https://raw.githubusercontent.com/gerardroche/sublime-phpunit/master/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat)](https://github.com/gerardroche/sublime-phpunit/stargazers)

[![Sublime version](https://img.shields.io/badge/sublime-v3-lightgrey.svg?style=flat)](https://sublimetext.com)
[![Latest version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?label=release&style=flat&maxAge=2592000)](https://github.com/gerardroche/sublime-phpunit/tags)
[![Downloads](https://img.shields.io/packagecontrol/dt/phpunitkit.svg?style=flat&maxAge=2592000)](https://packagecontrol.io/packages/phpunitkit)

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
2. Download or clone this repository to a directory named <tt>phpunitkit</tt> in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunitkit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunitkit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunitkit`
3. The features listed above will be available the next time Sublime Text is started.

## Commands

* PHPUnit: Run All Tests
* PHPUnit: Run Single Test
* PHPUnit: Run Last Test
* PHPUnit: Switch Test Case / Class Under Test
* PHPUnit: Toggle --tap option
* PHPUnit: Toggle --testdox option
* PHPUnit: Toggle --no-coverage option
* PHPUnit: Open HTML Code Coverage in Browser

## Key Bindings

OS X | Windows / Linux | Description
-----|-----------------|------------
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run all tests
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run tests
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Rerun last test run
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch test case / class under test
<kbd>F4</kbd> | <kbd>F4</kbd> | Goto to next test failure file line number
<kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Goto to previous test failure file line number

### Vintage / Vintageous

Vintage / Vintageous key bindings are disabled by default. See the [configuration](#configuration) section.

OS X / Windows / Linux | Description
-----------------------|------------
<kbd>,</kbd><kbd>t</kbd> | Run all tests
<kbd>,</kbd><kbd>r</kbd> | Run tests
<kbd>,</kbd><kbd>e</kbd> | Rerun last test run
<kbd>,</kbd><kbd>.</kbd> | Switch test case / class under test

## Configuration

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.options` | Options to pass to PHPUnit on test runs. All PHPUnit options are valid, see <tt>phpunit --help</tt> for an up-to-date list of available options. | `dict` | `{}`
`phpunit.keymaps` | Enable the default keymaps. | `boolean` | `true`
`phpunit.composer` | Enable composer support. If a composer installed PHPUnit is found then it is used to run tests. | `boolean` | `true`
`phpunit.vi_keymaps` | Enable the default vi keymaps. | `boolean` | `false`
`phpunit.save_all_on_run` | Enable writing out every buffer with changes and a file name, on test runs. | `boolean` | `true`

### User settings

`Preferences > Settings - User`

```json
{
    "phpunit.{Key}": "{Value}"
}
```

### Per-project settings

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.{Key}": "{Value}"
    }
}
```

#### Example

```json
{
    "settings": {
        "phpunit.options": {
            "no-coverage": true,
            "verbose": true
        },
        "phpunit.keymaps": true,
        "phpunit.composer": true,
        "phpunit.vi_keymaps": false,
        "phpunit.save_all_on_run": true
    }
}
```

## Contributing

Your issue reports and pull requests are welcome.

**Debug messages**

Debug messages are disabled by default. To enable them set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=y`. To disable them set unset it or set it to a blank value e.g. `SUBLIME_PHPUNIT_DEBUG=`.

On Linux, for example, Sublime Text can be started at the Terminal with an exported environment variable.

```
$ export SUBLIME_PHPUNIT_DEBUG=y; subl
```

**Running the tests**

Enable plugin development; set <tt>phpunit.development</tt> to <tt>true</tt>
and from the command palette run "PHPUnit: Run all Plugin Tests".

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
