#include <aJSON.h>
#include <LiquidCrystal.h>

char* parseJson(char *jsonString);

// rgb led pins
int redPin = 9;
int greenPin = 10;
int bluePin = 6;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  // setup the lcd display
  lcd.begin(16, 2); 
  lcd.clear();
  
  // setup rgb led
  pinMode (redPin, OUTPUT);
  pinMode (bluePin, OUTPUT);
  pinMode (greenPin, OUTPUT);
  updateRgbLed(189, 234, 19);
  
  // setup serial communication
  Serial.begin(9600); 
}

void updateRgbLed(int r, int g, int b) {
  analogWrite(redPin, r);
  analogWrite(greenPin, g);
  analogWrite(bluePin, b);
}

void updateLcdDisplay(String line1, String line2) {  
  lcd.clear();
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void loop() {
  readSerialLine();
}

void readSerialLine() {
  if (Serial.available()) {
    int i;
    char local_input[300];
    int bytes_read = Serial.readBytesUntil('\n', local_input, 300);
    char return_buffer[bytes_read+1];
    for (i=0; i<bytes_read; i++) {
      return_buffer[i] = local_input[i];
    }
    return_buffer[i] = '\0';
    
    parseJson(return_buffer);
  }
}

char* parseJson(char *jsonString) {
  // Extract and set rgb led color and lcd display message
  int red, green, blue;
  String lcd_row_1, lcd_row_2;
  aJsonObject* root = aJson.parse(jsonString);
  
  if (root != NULL) {
    aJsonObject* color = aJson.getObjectItem(root, "rgb");
    if (color != NULL) {
      red = color->child->valueint;
      green = color->child->next->valueint;
      blue = color->child->next->next->valueint;
    }
    
    aJsonObject* screenobj = aJson.getObjectItem(root, "screen");
    if (screenobj != NULL) {
      lcd_row_1 = screenobj->child->valuestring;
      lcd_row_2 = screenobj->child->next->valuestring;
    }
  }
  
  updateRgbLed(red, green, blue);
  updateLcdDisplay(lcd_row_1, lcd_row_2);
  
  aJson.deleteItem(root);
}
