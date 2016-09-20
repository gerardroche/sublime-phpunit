# phpunitkit

[![Author](https://img.shields.io/badge/author-@gerardroche-blue.svg?style=flat)](https://twitter.com/gerardroche)
[![Source Code](https://img.shields.io/badge/source-GitHub-blue.svg?style=flat)](https://github.com/gerardroche/sublime-phpunit)
[![License](https://img.shields.io/badge/license-BSD--3-blue.svg?style=flat)](https://raw.githubusercontent.com/gerardroche/sublime-phpunit/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat)](https://github.com/gerardroche/sublime-phpunit/stargazers)

[![Sublime version](https://img.shields.io/badge/sublime-v3-lightgrey.svg?style=flat)](https://sublimetext.com)
[![Latest version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?label=release&style=flat&maxAge=2592000)](https://github.com/gerardroche/sublime-phpunit/tags)
[![Downloads](https://img.shields.io/packagecontrol/dt/phpunitkit.svg?style=flat&maxAge=2592000)](https://packagecontrol.io/packages/phpunitkit)

[PHPUnit](https://phpunit.de) support for [Sublime Text](https://sublimetext.com). It provides an abstraction over running tests from the command-line. Works best alongside [PHP Grammar], [PHP Completions], and [PHP Snippets].

![Screenshot](screenshot.png)

## Overview

* [Features](#features)
* [Commands](#commands)
* [Key Bindings](#key-bindings)
* [Configuration](#configuration)
* [Installation](#installation)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## Features

* Zero configuration required; Does the Right Thing™
* Fully customized CLI options configuration
* Run test suite
* Run single test case
* Run single test (test case methods named `test*`)
* Run multiple tests (using multiple selections)
* Run test case for current class under test
* Rerun last test(s)
* Supports [Composer]
* Test results output in color (including color failure diffs)
* Jump to next / previous failure (navigates to file line number of failure)
* Switch, split, and focus test case &amp; class under test

## Commands

* PHPUnit: Run All Tests
* PHPUnit: Run Last Test
* PHPUnit: Run Single Test
* PHPUnit: Toggle --tap option
* PHPUnit: Toggle --testdox option
* PHPUnit: Toggle --no-coverage option
* PHPUnit: Open HTML Code Coverage in Browser
* PHPUnit: Switch Test Case / Class Under Test

## Key Bindings

OS X | Windows / Linux | Description
-----|-----------------|------------
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run single test case or test(s)
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run test suite
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Rerun last test(s)
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch, split, and focus test case &amp; class under test
<kbd>F4</kbd> | <kbd>F4</kbd> | Jump to next failure
<kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Jump to previous failure

### Vintage / Vintageous

Disabled by default.

OS X / Windows / Linux | Description
-----------------------|------------
<kbd>,</kbd><kbd>r</kbd> | Run single test case or test(s)
<kbd>,</kbd><kbd>t</kbd> | Run test suite
<kbd>,</kbd><kbd>e</kbd> | Rerun last test(s)
<kbd>,</kbd><kbd>.</kbd> | Switch, split, and focus test case &amp; class under test

## Configuration

phpunitkit goes to great lengths to predict how to invoke PHPUnit for the project environment.

For example, if PHPUnit is installed via [Composer] for the current project then the PHPUnit command-line test runner is invoked through `vendor/bin/phpunit`, otherwise it is assumed PHPUnit is available on the system path and so is invoked via `phpunit`.

Another example is, if `phpunit.xml` or `phpunit.xml.dist` (in that order) is found in the current or the nearest common ancestor directory of the active view, the location is set as the current working directory when invoking PHPUnit and so the configuration will be automatically read by PHPunit. Placing PHPUnit configuration files at the root of a project is highly recommended.

### Specifying PHPUnit Command-Line Options

Most configurations you might want to specify when invoking PHPUnit are probably best set in the [configuration](https://phpunit.de/manual/current/en/appendixes.configuration.html) file which is automatically read by PHPUnit.

> If `phpunit.xml` or `phpunit.xml.dist` (in that order) exist in the current working directory and `--configuration` is not used, the configuration will be automatically read from that file. &mdash; [PHPUnit Manual](https://phpunit.de/manual/current/en/textui.html)

See [`phpunit --help`](https://phpunit.de/manual/current/en/textui.html#textui.clioptions) for a up-to-date list of PHPUnit command-line options.

For example, rather than specifying PHPUnit options via sublime text settings, configure PHPUnit via its XML configuration file.

#### Example &mdash; Not So Good

```json
{
    "settings": {
        "phpunit.options": {
            "no-coverage": true,
            "verbose": true,
            "stop-on-error": true,
            "d": "xdebug.scream=0"
        }
    }
}
```

#### Example &mdash; Good

```
<phpunit verbose="true"
         stopOnError="true">

    <ini name="xdebug.scream" value="0" />

    <!--
    Comment out the code coverage configurations i.e. --no-coverage
    <logging>
        <log type="coverage-html" target="build/coverage" />
    </logging>
    -->

</phpunit>
```

There are session toggles for settings you might want to enable and disable on the fly like toggle `--no-coverage`, `--tap` and `--textdox`. See [Commands](#commands) for up-to-date list of available toggles.

### Settings

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.options` | Command-line options to pass to PHPUnit. See [`phpunit --help`](https://phpunit.de/manual/current/en/textui.html#textui.clioptions) for an up-to-date list of command-line options. | `dict` | `{}`
`phpunit.keymaps` | Enable the default keymaps. | `boolean` | `true`
`phpunit.composer` | Enable [Composer] support. If a composer installed PHPUnit is found then it is used to run tests. | `boolean` | `true`
`phpunit.vi_keymaps` | Enable the default vi keymaps. | `boolean` | `false`
`phpunit.save_all_on_run` | Enable writing out every buffer with changes and a file name, on test runs. | `boolean` | `true`

#### User Settings

`Preferences > Settings - User`

```json
{
    "phpunit.{Key}": "{Value}"
}
```

#### Per-Project Settings

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.{Key}": "{Value}"
    }
}
```

## Installation

Works best alongside [PHP Grammar], [PHP Completions], and [PHP Snippets].

### Package Control installation

The preferred method of installation is [Package Control].

### Manual Installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named **`phpunitkit`** in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunitkit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunitkit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunitkit`
3. Done!

## Contributing

Your issue reports and pull requests are welcome.

### Debug messages

Debug messages are disabled by default. To enable them set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=y`. To disable them set unset it or set it to a blank value e.g. `SUBLIME_PHPUNIT_DEBUG=`.

For more information on environment variables read [What are PATH and other environment variables, and how can I set or use them?](http://superuser.com/questions/284342/what-are-path-and-other-environment-variables-and-how-can-i-set-or-use-them)

#### Example &mdash; Linux

Sublime Text can be started at the Terminal with an exported environment variable.

```
$ export SUBLIME_PHPUNIT_DEBUG=y; subl
```

To set the environment permanently set it in `~/.profile` (requires restart).

```
export SUBLIME_PHPUNIT_DEBUG=y
```

Alternatively, create a [debug script (subld)](https://github.com/gerardroche/dotfiles/blob/1a27abed589f2fea9126a0496ef4d1cae0479722/src/bin/subld) with debugging environment variables enabled.

#### Example &mdash; Windows

Sublime Text can be started at the Command Prompt with an exported environment variable.

```
> set SUBLIME_PHPUNIT_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"
```

To set the environment permanently set it as a *system* environment variable (requires restart).

1. Control Panel > System and Security > System > Advanced system settings
2. Advanced > Environment Variables
3. System variables > New...
4. Add Variable name `SUBLIME_PHPUNIT_DEBUG` with Variable value `y`
5. Restart

### Running tests

To be able to run the tests enable plugin development. This will make the command "PHPUnit: Run all Plugin Tests" available in the Command Palette.

Preferences > Settings - User

```
{
    "phpunit.development": true
}
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests) and [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit).

## License

Released under the [BSD 3-Clause License](LICENSE).

[Package Control]: https://packagecontrol.io/browse/authors/gerardroche
[PHP Grammar]: https://packagecontrol.io/browse/authors/gerardroche
[PHP Completions]: https://packagecontrol.io/browse/authors/gerardroche
[PHP Snippets]: https://packagecontrol.io/browse/authors/gerardroche
[PHPUnit]: https://packagecontrol.io/browse/authors/gerardroche
[Composer]: https://getcomposer.org
