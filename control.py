#!/usr/bin/env python

import time
import os
import sys
# CM19a module
import CM19aDriver

# *************** CONFIGURATION ***************
POLLFREQ = 1   # Polling Frequency - Check for inbound commands every 1 second
HOST = '8.8.8.8'
# FAILURE needs to be determined by what the system ping returns
FAILURE = '0 received'
# prior failure test
#if 'request timed out' in data or 'Unreachable' or "100% packet loss" in data:

# Start logging and initialize driver
log = CM19aDriver.startLogging()      # log is an instance of the logger class
cm19a = CM19aDriver.CM19aDevice(POLLFREQ, log, polling = True) 

def test():
    if (os.path.exists('/tmp/teston')):
        if cm19a.initialised:
            print "Turning on test..."
            print time.ctime()
            result = cm19a.send("C", "1", "on")
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
        os.remove('/tmp/teston')
    if (os.path.exists('/tmp/testoff')):
        if cm19a.initialised:
            print "Turning off test..."
            print time.ctime()
            result = cm19a.send("C", "1", "off")
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
        os.remove('/tmp/testoff')

def lamp():
    if (os.path.exists('/tmp/lampon')):
        if cm19a.initialised:
            print "Turning on lamp..."
            print time.ctime()
            result = cm19a.send("C", "2", "on")
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
                lamp();
        os.remove('/tmp/lampon')
    if (os.path.exists('/tmp/lampoff')):
        if cm19a.initialised:
            print "Turning off lamp..."
            print time.ctime()
            for i in range (0,5):
                result = cm19a.send("C", "2", "off")
                time.sleep(2)
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
                lamp();
        os.remove('/tmp/lampoff')

def program():
    if (os.path.exists('/tmp/program')):
        if cm19a.initialised:
            print "Programming device..."
            print time.ctime()
            for i in range (0,5):
                result = cm19a.send("C", "3", "on")
                time.sleep(1)
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
        os.remove('/tmp/program')

def basement():
    if (os.path.exists('/tmp/basementon')):
        if cm19a.initialised:
            print "Turning on lamp..."
            print time.ctime()
            result = cm19a.send("C", "3", "on")
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
                lamp();
        os.remove('/tmp/basementon')
    if (os.path.exists('/tmp/basementoff')):
        if cm19a.initialised:
            print "Turning off lamp..."
            print time.ctime()
            for i in range (0,5):
                result = cm19a.send("C", "3", "off")
                time.sleep(2)
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
                lamp();
        os.remove('/tmp/basementoff')

def openspot():
    if (os.path.exists('/tmp/openspot-on')):
        if cm19a.initialised:
            print "Turning on Openspot..."
            print time.ctime()
            result = cm19a.send("C", "4", "on")
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
                lamp();
        os.remove('/tmp/openspot-on')
    if (os.path.exists('/tmp/openspot-off')):
        if cm19a.initialised:
            print "Turning off Openspot..."
            print time.ctime()
            for i in range (0,5):
                result = cm19a.send("C", "4", "off")
                time.sleep(2)
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
                lamp();
        os.remove('/tmp/openspot-off')

def reboot():
    if (os.path.exists('/tmp/reboot')):
        if cm19a.initialised:
            print "Shutting off router..."
            result = cm19a.send("A", "1", "off")
            if result:
                print "...Success"
            else:
                print  >> sys.stderr, "Command failed"
            time.sleep(10)
            print "Turning on router..."
            result = cm19a.send("A", "1", "on")
            if result:
                print "...Success"
                os.remove('/tmp/reboot')
                i = 0
            else:
                print  >> sys.stderr, "Command failed"

def control():
    test()
    lamp()
    basement()
    openspot()
    program()
    reboot()

while True:
    control()
    data = os.popen('ping -c 1 ' + HOST).read()
    if FAILURE in data:
        print "host unreachable at " + time.ctime()
        #print time.ctime()
        for i in range (0,12):
            control()
            data = os.popen('ping -c 1 ' + HOST).read()
            if FAILURE in data:
                print 'failure try # ' + str(i + 1) + " " + time.ctime()
                bounce = 1
                continue
            else:
                print "made connection at " + time.ctime() + "\n"
                bounce = 0
                break
        if (bounce == 1):
            print "Rebooting router"
            control()
            if cm19a.initialised:
                print "Turning off router at " + time.ctime()
                result = cm19a.send("A", "1", "off")
                if result:
                    print "...Success"
                    # sleep for 10 seconds to make sure router is truly off
                    time.sleep(10)
                    control()
                else:
                    print  >> sys.stderr, "Command failed"
                print "Now turning on router at "  + time.ctime()
                result = cm19a.send("A", "1", "on")
                if result:
                    print "...Success"
                    # sleep for 5 minutes. Check control() every 10 sec
                    #for i in range (0,90):
                    for i in range (0,30):
                        control()
                        time.sleep(10)
                else:
                    print  >> sys.stderr, "Command failed"
    else:
        time.sleep(10)
