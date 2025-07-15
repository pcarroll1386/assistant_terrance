#!/usr/bin/env python3
########################################################################
# Filename    : demo.py
# Description : Demo script showing the LCD system in action
# Author      : LCD Product Display System
# Date        : 2025/07/14
########################################################################

import time
import random

class DemoLCD:
    """Demo LCD class that prints to console"""
    def __init__(self, address=0x27):
        print(f"🖥️  Demo LCD initialized at I2C address {hex(address)}")
        print("📱 Simulating 16x2 LCD display")
        print("-" * 20)
    
    def clear(self):
        print("\n" + "🧹 CLEAR DISPLAY".center(20))
    
    def print_line(self, line, message):
        # Format message to 16 characters
        formatted = str(message)[:16].ljust(16)
        print(f"│{formatted}│ <- Line {line}")
    
    def backlight_off(self):
        print("💡 Backlight OFF")

def demo_basic_functionality():
    """Demonstrate basic LCD functionality"""
    print("🎬 Demo: Basic LCD Functionality")
    print("=" * 40)
    
    lcd = DemoLCD(0x27)
    time.sleep(1)
    
    # Show initialization
    lcd.clear()
    lcd.print_line(0, "Initializing...")
    lcd.print_line(1, "Please wait...")
    time.sleep(2)
    
    # Show product display
    products = [
        "Apple iPhone 15",
        "Samsung Galaxy",
        "Google Pixel 8",
        "iPad Pro 12.9",
        "MacBook Air M2"
    ]
    
    print("\n🔄 Simulating product navigation...")
    for i, product in enumerate(products):
        lcd.clear()
        lcd.print_line(0, product)
        lcd.print_line(1, f"Time: {i:02d}:{(i*15)%60:02d}")
        print(f"   (Button press {i+1} - Product {i+1})")
        time.sleep(1.5)
    
    # Show timer progression
    print("\n⏱️  Simulating timer updates...")
    lcd.clear()
    lcd.print_line(0, "Final Product")
    for seconds in range(0, 65, 5):
        minutes = seconds // 60
        secs = seconds % 60
        lcd.print_line(1, f"Time: {minutes:02d}:{secs:02d}")
        time.sleep(0.5)
    
    # Shutdown sequence
    print("\n🛑 Simulating shutdown...")
    lcd.clear()
    lcd.print_line(0, "Goodbye!")
    lcd.print_line(1, "System shutdown")
    time.sleep(1)
    lcd.clear()
    lcd.backlight_off()

def demo_button_simulation():
    """Demonstrate button press simulation"""
    print("\n🎮 Demo: Button Press Simulation")
    print("=" * 40)
    
    products = ["iPhone", "Samsung", "Google", "iPad", "MacBook"]
    current_index = 0
    stopwatch_time = 0
    is_running = False
    
    lcd = DemoLCD()
    
    # Simulate random button presses
    for _ in range(10):
        button = random.choice(["UP", "DOWN", "TIMER"])
        
        if button == "UP":
            current_index = (current_index - 1) % len(products)
            print("🔼 UP button pressed")
        elif button == "DOWN":
            current_index = (current_index + 1) % len(products)
            print("🔽 DOWN button pressed")
        else:  # TIMER
            is_running = not is_running
            if is_running:
                print("⏱️  TIMER button pressed - Stopwatch STARTED")
            else:
                print("⏸️  TIMER button pressed - Stopwatch STOPPED")
            if is_running:
                stopwatch_time += 1
        
        print(f"   → Product index: {current_index}")
        status = "▶" if is_running else "⏸"
        timer_display = f"{status}{stopwatch_time//60:02d}:{stopwatch_time%60:02d}"
        
        lcd.print_line(0, products[current_index])
        lcd.print_line(1, timer_display)
        time.sleep(1.5)

def demo_features():
    """Demonstrate all features"""
    print("\n🌟 Demo: Feature Showcase")
    print("=" * 40)
    
    lcd = DemoLCD()
    
    features = [
        ("Debounced Buttons", "No double-press"),
        ("File Loading", "products.txt"),
        ("Stopwatch Timer", "Start/Stop toggle"),
        ("Visual Indicators", "▶ Running ⏸ Paused"),
        ("Long Text", "Auto-truncation"),
        ("Graceful Exit", "Clean shutdown")
    ]
    
    for feature, description in features:
        lcd.clear()
        lcd.print_line(0, feature)
        lcd.print_line(1, description)
        print(f"✨ Feature: {feature}")
        print(f"   {description}")
        time.sleep(2)

def main():
    """Run the complete demo"""
    print("🎪 LCD Product Display System - DEMO")
    print("=" * 50)
    print("This demo simulates the LCD system without hardware")
    print()
    
    try:
        demo_basic_functionality()
        demo_button_simulation()
        demo_features()
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print()
        print("📋 What you saw:")
        print("• LCD initialization and loading screen")
        print("• Product navigation with UP/DOWN buttons")
        print("• Stopwatch timer with START/STOP toggle")
        print("• Visual indicators (▶ running, ⏸ paused)")
        print("• Real-time timer display (MM:SS format)")
        print("• Graceful shutdown sequence")
        print("• Debounced button handling")
        print("• File-based product management")
        print()
        print("🚀 Ready to run on actual hardware!")
        print("   Connect your LCD and buttons, then run: python3 product_display.py")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == '__main__':
    main()
