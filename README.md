# LCD Product Display System

A Raspberry Pi project that displays product names on a 1602 I2C LCD with button navigation and an elapsed timer.

## Features

- **📺 I2C LCD Display**: Shows product names and stopwatch time on a 16x2 LCD
- **🔘 Button Navigation**: Use UP/DOWN buttons to cycle through products
- **⏱️ Stopwatch Timer**: Toggle-able stopwatch with START/STOP functionality
- **📋 Product Management**: Load products from file or use defaults
- **🛡️ Debounced Buttons**: Prevents multiple triggers from single button press
- **🚀 Loading Screen**: Shows initialization message on startup
- **🔄 Graceful Shutdown**: Clean exit with Ctrl+C

## Hardware Requirements

### Components
- Raspberry Pi (any model with GPIO)
- 1602 I2C LCD Display (Freenove brand recommended)
- 3x Push buttons (UP, DOWN, TIMER)
- 3x 10kΩ resistors (pull-up resistors, optional - internal pull-ups used)
- Breadboard and jumper wires

### Wiring Diagram

#### LCD Connections (I2C)
```
LCD Pin    → Raspberry Pi Pin
VCC        → 5V (Pin 2)
GND        → Ground (Pin 6)
SDA        → SDA (Pin 3, GPIO 2)
SCL        → SCL (Pin 5, GPIO 3)
```

#### Button Connections
```
Button     → GPIO Pin    → Physical Pin
UP         → GPIO 17     → Pin 11
DOWN       → GPIO 27     → Pin 13
TIMER      → GPIO 22     → Pin 15
```

**Button Wiring:**
- Connect one side of each button to GPIO pin
- Connect other side to Ground
- Internal pull-up resistors are used (configured in software)

## Software Setup

### 1. Enable I2C on Raspberry Pi

```bash
sudo raspi-config
```
- Navigate to: `Interface Options` → `I2C` → `Yes`
- Reboot: `sudo reboot`

### 2. Install Dependencies

```bash
# Update system
sudo apt update

# Install I2C tools (optional, for testing)
sudo apt install i2c-tools

# Install Python dependencies
pip install -r requirements.txt

# Alternative manual installation:
pip install smbus2
```

### 3. Find LCD I2C Address

```bash
# Scan for I2C devices
sudo i2cdetect -y 1
```
Common addresses: `0x27`, `0x3F`

If your LCD uses a different address, modify the address in `product_display.py`:
```python
lcd = LCD1602(0x27)  # Change 0x27 to your address
```

## Usage

### Quick Start

```bash
# Clone or download the project
cd lcd_product_display

# Run the program
python3 product_display.py
```

### Program Controls

- **UP Button (GPIO 17)**: Navigate to previous product
- **DOWN Button (GPIO 27)**: Navigate to next product  
- **TIMER Button (GPIO 22)**: Start/Stop stopwatch timer
- **Ctrl+C**: Graceful shutdown

### Display Layout

```
Line 1: [Product Name    ]
Line 2: [▶MM:SS] or [⏸MM:SS]
```

**Display Indicators:**
- `▶` = Stopwatch is running
- `⏸` = Stopwatch is paused/stopped

## File Structure

```
lcd_product_display/
├── product_display.py    # Main application
├── LCD1602.py           # LCD driver module
├── products.txt         # Product names list
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Customization

### Adding/Editing Products

Edit `products.txt` to customize the product list:
```
Apple iPhone 15
Samsung Galaxy S24
Your Custom Product
Another Product Name
```

### Changing GPIO Pins

Modify pin assignments in `product_display.py`:
```python
# GPIO pin definitions
UP_BUTTON = 17      # Change to your preferred pin
DOWN_BUTTON = 27    # Change to your preferred pin  
TIMER_BUTTON = 22   # Change to your preferred pin
```

### Adjusting Debounce Time

Change button debounce sensitivity:
```python
DEBOUNCE_TIME = 0.3  # Seconds (increase for less sensitivity)
```

## Code Architecture

### Core Components

1. **LCD1602.py**: Hardware abstraction for I2C LCD
   - Based on PCF8574 I/O expander
   - Handles 4-bit LCD communication
   - Provides high-level printing functions

2. **product_display.py**: Main application logic
   - GPIO button handling with debouncing (UP, DOWN, TIMER buttons)
   - Stopwatch functionality with start/stop toggle
   - Display updates and product navigation
   - Graceful shutdown handling

### Key Features Implementation

#### 1. Display Initialization
```python
lcd = LCD1602(0x27)  # Initialize with I2C address
display_loading_screen()  # Show "Initializing..." for 2 seconds
```

#### 2. Button Setup with Pull-up Resistors
```python
GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(UP_BUTTON, GPIO.FALLING, callback=up_button_pressed, bouncetime=200)
```

#### 3. Product Navigation with Index Clamping
```python
product_index = (product_index + 1) % len(products)  # Wrap around list
```

#### 4. Timer Display (MM:SS Format)
```python
def format_elapsed_time():
    elapsed = datetime.now() - start_time
    total_seconds = int(elapsed.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"
```

#### 5. Debounced Button Handling
```python
def up_button_pressed(channel):
    current_time = time.time()
    if current_time - last_button_time < DEBOUNCE_TIME:
        return  # Ignore rapid presses
    last_button_time = current_time
    # Handle button press...
```

#### 6. Graceful Shutdown
```python
def signal_handler(sig, frame):
    lcd.clear()
    lcd.print_line(0, "Goodbye!")
    GPIO.cleanup()
    sys.exit(0)
```

## Troubleshooting

### Common Issues

1. **LCD not displaying**
   - Check I2C wiring (SDA, SCL, VCC, GND)
   - Verify I2C address with `sudo i2cdetect -y 1`
   - Ensure I2C is enabled in raspi-config

2. **Buttons not responding**
   - Check GPIO pin connections
   - Verify buttons are connected to ground
   - Check for loose connections

3. **Import errors**
   - Install missing dependencies: `pip install smbus2`
   - Ensure running on Raspberry Pi for GPIO access

4. **Permission errors**
   - Run with sudo if needed: `sudo python3 product_display.py`
   - Add user to gpio group: `sudo usermod -a -G gpio $USER`

### Testing Components

#### Test I2C LCD:
```python
from LCD1602 import LCD1602
lcd = LCD1602(0x27)
lcd.print_line(0, "Hello World!")
lcd.print_line(1, "LCD Test")
```

#### Test Buttons:
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("Press button:", GPIO.input(17))
```

## Development Mode

The program includes a simulation mode for development on non-Raspberry Pi systems:

```python
# Automatically detects if RPi.GPIO is available
# Falls back to console output if running on PC
```

## License

Based on Freenove examples. Free for educational and personal use.

## Contributing

Feel free to submit issues and enhancement requests!

### Possible Enhancements

- [ ] Add buzzer feedback for button presses
- [ ] Store timer state between runs
- [ ] Add product categories
- [ ] Web interface for remote control
- [ ] Multiple display pages
- [ ] Temperature/humidity display
- [ ] Network connectivity status

---

**Happy Making! 🚀**
