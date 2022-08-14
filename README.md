### Temperature Sensor

Compiler and IDE: https://ide.mbed.com/compiler/#nav:/mbed-os-example-mbed5-blinky/main.cpp;

Docs: https://cued-partib-device-programming.readthedocs.io/en/latest/introduction.html

### How to use

#### STM32 Nucleo

- Take the `temperature_sensor.bin` file and place it into the microcontroller directory
- Run `graph_live_temp.py` to view the live temperature

#### Arduino [see here for wireless version](https://github.com/lorcan2440/Wireless-Temperature-Sensor)

- Take the `temperature_sensor.cpp` file and copy the code into Arduino IDE
- Most likely need to adjust some pin numbers and maybe change how Serial works, but compile and run
- Run `graph_live_temp.py` to view the live temperature

![](connections.png?raw=true)
![](screenshot.png?raw=true)
