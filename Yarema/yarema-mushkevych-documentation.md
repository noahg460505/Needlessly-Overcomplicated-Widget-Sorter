# Yarema Mushkevych's Daily Notebook

NOTE: Documentation isn’t 100% accurate. Some info may be missing from certain days

## Day 1 — 12/1/2025

Today, I wrote rudimentary Arduino code in TinkerCAD to detect input to the serial monitor. I designed a basic decimal to binary converter and began implementing the LEDs for the binary

## Day 2 — 12/3/2025

Today, I rewired the TinkerCAD BreadBoard to fit more components. Because we’re cool and using a binary display, the LEDs take up a lot of space and RedBoard pins, so the more space we can use, the better. Using the servo.h library, I added functionality to a motor — it spins one way if the widget is good (serial monitor receives a 1) and another way if it is bad (serial monitor receives a 0) — and wired it up to the BreadBoard. I also implemented a switch that turns the entire setup on and off.

Today, Markus brought in his Linear Actuator, which is basically a gearmotor with fancy parts. Using the gearmotor design in TinkerCAD and a motor controller, I simulated a linear actuator. Currently, it’s only set to spin while the sorter is active. Next time I work on it, I’ll make it turn on and off based on a signal. 

## Day 3 — 12/5/2025

Today, I reworked the code for detecting a new widget. Now, it receives a 2-digit value; the 10’s place is the number of good widgets and the 1’s place is the number of bad widgets. I added functionality for an extra servo to hold the widgets in place while the camera will take a photo.  

## Day 4 — 12/9/2025

I somehow thought that VIN will magically turn 5v into 12v and that I didn’t need a separate 12v power supply. Noah pointed out my mistake, but the arduino we were using didn’t have the 12v port, so I had to transfer all of the wiring (which thankfully wasn’t that much) to a different board. We tested the actuator and it worked. Next class I plan to finish the LEDs and maybe do more servo work.

## Day 5 — 12/11/2025

I wired up the LEDs, but there were issues with the green LEDs not being bright enough, so I ended up swapping them out for blue LEDs. 

## Day 6 — 12/15/2025

I worked on code for the arduino motors. Somehow Noah thought that we needed to run 12v into the motors, but they only need like 4.5. I switched to using 5v for the motors and they worked. 

## Day 7 — 12/17/2025

Today we listened to a presentation from OSU. I converted the code into functions to make it easier to move things around. 

## Day 8 — 12/19/2025

This was the last work day before break. I finished the code, but will still need to test it with the completed sorter body. 

## Day 9 — 1/7/2026

I didn’t have any more coding or wiring to do, so I helped wood glue the box together while Noah and Markus and Mr. Small tried to debug the CNC. Some guy in the class was watching Steins;Gate Ep. 12 on his laptop. Noah was very confused as to how I figured this out. 

## Day 10 — 1/9/2026

I did some more wood gluing. We got the CNC working. The protective layer took like 20 minutes to get off, but Markus gave the wrong dimensions :(. Noah made a github repository. We realized that we needed a red and green LED to show what the previous widget was (good or bad). We didn’t have room on the RedBoard so we swapped our yellow LED out for an RGB one. It did not work as expected, but I didn’t have to time to fix the issues.

## Day 11 — 1/13/2026

We got the final CNC done. I spent the entirety of class trying to fix the RGB led. I was unable to get it to work. I’m using the exact same code as in the arduino forums but it doesn’t work. I added stuff to the github at home. Keegan helped debug some of the AI code. At home I got the RGB to turn yellow(ish) when the mag was emptied but less than 10 widgets were sorted.

## Day 12 — 1/15/2026

I asked Claude and looked on the Arduino forums and figured out that I needed to change my wiring in order for the RGB to work. I changed the wiring but a lot of things broke. During seminar, I fixed the wiring issues and had the arduino send “READY” and “CAPTURE” commands to the Pi. Everything worked EXCEPT the flipperFlopper. 

## Day 13 — 1/19/2026

Today we were in Noah’s house from 9:30 – 2:00. We got the FlipperStopper working but it was janky, so we changed the initial position to 30° (center) and then 60° and 0° for good and bad widget. We took a video to prove that it worked in case it broke before tuesday. Noah didn’t have loc-tite so Marus drove us to Walmart so that we could buy some and glue the magazine together. We also finished the wood gluing. Our final test took a while since the sun was affecting our camera calibration. Noah’s dad ended up killing the sun which fixed our issue. The binary display broke near the end, so I’ll have to fix the wiring before next class

## Day 14 — 1/20/2026

Today was the last day to work. The fluorescent lights were causing issues with the threshold calibration for the image analysis software, but because that was an error that we couldn't really fix, Mr. Small just said that we didn't have to push ourselves further and that we did well. I started work on my portfolio
