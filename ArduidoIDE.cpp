#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define BUZZER_PIN 2

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {

  Serial.begin(9600);

  SPI.begin();

  rfid.PCD_Init();

  pinMode(BUZZER_PIN, OUTPUT);

  tone(BUZZER_PIN, 2000, 100);

  Serial.println("Sistema iniciado");
}

void loop() {

  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  String uid = "";

  for (byte i = 0; i < rfid.uid.size; i++) {

    if (rfid.uid.uidByte[i] < 0x10) {
      uid += "0";
    }

    uid += String(rfid.uid.uidByte[i], HEX);
  }

  uid.toUpperCase();

  tone(BUZZER_PIN, 1500, 100);

  Serial.print("{"evento":"rfid","uid":"");
  Serial.print(uid);
  Serial.println(""}");

  rfid.PICC_HaltA();
}