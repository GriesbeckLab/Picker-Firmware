# Picker-Firmware
## Firmware and Low-Level interface for the Colony Picking robot.



![Image of Picker](https://raw.githubusercontent.com/GriesbeckLab/Picker-Firmware/master/picker.jpg)


## Description

This repositor consists of two sets of code: A custom modified version of the [Marlin firmware](https://github.com/MarlinFirmware/Marlin) based on the [Arduino platfrom](https://www.arduino.cc), and the low-level serial interface [Printrun](https://github.com/kliment/Printrun), which has been modified to handle the optical filter-wheel.
It should be used on the [Sanguinololu platform](http://reprap.org/wiki/Sanguinololu), but all Marlin-firmware Arduino-based board could be modified to use this firmware.

## Installing the Firmware

Install the Arduino framework, using [version 023](https://www.arduino.cc/en/Main/OldSoftwareReleases#00xx)

Then follow the folling procedure:
* If required, flash the boot-loader on the board, following these [instruction](http://reprap.org/wiki/Sanguinololu#Firmware)
* Add the Sanguinololu board-files to the arduino-0023\hardware directory
* Open the /Marlin/Marlin.ino file in Arduino 023
* Connect the board to the PC via USB, take note of the new serial port number.
* In the Arduino application, select Sanguinololu from Tools/Boards, and the new serial port from Tools/Srial Port
* Finally, click the 'Upload'buttong to compile and upload the firmware to the Sanguinololu Board. 

## Using the Firmware
* The Picker-Firmware/Printrun/ directory contains detailed information for using the Printrun software stack with the Sanguinololu board
* Refer to the Picker-Analysis repository for example applications of the firmware.
