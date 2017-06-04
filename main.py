#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import signal
import sys
import datetime
import httplib, urllib  # for Push Notifications
from astral import Astral

# Pushover tokens
pushover_token = 'aZ48abAEXfJouw9p3ZHaXPtrgo1URM'
pushover_user = 'u585xQwjtPfKEQdjFkdC243J8uryyk'

# Setting up Board GPIO Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)  # motor
GPIO.setup(22, GPIO.OUT)  # motor
GPIO.setup(16, GPIO.IN)  # Open
GPIO.setup(12, GPIO.IN)  # Locked

