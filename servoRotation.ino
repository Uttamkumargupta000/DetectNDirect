#include <Servo.h>

Servo panServo;  // Define pan servo object
Servo tiltServo; // Define tilt servo object

void setup() {
  Serial.begin(9600);
  panServo.attach(10);  // Attach pan servo to pin 9
  tiltServo.attach(9); // Attach tilt servo to pin 10
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read the data until newline character
    int commaIndex = data.indexOf(','); // Find the index of comma separating theta1 and theta2 angles
    if (commaIndex != -1) {
      String theta1Str = data.substring(0, commaIndex); // Extract theta1 angle substring
      String theta2Str = data.substring(commaIndex + 1); // Extract theta2 angle substring
      int theta1 = theta1Str.toInt(); // Convert theta1 angle string to integer
      int theta2 = theta2Str.toInt(); // Convert theta2 angle string to integer
      // Do something with theta1 and theta2 (e.g., control servo motors)
      
      // Map theta1 and theta2 to servo angles
      int panAngle = map(theta1, 0, 180, 0, 180); // Map theta1 to pan servo range (0-180)
      int tiltAngle = map(theta2, 0, 180, 0, 180); // Map theta2 to tilt servo range (0-180)
      
      // Move servos to mapped angles
      panServo.write(panAngle);
      tiltServo.write(tiltAngle);
      
      // Print received data for debugging
      Serial.print("Received theta1: ");
      Serial.print(theta1);
      Serial.print(", theta2: ");
      Serial.println(theta2);
    }
  }
}