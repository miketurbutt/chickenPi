#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import math
import signal
import sys
import datetime
import httplib, urllib  # for Push Notifications

# config.txt included in .gitignore first line is the token, the second line is the key
# config = open('config.txt').readlines()
pushover_token = 'aZ48abAEXfJouw9p3ZHaXPtrgo1URM'
pushover_user = 'u585xQwjtPfKEQdjFkdC243J8uryyk'

RunningTime = 0
DoorStatus = 'unknown'
TimeStart = time.time()

# Setting up Board GPIO Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)  # motor
GPIO.setup(22, GPIO.OUT)  # motor
GPIO.setup(16, GPIO.IN)  # Open
GPIO.setup(12, GPIO.IN)  # Closed

def getRunningTime():
    time.sleep(1)
    # print 'getRunningTime', TimeStart, time.time()
    return math.floor(time.time() - TimeStart)

# Clean kill of script function (Stops Motor, cleans GPIO)
def Safe_Kill():
    print 'Performing safe shutoff!'
    GPIO.output(18, False)
    GPIO.output(22, False)
    GPIO.cleanup()
    time.sleep(1)
    return('Motors shutdown, GPIO cleaned')

def isOpen():
    return GPIO.input(16) == 0
    
def isClosed():    
    return GPIO.input(12) == 0
 
def driveOpen():
    GPIO.output(18, True)
    GPIO.output(22, False)

def driveClosed():
    GPIO.output(18, False)
    GPIO.output(22, True)

if isClosed(): DoorStatus = 'Closed'
elif isOpen(): DoorStatus = 'open'

def PushOver(message, sound):
    Safe_Kill()
    print 'Sending Pushover', message, sound
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
         urllib.urlencode({
             "token": pushover_token,
             "user": pushover_user,
             "message": message,
             "sound": sound,
             "timestamp": datetime.datetime,
         }), {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    print response.status
    sys.exit(0)

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
    if int(sys.argv[2]) > 39:  # Checks that a time longer than 39s isn't entered
        print 'Please choose a time less than 39s'
        print "Exiting program..."
        sys.exit(0)

if len(sys.argv) > 1:  # Argument for door action
    if sys.argv[1] not in ['close', 'open', 'status']:
        print 'Please choose "open", "close" or "status"'
        print "Exiting program..."
        sys.exit(0)

if len(sys.argv) == 3:
    print 'Forcing door to', str(sys.argv[1]), 'for', str(sys.argv[2]), 'seconds'
    DoorAction = sys.argv[1]
    DoorTimeout = int(sys.argv[2])
if len(sys.argv) == 2:
    print 'Forcing door to ', str(sys.argv[1])
    DoorAction = sys.argv[1]
    DoorTimeout = 39  # This is a safety time
if len(sys.argv) == 1:
    DoorAction = 'default'  # Will reverse door state
    DoorTimeout = 39  # This is a safety time

print 'DoorAction is', DoorAction
print 'DoorTimeout is', DoorTimeout
print 'DoorStatus is', DoorStatus

# TODO try and except 

if DoorAction == 'status':
    PushOver(DoorStatus, 'Bike')
elif DoorAction == 'open':
    while RunningTime < DoorTimeout:
        driveOpen()
        RunningTime = getRunningTime()
        if isOpen(): PushOver('Coop opened successfully in ' + str(RunningTime) + ' secs :)', 'Bugle')
    PushOver('Coop open FAILED! :(', 'Siren')
elif DoorAction == 'close':
    while RunningTime < DoorTimeout:
        driveClosed()
        RunningTime = getRunningTime()
        if isClosed(): PushOver('Coop closed successfully in ' + str(RunningTime) + ' secs :)', 'Bugle')
    PushOver('Coop close FAILED! :(', 'Siren')
elif DoorAction != 'default':
    PushOver('Invalid DoorAction of: ' + DoorAction, 'Run')
elif isClosed() and isOpen():
    PushOver('Invalid DoorStatus (both): ' + DoorStatus, 'Run')
elif not isClosed() and not isOpen():
    PushOver('Invalid DoorStatus (neither): ' + DoorStatus, 'Run')
elif isClosed():
    print 'The door is closed and so being opened!'
    while RunningTime < DoorTimeout:
        driveOpen()
        RunningTime = getRunningTime()
        if isOpen(): PushOver('Coop opened successfully in ' + str(RunningTime) + ' secs :)', 'Bugle') 
    PushOver('Coop open FAILED! :(', 'Siren')    
elif isOpen():
    print 'The door is open and so going down!'
    while RunningTime < DoorTimeout:
        driveClosed()
        RunningTime = getRunningTime()
        if isClosed(): PushOver('Coop closed successfully ' + str(RunningTime) + ' secs :)', 'Bugle') 
    PushOver('Coop close FAILED! :(', 'Siren')

PushOver('WTF is happening?! :o', 'Run') 

