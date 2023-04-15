# PHPUnit

<p>
    <a href="https://github.com/gerardroche/sublime-phpunit/actions/workflows/ci.yml"><img alt="GitHub CI Status" src="https://github.com/gerardroche/sublime-phpunit/actions/workflows/ci.yml/badge.svg?branch=master"></a>
    <a href="https://ci.appveyor.com/project/gerardroche/sublime-phpunit/branch/master"><img alt="AppVeyor CI Status" src="https://ci.appveyor.com/api/projects/status/wknvpma8qgjlqh1q/branch/master?svg=true"></a>
    <a href="https://codecov.io/gh/gerardroche/sublime-phpunit"><img src="https://codecov.io/gh/gerardroche/sublime-phpunit/branch/master/graph/badge.svg?token=rnB0MiBXlK" alt="CodeCov Coverage Status" /></a>
    <a href="https://packagecontrol.io/packages/PHPUnitKit"><img alt="Downloads" src="https://img.shields.io/packagecontrol/dt/PHPUnitKit.svg"></a>
</p>

PHPUnit support for [Sublime Text](https://sublimetext.com).

<img src="https://raw.githubusercontent.com/gerardroche/sublime-phpunit/master/screenshot.png" width="585" alt="Screenshot">

## Features

* Run Test File
* Run Test Suite
* Run Test Nearest
* Run Test Last
* Switch Test
* Supports Artisan, Composer, iTerm2, Kitty, Pest
* Supports jump-to-next and jump-to-previous failure

## Installation

Install PHPUnitKit via [Package Control](https://packagecontrol.io/packages/PHPUnitKit).

## Setup

Add your preferred key bindings via Menu &gt; Preferences &gt; Key Bindings:

```json
[
    { "keys": ["ctrl+shift+a"], "command": "phpunit_test_suite" },
    { "keys": ["ctrl+shift+c"], "command": "phpunit_test_cancel" },
    { "keys": ["ctrl+shift+f"], "command": "phpunit_test_file" },
    { "keys": ["ctrl+shift+l"], "command": "phpunit_test_last" },
    { "keys": ["ctrl+shift+n"], "command": "phpunit_test_nearest" },
    { "keys": ["ctrl+shift+r"], "command": "phpunit_test_results" },
    { "keys": ["ctrl+shift+s"], "command": "phpunit_test_switch" },
    { "keys": ["ctrl+shift+v"], "command": "phpunit_test_visit" },
]
```

## Commands

You can execute all commands from the Command Palette. All commands are prefixed with "PHPUnit: ".

Command                 | Description
:---------------------- | :----------
**Test&nbsp;Suite**     | Runs the whole test suite (if the current file is a test file, runs that framework's test suite).
**Test&nbsp;File**      | In a test file runs all tests in the current file, otherwise runs that file's tests.
**Test&nbsp;Last**      | Runs the last test.
**Test&nbsp;Nearest**   | In a test file runs the test nearest to the cursor, otherwise runs that file's tests.
**Test&nbsp;Switch**    | In a test file opens the file under test, otherwise opens the test file.
**Test&nbsp;Visit**     | Visits the test file from which you last run your tests (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests).
**Test&nbsp;Results**   | Opens the test results panel.
**Test&nbsp;Cancel**    | Cancels the test runner.
**Test&nbsp;Coverage**  | Opens the code coverage report in default browser.
**Toggle&nbsp;Option**  | Toggles PHPUnit options.

## Key Bindings

Key         | Description
:---        | :----------
`F4`        | Jump to next failure
`Shift+F4`  | Jump to previous failure

## Strategies

PHPUnitKit can run tests using different execution environments called "strategies". To use a specific strategy, assign it to a setting:

```json
{
    "phpunit.strategy": "iterm"
}
```

| Strategy              | Identifier    | Description
| :------:              | :--------:    | :----------
| **Basic** (default)   | `basic`       | Runs tests commands with Sublime Text exec command.
| **iTerm2.app**        | `iterm`       | Sends test commands to `iTerm2 >= 2.9` (useful in MacVim GUI).
| **[Kitty]**           | `kitty`       | Sends test commands to Kitty terminal.

## Configuring

Edit settings via Menu &gt; Preferences &gt; Settings:

Setting                     | Description                                       | Type                  | Default
:---                        | :----------                                       | :---                  | :------
`phpunit.options`           | Options to use when running tests.                | `dict`                | `{}`
`phpunit.executable`        | Path to PHPUnit executable.                       | `string\|list`        | Auto discovered.
`phpunit.php_executable`    | Path to PHP executable.                           | `string`              | Auto discovered.
`phpunit.save_all_on_run`   | Save all dirty buffers before running tests.      | `bool`                | `true`
`phpunit.on_post_save`      | Events to trigger when a file is saved.           | `list`                | `[]`
`phpunit.prepend_cmd`       | Prepends test runner command.                     | `list`                | `[]`
`phpunit.strategy`          | Output type.                                      | `string`              | `basic`
`phpunit.composer`          | Use PHPUnit installed by Composer if it exists.   | `bool`                | `true`
`phpunit.artisan`           | Use Artisan test runner if it exists.             | `bool`                | `false`
`phpunit.pest`              | Use Pest test runner if it exists.                | `bool`                | `false`

### Options

If you want some CLI options to stick around, you can configure them in your global preferences:

```
"phpunit.options": {
    "no-coverage": true,
    "colors=never": true,
    "coverage-html": "build/coverage",
    "d": ["display_errors=1", "xdebug.scream=0"]
}
```

The above options would be pass to PHPUnit as the following CLI options:

```
-d "display_errors=1" -d "xdebug.scream=0" --no-coverage --colors=never --coverage-html build/coverage
```

### PHPUnit Executable

You can instruct the test runner to use a custom PHPUnit executable. The default is auto discovery.

```
"phpunit.executable": "vendor/bin/phpunit"
"phpunit.executable": ["vendor/bin/phpunit"]
"phpunit.executable": "~/path-to/phpunit"
"phpunit.executable": ["artisan", "test"]
```

### PHP Executable

You can instruct the test runner to use a custom PHP executable. The default is auto discovery.

```
"phpunit.php_executable": "~/.phpenv/versions/7.3.1/bin/php"
```

### Auto run test file command on save

The `on_post_save` setting allows you to run the test file command immediatley after you save a file:

```
"phpunit.on_post_save": [
    "run_test_file"
]
```

Event | Description
:---- | :----------
`run_test_file` | Runs the the "test file" command for the active view.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on, and inspired by, [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests), [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit), and [janko-m/vim-test](https://github.com/janko-m/vim-test).

## License

Released under the [BSD 3-Clause License](LICENSE).

[Kitty]: https://github.com/kovidgoyal/kitty
