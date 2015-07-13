# sublime-phpunit

sublime-phpunit plugin for Sublime Text 3. Provides decent PHPUnit support.

![Screenshot](screenshot.png)

## Overview

* [Features](#features)
* [Commands](#commands)
* [Key Bindings](#key-bindings)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [Installation](#installation)
* [Changelog](#changelog)
* [Complementary Plugins](#complementary-plugins)
* [Credits](#credits)
* [License](#license)

## Features

* Run all tests
* Run single test-case
* Run single test method
* Run multiple test methods *(using multiple selection)*
* Run the test-case for current class
* Rerun last test
* Jump to next and previous failure file linenumber
* Switch, split, and focus on class and test-case
* Composer support
* Test results in colour including failure diffs

## Commands

* `PHPUnit: Run All Tests`
* `PHPUnit: Run Single Test`
* `PHPUnit: Run Last Test`
* `PHPUnit: Toggle TAP format`
* `PHPUnit: Toggle Textdox format`
* `PHPUnit: Switch Test/Implementation`
* `PHPUnit: Open HTML Code Coverage in Browser`

## Key Bindings

| OS X | Windows / Linux | Description |
|------|-----------------|--------------|
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run all tests |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run single test-case / test method(s) |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Rerun last test |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch test / implementation |
| <kbd>F4</kbd> | <kbd>F4</kbd> | Goto to next test failure file line number |
| <kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Goto to previous test failure file line number |

Keymaps are enabled by default. To disable them set `"phpunit.keymaps": false` in User Settings. Access this file from `Preferences > Settings - User` menu item.

Vintage/Vintageous keymaps are disabled by default. To enable them set `"phpunit.vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

| OS X / Windows / Linux | Description |
|------------------------|--------------|
| <kbd>,</kbd><kbd>t</kbd> | Run all tests |
| <kbd>,</kbd><kbd>r</kbd> | Run single test-case / test method(s) |
| <kbd>,</kbd><kbd>e</kbd> | Rerun last test |
| <kbd>,</kbd><kbd>.</kbd> | Switch test / implementation |

## Configuration

### User settings

`Preferences > Settings - User`

```json
{
    "phpunit.save_all_on_run": false
}
```

### Per-project settings

Set per-project settings in the project definition.

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.save_all_on_run": false
    }
}
```

### Settings

**`phpunit.color_scheme`** `<string|null>` Default is monokai

The colour scheme to use for test results. To set no colour scheme set to null. The bundled schemes are:

* `Packages/phpunit/color-schemes/monokai.hidden-tmTheme` (default)
* `Packages/phpunit/color-schemes/monokai-extended-seti.hidden-tmTheme`
* `Packages/phpunit/color-schemes/solarized-dark.hidden-tmTheme`

**`phpunit.keymaps`** `<bool>` Default is true

**`phpunit.vi_keymaps`** `<bool>` Default is false

**`phpunit.save_all_on_run`** `<bool>` Default is true

**`phpunit.development`** `<bool>` Default is false

## Contributing

Issue reports and pull requests are always welcome.

**Running the tests**

Enable development mode (see the configuration section) and run "PHPUnit: Run all Plugin Tests" from the command palette.

**Debug messages**

Debug messages are disabled by default. To enable debug messages set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=yes`. To disable set it to a blank value e.g. `SUBLIME_PHPUNIT_DEBUG=`.

On Linux, for example, Sublime Text can be opened at a Terminal with an exported environment variable:

```sh
export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text
```

## Installation

1. Close Sublime Text
2. Download or clone this repository to a directory named `phpunit` in the Sublime Text Packages directory for the platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunit`
3. Done. The features listed above should now be available.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Complementary Plugins

* [PHPUnit Completions](https://github.com/gerardroche/sublime-phpunitck)
* [PHPUnit Snippets](https://github.com/gerardroche/sublime-phpunit-snippets)
* [PHP Grammar](https://github.com/gerardroche/sublime-php-grammar)
* [PHP Completions](https://github.com/gerardroche/sublime-phpck)
* [PHP Snippets](https://github.com/gerardroche/sublime-php-snippets)

## Credits

sublime-phpunit is based initially on [Sublime Text Ruby Tests](https://github.com/maltize/sublime-text-2-ruby-tests).

## License

sublime-phpunit is released under the [BSD 3-Clause License](LICENSE).
