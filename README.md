# WHAT PHPUNITKIT IS

[![Author](https://img.shields.io/badge/author-@gerardroche-blue.svg?style=flat-square&maxAge=86400)](https://twitter.com/gerardroche) [![Source Code](https://img.shields.io/badge/source-GitHub-blue.svg?style=flat-square&maxAge=86400)](https://github.com/gerardroche/sublime-phpunit) [![License](https://img.shields.io/badge/license-BSD--3-blue.svg?style=flat-square&maxAge=86400)](LICENSE) [![GitHub stars](https://img.shields.io/github/stars/gerardroche/sublime-phpunit.svg?style=flat-square&maxAge=86400)](https://github.com/gerardroche/sublime-phpunit/stargazers) [![Sublime version](https://img.shields.io/badge/sublime-v3.0.0-green.svg?style=flat-square&maxAge=86400)](https://sublimetext.com) [![Latest version](https://img.shields.io/github/tag/gerardroche/sublime-phpunit.svg?style=flat-square&maxAge=86400&label=release)](https://github.com/gerardroche/sublime-phpunit/tags) [![Downloads](https://img.shields.io/packagecontrol/dt/phpunitkit.svg?style=flat-square&maxAge=86400)](https://packagecontrol.io/packages/phpunitkit)

PHPUNITKIT is a plugin that provides [PHPUnit](https://phpunit.de) support in [Sublime Text](https://sublimetext.com). It provides an abstraction over running tests from the command-line. It works best alongside other PHP development plugins such as [PHP Grammar], [PHP Snippets], and [PHP Completions].

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

* Zero configuration required; Does the Right Thing™
* Fully customized CLI options configuration
* Supports [Composer]
* Run test suite <kbd>Ctrl+Shift+t</kbd>
* Run test case <kbd>Ctrl+Shift+r</kbd>
* Run test method <kbd>Ctrl+Shift+r</kbd> (put cursor on test method)
* Run test methods <kbd>Ctrl+Shift+r</kbd> (use multiple cursor selection of test method)
* Run test case for current class under test <kbd>Ctrl+Shift+r</kbd>
* Rerun last test(s) <kbd>Ctrl+Shift+e</kbd>
* Test results output in color (including color failure diffs)
* Jump to next <kbd>F4</kbd> / previous failure <kbd>Shift+F4</kbd> (navigates to file line number of failure)
* Switch, split, and focus test case &amp; class under test <kbd>Ctrl+Shift+.</kbd>

## COMMANDS

* PHPUnit: Run All Tests <kbd>Ctrl+Shift+t</kbd>
* PHPUnit: Run Last Test <kbd>Ctrl+Shift+e</kbd>
* PHPUnit: Run Single Test <kbd>Ctrl+Shift+r</kbd>
* PHPUnit: Switch Test Case / Class Under Test <kbd>Ctrl+Shift+.</kbd>
* PHPUnit: Open HTML Code Coverage in Browser
* PHPUnit: Toggle Option --debug
* PHPUnit: Toggle Option --disallow-test-output
* PHPUnit: Toggle Option --disallow-todo-tests
* PHPUnit: Toggle Option --enforce-time-limit
* PHPUnit: Toggle Option --no-coverage
* PHPUnit: Toggle Option --report-useless-tests
* PHPUnit: Toggle Option --stop-on-error
* PHPUnit: Toggle Option --stop-on-failure
* PHPUnit: Toggle Option --stop-on-incomplete
* PHPUnit: Toggle Option --stop-on-risky
* PHPUnit: Toggle Option --stop-on-skipped
* PHPUnit: Toggle Option --strict-coverage
* PHPUnit: Toggle Option --strict-global-state
* PHPUnit: Toggle Option --tap
* PHPUnit: Toggle Option --testdox
* PHPUnit: Toggle Option --verbose

## KEY BINDINGS

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

## CONFIGURATION

phpunitkit goes to great lengths to predict how to invoke PHPUnit for the project environment.

For example, if PHPUnit is installed via [Composer] for the current project then the PHPUnit command-line test runner is invoked through `vendor/bin/phpunit`, otherwise it is assumed PHPUnit is available on the system path and so is invoked via `phpunit`.

Another example is, if `phpunit.xml` or `phpunit.xml.dist` (in that order) is found in the current or the nearest common ancestor directory of the active view, the location is set as the current working directory when invoking PHPUnit and so the configuration will be automatically read by PHPunit. Placing PHPUnit configuration files at the root of a project is highly recommended.

> If `phpunit.xml` or `phpunit.xml.dist` (in that order) exist in the current working directory and `--configuration` is not used, the configuration will be automatically read from that file. &mdash; [PHPUnit Manual](https://phpunit.de/manual/current/en/textui.html)

### Specifying PHPUnit Command-Line Options

PHPUnit's core functionality can be configured via its [XML Configuration File](https://phpunit.de/manual/current/en/appendixes.configuration.html).

[Command-Line Options](https://phpunit.de/manual/current/en/textui.html#textui.clioptions) can be specified explicitly via sublime text settings.

#### Example &mdash; PHPUnit XML Configuration

```
<?xml version="1.0" encoding="UTF-8"?>
<phpunit verbose="true"
         stopOnFailure="true"
         >

    <php>
        <ini name="display_errors" value="1" />
        <ini name="xdebug.scream" value="0" />
    </php>

    <testsuites>
        <testsuite name="unit">
             <directory>test</directory>
        </testsuite>
    </testsuites>

    <filter>
        <whitelist processUncoveredFilesFromWhitelist="true">
            <directory>src</directory>
        </whitelist>
    </filter>

</phpunit>
```

#### Example &mdash; PHPUnit Command-Line Options

##### Command-Line Options can be specified Per-Project.

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.options": {
            "v": true,
            "stop-on-failure": true,
            "no-coverage": true,
            "d": [
                "display_errors=1",
                "xdebug.scream=0"
            ]
        }
    }
}
```

The above settings result in the following Command-Line Options being passed to PHPUnit:

```
--stop-on-failure -d "display_errors=1" -d "xdebug.scream=0" -v --no-coverage
```

##### Command-Line Options can be specified as User level settings.

`Preferences > Settings - User`

*Note: the `settings` key is not required for User level settings like it is for Per-Project settings.*

```json
{
    "phpunit.options": {
        "v": true,
        "stop-on-failure": true,
        "no-coverage": true,
        "d": [
            "display_errors=1",
            "xdebug.scream=0"
        ]
    }
}
```

The above settings result in the following Command-Line Options being passed to PHPUnit:

```
--stop-on-failure -d "display_errors=1" -d "xdebug.scream=0" -v --no-coverage
```

### Settings

Key | Description | Type | Default
----|-------------|------|--------
`phpunit.options` | Command-line options to pass to PHPUnit. See [`phpunit --help`](https://phpunit.de/manual/current/en/textui.html#textui.clioptions) for an up-to-date list of command-line options. | `dict` | `{}`
`phpunit.keymaps` | Enable the default keymaps. | `boolean` | `true`
`phpunit.keymaps.vi` | Enable the default vi keymaps (requires `phpunit.keymaps` to be enabled). | `boolean` | `false`
`phpunit.composer` | Enable [Composer] support. If a Composer installed PHPUnit is found then it is used to run tests. | `boolean` | `true`
`phpunit.save_all_on_run` | Enable writing out every buffer (active window) with changes and a file name, on test runs. | `boolean` | `true`

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

## INSTALLATION

Works best alongside [PHP Grammar], [PHP Completions], and [PHP Snippets].

### Package Control

The preferred method of installation is [Package Control].

### Manual

1. Close Sublime Text.
2. Download or clone this repository to a directory named **`phpunitkit`** in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunitkit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunitkit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunitkit`
3. Done!

## CONTRIBUTING

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
5. Restart Windows

### Running tests

To be able to run the tests enable plugin development. This will make the command "PHPUnit: Run all Plugin Tests" available in the Command Palette.

Preferences > Settings - User

```
{
    "phpunit.development": true
}
```

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md).

## CREDITS

Based initially on [maltize/sublime-text-2-ruby-tests](https://github.com/maltize/sublime-text-2-ruby-tests) and [stuartherbert/sublime-phpunit](https://github.com/stuartherbert/sublime-phpunit).

## LICENSE

Released under the [BSD 3-Clause License](LICENSE).

[Package Control]: https://packagecontrol.io/browse/authors/gerardroche
[PHP Grammar]: https://packagecontrol.io/browse/authors/gerardroche
[PHP Completions]: https://packagecontrol.io/browse/authors/gerardroche
[PHP Snippets]: https://packagecontrol.io/browse/authors/gerardroche
[PHPUnit]: https://packagecontrol.io/browse/authors/gerardroche
[Composer]: https://getcomposer.org
