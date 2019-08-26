/* This code is used to cominucate with the PC and the NeoTrellis keypad*/

#include "Adafruit_NeoTrellis.h"
#include "stdio.h"
#define TIME_OUT 30 // 60 per second so 180 = 3s
#define BAUD_RATE 115200 // default is 9600
Adafruit_NeoTrellis trellis;

bool key_rising_edge = false;
bool key_rising_edge_old = false;
bool time_out_ctr_state = false;
int time_out_ctr = (TIME_OUT + 1);
int key_number = 16;
int key_number_old = 16;
int num = 16;
int color = 256;
char buf[80];
const int n = 3;
const int c = 4;
char buf_num[n];
char buf_color[c];
int colors[17];

//define a callback for key presses
TrellisCallback blink(keyEvent evt) {
  // Check is the pad pressed?
  if (evt.bit.EDGE == SEESAW_KEYPAD_EDGE_RISING) {
    key_rising_edge = false;
    key_number = evt.bit.NUM;
    trellis.pixels.setPixelColor(key_number, 0); //off rising
  } else if (evt.bit.EDGE == SEESAW_KEYPAD_EDGE_FALLING) {
    // or is the pad released?
    key_rising_edge = true;
    key_number = evt.bit.NUM;
    set_color(key_number); //on falling

  }
  // Turn on/off the neopixels!
  trellis.pixels.show();


  return 0;
}

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial);

  Serial.println("start");
  if (!trellis.begin()) {
    Serial.println("error"); //Could not start trellis, check wiring?
    while (1);               //This message wil not print because trellis.begin() is blocking
  } else {
    Serial.println("done"); //NeoPixel Trellis started
  }

  //activate all keys and set callbacks
  for (int i = 0; i < NEO_TRELLIS_NUM_KEYS; i++) {
    trellis.activateKey(i, SEESAW_KEYPAD_EDGE_RISING);
    trellis.activateKey(i, SEESAW_KEYPAD_EDGE_FALLING);
    trellis.registerCallback(i, blink);
  }

  //do a little animation to show we're on
  for (uint16_t i = 0; i < trellis.pixels.numPixels(); i++) {
    trellis.pixels.setPixelColor(i, Wheel(map(i, 0, trellis.pixels.numPixels(), 0, 255)));
    colors[i] = map(i, 0, trellis.pixels.numPixels(), 0, 255) + 1;
    trellis.pixels.show();
    delay(50);
  }
  //  for (uint16_t i = 0; i < trellis.pixels.numPixels(); i++) {
  //    trellis.pixels.setPixelColor(i, 0x000000);
  //    trellis.pixels.show();
  //    delay(50);
  //  }
}

void loop() {
  trellis.read();  // interrupt management does all the work! :)

  if ((time_out_ctr > TIME_OUT) or (key_number_old != key_number)) {
    time_out_ctr = 0;
    time_out_ctr_state = false;
  }
  else if (time_out_ctr <= TIME_OUT) {
    time_out_ctr += 1;
  }

  if (((key_rising_edge_old != key_rising_edge) and (time_out_ctr_state == false))) {
    Serial.println(key_number);
    key_number_old = key_number;
    time_out_ctr_state = true;
  }

  key_rising_edge_old = key_rising_edge;

  if (readline(Serial.read(), buf, 80) > 0) {
    // The first 2 numbers are the number of the button
    strncpy(buf_num, buf , 2);
    sscanf(buf_num, "%d", &num);
    // The second 3 numbers are the desired color
    strncpy(buf_color, buf + 2 , 3);
    sscanf(buf_color, "%d", &color);
    // The correct colors are saved in the array colors
    colors[num] = color;
    // Set the new color
    set_color(num);
    // Turn on/off the neopixels!
    trellis.pixels.show();
  }
  delay(20); //the trellis has a resolution of around 60hz
}


/******************************************/

// Input a value 0 to 255 to get a color value.
// The colors are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if (WheelPos < 85) {
    return trellis.pixels.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    return trellis.pixels.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
    WheelPos -= 170;
    return trellis.pixels.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  return 0;
}


/******************************************/

// Handle the input stream
int readline(int readch, char *buffer, int len) {
  static int pos = 0;
  int rpos;

  if (readch > 0) {
    switch (readch) {
      case '\r': // Ignore CR
        break;
      case '\n': // Return on new-line
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
      default:
        if (pos < len - 1) {
          buffer[pos++] = readch;
          buffer[pos] = 0;
        }
    }
  }
  return 0;
}

/******************************************/

// Set the color
void set_color(int num) {
  if (colors[num] == 0) {
    trellis.pixels.setPixelColor(num, 0);
  }
  else {
    trellis.pixels.setPixelColor(num, Wheel(colors[num] - 1));
  }
  return;
}


/******************************************/

// Print the color
//void set_color(int num) {
//  for (int i = 0; i < 16; i++) {
//    Serial.println(colors[i]);
//  }
//  return;
//}
