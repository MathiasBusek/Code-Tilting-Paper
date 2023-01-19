#include "Arduino_NineAxesMotion.h"        //Contains the bridge code between the API and the Arduino Environment
#include <Wire.h>

// Including the required Arduino libraries
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

// Uncomment according to your hardware type
//#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define HARDWARE_TYPE MD_MAX72XX::GENERIC_HW

// Defining size, and output pins
#define MAX_DEVICES 1
#define CS_PIN 3

// Create a new instance of the MD_Parola class with hardware SPI connection
MD_Parola myDisplay = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

NineAxesMotion mySensor;         //Object that for the sensor 
unsigned long lastStreamTime = 0;     //To store the last streamed time stamp
const int streamPeriod = 50;          //To stream at 50Hz without using additional timers (time period(ms) =1000/frequency(Hz))

float currRoll = 0;
float lastRoll[2];
float currPitch = 0;
float lastPitch[2];
unsigned long lastTime;

char tilt_y[7];
char tilt_z[7];
char rpm[4];
char text[50];

float treshhold = 0.2;

void setup() //This code is executed once
{
  //Peripheral Initialization
  Serial.begin(9600);           //Initialize the Serial Port to view information on the Serial Monitor
  Wire.begin();                    //Initialize I2C communication to the let the library communicate with the sensor.
  //Sensor Initialization
  mySensor.initSensor();          //The I2C Address can be changed here inside this function in the library
  mySensor.setOperationMode(OPERATION_MODE_NDOF);   //Can be configured to other operation modes as desired
  mySensor.setUpdateMode(MANUAL);  //The default is AUTO. Changing to MANUAL requires calling the relevant update functions prior to calling the read functions
  //Setting to MANUAL requires fewer reads to the sensor

    // Intialize the object
  myDisplay.begin();

  // Set the intensity (brightness) of the display (0-15)
  myDisplay.setIntensity(10);

  // Clear the display
  myDisplay.displayClear();

  memset(text, '.', 50);
  
  lastTime = 0;
  lastPitch[0] = 0;
  lastPitch[1] = 0;
  lastRoll[0] = 0;
  lastRoll[1] = 0;

}

void loop() //This code is looped forever
{
  if ((millis() - lastStreamTime) >= streamPeriod)
  {
    lastStreamTime = millis();
    mySensor.updateEuler();        //Update the Euler data into the structure of the object
    mySensor.updateCalibStatus();  //Update the Calibration Statu
    mySensor.readEulerHeading();
    currRoll = mySensor.readEulerRoll();
    currPitch = mySensor.readEulerPitch();

    Serial.print(millis());
    Serial.print(";");
    Serial.print(currRoll);
    Serial.print(";");
    Serial.println(currPitch);

    if((currPitch < lastPitch[0]) && (lastPitch[0] > lastPitch[1])) 
      dtostrf(lastPitch[0], 6, 2, tilt_z);
    if((currRoll < lastRoll[0]) && (lastRoll[0] > lastRoll[1])) 
      dtostrf(lastRoll[0], 6, 2, tilt_y);
          
    if(fabs(currPitch-currRoll) < treshhold) {
      if ((lastTime > 0) && ((millis() - lastTime) > 500)) {
            dtostrf(30000/((float)millis()-(float)lastTime), 3, 1, rpm);
            memset(text, ' ', 50);
            sprintf(text, " tilt_y:%s tilt_z:%s rpm:%s -", tilt_y, tilt_z, rpm);
      }
      lastTime = millis();
    }
              
    lastPitch[1] = lastPitch[0];
    lastPitch[0] = currPitch;
    lastRoll[1] = lastRoll[0];
    lastRoll[0] = currRoll;
    
  }
  if (myDisplay.displayAnimate())
    myDisplay.displayText(text, PA_CENTER, 50, 50, PA_SCROLL_LEFT);
  
}
