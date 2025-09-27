import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import serial
import time
from datetime import datetime
import os

# Fix Qt threading issues on Linux
os.environ['QT_QPA_PLATFORM'] = 'xcb'

# xla_gpu_strict_conv_algorithm_picker=False

class PlantDetectionSystem:
    def __init__(self, arduino_port='/dev/ttyUSB0', baud_rate=9600, camera_index=3):
        """
        Initialize the plant detection and watering system
        
        Args:
            arduino_port: Serial port for Arduino communication
            baud_rate: Serial communication baud rate
            camera_index: Camera index (0=built-in, 1=first external, 2=second external, etc.)
        """
        # Initialize camera
        self.cap = cv2.VideoCapture(camera_index)
        
        # Initialize Arduino connection
        try:
            self.arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print("Arduino connected successfully")
        except Exception as e:
            print(f"Arduino connection failed: {e}")
            self.arduino = None
        
        # Load pre-trained model (you can replace this with a custom trained model)
        self.model = MobileNetV2(weights='imagenet')
        
        # Plant detection confidence threshold
        self.confidence_threshold = 0.3

        ############################################################################################################################
        # Watering durations (in seconds)
        self.money_plant_water_time = 3  # More water for money plant
        self.cactus_water_time = 1       # Less water for cactus
        ############################################################################################################################

        # Detection history for stability
        self.detection_history = []
        self.history_size = 10
        
    def capture_image(self):
        """Capture image from webcam"""
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None
    
    def preprocess_image(self, img):
        """Preprocess image for model prediction"""
        # Resize image to 224x224 (MobileNetV2 input size)
        img_resized = cv2.resize(img, (224, 224))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Convert to array and add batch dimension
        img_array = image.img_to_array(img_rgb)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        return img_array
    
    def detect_plant(self, img):
        """
        Detect if image contains a cactus or money plant
        Note: This uses ImageNet classes as an example. For better accuracy,
        you should train a custom model with your specific plants.
        """
        processed_img = self.preprocess_image(img)
        predictions = self.model.predict(processed_img)
        decoded_predictions = decode_predictions(predictions, top=5)[0]
        
        ##########################################################################################################################################################################################
        # Check for plant-related classes in ImageNet
        plant_keywords = {
            'cactus': ['barrel_cactus', 'prickly_pear', 'thorns', 'cactus_pot', 'cactus_plant', 'cacti', 'cactuses', 'cacti_plants', 'cactuses_plants', 'cacti_plant', 'cardoon'],
            'money_plant': ['pot_plant', 'vine', 'leaves', 'money_plant']  # Money plant is often pots
        }
        ##########################################################################################################################################################################################

        for pred in decoded_predictions:
            class_name = pred[1].lower()
            confidence = pred[2]
            
            print(f"Detected: {class_name} with confidence: {confidence:.3f}")
            
            # Check for cactus
            for keyword in plant_keywords['cactus']:
                if keyword in class_name and confidence > self.confidence_threshold:
                    return 'cactus', confidence
            
            # Check for money plant
            for keyword in plant_keywords['money_plant']:
                if keyword in class_name and confidence > self.confidence_threshold:
                    return 'money_plant', confidence
        
        return 'unknown', 0.0
    
    def update_detection_history(self, plant_type):
        """Update detection history for stable detection"""
        self.detection_history.append(plant_type)
        if len(self.detection_history) > self.history_size:
            self.detection_history.pop(0)
    
    def get_stable_detection(self):
        """Get stable detection based on history"""
        if len(self.detection_history) < 5:
            return 'unknown'
        
        # Count occurrences
        cactus_count = self.detection_history.count('cactus')
        money_plant_count = self.detection_history.count('money_plant')
        
        # Return most frequent detection
        if cactus_count > money_plant_count and cactus_count > 3:
            return 'cactus'
        elif money_plant_count > cactus_count and money_plant_count > 3:
            return 'money_plant'
        
        return 'unknown'
    
    def send_arduino_command(self, plant_type):
        """Send watering command to Arduino"""
        if not self.arduino:
            print("Arduino not connected")
            return
        
        try:
            if plant_type == 'money_plant':
                command = f"WATER_MONEY_{self.money_plant_water_time}\n"
                print(f"Watering money plant for {self.money_plant_water_time} seconds")
            elif plant_type == 'cactus':
                command = f"WATER_CACTUS_{self.cactus_water_time}\n"
                print(f"Watering cactus for {self.cactus_water_time} seconds")
            else:
                return
            
            self.arduino.write(command.encode())
            
            # Wait for Arduino acknowledgment
            response = self.arduino.readline().decode().strip()
            print(f"Arduino response: {response}")
            
        except Exception as e:
            print(f"Arduino communication error: {e}")
    
    def run_single_detection(self):
        """Single shot detection and watering"""
        print("Starting single-shot plant detection...")
        
        # Capture single image
        print("Capturing image from webcam...")
        frame = self.capture_image()
        
        if frame is None:
            print("Failed to capture image from webcam")
            return
        
        print("Image captured successfully")
        
        # Save captured image for reference
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"res_frames/captured_plant_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as: {filename}")
        
        # Analyze the image
        print("\Analyzing image for plant detection...")
        plant_type, confidence = self.detect_plant(frame)
        
        # Print detailed results
        print("\n" + "="*50)
        print("DETECTION RESULTS:")
        print("="*50)
        
        if plant_type == 'unknown':
            print("CONCLUSION: No recognized plant detected")
            print("ACTION: No watering performed")
        else:
            print(f"DETECTED PLANT: {plant_type.upper()}")
            print(f"CONFIDENCE: {confidence:.2%}")
            
            if plant_type == 'money_plant':
                print(f"WATERING PLAN: {self.money_plant_water_time} seconds (Money plants need more water)")
            elif plant_type == 'cactus':
                print(f"WATERING PLAN: {self.cactus_water_time} seconds (Cacti need less water)")
            
            # Send command to Arduino
            print(f"\nSending command to Arduino...")
            self.send_arduino_command(plant_type)

            wait_time = self.money_plant_water_time if plant_type == 'money_plant' else self.cactus_water_time
            time.sleep(wait_time*1000)  # Convert to milliseconds

        print("="*50)
        print("Detection and watering cycle complete")
        
        # Clean up
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        if self.arduino:
            self.arduino.close()
        # No GUI windows to destroy in single-shot mode
        print("System shutdown complete")

def find_available_cameras():
    """Find all available camera devices"""
    available_cameras = []
    
    for i in range(10):  # Check first 10 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"Camera {i}: Available")
            cap.release()
        else:
            break
    
    return available_cameras

def main():
    """Main function to run the plant detection system"""
    # Find available cameras
    print("Scanning for available cameras...")
    cameras = find_available_cameras()
    print(f"Available cameras: {cameras}")
    
    # Ceate saved_images directory if it doesn't exist
    os.makedirs("res_frames", exist_ok=True)

    # Initialize system with external webcam
    camera_to_use = 1 if len(cameras) > 1 else 0  # Use external if available
    
    system = PlantDetectionSystem(arduino_port='/dev/ttyACM0', camera_index=camera_to_use)
    
    print(f"Using camera index: {camera_to_use}")
    
    try:
        # Run single detection instead of continuous loop
        system.run_single_detection()
    except KeyboardInterrupt:
        print("\nShutting down system...")
        system.cleanup()

if __name__ == "__main__":
    main()
