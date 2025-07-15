#!/bin/bash
########################################################################
# Filename    : install.sh
# Description : Installation script for LCD Product Display System
# Author      : LCD Product Display System
# Date        : 2025/07/14
########################################################################

echo "🚀 LCD Product Display System - Installation Script"
echo "=================================================="

# Check if running on Raspberry Pi
if ! command -v raspi-config &> /dev/null; then
    echo "⚠️  Warning: This script is designed for Raspberry Pi"
    echo "   You may need to modify it for other systems"
    echo ""
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install I2C tools
echo "🔧 Installing I2C tools..."
sudo apt install -y i2c-tools python3-pip

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install smbus2

# Check if I2C is enabled
echo "🔍 Checking I2C configuration..."
if ! lsmod | grep -q i2c_bcm; then
    echo "⚙️  I2C may not be enabled. Please run:"
    echo "   sudo raspi-config"
    echo "   Then navigate to: Interface Options > I2C > Yes"
    echo "   Reboot after enabling I2C"
else
    echo "✅ I2C appears to be enabled"
fi

# Make scripts executable
echo "🔐 Making scripts executable..."
chmod +x product_display.py
chmod +x test_lcd.py

# Test I2C devices
echo "🔎 Scanning for I2C devices..."
if command -v i2cdetect &> /dev/null; then
    echo "Found I2C devices:"
    sudo i2cdetect -y 1
    echo ""
    echo "📝 Note: Common LCD addresses are 0x27 and 0x3F"
    echo "   If your LCD uses a different address, edit product_display.py"
else
    echo "⚠️  i2cdetect not available. Install i2c-tools manually if needed."
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Connect your LCD to I2C pins (SDA=GPIO2, SCL=GPIO3)"
echo "2. Connect buttons to GPIO 17 (UP) and GPIO 27 (DOWN)"
echo "3. Test LCD: python3 test_lcd.py"
echo "4. Run main program: python3 product_display.py"
echo ""
echo "📚 See README.md for detailed wiring instructions"
echo "🐛 If you encounter issues, check the troubleshooting section"
