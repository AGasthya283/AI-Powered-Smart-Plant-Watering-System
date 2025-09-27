# 🌱 AI-Powered Smart Plant Watering System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Arduino](https://img.shields.io/badge/Arduino-IDE-green.svg)](https://arduino.cc)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent plant care system that uses computer vision to identify different plants and automatically provides appropriate watering based on their needs. The system distinguishes between water-loving plants (like Money Plants) and drought-resistant plants (like Cacti) to deliver optimal care.

## 🚀 Features

- **🔍 AI Plant Detection**: Uses TensorFlow/Keras for real-time plant identification
- **📷 Webcam Integration**: Supports both built-in and external USB cameras
- **⚡ Arduino Control**: Automated pump control via relay switching
- **💧 Smart Watering**: Different watering schedules for different plant types
- **🛡️ Safety Features**: Emergency stop, status monitoring, and auto-shutoff
- **📊 Detailed Logging**: Comprehensive feedback and image saving
- **🔧 Cross-Platform**: Works on Linux, Windows, and macOS

## 🎯 How It Works

1. **Capture**: System captures image from webcam
2. **Analyze**: AI model identifies plant type (Money Plant vs Cactus)
3. **Decide**: Determines appropriate watering duration
4. **Execute**: Sends command to Arduino to control water pump
5. **Monitor**: Provides detailed feedback and saves captured images

## 🛠️ Hardware Requirements

### Electronics
- **Arduino Uno/Nano** (any compatible board)
- **5V Relay Module** (for pump control)
- **Water Pump** (5V or 12V with appropriate power supply)
- **USB Webcam** (or use built-in laptop camera)
- **LEDs** (optional, for status indication)
- **Jumper Wires**
- **Breadboard** (optional)

### Circuit Connections
```
Arduino Pin 7  → Relay IN
Arduino Pin 12 → Money Plant LED (optional)
Arduino Pin 13 → Cactus LED (optional)
Arduino 5V     → Relay VCC
Arduino GND    → Relay GND

Relay COM      → Pump Positive
Relay NO       → Power Supply Positive
Power GND      → Pump Negative & Arduino GND
```

## 📋 Software Requirements

### Python Dependencies
```bash
pip install opencv-python tensorflow pyserial numpy
```

### System Requirements
- **Python 3.8+**
- **Arduino IDE** (for uploading Arduino code)
- **Webcam** (USB or built-in)
- **Linux/Windows/macOS**

### Optional Packages
```bash
# For better camera support on Linux
sudo apt install v4l-utils

# For enhanced TensorFlow performance
pip install tensorflow-gpu  # If you have compatible GPU
```

## 🚀 Quick Start

### 1. Setup Hardware
1. Connect your Arduino circuit according to the wiring diagram
2. Connect your water pump through the relay
3. Connect USB webcam (if using external camera)

### 2. Upload Arduino Code
1. Open Arduino IDE
2. Copy the code from `arduino_plant_watering.ino`
3. Upload to your Arduino board
4. Open Serial Monitor to verify "Arduino Plant Watering System Ready"

### 3. Setup Python Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-plant-watering-system.git
cd ai-plant-watering-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure and Run
```bash
# Find your Arduino port
ls /dev/tty*  # Linux/macOS
# or check Device Manager on Windows

# Update the port in main.py (if needed)
# arduino_port='/dev/ttyACM0'  # Linux
# arduino_port='COM3'          # Windows

# Run the system
python main.py
```

## 📁 Project Structure

```
ai-plant-watering-system/
├── main.py                    # Main Python application
├── arduino_plant_watering.ino # Arduino code
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── docs/
│   ├── circuit_diagram.png    # Wiring diagram
│   ├── setup_guide.md         # Detailed setup instructions
│   └── troubleshooting.md     # Common issues and solutions
├── images/                    # Captured plant images
└── models/                    # Custom trained models (optional)
```

## 🔧 Configuration

### Camera Settings
```python
# Use built-in camera
system = PlantDetectionSystem(camera_index=0)

# Use external USB camera
system = PlantDetectionSystem(camera_index=1)

# Auto-detect best camera
system = PlantDetectionSystem()  # Auto-selects external if available
```

### Watering Duration
```python
# Customize watering times (in seconds)
self.money_plant_water_time = 5  # Money plants need more water
self.cactus_water_time = 2       # Cacti need less water
```

### Arduino Port
```python
# Linux
system = PlantDetectionSystem(arduino_port='/dev/ttyACM0')

# Windows
system = PlantDetectionSystem(arduino_port='COM3')
```

## 📊 Plant Detection

The system currently uses a pre-trained MobileNetV2 model to detect:
- **Money Plants** (Pothos family)
- **Cacti** (Various species)

### Improving Accuracy
For better plant recognition:
1. Collect 100+ images of your specific plants
2. Train a custom CNN model
3. Replace the detection model in `detect_plant()` method

## 🛡️ Safety Features

- **Emergency Stop**: Send `PUMP_OFF` command to immediately stop watering
- **Auto-Shutoff**: Pump automatically turns off after specified duration
- **Status Monitoring**: Check pump state with `STATUS` command
- **Error Handling**: Comprehensive error catching and reporting
- **Default OFF State**: Pump is OFF by default, preventing accidental flooding

## 🐛 Troubleshooting

### Camera Issues
```bash
# Check available cameras
v4l2-ctl --list-devices

# Test camera access
ffplay /dev/video1

# Fix permissions
sudo usermod -a -G video $USER
```

### Arduino Connection Issues
```bash
# Find Arduino port
ls /dev/tty* | grep -E "(ACM|USB)"

# Test connection
arduino-cli board list

# Fix permissions
sudo usermod -a -G dialout $USER
```

### TensorFlow GPU Issues
```bash
# Force CPU usage
export CUDA_VISIBLE_DEVICES=-1
python main.py

# Or install CPU-only version
pip install tensorflow-cpu
```

## 📈 Example Output

```
Scanning for available cameras...
✅ Camera 3: Available - Resolution: 1920x1080
✅ Successfully initialized with camera index: 3
Starting single-shot plant detection...
📸 Image saved as: captured_plant_20250830_182004.jpg

🔍 Analyzing image for plant detection...

==================================================
DETECTION RESULTS:
==================================================
🌱 DETECTED PLANT: MONEY_PLANT
🎯 CONFIDENCE: 87.32%
💧 WATERING PLAN: 5 seconds (Money plants need more water)

📡 Sending command to Arduino...
Arduino response: Starting watering: money_plant for 5 seconds
Arduino response: Pump ON - watering started
Arduino response: Pump OFF - watering complete: money_plant
==================================================
✅ Detection and watering cycle complete
```

## 🔮 Future Enhancements

- [ ] **Custom Model Training**: Train on specific plant species
- [ ] **Soil Moisture Sensors**: Add moisture feedback to watering decisions
- [ ] **Multiple Plant Support**: Handle multiple plants simultaneously
- [ ] **Web Dashboard**: Browser-based monitoring and control
- [ ] **Scheduling**: Time-based automated watering
- [ ] **Plant Health Monitoring**: Detect diseases or stress
- [ ] **Mobile App**: Remote monitoring and control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TensorFlow/Keras** for the pre-trained models
- **OpenCV** for computer vision capabilities
- **Arduino Community** for hardware control examples
- **Plant Care Enthusiasts** for watering guidance

## 📞 Support

If you encounter issues:
1. Check the [Troubleshooting Guide](docs/troubleshooting.md)
2. Review [Setup Instructions](docs/setup_guide.md)
3. Open an [Issue](https://github.com/yourusername/ai-plant-watering-system/issues)

---

⭐ **Star this repo if it helped your plants thrive!** 🌿
