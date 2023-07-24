<h1 align="center">PHPUnit Kit</h1>

<p align="center">
    <a href="https://github.com/gerardroche/sublime-phpunit/actions/workflows/ci.yml"><img alt="GitHub CI Status" src="https://github.com/gerardroche/sublime-phpunit/actions/workflows/ci.yml/badge.svg?branch=master"></a>
    <a href="https://ci.appveyor.com/project/gerardroche/sublime-phpunit/branch/master"><img alt="AppVeyor CI Status" src="https://ci.appveyor.com/api/projects/status/wknvpma8qgjlqh1q/branch/master?svg=true"></a>
    <a href="https://codecov.io/gh/gerardroche/sublime-phpunit"><img src="https://codecov.io/gh/gerardroche/sublime-phpunit/branch/master/graph/badge.svg?token=rnB0MiBXlK" alt="CodeCov Coverage Status" /></a>
    <a href="https://packagecontrol.io/packages/PHPUnitKit"><img alt="Downloads" src="https://img.shields.io/packagecontrol/dt/PHPUnitKit.svg"></a>
</p>

PHPUnit support for [Sublime Text](https://sublimetext.com).

<img src="https://raw.githubusercontent.com/gerardroche/sublime-phpunit/master/screenshot.png" width="585" alt="PHPUnitKit">

## Features

* Run a test method
* Run a test file
* Run the test suite
* Run the nearest test
* Run the last test
* Run multiple test methods using a multiple cursor
* Auto run test on save
* Colour output
* Fast jump to next and previous failure
* Fast switch between test and file-under-test
* Toggle CLI options from the command palette
* Fully customized CLI options configuration
* Support for
    - [Artisan] - Artisan is the command line interface included with Laravel.
    - [Composer] - Composer is a Dependency Manager for PHP.
    - [iTerm2] - iTerm2 brings the terminal into the modern age.
    - [Kitty] - Kitt is a fast, feature-rich, cross-platform, GPU based terminal.
    - [ParaTest] - ParaTest adds parallel testing support in PHPUnit.
    - [Pest] - Pest is a testing framework with a focus on simplicity.
- Zero configuration required

Read [Running PHPUnit Tests from Sublime Text](https://blog.gerardroche.com/2023/05/05/running-phpunit-tests-within-sublime-text/) for a quick introduction.

## Installation

Install [PHPUnitKit](https://packagecontrol.io/packages/PHPUnitKit) via Package Control.

## Setup

Zero configuration required.

Optional. Add your preferred key bindings.

Menu → Preferences → Key Bindings

```js
{ "keys": ["ctrl+shift+a"], "command": "phpunit_test_suite" },
{ "keys": ["ctrl+shift+c"], "command": "phpunit_test_cancel" },
{ "keys": ["ctrl+shift+f"], "command": "phpunit_test_file" },
{ "keys": ["ctrl+shift+l"], "command": "phpunit_test_last" },
{ "keys": ["ctrl+shift+n"], "command": "phpunit_test_nearest" },
{ "keys": ["ctrl+shift+r"], "command": "phpunit_test_results" },
{ "keys": ["ctrl+shift+s"], "command": "phpunit_test_switch" },
{ "keys": ["ctrl+shift+v"], "command": "phpunit_test_visit" },
```

## Commands

Command                              | Description
:------                              | :----------
**PHPUnit:&nbsp;Test&nbsp;Nearest**  | In a test file runs the test nearest to the cursor, otherwise runs the test for the current file.
**PHPUnit:&nbsp;Test&nbsp;File**     | In a test file runs all tests in the current file, otherwise runs test for the current file.
**PHPUnit:&nbsp;Test&nbsp;Suite**    | Runs the whole test suite.
**PHPUnit:&nbsp;Test&nbsp;Last**     | Runs the last test.
**PHPUnit:&nbsp;Test&nbsp;Switch**   | In a test file opens the file under test, otherwise opens the test file.
**PHPUnit:&nbsp;Test&nbsp;Visit**    | Visits the test file from which you last run your tests (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests).
**PHPUnit:&nbsp;Test&nbsp;Results**  | Opens the exec test output panel.
**PHPUnit:&nbsp;Test&nbsp;Cancel**   | Cancels any currently running test.
**PHPUnit:&nbsp;Test&nbsp;Coverage** | Opens code coverage in browser.
**PHPUnit:&nbsp;Toggle...**             | Toggle PHPUnit options.

## Key Bindings

Key         | Description
:---        | :----------
`F4`        | Jump to next failure
`Shift+F4`  | Jump to previous failure

## Strategies

PHPUnitKit can run tests using different execution environments called "strategies". To use a specific strategy, assign it to a setting:

```js
"phpunit.strategy": "iterm"
```

| Strategy              | Identifier    | Description
| :------:              | :--------:    | :----------
| **Basic** (default)   | `basic`       | Sends test commands to Sublime Text exec output panel.
| **iTerm2.app**        | `iterm`       | Sends test commands to `iTerm2 >= 2.9` (useful in MacVim GUI).
| **[Kitty]**           | `kitty`       | Sends test commands to Kitty terminal.

## Configuring

Menu → Preferences → Settings

| Setting                   | Type               | Default          | Description
| :------------------------ | :----------------- | :--------------- | :----------
| `phpunit.executable`      | `string` or `list` | Auto discovered. | Path to PHPUnit executable.
| `phpunit.php_executable`  | `string`           | Auto discovered. | Path to PHP executable.
| `phpunit.options`         | `dict`             | `{}`             | CLI Options to pass to PHPUnit.
| `phpunit.save_all_on_run` | `boolean`          | `true`           | Save all dirty buffers before running tests.
| `phpunit.on_post_save`    | `list`             | `[]`             | Auto commands when views are saved.
| `phpunit.prepend_cmd`     | `list`             | `[]`             | Prepends test runner command.
| `phpunit.strategy`        | `string`           | `basic`          | Execution environment to run tests.
| `phpunit.composer`        | `boolean`          | `true`           | Use Composer installed executables, if they exist.
| `phpunit.artisan`         | `boolean`          | `false`          | Use Artisan to run tests, if it exists.
| `phpunit.paratest`        | `boolean`          | `false`          | Use ParaTest to run tests, if it exists.
| `phpunit.pest`            | `boolean`          | `false`          | Use Pest to run tests, if it exists.
| `phpunit.font_size`       | `integer`          | Editor default.  | Font size of PHPUnit output.

### CLI Options

If you want some CLI options to stick around, you can configure them in your settings.

Menu → Preferences → Settings

```js
"phpunit.options": {
    "no-coverage": true,
    "no-progress": true,
    "colors=never": true,
    "order-by=": "defects",
    "coverage-html": "build/coverage",
    "d": ["display_errors=1", "xdebug.scream=0"],
}
```

The above options will be passed to PHPUnit as CLI options:

```shell
-d "display_errors=1" \
-d "xdebug.scream=0" \
--no-coverage \
--no-progress \
--colors=never \
--order-by=defects \
--coverage-html build/coverage
```

**Disabling code coverage by default**

For instance, you can disable coverage by default and toggle it on when you need it. This will help keep your tests fast.

Menu → Preferences → Settings

```js
"phpunit.options": {
    "no-coverage": true,
}
```

Then toggle coverage on and off from the command palette.

```
Command Palette → PHPUnit: Toggle --no-coverage
```

**Stopping on defect by default**

If you want to always pass an option like `--stop-on-defect` to PHPUnit, add it to the options hash in settings.

Menu → Preferences → Settings

```
"phpunit.options": {
    "stop-on-defect": true
}
```

And/Or toggle it on and off from the command palette when you need it.

```
Command Palette → PHPUnit: Toggle --stop-on-defect
```

There are many other command palette toggles. Pretty much any option available in PHPUnit is available as a command palette toggle. If there is any missing, please open an issue and I can add it.

### PHPUnit Executable

You can instruct the test runner to use a custom PHPUnit executable. The default is auto discovery.

Generally you won't need to change this.

Menu → Preferences → Settings

```js
"phpunit.executable": "vendor/bin/phpunit"
"phpunit.executable": ["vendor/bin/phpunit"]
"phpunit.executable": "~/path-to/phpunit"
"phpunit.executable": ["artisan", "test"]
```

### PHP Executable

You can instruct the test runner to use a custom PHP executable. The default is auto discovery.

Menu → Preferences → Settings

```js
"phpunit.php_executable": "~/.phpenv/versions/7.3.1/bin/php"
```

### Autocommands

You can configure the `on_post_save` event to run the "Test File" command when views are saved. This will instruct the runner to automatically run a test every time it is saved.

Menu → Preferences → Settings

```js
"phpunit.on_post_save": [
    "phpunit_test_file"
]
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on, and inspired by the awesome work of [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests), [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit), [janko-m/vim-test](https://github.com/janko-m/vim-test), and many others.

## License

Released under the [GPL-3.0-or-later License](LICENSE).

[Artisan]: https://laravel.com/docs/artisan
[Composer]: https://getcomposer.org
[Kitty]: https://github.com/kovidgoyal/kitty
[ParaTest]: https://github.com/paratestphp/paratest
[Pest]: https://pestphp.com
[iTerm2]: https://iterm2.com
