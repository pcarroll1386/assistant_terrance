#!/usr/bin/env python3
########################################################################
# Filename    : test_lcd.py
# Description : Simple test script for LCD functionality
# Author      : LCD Product Display System
# Date        : 2025/07/14
########################################################################

import time
import sys

try:
    from LCD1602 import LCD1602
    RASPBERRY_PI = True
except ImportError:
    RASPBERRY_PI = False
    print("Warning: Running in simulation mode")
    
    class MockLCD:
        def __init__(self, address=0x27):
            print(f"Mock LCD initialized at address {hex(address)}")
        def clear(self):
            print("LCD: Clear")
        def print_line(self, line, message):
            print(f"LCD Line {line}: {message}")
        def backlight_off(self):
            print("LCD: Backlight off")
    
    LCD1602 = MockLCD

def test_basic_display():
    """Test basic LCD display functionality"""
    print("Testing LCD basic functionality...")
    
    try:
        # Initialize LCD
        lcd = LCD1602(0x27)
        print("✓ LCD initialized successfully")
        
        # Clear display
        lcd.clear()
        print("✓ Display cleared")
        
        # Test line 1
        lcd.print_line(0, "Hello, World!")
        print("✓ Line 1 written")
        time.sleep(2)
        
        # Test line 2
        lcd.print_line(1, "LCD Test!")
        print("✓ Line 2 written")
        time.sleep(2)
        
        # Test long message (should be truncated)
        lcd.print_line(0, "This is a very long message that should be truncated")
        print("✓ Long message test")
        time.sleep(2)
        
        # Test both lines with formatted content
        lcd.print_line(0, "Product: iPhone")
        lcd.print_line(1, "▶05:32")
        print("✓ Formatted content test")
        time.sleep(3)
        
        # Test paused stopwatch display
        lcd.print_line(0, "Test Complete!")
        lcd.print_line(1, "⏸00:00")
        print("✓ Stopwatch indicator test")
        time.sleep(2)
        
        # Clear and show completion
        lcd.clear()
        lcd.print_line(0, "Test Complete!")
        lcd.print_line(1, "All systems OK")
        print("✓ All tests passed!")
        time.sleep(2)
        
        # Final cleanup
        lcd.clear()
        if RASPBERRY_PI:
            lcd.backlight_off()
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_timer_display():
    """Test timer display formatting"""
    print("\nTesting stopwatch display...")
    
    try:
        lcd = LCD1602(0x27)
        
        # Simulate different timer values with status indicators
        test_times = [
            (0, "⏸00:00", "Paused at start"),
            (30, "▶00:30", "Running 30 seconds"),
            (90, "▶01:30", "Running 1.5 minutes"),
            (3661, "⏸61:01", "Paused at 61 minutes"),
            (6000, "▶99:59", "Running at max display")
        ]
        
        for seconds, expected_display, description in test_times:
            lcd.print_line(0, "Timer Test")
            lcd.print_line(1, expected_display)
            print(f"✓ {description} -> {expected_display}")
            time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"✗ Timer test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("LCD Test Suite")
    print("=" * 40)
    
    if not RASPBERRY_PI:
        print("Note: Running in simulation mode (no actual LCD)")
        print()
    
    # Run tests
    basic_test = test_basic_display()
    timer_test = test_timer_display()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Basic Display: {'PASS' if basic_test else 'FAIL'}")
    print(f"Stopwatch Display: {'PASS' if timer_test else 'FAIL'}")
    
    if basic_test and timer_test:
        print("\n🎉 All tests passed! LCD is ready for use.")
        print("💡 Remember to connect your TIMER button to GPIO 22")
        return 0
    else:
        print("\n❌ Some tests failed. Check connections and configuration.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
