# chickenPi

This is a simple RasPi chicken coop door control system.

I had this running via Node-Red so that it was use sunrise/sunset times to trigger the commandline python script.
The script checks whether the door is open or closed using reed switches with magnets on the door and then opens/closes the door with a single command:

```
python door_control
```

Args can be passed to the cmmd for testing (see script).

I used Pushover as a mobile notification system to tell me if the coop had opened/closed successfully or if there was an error that I had to physically check.

_PLEASE NOTE: This project is now dead as we moved house and no longer have chickens!_
_It was a couple of years ago so I can't remember a lot of the specifics so you're on your own._

You can see the door in operation at https://www.youtube.com/watch?v=rZawOiooJZ4

I used the following hardware components:

- Raspberry Pi (running local Node_Red and my script)
- LN298N motor controller
- 2 x Honeywell 2SS52M magnet sensors
- 12v PSU with stepdown from driving the Pi
