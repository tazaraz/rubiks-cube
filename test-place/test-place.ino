int ledPin = 22;  // LED connected to digital pin 13

void setup() {
  pinMode(ledPin, OUTPUT);  // sets the digital pin 13 as output
}

void loop() {
  digitalWrite(ledPin, HIGH);  // sets the LED to the button's value
}
