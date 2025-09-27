import serial
import time

try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)
    print("Arduino connected successfully!")
    arduino.close()
except Exception as e:
    print(f"Connection failed: {e}")