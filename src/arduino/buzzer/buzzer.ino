const int BUZZER[] = {
  2, 3, 4, 5, 6, 7, 8, 9
};
const int LED_PIN = 13;

int number_of_buzzer = 8;
bool buzzer_active[] = {
  true, true, true, true, true, true, true, true
};
bool locked = false;


void setup() {
  Serial.begin(9600);
  for (int i = 0; i < number_of_buzzer; i++) {
    pinMode(BUZZER[i], INPUT);
  }
  pinMode(LED_PIN, OUTPUT);
}


void loop() {
  // check if buzzer is pressed and print information to serial interface
  for (int i = 0; i < number_of_buzzer; i++) {
    if (digitalRead(BUZZER[i]) && buzzer_active[i]) {
      Serial.print(i);
      Serial.print(";");
      Serial.print(BUZZER[i]);
      Serial.print(";");
      Serial.println(millis());
      buzzer_active[i] = false;
      locked = true;
    }
  }

  // display on arduino that someone has already buzzered
  if (locked) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  if (Serial.available()) {
    String input_string = Serial.readString();
    if (input_string == "reset\n") {
      locked = false;
      for (int i = 0; i < number_of_buzzer; i++) {
        buzzer_active[i] = true;
      }
    }
  }

  delay(1);
}
