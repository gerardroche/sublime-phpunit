# PHPUnitKit

A Sublime Text wrapper for running tests on different granularities.

[![Build Status](https://img.shields.io/travis/gerardroche/sublime-phpunit/master.svg?style=flat-square)](https://travis-ci.org/gerardroche/sublime-phpunit) [![Build status](https://img.shields.io/appveyor/ci/gerardroche/sublime-phpunit/master.svg?style=flat-square)](https://ci.appveyor.com/project/gerardroche/sublime-phpunit/branch/master) [![Coverage Status](https://img.shields.io/coveralls/gerardroche/sublime-phpunit/master.svg?style=flat-square)](https://coveralls.io/github/gerardroche/sublime-phpunit?branch=master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Latest Stable Version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?style=flat-square&label=stable)](https://github.com/gerardroche/sublime-phpunit/tags) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat-square)](https://github.com/gerardroche/sublime-phpunit/stargazers) [![Downloads](https://img.shields.io/packagecontrol/dt/PHPUnitKit.svg?style=flat-square)](https://packagecontrol.io/packages/PHPUnitKit)

![Screenshot](screenshot.png)

## Features

* Run Test File
* Run Test Suite
* Run Nearest Test
* Run Last Test
* Fully customisable configuration
* Supports Composer installed PHPUnit
* Supports colour results, diffs, errors, etc.
* Jump to next and jump to previous failure

## Installation

### Package Control installation

The preferred method of installation is [Package Control](https://packagecontrol.io/packages/PHPUnitKit).

### Manual installation

Close Sublime Text, then download or clone the [repository](https://github.com/gerardroche/sublime-phpunit) to a directory named **PHPUnitKit** in the Sublime Text **Packages directory** for your platform:

OS | Command
-- | -----
Linux | `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/PHPUnitKit`
OSX | `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/PHPUnitKit`
Windows | `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/PHPUnitKit`

## Commands

These commands are available through the Command Palette. To use the command palette. To use the command palette:

1. Press `Ctrl+Shift+p` (Win, Linux) or `Cmd+Shift+p` (OS X)
2. Select a command (all PHPUnitKit commands begin with **PHPUnit:**)
3. Press `Enter` to run the command

command | description
------- | -----------
`TestSuite` | Runs the whole test suite (if the current file is a test file, runs that framework's test suite).
`TestFile` | In a test file runs all tests in the current file, otherwise runs that file's tests.
`TestNearest` | In a test file runs the test nearest to the cursor, otherwise runs that file's tests.
`TestLast` | Runs the last test.
`TestVisit` | Visits the test file from which you last run your tests (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests).
`TestSwitch` | In a test file opens the file under test, otherwise opens the test file.
`TestResults` | Opens the test results panel.
`TestCancel` | Cancels the test runner.
`TestCoverage` | Opens the code coverage report in default browser.
`ToggleOption` | Toggles PHPUnit options.

## Key Bindings

Add your preferred key bindings via **Menu > Preferences > Key Bindings** or use the command palette:

1. Press `Ctrl+Shift+p` (Win, Linux) or `Cmd+Shift+p` (OS X)
2. Select the "Preferences: Key Bindings" command
3. Press `Enter`

```json
[
    { "keys": ["ctrl+shift+a"], "command": "phpunit_test_suite" },
    { "keys": ["ctrl+shift+c"], "command": "phpunit_test_cancel" },
    { "keys": ["ctrl+shift+f"], "command": "phpunit_test_file" },
    { "keys": ["ctrl+shift+l"], "command": "phpunit_test_last" },
    { "keys": ["ctrl+shift+n"], "command": "phpunit_test_nearest" },
    { "keys": ["ctrl+shift+r"], "command": "phpunit_test_results" },
    { "keys": ["ctrl+shift+s"], "command": "phpunit_test_switch" },
    { "keys": ["ctrl+shift+v"], "command": "phpunit_test_visit" }
]
```

key | description
--- | -----------
`F4` | Jump to Next Failure
`Shift+F4` | Jump to Previous Failure

## Strategies

You can run tests using different execution environments called "strategies". To use a specific strategy, assign it to a setting:

```json
// make test commands execute using iTerm2
"phpunit.strategy": "iterm"
```

Strategy | Identifier | Description
-------- | ---------- | -----------
**Panel** (default) | `default` | Runs test commands in a panel at the bottom of your editor window.
**iTerm2.app** | `iterm` | Sends test commands to iTerm2 >= 2.9 (useful in MacVim GUI).

## Configuration

Configure settings via `Menu > Preferences > Settings` or by the Command Palette. To use the command palette:

1. Press `Ctrl+Shift+P`
2. Select the "Preferences: Settings" command
3. Press `Enter`

key | description | type | default
--- | ----------- | ---- | -------
`phpunit.options` | Default CLI options. | `dict` | `{}`
`phpunit.composer` | Use Composer installed PHPUnit. | `boolean` | `true`
`phpunit.save_all_on_run` | Save dirty buffers before test run. | `boolean` | `true`
`phpunit.php_executable` | Custom PHP executable. | `string` | System PATH
`phpunit.php_versions_path` | Location of phpenv versions. | `string` | `~/.phpenv/versions`

### phpunit.composer

When enabled, the test runner will checks if there is a Composer installed PHPUnit available, otherwise the system PATH will be used to find PHPUnit. When disabled, the Composer check is skipped. Composer support is enabled by default, but you can disabled it.

```json
"phpunit.composer": false
```

### phpunit.options

If you want some CLI options to stick around, you can configure them in your global preferences:

```json
// The following options translates to:
//
//   --colors=never
//   --coverage-html build/coverage
//   -d "display_errors=1"
//   -d "xdebug.scream=0"
//   --no-coverage

"phpunit.options": {
    "colors=never": true,
    "coverage-html": "build/coverage",
    "d": ["display_errors=1", "xdebug.scream=0"],
    "no-coverage": true
}
```

### phpunit.php_executable

You can instruct the test runner to use a custom PHP executable.

```json
"phpunit.php_executable": "~/.phpenv/versions/7.3.1/bin/php"
```

### phpunit.save_all_on_run

Write out every buffer that has changes before running tests.

```json
"phpunit.save_all_on_run": false
```

## Runner commands

Aside from the main commands, you can configure your own custom test runners (which also accept options):

```json
// Key Binding to run two specific test suites
{"keys": ["ctrl+shift+a"], "command": "test_suite", "args": {"testsuite": "fizz,buzz"}},

// Key Binding to run test suite with code coverage
{"keys": ["ctrl+shift+c"], "command": "test_suite", "args": {"coverage-html": "build/coverage"}},
```

The following commands accept CLI options:

* `phpunit_test_suite`
* `phpunit_test_file`
* `phpunit_test_nearest`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on, and inspired by, [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests), [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit), and [janko-m/vim-test](https://github.com/janko-m/vim-test).

## License

Released under the [BSD 3-Clause License](LICENSE).
