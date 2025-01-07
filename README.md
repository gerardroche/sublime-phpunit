<h1>Welcome to PHPUnit Kit</h1>

<p>
    <a href="https://github.com/gerardroche/sublime-phpunit/actions/workflows/ci.yml"><img alt="GitHub CI Status" src="https://github.com/gerardroche/sublime-phpunit/actions/workflows/ci.yml/badge.svg?branch=master"></a>
    <a href="https://codecov.io/gh/gerardroche/sublime-phpunit"><img alt="CodeCov Coverage Status" src="https://codecov.io/gh/gerardroche/sublime-phpunit/branch/master/graph/badge.svg?token=rnB0MiBXlK"></a>
    <a href="https://packagecontrol.io/packages/PHPUnitKit"><img alt="Download Count" src="https://img.shields.io/packagecontrol/dt/PHPUnitKit.svg"></a>
</p>

Enhance your coding experience with seamless PHPUnit integration for [Sublime Text](https://sublimetext.com).

<img alt="PHPUnitKit in Action" src="https://raw.githubusercontent.com/gerardroche/sublime-phpunit/master/screenshot.png" width="585">

## Features

* Run a test
* Run a test file
* Run the test suite
* Run the nearest test
* Run the last test
* Run tests via SSH
* Run tests via Docker
* Run tests via sidebar and context menus
* Run multiple tests (multiple cursor)
* Auto-run tests on save
* Jump to next and previous failures
* File and test switcher
* Toggle options
* Fully customizable
* Zero configuration required
* Support for:
    - [Artisan] - Artisan is the command-line interface included with Laravel.
    - [Composer] - Composer is a Dependency Manager for PHP.
    - [iTerm2] - iTerm2 brings the terminal into the modern age.
    - [Kitty] - Kitty is a fast, feature-rich, cross-platform, GPU-based terminal.
    - [ParaTest] - ParaTest adds parallel testing support in PHPUnit.
    - [Pest] - Pest is a testing framework with a focus on simplicity.
    - [xterm] - A terminal emulator for the X Window System.
    - [cmd] - A command-line interpreter for Windows.
    - [PowerShell] - A cross-platform command-line shell.
    - [Tmux] - A terminal multiplexer.

Read [Running PHPUnit Tests from Sublime Text](https://blog.gerardroche.com/2023/05/05/running-phpunit-tests-within-sublime-text/) for a quick introduction.

<details>
 <summary><strong>Table of Contents</strong> (click to expand)</summary>

- [Command Palette](#command-palette)
- [Key Bindings](#key-bindings)
- [Strategies](#strategies)
- [Settings](#settings)
- [NeoVintageous mappings](#neovintageous-mappings)
- [Installation](#installation)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Credits](#credits)
- [License](#license)

</details>

## Command Palette

| Command                           | Description
| :-------------------------------- | :----------
| PHPUnit:&nbsp;Test&nbsp;Nearest   | Executes the test closest to the cursor. If the current file isn't a designated test file, it runs tests for the current file.
| PHPUnit:&nbsp;Test&nbsp;File      | Runs tests for the currently open file. If it's not a test file, it runs tests for the current file.
| PHPUnit:&nbsp;Test&nbsp;Suite     | Runs the test suite associated with the current file.
| PHPUnit:&nbsp;Test&nbsp;Last      | Runs the most recently executed test.
| PHPUnit:&nbsp;Test&nbsp;Switch    | In a test file, opens the file under test; otherwise, opens the corresponding test file.
| PHPUnit:&nbsp;Test&nbsp;Visit     | Quickly accesses the last run test.
| PHPUnit:&nbsp;Test&nbsp;Results   | Opens the test output panel (applies to "sublime" strategy).
| PHPUnit:&nbsp;Test&nbsp;Cancel    | Halts any ongoing test executions.
| PHPUnit:&nbsp;Test&nbsp;Coverage  | Views code coverage using your default browser.
| PHPUnit:&nbsp;Toggle...           | Various toggle commands.

## Key Bindings

| Key        | Description
| :--------- | :----------
| `F4`       | Jump to the next failure
| `Shift+F4` | Jump to the previous failure

### Create your preferred key bindings

> Command Palette → Preferences: Key Bindings

Linux / Win

```jsonl
{ "keys": ["ctrl+shift+a"], "command": "phpunit_test_suite" },
{ "keys": ["ctrl+shift+c"], "command": "phpunit_test_cancel" },
{ "keys": ["ctrl+shift+f"], "command": "phpunit_test_file" },
{ "keys": ["ctrl+shift+l"], "command": "phpunit_test_last" },
{ "keys": ["ctrl+shift+n"], "command": "phpunit_test_nearest" },
{ "keys": ["ctrl+shift+r"], "command": "phpunit_test_results" },
{ "keys": ["ctrl+shift+s"], "command": "phpunit_test_switch" },
{ "keys": ["ctrl+shift+v"], "command": "phpunit_test_visit" },
```

Mac

```jsonl
{ "keys": ["super+shift+a"], "command": "phpunit_test_suite" },
{ "keys": ["super+shift+c"], "command": "phpunit_test_cancel" },
{ "keys": ["super+shift+f"], "command": "phpunit_test_file" },
{ "keys": ["super+shift+l"], "command": "phpunit_test_last" },
{ "keys": ["super+shift+n"], "command": "phpunit_test_nearest" },
{ "keys": ["super+shift+r"], "command": "phpunit_test_results" },
{ "keys": ["super+shift+s"], "command": "phpunit_test_switch" },
{ "keys": ["super+shift+v"], "command": "phpunit_test_visit" },
```

## Strategies

You can run tests using different execution environments known as "strategies".

| Strategy              | Identifier    | Description
| :---------------------| :-------------| :----------
| Sublime<br>(default)  | `sublime`     | Sends test commands to Sublime Text's exec output panel.
| iTerm2.app            | `iterm`       | Sends test commands to `iTerm2 >= 2.9`.
| [Kitty]               | `kitty`       | Sends test commands to the Kitty terminal.
| [xterm]               | `xterm`       | Sends test commands to the xterm terminal.
| [cmd]                 | `cmd`         | Sends test commands to the cmd.exe terminal.
| [PowerShell]          | `powershell`  | Sends test commands to the PowerShell command shell.
| [Tmux]                | `tmux`        | Sends test commands to the Tmux terminal multiplexer.

**Example:** Use the Tmux strategy

> Command Palette → Preferences: PHPUnit Settings

```jsonl
"phpunit.strategy": "tmux"
```

## Settings

> Command Palette → Preferences: PHPUnit Settings

| Setting                   | Type               | Default              | Description
| :------------------------ | :----------------- | :------------------- | :----------
| `phpunit.executable`      | `string` or `list` | Auto-discovery       | Path to the PHPUnit executable for running tests. Environment variables and user home directory ~ placeholder are expanded. The executable can be a string or a list of parameters. Example: `vendor/bin/phpunit`
| `phpunit.options`         | `dict`             | `{}`                 | Command-line options to pass to PHPUnit. Example: `{"no-coverage": true}`
| `phpunit.php_executable`  | `string`           | Auto-discovery       | Path to the PHP executable for running tests. Environment variables and user home directory ~ placeholder are expanded. Example: `~/.phpenv/versions/8.2/bin/php`
| `phpunit.save_all_on_run` | `boolean`          | `true`               | Automatically saves all unsaved buffers before running tests.
| `phpunit.on_post_save`    | `list`             | `[]`                 | Auto commands to execute when views are saved. Example: `["phpunit_test_file"]`
| `phpunit.debug`           | `boolean`          | `false`              | Prints debug information about the test runner.
| `phpunit.prepend_cmd`     | `list`             | `[]`                 | Prepends custom commands to the test runner.
| `phpunit.strategy`        | `string`           | `sublime`            | The execution environment used for running tests.
| `phpunit.font_size`       | `integer`          | Editor default       | Font size of PHPUnit's output.
| `phpunit.composer`        | `boolean`          | `true`               | Uses Composer-installed executables.
| `phpunit.artisan`         | `boolean`          | `false`              | Uses Artisan to run tests.
| `phpunit.paratest`        | `boolean`          | `false`              | Uses ParaTest to run tests.
| `phpunit.pest`            | `boolean`          | `false`              | Uses Pest to run tests.

**SSH Settings**

Configure SSH settings for running tests remotely:

| Setting               | Type          | Default   | Description
| :-------------------- | :------------ | :-------- | :----------
| `phpunit.ssh`         | `boolean`     | `false`   | Enable SSH for remote testing.
| `phpunit.ssh_options` | `dict`        | `{}`      | Options for running tests via SSH. Example: `{"-p": "22", "-tt": true}`.
| `phpunit.ssh_user`    | `string`      | `null`    | User for running tests via SSH. Example: `vagrant`
| `phpunit.ssh_host`    | `string`      | `null`    | Host for running tests via SSH. Example: `homestead.test`
| `phpunit.ssh_paths`   | `dict`        | `{}`      | Path mapping for running tests via SSH. Keys: local paths, Values: corresponding remote paths. Environment variables and user home directory ~ placeholder are expanded. Example: `{"~/code/project1": "~/project1"}`

**Docker Settings**

Configure Docker settings for running tests within containers:

| Setting               | Type          | Default   | Description
| :-------------------- | :------------ | :-------- | :----------
| `phpunit.docker`         | `boolean`  | `false`   | Enable Docker for testing.
| `phpunit.docker_command` | `list`     | `[]`      | Command to use when running tests via Docker. Example: `["docker", "exec", "-it", "my-container"]`
| `phpunit.docker_paths`   | `dict`     | `{}`      | Path mapping for running tests via Docker. Keys: local paths, Values: corresponding remote paths. Environment variables and user home directory ~ placeholder are expanded. Example: `{"~/code/project1": "~/project1"}`

**Tmux Settings** :new:

Configure Tmux settings for running tests in a tmux pane:

| Setting                           | Type          | Default   | Description
| :-------------------------------- | :------------ | :-------- | :----------
| `phpunit.tmux_clear`              | `bool`        | `true`    | Clear the terminal screen before running tests.
| `phpunit.tmux_clear_scrollback`   | `bool`        | `true`    | Clear the terminal's scrollback buffer or do not attempt to clear it using the extended "E3" capability.
| `phpunit.tmux_target`             | `string`      | `:.`      | Specify the session, window, and pane which should be used to run tests. <br><br>Format: `{session}:{window}.{pane}` <br><br>The default means the current pane. <br><br>For example, `:{start}.{top}` would mean the current session, lowest-numbered window, top pane. <br><br>See [Tmux documentation](http://man.openbsd.org/OpenBSD-current/man1/tmux.1#COMMANDS) for target usage.

### phpunit.options

- Type: `dict`
- Default: `{}`

Default command-line options to pass to PHPUnit. If you want some CLI options to stick around, you can configure them in your settings.

```jsonl
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

**Ignore code coverage reporting configured in the XML configuration file**

This can help keep your tests fast. You can toggle no-coverage from the command palette when you need it.

```jsonl
"phpunit.options": {
    "no-coverage": true,
}
```

**Stop after first error, failure, warning, or risky test**

```jsonl
"phpunit.options": {
    "stop-on-defect": true
}
```

**Disable progress and output**

This is useful if you are migrating from PHPUnit to Pest and want to hide superfluous output.

```jsonl
"phpunit.options": {
    "no-progress": true,
    "no-output": true,
}
```

### phpunit.executable

- Type: `string | list`
- Default: Auto-discovery

The PHPUnit executable to use when running tests.

```jsonl
"phpunit.executable": "vendor/bin/phpunit",
```

Environment variables and user home directory `~` placeholders are expanded.

```jsonl
"phpunit.executable": "~/path/to/phpunit",
```

As a list of arguments:

```jsonl
"phpunit.executable": ["artisan", "test"]
```

### phpunit.php_executable

- Type: `string`
- Default: Auto-discovery

The PHP executable to use when running tests.

Environment variables and user home directory `~` placeholders are expanded.

```jsonl
"phpunit.php_executable": "~/.phpenv/versions/8.2/bin/php"
```

### phpunit.save_all_on_run

- Type: `boolean`
- Default: `true`

Automatically save all unsaved views before running tests.

### phpunit.on_post_save

- Type: `list`
- Default: `[]`

Auto commands to execute when views are saved.

*Currently only supports running the test file command.*

```jsonl
"phpunit.on_post_save": [
    "phpunit_test_file"
]
```

### phpunit.debug

- Type: `boolean`
- Default: `false`

Enable debug logging when running tests.

### phpunit.prepend_cmd

- Type: `list`
- Default: `[]`

Prepends custom commands to the test runner.

### phpunit.strategy

- Type: `string`
- Default: `sublime`

The execution environment used for running tests.

### phpunit.font_size

- Type: `integer`
- Default: Editor default

Font size of PHPUnit's output.

### phpunit.composer

- Type: `boolean`
- Default: `true`

Discover and use Composer executables.

### phpunit.artisan

- Type: `boolean`
- Default: `false`

Discover and use Artisan to run tests.

### phpunit.paratest

- Type: `boolean`
- Default: `false`

Discover and use ParaTest to run tests.

### phpunit.pest

- Type: `boolean`
- Default: `false`

Discover and use Pest to run tests.

### phpunit.ssh

- Type: `boolean`
- Default: `false`

Enable SSH for remote testing.

Run tests via SSH using [Laravel Homestead](https://laravel.com/docs/homestead?ref=blog.gerardroche.com)

```jsonl
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
```

### phpunit.ssh_options

- Type: `dict`
- Default: `{}`

Options for running tests via SSH.

```jsonl
"phpunit.ssh_options": {
    "-p": "22",
    "-tt": true
}
```

### phpunit.ssh_user

- Type: `string`
- Default: `null`

User for running tests via SSH.

```jsonl
"phpunit.ssh_user": "vagrant"
```

### phpunit.ssh_host

- Type: `string`
- Default: `null`

Host for running tests via SSH.

```jsonl
"phpunit.ssh_host": "homestead.test"
```

### phpunit.ssh_paths

- Type: `dict`
- Default: `{}`

Path mapping for SSH.

Environment variables and user home directory `~` placeholders are expanded.

```jsonl
"phpunit.ssh_paths": {
    "~/code/project1": "~/project1"
}
```

### phpunit.docker

- Type: `boolean`
- Default: `false`

Enable Docker for testing.

Run tests via [Docker](https://www.docker.com?ref=blog.gerardroche.com)

```jsonl
"phpunit.docker": true,
"phpunit.docker_command": ["docker", "exec", "-it", "my-container"],
"phpunit.docker_paths": {
    "~/code/project1": "~/project1",
    "/home/code/project2": "/home/vagrant/project2",
}
```

### phpunit.docker_command

- Type: `list`
- Default: `[]`

Command to use when running tests via Docker.

```jsonl
"phpunit.docker_command": [
    "docker",
    "exec",
    "-it",
    "my-container"
]
```

### phpunit.docker_paths

- Type: `dict`
- Default: `{}`

Path mapping for Docker.

Environment variables and user home directory `~` placeholders are expanded.

```jsonl
"phpunit.docker_paths": {
    "~/code/project1": "~/project1"
}
```

### phpunit.tmux_clear

- Type: `bool`
- Default: `true`

Clear the terminal screen before running tests.

### phpunit.tmux_clear_scrollback

- Type: `bool`
- Default: `true`

Clear the terminal's scrollback buffer or do not attempt to clear it using the extended "E3" capability.

### phpunit.tmux_target

- Type: `string`
- Default: `:.` (current pane)

Set the session, window, and pane, to be used to run tests. The format is `{session}:{window}.{pane}`, see [Tmux documentation](http://man.openbsd.org/OpenBSD-current/man1/tmux.1?ref=blog.gerardroche.com#COMMANDS) for details.

Current session, lowest-numbered window, top pane.

```
:{start}.{top}
```

Use the `no-coverage` option by default, and then use the Command Palette Toggle no-coverage command, to toggle code coverage on and off when you need it. This can make your tests run faster by default.

```jsonl
"phpunit.strategy": "tmux",
"phpunit.tmux_target": ":{start}.{top}",
"phpunit.options": {
    "colors": true,
    "no-coverage": true
}
```

## Auto run

You can automatically run a test file on save.

Command Palette → Preferences: PHPUnit Settings

```jsonl
"phpunit.on_post_save": [
    "phpunit_test_file"
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
   git clone https://github.com/gerardroche/sublime-phpunit.git PHPUnitKit
   ```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Based initially on, and inspired by the awesome work of [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests), [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit), [janko-m/vim-test](https://github.com/janko-m/vim-test), and many others.

## License

Released under the [GPL-3.0-or-later License](LICENSE).

[Artisan]: https://laravel.com/docs/artisan?ref=blog.gerardroche.com
[Composer]: https://getcomposer.org?ref=blog.gerardroche.com
[Kitty]: https://github.com/kovidgoyal/kitty?ref=blog.gerardroche.com
[ParaTest]: https://github.com/paratestphp/paratest?ref=blog.gerardroche.com
[Pest]: https://pestphp.com?ref=blog.gerardroche.com
[PowerShell]: https://learn.microsoft.com/en-us/powershell/?ref=blog.gerardroche.com
[Tmux]: https://github.com/tmux/tmux/wiki?ref=blog.gerardroche.com
[cmd]: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd?ref=blog.gerardroche.com
[iTerm2]: https://iterm2.com?ref=blog.gerardroche.com
[xterm]: https://invisible-island.net/xterm/?ref=blog.gerardroche.com
