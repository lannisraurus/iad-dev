# Instrumentation and Data Acquisition Projects

This repository contains two projects that were developed as part of the Instrumentation and Data Acquisition course in the BSc. of Engineering Physics @ Instituto Superior Técnico.

Both projects were developed over the course of 8 weeks, and involved circuitry, communication between controller boards like Arduino and Raspberry Pi, and the acquisition of physical quantities (images, voltages, ...).

# Arduino Interface

The first project, *Arduino Interface*, was developed in the first two weeks.

It consists of a GUI application for a RPi / Regular computer which is connected to an Arduino, and is used to send instructions and receive gathered data.

The applications allows for the control of programme variables through commands (written in a text input bar with terminal-like functionalities like accessing previously sent commands), plotting data and provides a text window with the command descriptions, which also shows the commands implemented in the Arduino. Commands which only affect the programme are called 'internal'; commands which are entirely processed by the Arduino are called 'external'; finally, commands which use both commands (example: data gathering routines) are called 'mixed'. The applications also provides a console log, a run and interrupt button.

The application is inside the 'Arduino Interface' folder.

![Arduino Interface](arduino_interface_example.png)

# Astrolocator

The second project, *Astrolocator*, was developed in the subsequent weeks.

It consists of a GUI application for a RPi, which is used to control various periferals - a camera, a laser and 2 stepper motors.

The programme provides 