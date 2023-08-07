<h1>PHPUnit Kit</h1>

<p>
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
* Run tests on remote server via SSH :new:
* Run tests via Docker :new:
* Run tests via side bar menu :new:
* Run tests via context menu :new:
* Auto run test on save
* Colour output
* Fast jump to next and previous failure
* Fast switch between test and file-under-test
* Toggle options from the command palette
* Toggle run test on save :new:
* Fully customized CLI options configuration
* Support for
    - [Artisan] - Artisan is the command line interface included with Laravel.
    - [Composer] - Composer is a Dependency Manager for PHP.
    - [iTerm2] - iTerm2 brings the terminal into the modern age.
    - [Kitty] - Kitt is a fast, feature-rich, cross-platform, GPU based terminal.
    - [ParaTest] - ParaTest adds parallel testing support in PHPUnit.
    - [Pest] - Pest is a testing framework with a focus on simplicity.
    - [xterm] - A terminal emulator for the X Window System. :new:
    - [cmd] - A command-line interpreter for Windows. :new:
    - [PowerShell] - A cross-platform command-line shell. :new:
* Zero configuration required

Read [Running PHPUnit Tests from Sublime Text](https://blog.gerardroche.com/2023/05/05/running-phpunit-tests-within-sublime-text/) for a quick introduction.

<details>
 <summary><strong>Table of Contents</strong> (click to expand)</summary>

- [Installation](#installation)
- [Setup](#setup)
- [Commands](#commands)
- [Key Bindings](#key-bindings)
- [Strategies](#strategies)
- [Configuring](#configuring)
  - [CLI Options](#cli-options)
  - [PHPUnit Executable](#phpunit-executable)
  - [PHP Executable](#php-executable)
  - [SSH](#ssh)
  - [Docker](#docker)
  - [Auto Commands](#auto-commands)
  - [Toggle Commands](#toggle-commands)
  - [Custom Toggle Commands](#custom-toggle-commands)
- [NeoVintageous mappings](#neovintageous-mappings)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Credits](#credits)
- [License](#license)

</details>

## Installation

**Method 1: Using Package Control**

1. Open Sublime Text.
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the Command Palette.
3. Type "Package Control: Install Package" and press `Enter`.
4. In the input field, type "PHPUnitKit" and select it from the list of available packages.

**Method 2: Manual Installation**

1. Visit the [PHPUnitKit GitHub repository](https://github.com/gerardroche/sublime-phpunit).
2. Click on the "Code" button and select "Download ZIP."
3. Extract the downloaded ZIP file.
4. Open Sublime Text and go to `Preferences -> Browse Packages...` to open the Packages folder.
5. Copy the "PHPUnitKit" folder from the extracted ZIP and paste it into the Packages folder.

**Method 3: Manual Git Repository Installation**

1. Open a terminal or command prompt.
2. Navigate to the Sublime Text Packages directory:
    - On Windows: `%APPDATA%\Sublime Text\Packages`
    - On macOS: `~/Library/Application Support/Sublime Text/Packages`
    - On Linux: `~/.config/sublime-text/Packages`
3. Clone the plugin repository directly into the Packages directory using Git:
   ```
   git clone https://github.com/gerardroche/sublime-phpunit.git
   ```

## Setup

(Optional. Zero configuration required.)

To add your preferred key bindings, follow these steps:

1. Open the Sublime Text menu: `Command Palette → Preferences: Key Bindings`.
2. Add the following key bindings to the configuration file:

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

## Commands

| Command                                                       | Description
| :-------------------------------------------------------------| :----------
| **PHPUnit:&nbsp;Test&nbsp;Nearest**                           | Run a test nearest to the cursor. If the current file is not a test file, it runs the tests for current file.
| **PHPUnit:&nbsp;Test&nbsp;File**                              | Run tests for the current file.
| **PHPUnit:&nbsp;Test&nbsp;Suite**                             | Run test suite of the current file.
| **PHPUnit:&nbsp;Test&nbsp;Last**                              | Runs the last test.
| **PHPUnit:&nbsp;Test&nbsp;Switch**                            | In a test file opens the file under test, otherwise opens the test file.
| **PHPUnit:&nbsp;Test&nbsp;Visit**                             | Open the last run test.
| **PHPUnit:&nbsp;Test&nbsp;Results**                           | Opens the test output panel (only applies to "basic" strategy).
| **PHPUnit:&nbsp;Test&nbsp;Cancel**                            | Cancel any currently running tests.
| **PHPUnit:&nbsp;Test&nbsp;Coverage**                          | Opens the code coverage in a browser.
| **PHPUnit:&nbsp;Toggle&nbsp;Run&nbsp;Test&nbsp;On&nbsp;Save** | Toggle to quickly turn the Test File auto-command on and off.
| **PHPUnit:&nbsp;Toggle...**                                   | Toggle options e.g. PHPUnit CLI options.
| **Preferences:&nbsp;PHPUnit&nbsp;Settings**                   | Edit settings.

## Key Bindings

Key         | Description
:---        | :----------
`F4`        | Jump to next failure
`Shift+F4`  | Jump to previous failure

## Strategies

PHPUnitKit can run tests using different execution environments called "strategies".

**Example:** Use the Kitty terminal strategy

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.strategy": "kitty"
}
```

| Strategy              | Identifier    | Description
| :------:              | :--------:    | :----------
| **Basic** (default)   | `basic`       | Sends test commands to Sublime Text exec output panel.
| **iTerm2.app**        | `iterm`       | Sends test commands to `iTerm2 >= 2.9` (useful in MacVim GUI).
| **[Kitty]**           | `kitty`       | Sends test commands to Kitty terminal.
| **[xterm]**           | `xterm`       | Sends test commands to xterm terminal. :new:
| **[cmd]**             | `cmd`         | Sends test commands to cmd.exe terminal. :new:
| **[PowerShell]**      | `powershell`  | Sends test commands to PowerShell command shell. :new:

## Configuring

Command Palette → Preferences: PHPUnit Settings

| Setting                   | Type               | Default              | Description
| :------------------------ | :----------------- | :------------------- | :----------
| `phpunit.executable`      | `string`<br>`list` | Auto&nbsp;discovery. | The path to the PHPUnit executable to use when running tests. Environment variables and user home directory ~ placeholder are expanded. The executable can be a string or a list of parameters. <br>Example: `vendor/bin/phpunit`
| `phpunit.options`         | `dict`             | `{}`                 | Command-line options to pass to PHPUnit. <br>Example: `{"no-coverage": true}`
| `phpunit.php_executable`  | `string`           | Auto&nbsp;discovery. | The path to the PHP executable to use when running tests. Environment variables and user home directory ~ placeholder are expanded. <br>Example: `~/.phpenv/versions/8.2/bin/php`
| `phpunit.save_all_on_run` | `boolean`          | `true`               | Save all dirty buffers before running tests.
| `phpunit.on_post_save`    | `list`             | `[]`                 | Auto commands when views are saved. <br>Example: `["phpunit_test_file"]`
| `phpunit.debug`           | `boolean`          | `false`              | Prints test runner debug information.
| `phpunit.prepend_cmd`     | `list`             | `[]`                 | Prepends test runner command.
| `phpunit.strategy`        | `string`           | `basic`              | Execution environment to run tests.
| `phpunit.font_size`       | `integer`          | Editor default.      | Font size of PHPUnit output.
| `phpunit.composer`        | `boolean`          | `true`               | Use Composer installed executables.
| `phpunit.artisan`         | `boolean`          | `false`              | Use Artisan to run tests.
| `phpunit.paratest`        | `boolean`          | `false`              | Use ParaTest to run tests.
| `phpunit.pest`            | `boolean`          | `false`              | Use Pest to run tests.

**SSH settings** :rocket:

| Setting               | Type          | Default   | Description
| :-------------------- | :------------ | :-------- | :----------
| `phpunit.ssh`         | `boolean`     | `false`   | Enable SSH.
| `phpunit.ssh_options` | `dict`        | `{}`      | The options to use when running tests via SSH. <br>Example: `{"-p": "22", "-tt": true}`.
| `phpunit.ssh_user`    | `string`      | `null`    | The user to use when running tests via SSH. <br>Example: vagrant
| `phpunit.ssh_host`    | `string`      | `null`    | The host to use when running tests via SSH. <br>Example: homestead.test
| `phpunit.ssh_paths`   | `dict`        | `{}`      | The path map to use when running tests via SSH. The keys are local paths and the values are the replacement remote paths. Environment variables and user home directory ~ placeholder are expanded. Example: `{"~/code/project1": "~/project1"}`

**Docker settings** :rocket:

| Setting               | Type          | Default   | Description
| :-------------------- | :------------ | :-------- | :----------
| `phpunit.docker`         | `boolean`  | `false`   | Enable Docker.
| `phpunit.docker_command` | `list`     | `[]`      | The command to use when running tests via Docker. Example: `["docker", "exec", "-it", "my-container"]`
| `phpunit.docker_paths`   | `dict`     | `{}`      | The path map to use when running tests via Docker. The keys are local paths and the values are the replacement remote paths. Environment variables and user home directory ~ placeholder are expanded. Example: `{"~/code/project1": "~/project1"}`

### CLI Options

If you want some CLI options to stick around, you can configure them in your settings.

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.options": {
        "no-coverage": true,
        "no-progress": true,
        "colors=never": true,
        "order-by=": "defects",
        "coverage-html": "build/coverage",
        "d": ["display_errors=1", "xdebug.scream=0"],
    }
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

**Example:** Ignore code coverage reporting configured in the XML configuration file

This can help keep your tests fast. You can toggle no-coverage from the command palette when you need it.

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.options": {
        "no-coverage": true,
    }
}
```

**Example:** Stop after first error, failure, warning, or risky test

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.options": {
        "stop-on-defect": true
    }
}
```

**Example:** Disable progress and output

This is useful if you are migrating from PHPUnit to Pest and want to hide superfluous output.

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.options": {
        "no-progress": true,
        "no-output": true,
    }
}
```

### PHPUnit Executable

The path to the PHPUnit executable to use when running tests. Environment variables and user home directory ~ placeholder are expanded. The executable can be a string or a list of parameters.

Default: Auto discovery.

**Examples**

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.executable": "vendor/bin/phpunit",
    "phpunit.executable": "~/path/to/phpunit",
    "phpunit.executable": ["artisan", "test"]
}
```

### PHP Executable

The path to the PHP executable to use when running tests. Environment variables and user home directory ~ placeholder are expanded.

Default: Auto discovery.

**Examples**


Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.php_executable": "~/.phpenv/versions/8.2/bin/php"
}
```

### SSH

**Example:** Run tests via SSH using [Laravel Homestead](https://laravel.com/docs/homestead)

```json
{
    "phpunit.ssh": true,
    "phpunit.ssh_options": {
        "-p": "22",
        "-tt": true
    },
    "phpunit.ssh_user": "vagrant",
    "phpunit.ssh_host": "homestead.test",
    "phpunit.ssh_paths": {
        "~/code/project1": "~/project1",
        "/home/code/project2": "/home/vagrant/project2",
    }
}
```

### Docker

**Example:** Run tests via [Docker](https://www.docker.com)

```json
{
    "phpunit.docker": true,
    "phpunit.docker_command": ["docker", "exec", "-it", "my-container"],
    "phpunit.docker_paths": {
        "~/code/project1": "~/project1",
        "/home/code/project2": "/home/vagrant/project2",
    }
}
```

### Auto Commands

You can configure the `on_post_save` event to run the "Test File" command when views are saved. This will instruct the runner to automatically run a test every time it is saved.

**Example:** Run Test File on Save

Command Palette → Preferences: PHPUnit Settings

```json
{
    "phpunit.on_post_save": [
        "phpunit_test_file"
    ]
}
```

### Toggle Commands

You can toggle many PHPUnit CLI options from the command palette by prefixing the command with "PHPUnit: Toggle."

#### Execution

- PHPUnit: Toggle --process-isolation: Run each test in a separate PHP process.
- PHPUnit: Toggle --globals-backup: Backup and restore $GLOBALS for each test.
- PHPUnit: Toggle --static-backup: Backup and restore static properties for each test.
- PHPUnit: Toggle --strict-coverage: Be strict about code coverage metadata.
- PHPUnit: Toggle --strict-global-state: Be strict about changes to global state.
- PHPUnit: Toggle --disallow-test-output: Be strict about output during tests.
- PHPUnit: Toggle --enforce-time-limit: Enforce time limit based on test size.
- PHPUnit: Toggle --dont-report-useless-tests: Do not report tests that do not test anything.
- PHPUnit: Toggle --stop-on-defect: Stop after the first error, failure, warning, or risky test.
- PHPUnit: Toggle --stop-on-error: Stop after the first error.
- PHPUnit: Toggle --stop-on-failure: Stop after the first failure.
- PHPUnit: Toggle --stop-on-warning: Stop after the first warning.
- PHPUnit: Toggle --stop-on-risky: Stop after the first risky test.
- PHPUnit: Toggle --stop-on-deprecation: Stop after the first test that triggered a deprecation.
- PHPUnit: Toggle --stop-on-notice: Stop after the first test that triggered a notice.
- PHPUnit: Toggle --stop-on-skipped: Stop after the first skipped test.
- PHPUnit: Toggle --stop-on-incomplete: Stop after the first incomplete test.
- PHPUnit: Toggle --fail-on-warning: Signal failure using the shell exit code when a warning was triggered.
- PHPUnit: Toggle --fail-on-risky: Signal failure using the shell exit code when a test was considered risky.
- PHPUnit: Toggle --fail-on-deprecation: Signal failure using the shell exit code when a deprecation was triggered.
- PHPUnit: Toggle --fail-on-notice: Signal failure using the shell exit code when a notice was triggered.
- PHPUnit: Toggle --fail-on-skipped: Signal failure using the shell exit code when a test was skipped.
- PHPUnit: Toggle --fail-on-incomplete: Signal failure using the shell exit code when a test was marked incomplete.
- PHPUnit: Toggle --cache-result: Write test results to the cache file.
- PHPUnit: Toggle --do-not-cache-result: Do not write test results to the cache file.
- PHPUnit: Toggle --order-by=default: Run tests in order: default.
- PHPUnit: Toggle --order-by=defects: Run tests in order: defects.
- PHPUnit: Toggle --order-by=depends: Run tests in order: depends.
- PHPUnit: Toggle --order-by=duration: Run tests in order: duration.
- PHPUnit: Toggle --order-by=no-depends: Run tests in order: no-depends.
- PHPUnit: Toggle --order-by=random: Run tests in order: random.
- PHPUnit: Toggle --order-by=reverse: Run tests in order: reverse.
- PHPUnit: Toggle --order-by=size: Run tests in order: size.

#### Reporting

- PHPUnit: Toggle --no-progress: Disable output of test execution progress.
- PHPUnit: Toggle --no-results: Disable output of test results.
- PHPUnit: Toggle --no-output: Disable all output.
- PHPUnit: Toggle --display-incomplete: Display details for incomplete tests.
- PHPUnit: Toggle --display-skipped: Display details for skipped tests.
- PHPUnit: Toggle --display-deprecations: Display details for deprecations triggered by tests.
- PHPUnit: Toggle --display-errors: Display details for errors triggered by tests.
- PHPUnit: Toggle --display-notices: Display details for notices triggered by tests.
- PHPUnit: Toggle --display-warnings: Display details for warnings triggered by tests.
- PHPUnit: Toggle --reverse-list: Print defects in reverse order.
- PHPUnit: Toggle --teamcity: Replace default progress and result output with TeamCity format.
- PHPUnit: Toggle --testdox: Replace default result output with TestDox format.

#### Logging

- PHPUnit: Toggle --no-logging: Ignore logging configured in the XML configuration file.

#### Code Coverage

- PHPUnit: Toggle --path-coverage: Report path coverage in addition to line coverage.
- PHPUnit: Toggle --disable-coverage-ignore: Disable metadata for ignoring code coverage.
- PHPUnit: Toggle --no-coverage: Ignore code coverage reporting configured in the XML configuration file.

### Custom Toggle Commands

You can create your own toggle commands. The `phpunit_toggle_option` command accepts the following arguments:

Argument |  Type
:------- | :-----
`option` |  String
`value`  |  Boolean (default) or String

**Example:** Custom toggle commands

1. Open Sublime Text and go to `Preferences -> Browse Packages...` to open the Packages folder.
2. Create a file named "User/Default.sublime-commands"
3. Add the following commands to the configuration file:

   ```json
   [
       {
           "caption": "PHPUnit: Toggle --no-coverage",
           "command": "phpunit_toggle_option",
           "args": {
               "option": "no-coverage"
           }
       },
       {
           "caption": "PHPUnit: Toggle --order-by=depends,defects",
           "command": "phpunit_toggle_option",
           "args": {
               "option": "order-by=",
               "value": "depends,defects"
           }
       }
   ]
   ```


**Example:** Custom key binding to toggle coverage reporting generation

1. Open the Command Palette: `Command Palette → Preferences: Key Bindings`.
2. Add the following key binding to the configuration file:

   ```json
   [
       {
           "keys": ["ctrl+n"],
           "command": "phpunit_toggle_option",
           "args": {
               "option": "no-coverage"
           }
       },
   ]
   ```

## NeoVintageous mappings

[NeoVintageous](https://github.com/NeoVintageous/NeoVintageous) is a Vim emulator for Sublime Text.

1. Open the Command Palette: `Command Palette → NeoVintageous: Open neovintageous file`.
2. Add your preferred mappings.

   **Example**

   ```vim
   nnoremap <leader>t :TestNearest<CR>
   nnoremap <leader>T :TestFile<CR>
   nnoremap <leader>a :TestSuite<CR>
   nnoremap <leader>l :TestLast<CR>
   nnoremap <leader>g :TestVisit<CR>
   ```
3. To apply the changes, reload the neovintageousrc from the Command Palette: `Command Palette → NeoVintageous: Reload neovintageous file`.

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
[PowerShell]: https://learn.microsoft.com/en-us/powershell/
[cmd]: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd
[iTerm2]: https://iterm2.com
[xterm]: https://invisible-island.net/xterm/
