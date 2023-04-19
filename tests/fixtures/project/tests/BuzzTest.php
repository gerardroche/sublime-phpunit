<?php

declare(strict_types=1);

namespace GerardRoche\PHPUnitKitTest;

use PHPUnit\Framework\TestCase;

final class BuzzTest extends TestCase
{
    public function testAssertTrue()
    {
        $buzz = new Buzz();

        $this->assertIsObject($buzz);
        $this->assertIsObject($buzz);
    }
}
