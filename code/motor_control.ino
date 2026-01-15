#include <Servo.h>
int goodWidgets = 0;
int badWidgets = 0;
const int separationAngle = 30;
const int greenLEDpins[3] = {13, 12, 8};
const int redLEDpins[3] = {A2, A3, A4};
const int rgbLEDpins[3] = {9, 10, 11};
const int servoPins[2] = {A0, A1};
const int switchPin = 5;
const int actuatorPins[3] = {4,3,2};
int previousValue = 0; // the seperate input value for the widget counts. First integer is good widget count, second is bad widget count
int widgets = 0;
Servo flipperStopper;
Servo flipperFlopper;
const int flipperFlopperAngle = 25;
const int flipperFlopperStart = 0;

void setup() {
  pinMode(actuatorPins[0], OUTPUT);
  pinMode(actuatorPins[1], OUTPUT);
  pinMode(actuatorPins[2], OUTPUT);
  pinMode(rgbLEDpins[0], OUTPUT);
  pinMode(rgbLEDpins[1], OUTPUT); 
  pinMode(rgbLEDpins[2], OUTPUT);
  pinMode(greenLEDpins[0], OUTPUT);
  pinMode(greenLEDpins[1], OUTPUT);
  pinMode(greenLEDpins[2], OUTPUT);
  pinMode(redLEDpins[0], OUTPUT);
  pinMode(redLEDpins[1], OUTPUT);
  pinMode(redLEDpins[2], OUTPUT);
  pinMode(switchPin, INPUT_PULLUP);
  // fully retract actuator
  digitalWrite(actuatorPins[2], LOW); 
  digitalWrite(actuatorPins[1], HIGH);
  analogWrite(actuatorPins[0], 255);
  delay(2000);
  flipperStopper.attach(servoPins[0]);
  flipperFlopper.attach(servoPins[1]);
  flipperStopper.write(0);
  flipperFlopper.write(flipperFlopperStart);
  Serial.begin(9600);
  Serial.println("READY");
  if (digitalRead(switchPin) == HIGH) {
    indicateActiveAndReady();
  }
}

void loop() {
  if (digitalRead(switchPin) == HIGH) {
    extendActuator(); // push widget into camera zone
    Serial.println("CAPTURE");
    Serial.parseInt();
    int widgets = Serial.parseInt(); //widgets is the next value sent to the serial. First integer is good widget count, second is bad widget count     
    Serial.println(widgets); // for testing purposes only
    incrementWidgetCount(widgets); // increase the count of widgets and classify as good or bad
    flipperStopperUp(); //allow widget to pass into sorting block
    retractActuator(); // retract actuator in preparation for next widget
    flipperStopperDown(); //lower flipperStopper in preparation for next widget
    binaryDisplay(); // update the binary display
    flipperFlopper.write(flipperFlopperStart); // reset flipperFlopper
  } else {
    stop();
  }
}
void incrementWidgetCount(int widgets) {
  if (widgets == previousValue+1) {
    // this is a bad widget
    badWidgets++;
    delay(500);
    analogWrite(rgbLEDpins[0], 175);
    analogWrite(rgbLEDpins[1], 0);
    analogWrite(rgbLEDpins[2], 0);
    flipperFlopperRotation(0);
  } else if (widgets == previousValue+10) {
  	// this is a good widget
    goodWidgets++;
    delay(500);
    analogWrite(rgbLEDpins[0], 0);
    analogWrite(rgbLEDpins[1], 175);
    analogWrite(rgbLEDpins[2], 0);
    flipperFlopperRotation(1);
  } else if ((widgets == previousValue) and (widgets > 0)) {
    // no widget
    if ((goodWidgets + badWidgets) < 10) {
      analogWrite(rgbLEDpins[0], 0);
      analogWrite(rgbLEDpins[1], 0);
      analogWrite(rgbLEDpins[2], 0);
      delay(500);
      analogWrite(rgbLEDpins[0], 150);
      analogWrite(rgbLEDpins[1], 0);
      analogWrite(rgbLEDpins[2], 150);
    }
  }
  if (widgets > 0) {
    previousValue = widgets; //update "previous"
  }
}
void binaryDisplay() {
  int binaryGood[3];
  int binaryBad[3];
  
  int goodWidgetCountForBinary = goodWidgets;
  int badWidgetCountForBinary = badWidgets;
 
  //decimal to binary
  for (int i = 0; i < 3; i++) {
   binaryGood[i] = goodWidgetCountForBinary % 2;
   goodWidgetCountForBinary /= 2;  
   binaryBad[i] = badWidgetCountForBinary % 2;
   badWidgetCountForBinary /= 2;
  }
  //if pos in array is 1, light on, else off
  for (int i = 0; i < 3; i++) {
    if (binaryGood[i] == 1) {
    	digitalWrite(greenLEDpins[2-i], HIGH);
    } else {
    	digitalWrite(greenLEDpins[2-i], LOW);
    }
  }
  for (int i = 0; i < 3; i++) {
    if (binaryBad[i] == 1) {
        digitalWrite(redLEDpins[2-i], HIGH);
    } else {
        digitalWrite(redLEDpins[2-i], LOW);
    }
  }	
}
void flipperStopperUp() {
  flipperStopper.write(170);
  delay(1000);
}
void flipperStopperDown() {
  flipperStopper.write(0);
  delay(1000);
}
void extendActuator() {
  digitalWrite(actuatorPins[2], HIGH);
  digitalWrite(actuatorPins[1], LOW);
  analogWrite(actuatorPins[0], 255);
  delay(3500);
  digitalWrite(actuatorPins[2], LOW);
  digitalWrite(actuatorPins[1], LOW);
  analogWrite(actuatorPins[0], 0);
  delay(750);
}
void retractActuator() {
  digitalWrite(actuatorPins[2], LOW);
  digitalWrite(actuatorPins[1], HIGH);
  analogWrite(actuatorPins[0], 255);
  delay(3500);
  digitalWrite(actuatorPins[2], LOW);
  digitalWrite(actuatorPins[1], LOW);
  analogWrite(actuatorPins[0], 0);
  delay(750);
}
void flipperFlopperRotation(int widgetType) {
  if (widgetType == 1) {
    // this is a good widget
    flipperFlopper.write(flipperFlopperStart - flipperFlopperAngle);
   } else if (widgetType == 0) {
    // this is a bad widget
    flipperFlopper.write(flipperFlopperStart + flipperFlopperAngle);
   }
}
void indicateActiveAndReady() {
  digitalWrite(greenLEDpins[0], HIGH);
  digitalWrite(greenLEDpins[1], HIGH);
  digitalWrite(greenLEDpins[2], HIGH);
  digitalWrite(redLEDpins[0], HIGH);
  digitalWrite(redLEDpins[1], HIGH);
  digitalWrite(redLEDpins[2], HIGH);
  analogWrite(rgbLEDpins[0], 100);
  analogWrite(rgbLEDpins[1], 100);
  analogWrite(rgbLEDpins[2], 100);
  delay(1000);
  digitalWrite(greenLEDpins[0], LOW);
  digitalWrite(greenLEDpins[1], LOW);
  digitalWrite(greenLEDpins[2], LOW);
  digitalWrite(redLEDpins[0], LOW);
  digitalWrite(redLEDpins[1], LOW);
  digitalWrite(redLEDpins[2], LOW);
  analogWrite(rgbLEDpins[0], 0);
  analogWrite(rgbLEDpins[1], 0);
  analogWrite(rgbLEDpins[2], 0);
  delay(500);
}
void stop(){
  digitalWrite(actuatorPins[2], LOW);
  digitalWrite(actuatorPins[1], LOW);
  analogWrite(actuatorPins[0], 0);
  goodWidgets = 0;
  badWidgets = 0;
  digitalWrite(greenLEDpins[0], LOW);
  digitalWrite(greenLEDpins[1], LOW);
  digitalWrite(greenLEDpins[2], LOW);
  digitalWrite(redLEDpins[0], LOW);
  digitalWrite(redLEDpins[1], LOW);
  digitalWrite(redLEDpins[2], LOW);
  analogWrite(rgbLEDpins[0], 0);
  analogWrite(rgbLEDpins[1], 0);
  analogWrite(rgbLEDpins[2], 0);
}
