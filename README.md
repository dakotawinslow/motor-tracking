# motor-tracking
A repository of my research amterials for my acoustic motor tracking project

## Project Description

The idea here is to create a system that can detect the distance to a drone that is transmitting audio by beeping its motors. The process goes like this: 

1. Each drone motor emits a time-syncronized, gold-encoded, chirp-spread-spectrum modulated signal containing a timestamp and unique ID.
2. A signle microphone picks up the mixed signals.
3. An FPGA does the processing to demodulate and seperate the signals.
4. An ESP32 performs the final multilateration calculations to estimate the distance to the drone.

![receiver diagram](https://github.com/dakotawinslow/motor-tracking/blob/main/single-mic.drawio.png?raw=true)

However, it looks like the LilyGo board won't be able to do all of that. But maybe we can do the first part: reading the input data and storing it in a ring buffer that gets exposed to the ESP for transform analysis

basic signal of "!"(00100001), encoded with gold code 0: [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0]
110000101001101 001111010110010 001111010110010 001111010110010 001111010110010 110000101001101 001111010110010 001111010110010