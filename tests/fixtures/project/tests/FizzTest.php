<?php

declare(strict_types=1);

namespace GerardRoche\PHPUnitKitTest;

use PHPUnit\Framework\TestCase;

final class FizzTest extends TestCase
{
    public function testAssertTrue()
    {
        $fizz = new Fizz();

        $this->assertIsObject($fizz);
    }
}
