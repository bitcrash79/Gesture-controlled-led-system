#define LED1 2
#define LED2 3
#define LED3 4
#define LED4 5
#define LED5 6

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  Serial.println("Ready!");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.length() == 5) {
      digitalWrite(LED1, cmd[0] == '1' ? HIGH : LOW);
      digitalWrite(LED2, cmd[1] == '1' ? HIGH : LOW);
      digitalWrite(LED3, cmd[2] == '1' ? HIGH : LOW);
      digitalWrite(LED4, cmd[3] == '1' ? HIGH : LOW);
      digitalWrite(LED5, cmd[4] == '1' ? HIGH : LOW);
    }
  }
}