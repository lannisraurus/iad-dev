const byte input_pin = 2;
const byte output_pin = 4;
volatile byte state = LOW;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(input_pin, INPUT_PULLUP);
  pinMode(output_pin, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(input_pin)) state=LOW; else state=HIGH;

  digitalWrite(output_pin, state);


  delay(5);
}
