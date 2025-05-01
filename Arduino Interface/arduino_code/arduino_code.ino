/*
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva - Grupo 1 2024/2025

This file contains all Arduino functionalities, including data acquisition, external commands processing and other communication with the Raspberry Pi.
*/

// Needed variables
unsigned long pivot = 0;
int readPin = A0;
int outputPin = 2;
String currCmd = "";

// Setup routine: set pins as output and establish serial communication:
void setup() {
	// Initialize serial communication at 115200 bits per second:
	Serial.begin(115200);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT); 
}

// Loop for reading and executing commands
void loop() {
  
	if(Serial.available()>0) { // Checks for new commands in serial communication
    
    // Read serial
    currCmd = Serial.readStringUntil('\n');
    currCmd.trim();
    
		// Run current command
		if(currCmd == "") {}
    
		else if (currCmd == "acquire") {
			// Read the input on selected analog pin:
			int sensorValue = analogRead(readPin);
			// Print out the value you read and corresponding time relative to pivot (in milliseconds)
		  Serial.print(millis()-pivot);
      Serial.print(" ");
			Serial.println(sensorValue);
      
		}else if(currCmd == "request_commands") { 
      // Print out about all external commands handled by Arduino, split by |
      Serial.print("acquire: Acquire analog data from selected pin.");
      Serial.print("|change_read_pin [pin]: Change selected analog read pin.");
      Serial.print("|change_output_pin [pin]: Change selected digital output pin.");
      Serial.print("|switch_output_pin: Inverts selected digital pin output.");
      Serial.println("|read_output_pin: Reads current state of selected digital output pin." );
      
		}else if(currCmd.indexOf("change_read_pin") == 0) {
      // Change read pin to the selected analog pin, and print out message with changed pin
      if(readPin >= A0 && readPin <= A5) {
        readPin = currCmd.substring(16).toInt();
        Serial.print("changed read pin to ");
        Serial.println(readPin);
      }
      else { 
        // Only prints error log if read pin selected is not one of the analog pins
        Serial.println("Unrecognised read pin");
      }
      
		}else if(currCmd.indexOf("change_output_pin") == 0) {
      // Same as change_read_pin but for available digital output pins instead of analog pins
      if(outputPin >= 2 && outputPin <= 7) {
        outputPin = currCmd.substring(18).toInt();
        Serial.println("Changed output pin successfully");
      }
      else {
        Serial.println("Unrecognised output pin");
      }
      
    }else if(currCmd == "switch_output_pin"){
      // Switches state of selected output (digital) pin, and prints out message with new state
      bool oldState = digitalRead(outputPin);
      digitalWrite(outputPin, !oldState);
      Serial.print("Switched output pin to ");
      Serial.println(!oldState);
      
    }else if(currCmd == "set_pivot"){
      // Resets the pivot for resetting time values in acquired data, and prints out message
      pivot = millis();
      Serial.print("Reset Arduino pivot timer to ");
      Serial.println(pivot);

     }else if(currCmd == "read_output_pin"){
      // Reads state of selected output (digital) pin, and prints out message with state
      bool state = digitalRead(outputPin);
      Serial.print("Output pin state is ");
      Serial.println(state);
      
		} else {
      // If command is not one of the above commands, sends error message for unknown instruction
			Serial.println("ARDUINO ERROR: Unknown Instruction!");
		}
   currCmd="";
	}
}
