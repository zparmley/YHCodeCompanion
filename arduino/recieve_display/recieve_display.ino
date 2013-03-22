#include <aJSON.h>
// JSON TEST
char* parseJson(char *jsonString) ;

int redPin = 6;
int greenPin = 5;
int bluePin = 3;

int incomingByte = 0;   // for incoming serial data

//const byte MAXIMUM_INPUT_LENGTH = 500;
byte currentIndex = 0;
char local_input[300];
char endchar = '\n';
char* screen_1;
char* screen_2;
int rgb[3] = {0, 0, 0};
int i = 0;


void setup() {
  pinMode (redPin, OUTPUT); // Pino 3 declarado como saída
  pinMode (bluePin, OUTPUT); // Pino 5 declarado como saída
  pinMode (greenPin, OUTPUT); // Pino 6 declarado como saída
  Serial.begin(9600);
}

void clearLed() {
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);
}

void setLed(int l_rgb[3]) {
  Serial.println("Setting lcd");
  analogWrite(redPin, l_rgb[0]);
  analogWrite(greenPin, l_rgb[1]);
  analogWrite(bluePin, l_rgb[2]);
}

void setLcd(char* line1, char* line2) {
  Serial.println(line1);
  Serial.println(line2);
}

void loop() {
  readSerialLine();
}

//void readSerialLine() {
//  if (Serial.available()) {
//    char local_input[MAXIMUM_INPUT_LENGTH+1] = {'\0'};
//    byte local_current_index = 0;
//    char nextchar = Serial.read();
//    char endchar = '\n';
//    while (nextchar != endchar){
////      if (local_current_index>=MAXIMUM_INPUT_LENGTH){
////        for (byte i=0; i<=MAXIMUM_INPUT_LENGTH; i++) {
////          *local_input = '\0'; //clear input
////        }
////        local_current_index = 0; //start over
////      }
//      local_input[local_current_index++] = nextchar;
//      nextchar = Serial.read();
////      delay(200);
//    }
//    Serial.print("input is: ");
//    Serial.println(local_input);
//    parseJson(local_input);
//  }
//}

void readSerialLine() {
  if (Serial.available()) {
    int bytes_read = Serial.readBytesUntil(endchar, local_input, 300);
    char return_buffer[bytes_read+1];
    for (i=0; i<bytes_read; i++) {
      return_buffer[i] = local_input[i];
    }
    return_buffer[i] = '\0';
    i = 0;
    
//    Serial.println("input is: ");
//    Serial.println(return_buffer);
    parseJson(return_buffer);
  }
}


char* parseJson(char *jsonString) {
  Serial.println(jsonString);
  aJsonObject* root = aJson.parse(jsonString);
  if (root != NULL) {
    aJsonObject* color = aJson.getObjectItem(root, "rgb");
    if (color != NULL) {
      Serial.println("Color got it");
      rgb[0] = color->child->valueint;
      rgb[1] = color->child->next->valueint;
      rgb[2] = color->child->next->next->valueint;
    }
    
    aJsonObject* screenobj = aJson.getObjectItem(root, "screen");
    if (screenobj != NULL) {
      Serial.println("Screen got it");
      screen_1 = screenobj->child->valuestring;
      screen_2 = screenobj->child->next->valuestring;
    }
  }
  setLed(rgb);
  setLcd(screen_1, screen_2);
  
  aJson.deleteItem(root);
}
