/*
Code to rotate servos, light up LEDs, and actuate the actuator

This code is designed to run on an Arduino Uno, and can be uploaded with a standard microUSB.

This code was designed primarily by Yarema Mushkevych, with minor guidance from Noah Grimes, Markus Walker, Keegan Smit, The Arduino Forums, and Claude Sonnet 4.5
*/

// define the Servo library and setup constants
#include <Servo.h>
int goodWidgets = 0;
int badWidgets = 0;
const int greenLEDpins[3] = {7, 12, 8};
const int redLEDpins[3] = {A2, A3, A4};
const int rgbLEDpins[3] = {9, 10, 11};
const int servoPins[2] = {A0, A1};
const int switchPin = 5;
const int actuatorPins[3] = {4,3,2};
int previousValue = 0; 
int widgets = -1; // starts at -1 to not conflict with other code
Servo flipperStopper;
Servo flipperFlopper;
const int goodWidgetAngle = 0;
const int badWidgetAngle = 60;
const int flopperStart = 30;

void setup() {
  // define pins
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
  // write servos to the proper positions
  flipperStopper.attach(servoPins[0]);
  flipperFlopper.attach(servoPins[1]);
  flipperStopper.write(0);
  flipperFlopper.write(flopperStart);
  Serial.begin(9600); // define serial
  Serial.println("READY"); // send "READY" signal to begin 
  if (digitalRead(switchPin) == HIGH) {
    indicateActiveAndReady(); // flash all LEDs on (and then off) to indicate that the Arduino is active
  }
  delay(3000); // wait for Pi to finish calibration (if needed)
}

void loop() {
  if (digitalRead(switchPin) == HIGH) {
    // if the arduino is on:
    if (widgets != 0) {
      extendActuator(); // push widget into camera zone
      retractActuator(); // retract actuator in preparation for next widget
    }
    Serial.println("CAPTURE"); // tell PI
    widgets = Serial.parseInt(); //widgets is the next value sent to the serial. First integer is good widget count, second is bad widget count 
    if (widgets != 0) {
      // if a widget has been detected (prevents actuator from infinitely moving):
      incrementWidgetCount(widgets, rgbLEDpins[0], rgbLEDpins[1], rgbLEDpins[2]); // increase widget count (either good or bad) accordingly
      flipperStopperDown(); //lower flipperStopper in preparation for next widget
      binaryDisplay(goodWidgets, badWidgets); // update the binary display
      flipperFlopper.write(flopperStart); // reset flipperFlopper
    } else {
      retractActuator(); // otherwise, retract the actuator
    }
  } else {
    retractActuator();
    delay(1500);
    stop(0, rgbLEDpins[0], rgbLEDpins[1], rgbLEDpins[2]);
  }
}
void incrementWidgetCount(int widgets, int redPin, int greenPin, int bluePin) {
  if (widgets == previousValue+1) {
    // this is a bad widget
    badWidgets++;
    delay(500);
    // switch RGB LED to display red
    analogWrite(redPin, 255);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, 0);
    flipperFlopperRotation(0); //rotate flipperFlopper to sort widgets into bad bin
    delay(500);
    flipperStopperUp(); //allow widget to pass into sorting block
    delay(2500);
    flipperFlopper.write(flopperStart); //reset FlipperFlopper
  } else if (widgets == previousValue+10) {
  	// this is a good widget
    goodWidgets++;
    delay(500);
    //switch RGB LED to display green
    analogWrite(redPin, 0);
    analogWrite(greenPin, 255);
    analogWrite(bluePin, 0);
    flipperFlopperRotation(1); //rotate flipperFlopper to sort widgets into good bin
    delay(500); 
    flipperStopperUp(); //allow widget to pass into sorting block
    delay(2500);
    flipperFlopper.write(flopperStart); //reset FlipperFlopper
  } else if ((widgets == previousValue) and (widgets > 0)) {
    // if no widget detected:
    if ((goodWidgets + badWidgets) < 10) {
      // if less than 10 widgets were sorted
      retractActuator();
      delay(1500);
      stop(1, rgbLEDpins[0], rgbLEDpins[1], rgbLEDpins[2]); //turn off sorter, BUT turn RGB yellow
    } else {
      retractActuator();
      delay(1500);
      stop(0, rgbLEDpins[0], rgbLEDpins[1], rgbLEDpins[2]); // turn off sorter, and DON'T turn RGB yellow
    }
  }
  if (widgets > 0) {
    previousValue = widgets; //update previous value, but only if a widget was actually detected
  }

  
}
void binaryDisplay(int goodWidgetCountForBinary, int badWidgetCountForBinary) {
  // define lists to store binary counts
  int binaryGood[3]; 
  int binaryBad[3];
 
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
  // rotate flipperFlopper as needed
  if (widgetType == 1) {
    // this is a good widget
    flipperFlopper.write(goodWidgetAngle);
   } else if (widgetType == 0) {
    // this is a bad widget
    flipperFlopper.write(badWidgetAngle);
   }
}
void indicateActiveAndReady() {
  // briefly flash all LEDs on and then off to indicate 'active and ready'
  digitalWrite(greenLEDpins[0], HIGH);
  digitalWrite(greenLEDpins[1], HIGH);
  digitalWrite(greenLEDpins[2], HIGH);
  digitalWrite(redLEDpins[0], HIGH);
  digitalWrite(redLEDpins[1], HIGH);
  digitalWrite(redLEDpins[2], HIGH);
  analogWrite(rgbLEDpins[0], 255);
  analogWrite(rgbLEDpins[1], 255);
  analogWrite(rgbLEDpins[2], 255);
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
void stop(int hasYellow, int redPin, int greenPin, int bluePin){
  while (true) {
    digitalWrite(actuatorPins[2], LOW);
    digitalWrite(actuatorPins[1], LOW);
    analogWrite(actuatorPins[0], 0);
    goodWidgets = 0;
    badWidgets = 0;
    // determine whether to keep RGB as yellow or shut it off completely
    if (hasYellow == 1) {
      analogWrite(redPin, 255);
      analogWrite(greenPin, 255);
      analogWrite(bluePin, 10);
    } else if (hasYellow == 0) {
      digitalWrite(greenLEDpins[0], LOW);
      digitalWrite(greenLEDpins[1], LOW);
      digitalWrite(greenLEDpins[2], LOW);
      digitalWrite(redLEDpins[0], LOW);
      digitalWrite(redLEDpins[1], LOW);
      digitalWrite(redLEDpins[2], LOW);
    }
  }
}
