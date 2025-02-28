/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/


int pivot = 0;
int readPin = A0;
int outputPin = 2;
String currCmd = "";

// the setup routine runs once when you press reset:
void setup() {
	// initialize serial communication at 9600 bits per second:
	Serial.begin(115200);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
}


// the loop routine runs over and over again forever:
void loop() {
	if(Serial.available()>0) {
    // Read serial
    currCmd = Serial.readStringUntil('\n');
    currCmd.trim();
		//run curr cmd
		if(currCmd == "") {}
    
		else if (currCmd == "acquire") {
			// read the input on selected analog pin:
			int sensorValue = analogRead(readPin);
			// print out the value you read and corresponding time relative to pivot:
		  Serial.print(millis()-pivot);
      Serial.print(" ");
			Serial.println(sensorValue);
      
		}else if(currCmd == "request_commands") {
      Serial.println("acquire: Acquire analog data from selected pin.| change_read_pin [pin]: Change selected analog read pin.| change_output_pin [pin]: Change selected digital output pin.| switch_output_pin: inverts selected digital pin output" );
      
		}else if(currCmd.indexOf("change_read_pin") == 0) {
      if(readPin >= A0 && readPin <= A5) {
        readPin = currCmd.substring(16).toInt();
        Serial.println("changed read pin successfully");
      }
      else {
        Serial.println("unrecognised read pin");
      }
		}else if(currCmd.indexOf("change_output_pin") == 0) {
      if(outputPin >= 2 && outputPin <= 7) {
        outputPin = currCmd.substring(18).toInt();
        Serial.println("changed output pin successfully");
      }
      else {
        Serial.println("unrecognised output pin");
      }
    }else if(currCmd == "switch_output_pin"){
      digitalWrite(outputPin, !digitalRead(outputPin));
    }else if(currCmd == "set_pivot"){
      pivot = millis();
		} else {
			Serial.println("ARDUINO ERROR: Unknown Instruction!");
			currCmd = "";
		}
   currCmd = "";
	}
}
