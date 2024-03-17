# ReceiverLibrary
v.1.1

This library is intended for use in a Raspberry Pi Pico microcontroller to handle digital signals from a 433 MHz radio module. You can find this module on [Amazon](https://www.amazon.com/HiLetgo-Wireless-Transmitter-Receiver-Raspberry/dp/B01DKC2EY4/ref=sr_1_3?dib=eyJ2IjoiMSJ9.tNlJbSBQOEL92GF5uwdw_3SL16TQy5q53ghPMyP1cHEsrLxGHSv_Hrk051zSYoIKOV3SQOxT8WlPG1fWqBXTT2qJziGxOrVbRX8AA7w0lYnlZSmpK8G69bdIipY7qC98s63Tp4Auc2GXPUjxvkEA17zSVrBe0Hu2DsSEkeMOCp1ocImWadqcHmnRnU0TwXfq4_TeJ5_5FVu8ZNVvSN_ARLaKOvYZicok_mjMqcb6nTQ.SDqOOcts__5t69TnLcj5LbM_DOp22w5x4iSZq723qCQ&dib_tag=se&keywords=433mhz+receiver&qid=1710655441&sr=8-3). This module is perfect for simple short-range communication, whether it is to control your room LEDs or disable an alarm system. This module is cheap and easy to use. 

I created this library because, after some research, I couldn't find any other existing radio library that worked for Micropython (Raspberry Pi Pico's coding language). Therefore, I decided to make this library. 

## What the library does: 

This library receives a radio signal through the RF module and turns it into binary for your Raspberry Pi Pico. The algorithm is based on the Manchester code, a data transfer protocol that turns low and high-voltage signals to binary based on the length of the signal.
After receiving a signal from the RF module, the library translates the signal into binary code and returns if that code was expected. 

## How to use the library:

```python
from machine import Pin
from receiverLibrary import receiver

#For this function, use the pin you have your RF module connected to as an argument, in this example, I'm using GPIO pin 13.
rcv.receiver(13)

#This function saves an expected code as a string to an array starting from index 0. (Be careful not to use codes that are a mirror of each other)
rcv.add_expected('01101010')
rcv.add_expected('10011101')

#For this example, I'm going to use the LED that comes integrated into your Raspberry Pi Pico
led = Pin(25, Pin.OUT)

while True:

  #This function starts recording the input from the RF module to translate it into binary. 
  rcv.listen()

  #The get_index() function returns, in order, the index of the codes received. The index is determined by the order you saved the expected codes through the add_expected() function. 
  if rcv.get_index() == 0:
    #Code 01101010 turns the LED off
    led.value(0)
  elif rcv.get_index() == 1:
    #Code 10011101 turns the LED on
    led.value(1)

```
Alternatively to get_index(), you can use get_code() to get the whole string representing the code instead of just its index.
```python
rcv.get_code()
```

The library can read up to 24-bit-long messages at a time. By default, the library is set to read messages 8-bits long. You can change this by using:
```python
rcv.code_length = 16
```
Be sure that the codes you add through the add_expected() function are the same size as code_length(), you can see the current code_length by using
```python
print(rcv.get_code_length())
```

## How the library works:

The library measures the time between high voltage inputs sent by the RF whenever it detects a 433 MHz frequency. In other words, it measures how long the RF module doesn't receive any signal and turns it into binary depending on how long the lack of signal lasts. This has some advantages since you can send a very short signal and only worry about the time between the current and the next signal. Similar to Morse code. By default, the library expects a gap of 800 microseconds to represent a 1 and a gap of 2000 microseconds to represent a 0, but you can change it to any number you'd like as long as it is above 300 microseconds. Lower values have the chance to not be picked up. 
You can change these values by using:
```python
#Value must be in microseconds
rcv.set_short_pause(value)

rcv.set_long_pause(value)
```
