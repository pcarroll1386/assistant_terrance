#!/usr/bin/env python3
########################################################################
# Filename    : product_display.py
# Description : LCD Product Display with Timer and Button Navigation
# Author      : Based on Freenove examples
# Date        : 2025/07/14
########################################################################

import signal
import sys
import time
import threading
from datetime import datetime, timedelta
import os

try:
    import RPi.GPIO as GPIO
    from LCD1602 import LCD1602
    RASPBERRY_PI = True
except ImportError:
    # For development/testing on non-Pi systems
    RASPBERRY_PI = True
    print("Warning: RPi.GPIO not available. Running in simulation mode.")
    
    class MockGPIO:
        BCM = "BCM"
        IN = "IN"
        PUD_UP = "PUD_UP"
        FALLING = "FALLING"
        
        @staticmethod
        def setmode(mode): pass
        @staticmethod
        def setup(pin, mode, pull_up_down=None): pass
        @staticmethod
        def add_event_detect(pin, edge, callback=None, bouncetime=None): pass
        @staticmethod
        def cleanup(): pass
    
    class MockLCD:
        def __init__(self, address=0x27): pass
        def clear(self): pass
        def print_line(self, line, message): 
            print(f"LCD Line {line}: {message}")
        def backlight_off(self): pass
    
    GPIO = MockGPIO()
    LCD1602 = MockLCD

# GPIO pin definitions
UP_BUTTON = 17
DOWN_BUTTON = 27
TIMER_BUTTON = 22

# Global variables
lcd = None
product_index = 0
products = []
stopwatch_start_time = None
stopwatch_running = False
stopwatch_elapsed = 0.0  # Store elapsed time when paused
running = True
last_button_time = 0
DEBOUNCE_TIME = 0.3  # 300ms debounce

def load_products():
    """Load product names from file or use default list"""
    global products
    
    products_file = "products.txt"
    if os.path.exists(products_file):
        try:
            with open(products_file, 'r') as f:
                products = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(products)} products from {products_file}")
        except Exception as e:
            print(f"Error loading products file: {e}")
            products = get_default_products()
    else:
        products = get_default_products()
        # Create the products file with default items
        try:
            with open(products_file, 'w') as f:
                for product in products:
                    f.write(f"{product}\n")
            print(f"Created {products_file} with default products")
        except Exception as e:
            print(f"Error creating products file: {e}")

def get_default_products():
    """Return default list of products"""
    return [
        "Apple iPhone 15",
        "Samsung Galaxy S24",
        "Google Pixel 8",
        "iPad Pro 12.9",
        "MacBook Air M2",
        "Dell XPS 13",
        "Sony WH-1000XM5",
        "AirPods Pro 2",
        "Nintendo Switch",
        "Tesla Model Y",
        "Raspberry Pi 5",
        "Arduino Uno R4"
    ]

def setup_gpio():
    """Setup GPIO pins for buttons"""
    if not RASPBERRY_PI:
        return
        
    GPIO.setmode(GPIO.BCM)
    
    # Setup buttons with pull-up resistors
    GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TIMER_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Add event detection for button presses
    GPIO.add_event_detect(UP_BUTTON, GPIO.FALLING, callback=up_button_pressed, bouncetime=200)
    GPIO.add_event_detect(DOWN_BUTTON, GPIO.FALLING, callback=down_button_pressed, bouncetime=200)
    GPIO.add_event_detect(TIMER_BUTTON, GPIO.FALLING, callback=timer_button_pressed, bouncetime=200)

def up_button_pressed(channel):
    """Handle up button press with debouncing"""
    global product_index, last_button_time
    
    current_time = time.time()
    if current_time - last_button_time < DEBOUNCE_TIME:
        return
    
    last_button_time = current_time
    
    if len(products) > 0:
        product_index = (product_index - 1) % len(products)
        print(f"UP pressed - Product index: {product_index}")

def down_button_pressed(channel):
    """Handle down button press with debouncing"""
    global product_index, last_button_time
    
    current_time = time.time()
    if current_time - last_button_time < DEBOUNCE_TIME:
        return
    
    last_button_time = current_time
    
    if len(products) > 0:
        product_index = (product_index + 1) % len(products)
        print(f"DOWN pressed - Product index: {product_index}")

def timer_button_pressed(channel):
    """Handle timer button press - toggle stopwatch start/stop"""
    global stopwatch_running, stopwatch_start_time, stopwatch_elapsed, last_button_time
    
    current_time = time.time()
    if current_time - last_button_time < DEBOUNCE_TIME:
        return
    
    last_button_time = current_time
    
    if stopwatch_running:
        # Stop the stopwatch
        if stopwatch_start_time:
            stopwatch_elapsed += time.time() - stopwatch_start_time
        stopwatch_running = False
        stopwatch_start_time = None
        print("TIMER pressed - Stopwatch STOPPED")
    else:
        # Start the stopwatch
        stopwatch_running = True
        stopwatch_start_time = time.time()
        print("TIMER pressed - Stopwatch STARTED")

def format_stopwatch_time():
    """Format stopwatch time as MM:SS"""
    total_elapsed = stopwatch_elapsed
    
    # Add current session time if running
    if stopwatch_running and stopwatch_start_time:
        total_elapsed += time.time() - stopwatch_start_time
    
    total_seconds = int(total_elapsed)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    # Clamp to 99:59 maximum
    if minutes > 99:
        minutes = 99
        seconds = 59
    
    return f"{minutes:02d}:{seconds:02d}"

def update_display():
    """Update the LCD display with current product and stopwatch"""
    if lcd is None or len(products) == 0:
        return
    
    try:
        # Line 1: Current product name (truncated to 16 chars)
        current_product = products[product_index]
        lcd.print_line(0, current_product)
        
        # Line 2: Stopwatch with status indicator
        timer_text = format_stopwatch_time()
        if stopwatch_running:
            status_text = f"▶{timer_text}"  # Running indicator
        else:
            status_text = f"⏸{timer_text}"  # Paused indicator
        
        lcd.print_line(1, status_text)
        
    except Exception as e:
        print(f"Error updating display: {e}")

def display_loading_screen():
    """Show loading screen for 2 seconds"""
    if lcd is None:
        return
    
    try:
        lcd.clear()
        lcd.print_line(0, "Initializing...")
        lcd.print_line(1, "Please wait...")
        time.sleep(2)
        lcd.clear()
    except Exception as e:
        print(f"Error in loading screen: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\nShutting down gracefully...")
    running = False
    
    if lcd:
        try:
            lcd.clear()
            lcd.print_line(0, "Goodbye!")
            lcd.print_line(1, "System shutdown")
            time.sleep(1)
            lcd.clear()
            lcd.backlight_off()
        except Exception as e:
            print(f"Error during LCD cleanup: {e}")
    
    if RASPBERRY_PI:
        GPIO.cleanup()
    
    sys.exit(0)

def main():
    """Main program loop"""
    global lcd, start_time, running
    
    print("Product Display System Starting...")
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Load products
    load_products()
    if len(products) == 0:
        print("No products loaded! Exiting.")
        return
    
    # Initialize LCD
    try:
        if RASPBERRY_PI:
            lcd = LCD1602(0x27)  # Assuming I2C address 0x27
        else:
            lcd = LCD1602()
        print("LCD initialized successfully")
    except Exception as e:
        print(f"Failed to initialize LCD: {e}")
        return
    
    # Setup GPIO
    setup_gpio()
    print("GPIO setup complete")
    
    # Show loading screen
    display_loading_screen()
    
    print("Starting main loop...")
    print("Use UP button (GPIO 17) and DOWN button (GPIO 27) to navigate")
    print("Use TIMER button (GPIO 22) to start/stop stopwatch")
    print("Press Ctrl+C to exit")
    
    # Main loop
    try:
        while running:
            update_display()
            time.sleep(0.1)  # Update every 100ms for responsive stopwatch display
            
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        signal_handler(None, None)

if __name__ == '__main__':
    main()
