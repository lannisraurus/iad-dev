/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/


int pivot = 0;
int selectedPin = A0;
String currCmd = "";

// the setup routine runs once when you press reset:
void setup() {
	// initialize serial communication at 9600 bits per second:
	Serial.begin(9600);
}

void setPivot(){
  pivot = millis();
}

// the loop routine runs over and over again forever:
void loop() {
	if(!Serial.available()) {
    // Read serial
    currCmd = Serial.readString();
		//run curr cmd
		if(currCmd == "") {}
		else if (currCmd == "acquire") {
			// read the input on selected analog pin:
			int sensorValue = analogRead(selectedPin);
			// print out the value you read and corresponding time relative to pivot:
			Serial.print(millis()-pivot);
			Serial.println(" " + sensorValue);
		}else if(currCmd == "request_commands") {
      Serial.println("acquire: Acquire analog data from selected pin.\nchange_pin [pin]: Change selected pin.\n");
		}else if(currCmd.indexOf("change_pin") == 0){
      selectedPin = currCmd.substring(11).toInt();
		} else {
			Serial.println("* ARDUINO ERROR: unkown code");
			currCmd = "";
		}
   currCmd = "";
	}
}
