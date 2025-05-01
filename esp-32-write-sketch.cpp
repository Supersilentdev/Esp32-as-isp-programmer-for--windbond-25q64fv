#include <SPI.h>

#define FLASH_CS 5  // Change to the correct chip select pin

SPIClass spi;

void setup() {
  Serial.begin(115200);
  spi.begin();  // Initialize SPI
  pinMode(FLASH_CS, OUTPUT);
  digitalWrite(FLASH_CS, HIGH);  // Chip is deselected

  Serial.println("Ready to flash the Winbond chip...");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    Serial.print("Received command: ");
    Serial.println(command);
    
    if (command == "id") {
      send_chip_id();
    } else if (command == "write") {
      start_write();
    }
  }
}

void send_chip_id() {
  byte id[3];
  digitalWrite(FLASH_CS, LOW);
  spi.transfer(0x9F);  // Command to read manufacturer ID and device ID
  for (int i = 0; i < 3; i++) {
    id[i] = spi.transfer(0x00);
  }
  digitalWrite(FLASH_CS, HIGH);
  Serial.print("Chip ID: ");
  for (int i = 0; i < 3; i++) {
    Serial.print(id[i], HEX);
    if (i < 2) Serial.print(":");
  }
  Serial.println();
}

void start_write() {
  Serial.println("Ready to receive data for writing...");
  
  // Send BEGIN_WRITE message to Python script to indicate the chip is ready
  Serial.println("BEGIN_WRITE");

  // Waiting for data from Python script to write to chip
  while (Serial.available()) {
    byte buffer[1024];
    int bytesRead = Serial.readBytes(buffer, sizeof(buffer));

    if (bytesRead > 0) {
      // Flash writing code goes here, writing buffer to the chip via SPI
      write_to_flash(buffer, bytesRead);
    }
  }
  Serial.println("Write complete.");
}

void write_to_flash(byte *buffer, int len) {
  digitalWrite(FLASH_CS, LOW);
  for (int i = 0; i < len; i++) {
    spi.transfer(buffer[i]);
  }
  digitalWrite(FLASH_CS, HIGH);
}
