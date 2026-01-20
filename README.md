# Needlessly-Overcomplicated-Widget-Sorter
Portfolio for our widget sorter project

# Table of Contents

1. [Acknowledgments](https://github.com/noahg460505/Needlessly-Overcomplicated-Widget-Sorter/blob/main/README.md#acknowledgements)
2. [Setup](https://github.com/noahg460505/Needlessly-Overcomplicated-Widget-Sorter/blob/main/README.md#setup)
3. [Sorting](https://github.com/noahg460505/Needlessly-Overcomplicated-Widget-Sorter/blob/main/README.md#sorting)
4. [AI Acknowledgment](https://github.com/noahg460505/Needlessly-Overcomplicated-Widget-Sorter/blob/main/README.md#ai-acknowledgement)

# Acknowledgements

This widget sorter was designed, built, and tested by Noah, Yarema, and Markus, with help from Keegan, Nolan, and Claude Sonnet. 

Machining was done using equipment in the Southridge High School Engineering Lab, including
- A Carvera CNC
- A Prusa Mk3 3D-Printer
- A Laser Cutter

All CAD was done in OnShape 

All Arduino and C++ code was done in the latest version of both the Windows edition of the desktop IDE and the Linux edition of the desktop IDE. The Python code was done in Thonny on a Raspberry Pi 3B+, which was "acquired" from Mr. Cronk.

The Linear Actuator and Loctite used in this project were acquired through out-of-pocket funds. 

# Setup

(how to get this to work, hopefully)

Ensure that all LEDs on the Arduino are connected properly. This can be tested by uploading the code to the Arduino; if the wiring is successful, the LEDs should all light up. 

A standard microUSB should be connected from the Pi at port `USB0` into the Arduino. From the power strip, a 12v power supply should be connected. 
The Pi should be connected to a keyboard and monitor. We recommend using KDE Connect so that coding can be done from multiple devices. 

# Sorting

Start by turning on the Arduino and ensuring that it is fully active. Let the Arduino dispense one widget into the capture zone, and then take it out. Run the Python command to execute the widget sorting program. If the camera fails to connect, rerun the program. Once the Arduino is on, there is no need to restart it or turn it off. It is recommended to shine a light on the backside of the capture zone to minimize sorting errors. 

# AI Acknowledgement

The vast majority of [the Python code](code/widget_inspector.py) for this project was done by Claude Sonnet 4.5, with edits made by Noah Grimes and Keegan Smit.
