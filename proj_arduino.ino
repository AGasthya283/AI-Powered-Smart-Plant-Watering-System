/*
Arduino Code for Plant Watering System
Connect relay to pin 7
Connect LED indicators to pins 12 (money plant) and 13 (cactus)
*/

const int RELAY_PIN = 7;
const int MONEY_PLANT_LED = 12;
const int CACTUS_LED = 13;

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(MONEY_PLANT_LED, OUTPUT);
  pinMode(CACTUS_LED, OUTPUT);
  
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(MONEY_PLANT_LED, LOW);
  digitalWrite(CACTUS_LED, LOW);
  
  Serial.println("Arduino Plant Watering System Ready");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\\n');
    command.trim();
    
    if (command.startsWith("WATER_MONEY_")) {
      int waterTime = command.substring(12).toInt();
      waterPlant("money_plant", waterTime);
    }
    else if (command.startsWith("WATER_CACTUS_")) {
      int waterTime = command.substring(13).toInt();
      waterPlant("cactus", waterTime);
    }
  }
}

void waterPlant(String plantType, int duration) {
  Serial.println("Starting watering: " + plantType + " for " + String(duration) + " seconds");
  
  // Turn on appropriate LED
  if (plantType == "money_plant") {
    digitalWrite(MONEY_PLANT_LED, HIGH);
  } else if (plantType == "cactus") {
    digitalWrite(CACTUS_LED, HIGH);
  }
  
  // Turn on water pump via relay
  digitalWrite(RELAY_PIN, HIGH);
  
  // Wait for specified duration
  delay(duration * 1000);
  
  // Turn off pump and LED
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(MONEY_PLANT_LED, LOW);
  digitalWrite(CACTUS_LED, LOW);
  
  Serial.println("Watering complete: " + plantType);
}