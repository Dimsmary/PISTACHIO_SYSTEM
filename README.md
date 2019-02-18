# PISTACHIO_SYSTEM
This is a program for MCU,which witten in Micropython.  
MCU:ESP8266  
Learn more about the [Micropython](micropython.org)
## HardWare
ESP8266 MCU with 4MB SPI FLASH ROM.  
A 128x64 oled screen with I2C port.(SPI is also ok ,but you have to change the code)  
## How it works
A timer will start when boot.It will check the status of AP and STA.And display the status on the oled.  
A loop will send a HTML page to anyone who connect to it.  
CLASS:Block can read a 8x8 image from pic_lib,and display it.
