#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import signal
import sys
import datetime
import httplib, urllib  # for Push Notifications

# config.txt included in .gitignore first line is the token, the second line is the key
config = open('config.txt').readlines()
pushover_token = config[0].rstrip()
pushover_user = config[1].rstrip()

# Setting up Board GPIO Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)  # motor
GPIO.setup(22, GPIO.OUT)  # motor
GPIO.setup(16, GPIO.IN)  # Locked
GPIO.setup(12, GPIO.IN)  # Open


# Clean kill of script function (Stops Motor, cleans GPIO)
def Safe_Kill():
    print 'Performing safe shutoff!'
    GPIO.output(18, False)
    GPIO.output(22, False)
    GPIO.cleanup()
    sys.exit('Motors shutdown, GPIO cleaned')


def PushOver(message):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
         urllib.urlencode({
             "token": pushover_token,
             "user": pushover_user,
             "message": message,
             "sound": "bugle",
             "timestamp": datetime.datetime,
         }), {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    print response.status

# Argument controller
if len(sys.argv) > 3:  # Tests if you've entered too many arguments
    print "You've entered too many arguments!"
    print "Exiting program..."
    sys.exit(0)

if len(sys.argv) > 2:  # Argument for door action time
    try:
        float(sys.argv[2])
    except:
        print 'Error: ', str(sys.argv[2]), ' is not a number!'
        print "Exiting program..."
        sys.exit(0)
    if int(sys.argv[2]) > 65:  # Checks that a time longer than 60s isn't entered
        print 'Please choose a time less than 60s'
        print "Exiting program..."
        sys.exit(0)

if len(sys.argv) > 1:  # Argument for door action
    if sys.argv[1] != 'close' and sys.argv[1] != 'open':
        print 'Please choose "open" or "close"'
        print "Exiting program..."
        sys.exit(0)

if len(sys.argv) == 3:
    print 'Forcing door to', str(sys.argv[1]), 'for', str(sys.argv[2]), 'seconds'
    Door_Action = sys.argv[1]
    Door_Time = int(sys.argv[2])
if len(sys.argv) == 2:
    print 'Forcing door to ', str(sys.argv[1])
    Door_Action = sys.argv[1]
    Door_Time = 60  # This is a safety time
if len(sys.argv) == 1:
    Door_Action = 'default'  # Will reverse door state
    Door_Time = 60  # This is a safety time

# Start door!

# def DoorControl():
TimeStart = time.clock()
runTime = 0
# Check door status from Magnets
BottomHall = GPIO.input(16)
TopHall = GPIO.input(12)
if BottomHall == 0: print 'Door is locked'
if TopHall == 0: print 'Door is open'
if BottomHall == 1: print 'No magnet sensed on lock'
if TopHall == 1: print 'No magnet sensed top'
if Door_Action == 'open':  # Door is locked
    print 'The door is locked!'
    print 'The door is going up!'
    while TopHall == 1 and runTime < Door_Time:
        GPIO.output(18, True)
        GPIO.output(22, False)
        TopHall = GPIO.input(12)
        runTime = time.clock() - TimeStart
    if 65 == runTime:
        print 'Something went wrong, go check the door!'
        message = 'Coop open FAILED!'
        PushOver(message)
        Safe_Kill()
    if TopHall == 0:
        print 'Door is open!'
        message = 'Coop opened successfully!'
        PushOver(message)
        Safe_Kill()
elif Door_Action == 'close':  # Door is open
    print 'The door is open!'
    print 'The door is going down!'
    while BottomHall == 1 and runTime < Door_Time:
        GPIO.output(18, False)
        GPIO.output(22, True)
        BottomHall = GPIO.input(16)
        runTime = time.clock() - TimeStart
    if 65 == runTime:
        print 'Something went wrong, go check the door!'
        message = "Coop close FAILED!"
        PushOver(message)
        Safe_Kill()
    if BottomHall == 0:
        time.sleep(1)
        print 'Door is locked!'
        message = "Coop closed successfully!"
        PushOver(message)
        Safe_Kill()
elif BottomHall == 0:  # Door is locked
    print 'The door is locked!'
    print 'The door is going up!'
    while TopHall == 1 and runTime < Door_Time:
        GPIO.output(18, True)
        GPIO.output(22, False)
        TopHall = GPIO.input(12)
        runTime = time.clock() - TimeStart
    if 65 == runTime:
        print 'Something went wrong, go check the door!'
        message = "Coop open FAILED!"
        PushOver(message)
        Safe_Kill()
    if TopHall == 0:
        print 'Door is open!'
        message = "Coop opened successfully!"
        PushOver(message)
        Safe_Kill()
elif TopHall == 0:  # Door is open
    print 'The door is open!'
    print 'The door is going down!'
    while BottomHall == 1 and runTime < Door_Time:
        GPIO.output(18, False)
        GPIO.output(22, True)
        BottomHall = GPIO.input(16)
        runTime = time.clock() - TimeStart
    if 65 == runTime:
        print 'Something went wrong, go check the door!'
        message = "Coop close FAILED!"
        PushOver(message)
        Safe_Kill()
    if BottomHall == 0:
        print 'Door is locked!'
        message = "Coop closed successfully!"
        PushOver(message)
        Safe_Kill()
runTime = time.clock() - TimeStart
print 'Total Time: ' + str(runTime)
Safe_Kill()
