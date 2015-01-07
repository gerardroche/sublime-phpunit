# phpunit

phpunit plugin for Sublime Text. Provides decent PHPUnit support.

**Sublime Text 3 only**

[1.0.0 Roadmap](https://github.com/gerardroche/sublime-phpunit/issues/1)

## Overview

* [Features](#features)
* [Key Bindings](#key-bindings)
* [Commands](#commands)
* [Installation](#installation)
* [Similar Plugins](#similar-plugins)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Complementary Plugins](#complementary-plugins)
* [Credits](#credits)
* [License](#license)

## Features

* Run all tests
* Run a single test-case
* Run a single test by placing cursor on test method
* Run last test
* Toggle between test-case and class-under-test
* Jump to test failure file/line-number

PHPUnit is executed with the first configuration file, either `phpunit.xml` or `phpunit.xml.dist`, in the active view file directory or the nearest common ancestor directory in current open folders. e.g.

    +--- /home/user/code/php-form/src/Form/Command.php
    +--- /home/user/code/php-form/test/Form/CommandTest.php
    +--- /home/user/code/php-router/src/Router/Route.php
    +--- /home/user/code/php-router/test/Router/RouteTest.php

When the active view is `RouteTest.php` the following locations are checked for a PHPUnit configuration file:

* `/home/user/code/php-router/test/Router/phpunit.xml`
* `/home/user/code/php-router/test/Router/phpunit.xml.dist`
* `/home/user/code/php-router/test/phpunit.xml`
* `/home/user/code/php-router/test/phpunit.xml.dist`
* `/home/user/code/php-router/phpunit.xml`
* `/home/user/code/php-router/phpunit.xml.dist`
* `/home/user/code/phpunit.xml`
* `/home/user/code/phpunit.xml.dist`

## Key Bindings

| OS X | Windows / Linux | Descriptions |
|------|-----------------|--------------|
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run all tests |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run single test or test-case |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Run last test |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch class-under-test/test-case |
| <kbd>F4</kbd> | <kbd>F4</kbd> | Jump to test failure file/line-number |

## Commands

#### phpunit

Executes PHPUnit

Options:

* **working_dir** [String]: Required
* **unit_test_or_directory** [String]: Optional
* **options** [Dict]: Optional
    - TODO :memo: document PHPUnit command options

## Installation

### Manual installation

1. Download or clone this repository to a directory "phpunit" in the Sublime Text Packages directory for your platform:
    * Sublime Text 3
        - Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunit`
        - OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunit`
        - Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunit`
2. Restart Sublime Text to complete installation. The features listed above should now be available.

## Similar Plugins

TODO: Similar Plugins

## Known Bugs

* [F4 navigates to symlinked file out of sync with project](https://github.com/SublimeTextIssues/Core/issues/611)

## Contributing

Issue reports and pull requests are always welcome.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Complementary Plugins

* [php-completions]
* [php-grammar]
* [php-snippets]
* [phpunit-completions]
* [phpunit-snippets]
* [phpunit]

## Credits

TODO: Credits

## License

phpunit is released under the [BSD 3-Clause License][license].

[license]: LICENSE
[Package Control]: https://packagecontrol.io
[php-completions]: https://github.com/gerardroche/sublime-phpck
[php-fig]: http://www.php-fig.org
[php-grammar]: https://github.com/gerardroche/sublime-php-grammar
[php-snippets]: https://github.com/gerardroche/sublime-php-snippets
[phpunit-completions]: https://github.com/gerardroche/sublime-phpunitck
[phpunit-snippets]: https://github.com/gerardroche/sublime-phpunit-snippets
[phpunit]: https://github.com/gerardroche/sublime-phpunit
[semver]: http://semver.org
