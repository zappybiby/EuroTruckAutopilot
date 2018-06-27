EuroTruckAutopilot is a program written in Python that aims to autonomously drive a truck in Euro Truck Simulator 2. To do this, it uses computer vision to detect road lanes and then moves the mouse to drive the truck.

Currently, the program will only run on Windows. 

## Windows Instructions:
#### Required to allow input to work in Windows:
1. **Go to C:\Users\YOURUSERNAME\Documents\Euro Truck Simulator 2\profiles and edit controls.sii from** 
```
config_lines[0]: "device keyboard `di8.keyboard`"
config_lines[1]: "device mouse `fusion.mouse`"
```
to 
```
config_lines[0]: "device keyboard `sys.keyboard`"
config_lines[1]: "device mouse `sys.mouse`"
```
(thanks Komat!)

2. **While you are in controls.sii, make sure your sensitivity is set to:**
```
 config_lines[33]: "constant c_rsteersens 0.775000"
 config_lines[34]: "constant c_asteersens 4.650000"
```
3. **Finally, set controls.sii to read-only to prevent ETS2 from changing it.**

### Latest Video: Previous lines are now stored and mouse movement has been implemented

- https://www.youtube.com/watch?v=WxbL_NPUOnk

### Older Videos: 
1. Lane Detection proof-of-concept
    - https://www.youtube.com/watch?v=_s00JKtwZUc
