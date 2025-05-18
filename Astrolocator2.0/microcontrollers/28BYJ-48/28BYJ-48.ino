/*
Originally made by Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
Code was adapted to use for Astrolocator 2.0 stepper control - João Camacho.
*/

// EXTRACTION VARS
String currCmd = "";

// MOTOR VARS
const int xStepperPinN = 4;
const int xStepperPins[xStepperPinN] = {13, 12, 14, 27};

const int yStepperPinN = 4;
const int yStepperPins[yStepperPinN] = {26, 25, 33, 32};

const int xStepperPinSeqsHalf = 8;
const boolean xStepperSequencesHalf[xStepperPinSeqsHalf][xStepperPinN] = { {1, 0, 0, 0}, {1, 1, 0, 0}, {0, 1, 0, 0}, {0, 1, 1, 0}, {0, 0, 1, 0}, {0, 0, 1, 1}, {0, 0, 0, 1}, {1, 0, 0, 1} };

const int yStepperPinSeqsHalf = 8;
const boolean yStepperSequencesHalf[yStepperPinSeqsHalf][yStepperPinN] = { {1, 0, 0, 0}, {1, 1, 0, 0}, {0, 1, 0, 0}, {0, 1, 1, 0}, {0, 0, 1, 0}, {0, 0, 1, 1}, {0, 0, 0, 1}, {1, 0, 0, 1} };

const int xStepperPinSeqsFull = 4;
const boolean xStepperSequencesFull[xStepperPinSeqsFull][xStepperPinN] = { {1, 0, 0, 1}, {1, 1, 0, 0},  {0, 1, 1, 0}, {0, 0, 1, 1} };

const int yStepperPinSeqsFull = 4;
const boolean yStepperSequencesFull[yStepperPinSeqsFull][yStepperPinN] = { {1, 0, 0, 1}, {1, 1, 0, 0},  {0, 1, 1, 0}, {0, 0, 1, 1} };



int xPivot = 0;
int yPivot = 0;

// SETUP
void setup() {
	// Initialize serial communication at 115200 bits per second:
	Serial.begin(115200);
  // MOTORS
  for(int i = 0; i < xStepperPinN; i++) pinMode(xStepperPins[i], OUTPUT);
  for(int i = 0; i < yStepperPinN; i++) pinMode(yStepperPins[i], OUTPUT);
}

// MOTOR MOVEMENT
void motorStep(int* pivot, int seqN, int pinN, const int* pins, const boolean* seq, boolean direction){
  // Pivot clamp
  if (direction) *pivot = (*pivot + 1) % seqN;
  else *pivot = (*pivot - 1 + seqN) % seqN;
  // Step
  for (int i = 0; i < pinN; i++) {
    digitalWrite(pins[i], seq[i]);
  }
}

// MAIN LOOP
void loop() {
  
	if(Serial.available() > 0) { // Checks for new commands in serial communication
    
    // Read serial
    currCmd = Serial.readStringUntil('\n');
    currCmd.trim();
    
		// Run current command
		if(currCmd == "") 
    { 

    // Do 1 stepper step
    } else if (currCmd.indexOf("step") == 0) {

      String args = currCmd.substring(5);

      int space1 = args.indexOf(' ');
      int space2 = args.indexOf(' ', space1 + 1);

      boolean motor = args.substring(0, space1).toInt();
      boolean stepping = args.substring(space1 + 1, space2).toInt();
      boolean direction = args.substring(space2 + 1).toInt();

      int steppedX = 0;
      int steppedY = 0;

      if (stepping==0){
        if (motor==0) {
          motorStep(&xPivot, xStepperPinSeqsHalf, xStepperPinN, xStepperPins, xStepperSequencesHalf[xPivot], direction);
          steppedX = 1; if (!direction) steppedX *= -1;
        }
        else {
          motorStep(&yPivot, yStepperPinSeqsHalf, yStepperPinN, yStepperPins, yStepperSequencesHalf[yPivot], direction);
          steppedY = 1; if (!direction) steppedY *= -1;
        }
      }
      else {
        if (motor==0) {
          motorStep(&xPivot, xStepperPinSeqsFull, xStepperPinN, xStepperPins, xStepperSequencesFull[xPivot], direction);
          steppedX = 2; if (!direction) steppedX *= -1;
        }
        else {
          motorStep(&yPivot, yStepperPinSeqsFull, yStepperPinN, yStepperPins, yStepperSequencesFull[yPivot], direction);
          steppedY = 2; if (!direction) steppedY *= -1;
        }
      }
      
      Serial.print(steppedX);
      Serial.print(" ");
      Serial.println(steppedY);

    } else if (currCmd == "request_commands") { 
      // Print out about all external commands handled by Arduino, split by |
      Serial.print("request_commands: Gather commands from the arduino board.");
      Serial.println("|step [motor] [direction] [regime] - [motor]: 0 for X and 1 for Y; [direction]: 0 for backward and 1 for forward; [regime] 0 for half and 1 for full stepping.");
      
		} else {
      // If command is not one of the above commands, sends error message for unknown instruction
			Serial.println("ERROR: Unknown Instruction!");
		}

   currCmd="";

	}
}
