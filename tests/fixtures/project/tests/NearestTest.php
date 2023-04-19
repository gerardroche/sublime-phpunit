<?php

declare(strict_types=1);

namespace GerardRoche\PHPUnitKitTest;

use PHPUnit\Framework\TestCase;

final class NearestTest extends TestCase
{
    public function testFour()
    {
        $this->assertIsInt(4);
        $this->assertIsInt(4);
        $this->assertIsInt(4);
        $this->assertIsInt(4);
    }

    public function testFive()
    {
        $this->assertIsInt(5);
        $this->assertIsInt(5);
        $this->assertIsInt(5);
        $this->assertIsInt(5);
        $this->assertIsInt(5);
    }

    public function testSize()
    {
        $this->assertIsInt(6);
        $this->assertIsInt(6);
        $this->assertIsInt(6);
        $this->assertIsInt(6);
        $this->assertIsInt(6);
        $this->assertIsInt(6);
    }
}
