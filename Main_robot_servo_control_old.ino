#include<Servo.h>                               //servo library 

Servo BaseSer;
Servo ShldrSer;
Servo ElbwSer;
Servo GripSer;
												//servo objects
String serialData;                              //declare string

void setup() {
  BaseSer.attach(11);                           //assigns servos to pins
  ShldrSer.attach(10);
  ElbwSer.attach(9);
  GripSer.attach(6);
  Serial.begin(115200);                         //sets the baud rate
  Serial.setTimeout(10);						//sets the maximum milliseconds to wait for serial data		
}

void loop() {
}

void serialEvent() {
  serialData = Serial.readString();				//Reads Data
  BaseSer.write(parseDataA(serialData));       //Writes binary data to the serial port
  ShldrSer.write(parseDataB(serialData));
  ElbwSer.write(parseDataC(serialData));
  GripSer.write(parseDataD(serialData));
}

int parseDataA(String data){                  //.remove(index, count) index: The position at which to start the remove process (zero indexed), count: The number of characters to remove
  data.remove(data.indexOf("B"));             //removes data
  data.remove(data.indexOf("C"));
  data.remove(data.indexOf("D"));
  data.remove(data.indexOf("A"), 1);
  return data.toInt();
}

int parseDataB(String data){				  //Removes caracters from serial data to leave with the degree
  data.remove(0, data.indexOf("B") + 1);      //.indexOf, retuns index of letter
  return data.toInt();                        //Converts a valid String to an integer
}

int parseDataC(String data){
  data.remove(0, data.indexOf("C") + 1);
  return data.toInt();
}

int parseDataD(String data){
  data.remove(0, data.indexOf("D") + 1);
  return data.toInt();
}
