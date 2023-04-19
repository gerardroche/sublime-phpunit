<?php

declare(strict_types=1);

namespace GerardRoche\PHPUnitKitTest;

use PHPUnit\Framework\TestCase;

final class LastTest extends TestCase
{
    public function testAssertTrue()
    {
        $last = new Last();

        $this->assertIsObject($last);
        $this->assertIsObject($last);
        $this->assertIsObject($last);
    }

    public function testAssertFalse()
    {
        $last = new Last();

        $this->assertIsNotArray($last);
        $this->assertIsNotArray($last);
        $this->assertIsNotArray($last);
    }
}
