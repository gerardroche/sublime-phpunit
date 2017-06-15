# WHAT PHPUNITKIT IS

[![Build Status](https://travis-ci.org/gerardroche/sublime-phpunit.svg?branch=master)](https://travis-ci.org/gerardroche/sublime-phpunit) [![Build status](https://ci.appveyor.com/api/projects/status/wknvpma8qgjlqh1q/branch/master?svg=true)](https://ci.appveyor.com/project/gerardroche/sublime-phpunit/branch/master) [![Minimum Sublime version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg)](https://sublimetext.com) [![Downloads](https://img.shields.io/packagecontrol/dt/phpunitkit.svg)](https://packagecontrol.io/packages/phpunitkit) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg)](https://github.com/gerardroche/sublime-phpunit/stargazers) [![Latest Stable Version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?label=stable)](https://github.com/gerardroche/sublime-phpunit/tags) [![Source Code](https://img.shields.io/badge/source-github-blue.svg)](https://github.com/gerardroche/sublime-phpunit) [![Author](https://img.shields.io/badge/author-gerardroche-blue.svg)](https://twitter.com/gerardroche)

PHPUnitKit is a plugin that provides PHPUnit support in Sublime Text. It provides an abstraction over running tests from the command-line.

![Screenshot](screenshot.png)

## OVERVIEW

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## FEATURES

* Run Nearest Test
* Run Test File
* Run Test Suite
* Run Last Test
* Supports Composer
* Zero configuration required; Does the Right Thing
* Supports colour results (including diffs)
* Fully customized CLI options configuration
* Jump to next and jump to previous failure
* Switch Test File (splits window and puts test case and class under test side by side)

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

## USAGE

Command | Description
--------|------------
`:TestSuite` | Run test suite of the current file.
`:TestFile` | Run tests for the current file. If the current file is not a test file, it runs tests of the test file for the current file.
`:TestNearest` | Run a test nearest to the cursor (supports multiple selections). If the current file is not a test file, it runs tests of the test file for the current file.
`:TestLast` | Run the last test.
`:TestVisit` | Open the last run test in the current window (useful when you're trying to make a test pass, and you dive deep into application code and close your test buffer to make more space, and once you've made it pass you want to go back to the test file to write more tests).
`:TestSwitch` | Splits the window and puts nearest test case and class under test side by side.
`:TestResults` | Show the test results panel.
`:TestCancel` | Cancels current test run.
`:TestCoverage` | Open code coverage in browser.
`:ToggleOption*` | Toggle PHPUnit CLI options.

* Jump to Next Failure: <kbd>F4</kbd>
* Jump to Previous Failure: <kbd>Shift</kbd>+<kbd>F4</kbd>

Windows / Linux | OS X | Command
--------------- | ---- | -------
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | `:TestSuite`
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | `:TestNearest`
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | `:TestLast`
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | `:TestSwitch`

Vintage / [NeoVintageous](https://github.com/NeoVintageous/NeoVintageous)

Keymap | Command
-----------------------|--------
<kbd>,a</kbd> | `:TestSuite`
<kbd>,T</kbd> | `:TestFile`
<kbd>,t</kbd> | `:TestNearest`
<kbd>,l</kbd> | `:TestLast`
<kbd>,.</kbd> | `:TestSwitch`

## CONFIGURATION

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.options` | Command-line options to pass to PHPUnit. See [PHPUnit usage](https://phpunit.de/manual/current/en/textui.html#textui.clioptions) for an up-to-date list of command-line options. | `dict` | `{}`
`phpunit.composer` | Enable Composer support (if a Composer installed PHPUnit is found then it is used to run the tests, otherwise the system PATH is used to find PHPUnit). | `boolean` | `true`
`phpunit.save_all_on_run` | Enable writing out every buffer with changes in active window before running tests. | `boolean` | `true`
`phpunit.php_executable` | Path to PHP executable used to run PHPUnit (if not set then the system PATH is used to find PHP). | `string` | Uses the system PATH
`phpunit.php_versions_path` | Location of `.php-version` file PHP versions. | `string` | `~/.phpenv/versions`
`phpunit.keymaps` | Enable the default keymaps. | `boolean` | `true`
`phpunit.vi_keymaps` | Enable the default vi keymaps. | `boolean` | `true`

### Composer

If a Composer installed PHPUnit is found then it is used to run the tests, otherwise the system PATH is used to find PHPUnit. To disable Composer support:

`Menu > Preferences > Settings`

```json
{
    "phpunit.composer": false
}
```

You can also disable it per-project:

`Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.composer": false
    }
}
```

### PHP executable

Path to PHP executable used to run PHPUnit, otherwise the system PATH is used to find PHP. To set a default executable other than the one one the one found on system PATH (`~` and environment variables e.g. `$HOME` are expanded):

`Menu > Preferences > Settings`

```json
{
    "phpunit.php_executable": "~/.phpenv/versions/7.x/bin/php"
}
```

You can also set it per-project:

`Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.php_executable": "~/.phpenv/versions/7.x/bin/php"
    }
}
```

### PHP versions path

You can set a location to find different PHP versions and use `.php-version` files to select versions per-project. The default location is of PHP versions is `~/.phpenv/versions`. The structure of the versions directory should be:

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

To specify a version from the versions path to use for a project, create a file named `.php-version` with the name of the version as its contents and place it in the root of your project. For example, a `.php-version` file with the contents `7.1.4` and a PHP versions path of `~/.phpenv/versions` will expand to the PHP version at `~/.phpenv/versions/7.1.4/bin/php` on Linux and `~/.phpenv/versions/7.1.4/php` on Windows.

You can specify a PHP versions path other than the default:

`Menu > Preferences > Settings`

```json
{
    "phpunit.php_versions_path": "~/.phpenv/versions"
}
```

You can also set it per-project:

`Menu > Project > Edit Project`

```json
{
    "settings": {
        "phpunit.php_versions_path": "~/.phpenv/versions"
    }
}
```

### Options

To set PHPUnit options:

`Menu > Preferences > Settings`

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

You can also set them per-project:

`Menu > Project > Edit Project`

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

## CONTRIBUTING

Your issue reports and pull requests are welcome.

### Tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input "phpunitkit" as the package to test.

### Debugging

Debug messages are disabled by default. To enable them set the environment variable SUBLIME_PHPUNIT_DEBUG to a non-blank value. Debug messages are output to the Console (not the tests results output panel). Open the console via `Menu > View > Console` or click the icon in the bottom right of the status bar.

Below are detailed explanations on how to set environment variables for each OS. For more information on environment variables read [What are PATH and other environment variables, and how can I set or use them?](http://superuser.com/questions/284342/what-are-path-and-other-environment-variables-and-how-can-i-set-or-use-them).

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

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md).

## CREDITS

Based initially on [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests) and [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit). Also inspired by [janko-m/vim-test](https://github.com/janko-m/vim-test).

## LICENSE

Released under the [BSD 3-Clause License](LICENSE).
