# PHPUnitKit [![Build Status](https://img.shields.io/travis/gerardroche/sublime-phpunit/master.svg?style=flat-square)](https://travis-ci.org/gerardroche/sublime-phpunit) [![Build status](https://img.shields.io/appveyor/ci/gerardroche/sublime-phpunit/master.svg?style=flat-square)](https://ci.appveyor.com/project/gerardroche/sublime-phpunit/branch/master) [![Coverage Status](https://img.shields.io/coveralls/gerardroche/sublime-phpunit/master.svg?style=flat-square)](https://coveralls.io/github/gerardroche/sublime-phpunit?branch=master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Latest Stable Version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?style=flat-square&label=stable)](https://github.com/gerardroche/sublime-phpunit/tags) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat-square)](https://github.com/gerardroche/sublime-phpunit/stargazers) [![Downloads](https://img.shields.io/packagecontrol/dt/PHPUnitKit.svg?style=flat-square)](https://packagecontrol.io/packages/PHPUnitKit)

A Sublime Text plugin that provides an abstraction over running PHPUnit tests from the command-line.

![Screenshot](screenshot.png)

## Overview

* [Features](#features)
* [Installation](#installation)
* [Commands](#commands)
* [Keybindings](#key-bindings)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## Features

* Run Nearest Test
* Run Test File
* Run Test Suite
* Run Last Test
* Supports Composer
* Supported by the [Test](https://github.com/gerardroche/sublime-test) plugin
* Zero configuration required; Does the Right Thing
* Supports colour results (including diffs)
* Fully customized CLI options configuration
* Jump to next and jump to previous failure
* Switch Test File (splits window and puts test case and class under test side by side)

## Installation

### Package Control installation

The preferred method of installation is Package Control ([Search for PHPUnitKit](https://packagecontrol.io/browse/authors/gerardroche)).

### Manual installation

Close Sublime Text, then download or clone this repository to a directory named `PHPUnitKit` in the Sublime Text Packages directory for your platform:

* Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/PHPUnitKit`
* OSX: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/PHPUnitKit`
* Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/PHPUnitKit`

## Commands

Command Palette | Command | Description
--------------- | ------- | -----------
`:TestSuite` | `phpunit_test_suite` | Run test suite of the current file.
`:TestFile` | `phpunit_test_file` | Run tests for the current file. If the current file is not a test file, it runs tests of the test file for the current file.
`:TestNearest` | `phpunit_test_nearest` | Run a test nearest to the cursor (supports multiple selections). If the current file is not a test file, it runs tests of the test file for the current file.
`:TestLast` | `phpunit_test_last` | Run the last test.
`:TestVisit` | `phpunit_test_visit` | Open the last run test in the current window (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests).
`:TestSwitch` | `phpunit_test_switch` | Splits the window and puts nearest test case and class under test side by side.
`:TestResults` | `phpunit_test_results` | Show the test results panel.
`:TestCancel` | `phpunit_test_cancel` | Cancels current test run.
`:TestCoverage` | `phpunit_test_coverage` | Open code coverage in browser.
`:ToggleOption`| `phpunit_toggle_option`  | Toggle PHPUnit CLI options.

## Key Bindings

Add your preferred key bindings: `Menu > Preferences > Key Bindings`

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

Other key bindings (provided out-of-the-box by Sublime Text):

Key | Description
--- | -----------
`F4` | Jump to Next Failure
`Shift+F4` | Jump to Previous Failure

**See the [Test](https://github.com/gerardroche/sublime-test) plugin to unify test plugin key bindings.**

## Configuration

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.options` | A hash of command-line options to pass through to PHPUnit. | `dict` | `{}`
`phpunit.composer` | Use the Composer installed PHPUnit executable (if it exists), otherwise the system PATH is used to find the PHPUnit executable. If disabled, then any Composer installed PHPUnit executable is ignored. | `boolean` | `true`
`phpunit.save_all_on_run` | Write out every buffer (in the active window), that has changes, before running tests. | `boolean` | `true`
`phpunit.php_executable` | The PHP executable used to run PHPUnit. The default is to use the executable found on the system PATH. | `string` | The PHP executable found on the system PATH.
`phpunit.php_versions_path` | Location of `.php-version` file PHP versions. | `string` | `~/.phpenv/versions`

### phpunit.options

A hash of command-line options to pass through to PHPUnit.

Global: `Menu > Preferences > Settings`

```json
{
    "phpunit.options": {
        "verbose": true,
        "no-coverage": true,
        "d": [
            "display_errors=1",
            "xdebug.scream=0"
        ]
    }
}
```

Or per-project: `Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.options": {
            "verbose": true,
            "no-coverage": true,
            "d": [
                "display_errors=1",
                "xdebug.scream=0"
            ]
        }
    }
}
```

Both of the above configurations will expand as follows:

```
phpunit -d "display_errors=1" -d "xdebug.scream=0" --verbose --no-coverage
```

### phpunit.composer

Use the Composer installed PHPUnit executable (if it exists), otherwise the system PATH is used to find the PHPUnit executable. If disabled, then any Composer installed PHPUnit executable is ignored.

Global: `Menu > Preferences > Settings`

```json
{
    "phpunit.composer": true
}
```

Or per-project: `Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.composer": true
    }
}
```

### phpunit.save_all_on_run

Write out every buffer (in the active window), that has changes, before running tests.

Global: `Menu > Preferences > Settings`

```json
{
    "phpunit.save_all_on_run": true
}
```

Or per-project: `Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.save_all_on_run": true
    }
}
```

### phpunit.php_executable

The PHP executable used to run PHPUnit. The default is to use the executable found on the system PATH.

All environment variables and user place-holders are expanded e.g. `~` and `$HOME` will expand to the user home directory.

Global: `Menu > Preferences > Settings`

```json
{
    "phpunit.php_executable": "~/.phpenv/versions/7.3.0/bin/php"
}
```

Or per-project: `Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.php_executable": "~/.phpenv/versions/7.3.0/bin/php"
    }
}
```

### phpunit.php_versions_path

You can set a location to find different PHP versions and use `.php-version` files to select versions per-project.

The default location is `~/.phpenv/versions`.

The structure of the versions directory should be in the following form:

```
Linux and OSX                       Windows
└── .phpenv                         └── .phpenv
    └── versions                        └── versions
        ├── 7.0.18                          ├── 7.0.18
        │   └── bin                         │   └── php
        │       └── php                     │ 
        ├── 7.1.4                           ├── 7.1.4
        │   └── bin                         │   └── php
        │       └── php                     │
        └── 7.x                             └── 7.x
            └── bin                             └── php
                └── php
```

To specify a version, create a file named `.php-version` with the version as its contents, and place it in the root of your project.

For example, a `.php-version` file with the contents `7.1.4` and a PHP versions path of `~/.phpenv/versions`, will expand to the PHP version at `~/.phpenv/versions/7.1.4/bin/php` on Linux and OSX, and `~/.phpenv/versions/7.1.4/php` on Windows.

`Menu > Preferences > Settings`

```json
{
    "phpunit.php_versions_path": "~/.phpenv/versions"
}
```

`Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.php_versions_path": "~/.phpenv/versions"
    }
}
```

## Contributing

Your issue reports and pull requests are welcome.

### Testing

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input **PHPUnitKit** as the package to test.

### Debugging

Debug messages are disabled by default. To enable them set the environment variable SUBLIME_PHPUNIT_DEBUG to a non-blank value. Debug messages are output to the Console (not the tests results output panel). Open the console via `Menu > View > Console` or click the icon in the bottom right of the status bar.

Below are detailed explanations on how to set environment variables for each OS. For more information on environment variables read [What are PATH and other environment variables, and how can I set or use them?](http://superuser.com/questions/284342/what-are-path-and-other-environment-variables-and-how-can-i-set-or-use-them).

#### Linux

Sublime Text can be started at the Terminal with an exported environment variable.

```
$ export SUBLIME_PHPUNIT_DEBUG=y; subl
```

Alternatively, create a [script](https://github.com/gerardroche/dotfiles/blob/1a27abed589f2fea9126a0496ef4d1cae0479722/src/bin/subld).

#### Windows

Sublime Text can be started at the Command Prompt with an exported environment variable.

```
> set SUBLIME_PHPUNIT_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on, and inspired by, [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests), [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit), and [janko-m/vim-test](https://github.com/janko-m/vim-test).

## License

Released under the [BSD 3-Clause License](LICENSE).
