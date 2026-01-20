# Day 0
## 11/12/25
Today, we began some basic planning, I was still working on my box, but we were working on coming up with ideas. We decided that instead of doing something BORING and SIMPLE, we would use a webcam attached to a Raspberry Pi and do image recognition of good and bad widgets. While this is more complicated and requires more programming, it will actually make the mechanics significantly easier.

# Day 1
## 11/14/25
Yesterday, I flashed a Raspbian ISO onto a microSD card that Cronk gave me, then today I went to Cronk’s classroom to grab a Pi 3B+. Today during class we got a monitor, keyboard, and mouse that were going to be thrown out with the old engineering computers. We set up a little area in the corner of the room with the Pi, monitor, keyboard, and mouse and began working on our project. After all this was done, class was basically over, so we came in during seminar to work. We started with a quick feasibility test, we had Claude Sonnet 4.5 generate some testing code, it worked pretty well, and even better when using a flashlight placed right above the camera, putting the flashlight to the side created shadows that made the recognition unreliable.

# Day 2
## 11/18/25
Today, we had Claude adjust the code so it can also detect if there is a widget there at all, as it would say no widget = bad widget. Its code sucked and it didn’t work, and my Claude free prompts had run out for the day, but because I am a PYTHON PROGRAMMING GOD I fixed the code myself, so now it works, yippee! It can fairly reliably distinguish between good, bad, and no widgets. We also started on CAD, Markus made the magazine and I made a quick widget. During seminar, we got the we got the finished magazine and started to test it, we found you needed to push the widget ALL THE WAY OUT before it would fall.

# Day 3
## 11/20/25
To make the widgets come out easier, we chamfered the edges on the output. We also made the magazine modular so it is faster to print different variants of it.

# Day 4
## 12/1/25
Today, we did a TON more CAD, we found a linear actuator part on the public parts list in Onshape and modified our magazine to fit it. Markus bought a linear actuator that can extend four inches during the break, it should arrive tomorrow.

# Day 5
## 12/3/25
We got the linear actuator, did a ton of testing with it. It doesn’t really work unless you run it at 12v, which is fine, just good to know. Markus began work on a casing for the linear actuator so we can attach it near the front instead of the back. I started work on the ramp itself.

# Day 6
## 12/5/25
Did a bunch more work on the ramp, now have the linear actuator casing, but it doesn’t key in properly in the front, the actuator gets narrower, but casing stays at a constant width. The linear actuator is only attached to the casing in the back, so it needs to be tight in the front to not be able to rotate side-to-side.

# Day 7
## 12/9/25
I realized the side walls were too tall for the MDF sheets, so I made it shorter, and adjusted things a lot. This adjustment took me the vast majority of the class time we had today.

# Day 8
## 12/11/25
Today we tested the linear actuator with the box, but with the top plate so it was at the right height. The actuator was slightly too high and started hitting the wall. We couldn’t just sand the wall a bit to give it more room, because then the actuator would hit both the bottom and the next widget above, instead of JUST the bottom widget. We made these minor corrections and started printing, we didn’t get anything else done today. Yarema and Markus helped me study for a math quiz tomorrow.

# Day 9
## 12/15/25
Today I was struggling wayyyy too much to make finger joints for the sorting bins, so I personally didn’t get much done. Today we also tested the fixed version of widget magazine, the linear actuator no longer collides with it, yippee! During seminar, we started cutting the sorting boxes on the laser cutter, they didn’t finish before the end of seminar.

# Day 10
## 12/17/25
At the beginning of class we got the flipper stopper, which Markus designed). During class, we assembled the sorting bins with wood glue. We also cut out the servo mounting bracket for the flipper flopper. Not much else done this class, we had the OSU engineering presentation today. During seminar, I was able to do the last bits of CAD for the whole structure. I designed some MDF cross members to support the structure, and we got those all cut out on the laser cutter. Virtually everything is now ready to be manufactured and assembled now, yippee!
![CAD Overview](CAD-Screenshots/cad_overview_screenshot.png)

# Day 11
## 12/19/25
Today we just cut out a bunch of the side panels and such on the laser while Yarema finished the code.

# Day 12
## 1/7/26
Today we started gluing the whole structure together and also tried to figure out the CNC to get the ramp cut, we did not get it figured out.

# Day 13
## 1/9/26
We tried to CNC, we spent 20 minutes removing the paper from the acrylic, we then realized that the keying cut by the CNC was not even slightly centered because Markus gave Mr. Small the wrong dimensions >:c

Also everything that can be glued is now glued, the whole structure can stay together (the side panel is just sitting on, since the ramp still needs to be installed).

# Day 14
## 1/13/26
Mr. Small got our ramp cut on the CNC, so today we assembled everything - still without glue - and did some testing. I ran out of time to rewrite the awful AI code, so we just had to have the AI improve it with some modifications, ran out of prompts with completely broken code though, so we came in for seminar and had Keegan help fix it with us (He is much faster at troubleshooting than me, and that code is awful to read). We got it working though, minus the Arduino communication, gotta get that working tomorrow, hopefully we finish the project in time!

# Day 15
## 1/15/26
Mr. Small spent around half of class today talking about field trips and engineering classes for next year, so we had a bit less time. We did some final testing, it didn’t work perfectly, the flipper flopper didn’t want to move. We will have to work over the long weekend.

# Day ???
## 1/19/26
Today Yarema and Markus came to my house at 9:30 AM to work on the project, we got it fully working around 2 PM, although a lot of that time was waiting for glue to dry, lyrically analyzing J-pop, and going to Walmart to get glue because all the non-tacky glue my dad had was rock solid in the bottle.

