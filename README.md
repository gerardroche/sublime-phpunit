# WHAT PHPUNITKIT IS

[![Build Status](https://travis-ci.org/gerardroche/sublime-phpunit.svg?branch=master)](https://travis-ci.org/gerardroche/sublime-phpunit) [![Build status](https://ci.appveyor.com/api/projects/status/wknvpma8qgjlqh1q/branch/master?svg=true)](https://ci.appveyor.com/project/gerardroche/sublime-phpunit/branch/master) [![Minimum Sublime version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Downloads](https://img.shields.io/packagecontrol/dt/phpunitkit.svg?style=flat-square)](https://packagecontrol.io/packages/phpunitkit) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat-square)](https://github.com/gerardroche/sublime-phpunit/stargazers) [![Latest Stable Version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?style=flat-square&label=release)](https://github.com/gerardroche/sublime-phpunit/tags) [![Source Code](https://img.shields.io/badge/source-GitHub-blue.svg?style=flat-square)](https://github.com/gerardroche/sublime-phpunit) [![Author](https://img.shields.io/badge/author-@gerardroche-blue.svg?style=flat-square)](https://twitter.com/gerardroche)

Phpunitkit is a plugin that provides [PHPUnit](https://phpunit.de) support in [Sublime Text](https://sublimetext.com). It provides an abstraction over running tests from the command-line.

![Screenshot](screenshot.png)

## OVERVIEW

* [Features](#features)
* [Commands](#commands)
* [Key Bindings](#key-bindings)
* [Configuration](#configuration)
* [Installation](#installation)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## FEATURES

* Zero configuration required; Does the Right Thing
* Test Suite, Test File, Test Nearest, Test Last, and other commands
* Supports [Composer](https://getcomposer.org)
* Supports colour test results (including failure diffs)
* Jump to next/previous test failure via keybinding <kbd>F4</kbd>/<kbd>Shift+F4</kbd>
* Switch File (splits window and puts test case and class under test side by side)
* Fully customized CLI options configuration

## COMMANDS

*All commands in the Command Palette are prefixed with "PHPUnit: ".*

Command | Description
--------|------------
Test Suite | Runs the whole test suite.
Test File | Runs all the tests in the current file test case.
Test Nearest | Runs the test nearest to the cursor. A multiple selection can used to used to run several tests at once.
Test Last | Runs the last test.
Switch File | Splits the window and puts nearest test case and class under test side by side.
Show Results | Show the test results panel.
Open Code Coverage | Open code coverage in browser.
Toggle Option &lt;option&gt; | Toggle PHPUnit CLI options.

## KEY BINDINGS

OS X | Windows / Linux | Command
-----|-----------------|------------
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Test Suite
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Test Nearest
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Test Last
<kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch File
<kbd>F4</kbd> | <kbd>F4</kbd> | Jump to next failure
<kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Jump to previous failure

Vim/Vintage/Vintageous/[NeoVintageous](https://github.com/NeoVintageous/NeoVintageous) | Command
-----------------------|--------
<kbd>,</kbd><kbd>a</kbd> | Test Suite
<kbd>,</kbd><kbd>T</kbd> | Test File
<kbd>,</kbd><kbd>t</kbd> | Test Nearest
<kbd>,</kbd><kbd>l</kbd> | Test Last
<kbd>,</kbd><kbd>.</kbd> | Switch File

## CONFIGURATION

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.options` | Command-line options to pass to PHPUnit. See [PHPUnit usage](https://phpunit.de/manual/current/en/textui.html#textui.clioptions) for an up-to-date list of command-line options. | `dict` | `{}`
`phpunit.composer` | Enable Composer support. If a Composer installed PHPUnit executable is found then it is used to run tests. | `boolean` | `true`
`phpunit.save_all_on_run` | Enable writing out every buffer with changes in active window before running tests. | `boolean` | `true`
`phpunit.php_executable` | Default PHP executable used to run PHPUnit. If not set then the first PHP available found on the system PATH is used. | `string` | Uses PHP available on system path
`phpunit.php_versions_path` | Location of `.php-version` file versions. | `string` | `~/.phpenv/versions`
`phpunit.keymaps` | Enable the default keymaps. | `boolean` | `true`
`phpunit.vi_keymaps` | Enable the default vi keymaps. | `boolean` | `true`

### Composer

If a Composer installed PHPUnit executable is found then it is used to run tests, otherwise PHPUnit is assumed to be available via the system path.

To disable running tests via Composer installed PHPUnit: `Preferences > Settings`

```json
{
    "phpunit.composer": false
}
```

Or disable it per-project: `Project > Edit Project`

```json
{
    "settings": {
        "phpunit.composer": false
    }
}
```

### PHP executable

You can use a default PHP executable for running PHPUnit.

Set it globally: `Preferences > Settings`

```json
{
    "phpunit.php_executable": "~/.phpenv/versions/7.x/bin/php"
}
```

Or set it per-project: `Project > Edit Project`

```json
{
    "settings": {
        "phpunit.php_executable": "~/.phpenv/versions/7.x/bin/php"
    }
}
```

### PHP versions path

You can specific a location to find different PHP versions for running PHPUnit. The default location is `~/.phpenv/versions`. To specify the version to use for your project create a file named `.php-version` and place it in the root of your project (where the project phpunit.xml configuration file is located). For example a `.php-version` file with the contents `7.x` will mean the PHP executable located at `~/.phpenv/versions/7.x/bin/php` will be used to run PHPUnit.

To change the path set it globally: `Preferences > Settings`

```json
{
    "phpunit.php_versions_path": "~/.phpenv/versions"
}
```

Or set it per-project: `Project > Edit Project`

```json
{
    "settings": {
        "phpunit.php_versions_path": "~/.phpenv/versions"
    }
}
```

### Options

Set them globally: `Preferences > Settings`

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

Or set them per-project: `Project > Edit Project`

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

Both of the above configurations translate to the following PHPUnit options:

```
phpunit -d "display_errors=1" -d "xdebug.scream=0" --verbose --no-coverage
```

It is recommended to use your [phpunit.xml](https://phpunit.de/manual/current/en/appendixes.configuration.html) configuration file if you want some CLI options to stick around. Place it at the root of your project.

```
<?xml version="1.0" encoding="UTF-8"?>
<phpunit verbose="true">
    <php>
        <ini name="display_errors" value="1" />
        <ini name="xdebug.scream" value="0" />
    </php>
    <testsuites>
        <testsuite>
             <directory>tests</directory>
        </testsuite>
    </testsuites>
    <filter>
        <whitelist processUncoveredFilesFromWhitelist="true">
            <directory>src</directory>
        </whitelist>
    </filter>
</phpunit>
```

## INSTALLATION

### Package Control installation

The preferred method of installation is [Package Control](https://packagecontrol.io/browse/authors/gerardroche).

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named **`phpunitkit`** in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunitkit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunitkit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunitkit`
3. Done!

## CONTRIBUTING

Your issue reports and pull requests are welcome.

### Debugging

Debug messages are output to the Console (not the tests results output panel). Open the console: `Menu > View > Console` or click the icon in the bottom right of the status bar.

Debug messages are disabled by default. To enable them set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=y`. To disable them set unset it or set it to a blank value e.g. `SUBLIME_PHPUNIT_DEBUG=`.

For more information on environment variables read [What are PATH and other environment variables, and how can I set or use them?](http://superuser.com/questions/284342/what-are-path-and-other-environment-variables-and-how-can-i-set-or-use-them)

#### Linux

Sublime Text can be started at the Terminal with an exported environment variable.

```
$ export SUBLIME_PHPUNIT_DEBUG=y; subl
```

To set the environment permanently set it in `~/.profile` (requires restart).

```
export SUBLIME_PHPUNIT_DEBUG=y
```

Alternatively, create a [debug script (subld)](https://github.com/gerardroche/dotfiles/blob/1a27abed589f2fea9126a0496ef4d1cae0479722/src/bin/subld) with debugging environment variables enabled.

#### Windows

Sublime Text can be started at the Command Prompt with an exported environment variable.

```
> set SUBLIME_PHPUNIT_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"
```

To set the environment permanently set it as a *system* environment variable (requires restart).

1. Control Panel > System and Security > System > Advanced system settings
2. Advanced > Environment Variables
3. System variables > New...
4. Add Variable name `SUBLIME_PHPUNIT_DEBUG` with Variable value `y`
5. Restart Windows

### Tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input "phpunitkit" as the package to test.

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md).

## CREDITS

Based initially on [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests) and [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit). Also inspired by [janko-m/vim-test](https://github.com/janko-m/vim-test).

## LICENSE

Released under the [BSD 3-Clause License](LICENSE).
