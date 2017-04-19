import pigo
import time
import random

'''
MR. A's Final Project Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        print("Your piggy has be instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 80
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 40
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 97
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 100
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()


    ########################
    ### CLASS METHODS - these are the actions that your object can run
    #### (they can take parameters can return stuff to you, too)
    #### (they all take self as a param because they're not static methods)
    ########################


    ##### DISPLAY THE MENU, CALL METHODS BASED ON RESPONSE
    def menu(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "t": ("Turn test", self.turn_test),
                "s": ("Check status", self.status),
                "o": ("Count Obstacles", self.count_obstacles),
                "f": ("Final", self.final),
                "z": ("Total Obstacles", self.total_obstacles),
                "q": ("Quit", quit),
                "k": ("Smart Scan", self.smart_scan)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def final(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        while True:
            answer = self.is_clear()
            if answer:
                self.cruise()
            else:
                self.smart_cruise()



    def cruise(self):
        self.fwd()  # I added this to pigo
        while self.is_clear():
            time.sleep(.1)
        self.stop()
        self.encB(3)


    def smart_scan(self):
        #dump all values
        self.flush_scan()
        #Counting number of safe scans
        counter = 0
        for x in range(self.MIDPOINT-60, self.MIDPOINT+60, +2):
            self.servo(x)
            time.sleep(.1)
            scan1 = self.dist()
            time.sleep(.1)
            #double check the distance
            scan2 = self.dist()
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = self.dist()
                time.sleep(.1)
                #take another scan and average the three together
                scan1 = (scan1+scan2+scan3)/3
            print("Degree: "+str(x)+", distance: "+str(scan1))
            if scan1 > self.STOP_DIST + 20:
                counter += 1
            elif scan1 <= self.STOP_DIST + 20:
                counter = 0
            if counter == 7:
                print("I found seven in a row "+str(scan1))
                return x - 7
            time.sleep(.01)

    def smart_cruise(self):
        answer = self.smart_scan()
        if answer < self.MIDPOINT:
            print("I need to turn left")
            difference = abs(self.MIDPOINT - answer)
            self.encL(difference / 10)
        elif answer > self.MIDPOINT:
            print("I need to turn right")
            difference = abs(self.MIDPOINT - answer)
            self.encR(difference / 10)






# choose_path (Renamed choose_p) method need editing
    def choose_p(self):
        print('Considering options...')
        if self.is_clear():
            return "fwd"
        else:
            self.wide_scan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT-60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is '+str(avgRight)+'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT+60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"




    def count_obstacles(self):
        # run a scan
        self.wide_scan()
        # Count how many obstacles ive found
        counter = 0
        # Starting state assumes no obstacles
        found_something = False
        # loop though all my scan data
        for x in self.scan:
            # if x is not None and really close
            if x and x <= self.STOP_DIST:
                # if I've already found something
                if found_something:
                    print("obstacle continues")
                # is this is a new obstacle
                else:
                    # switch my tracker
                    found_something = True
                    print("Start of new obstacle")
            # if my data show safe distance...
            if x and x > self.STOP_DIST:
                # if my tracker had been triggered...
                if found_something:
                    print("end of obstacle")
                    # reset tracker
                    found_something = False
                    # increase count of obstacles
                    counter += 1
        print("Total number of obstacles in this scan " + str(counter))
        return counter

    def total_obstacles(self):
        counter = 0
        for x in range(4):
            counter += self.count_obstacles()
            self.encR(7)
        print("Total number of obstacles in this total scan: " + str(counter))

    def sweep(self):
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
            self.servo(x)
            self.scan[x] = self.dist()
        print("Here's what I saw: ")
        print(self.scan)

    def safety_dance(self):
        for y in range(3):
            for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60,2):
                self.servo(x)
                if self.dist() < 30:
                    print("WALLLLLLLLL-EEEEEEEEE")
                    return
                self.encR(7)
        self.dance()


    def turn_test(self):
        while True:
            ans = raw_input('Turn right, left or stop? (r/l/s): ')
            if ans == 'r':
                val = int(raw_input('/nBy how much?: '))
                self.encR(val)
            elif ans == 'l':
                val = int(raw_input('/nBy how much?: '))
                self.encL(val)
            else:
                break
        self.restore_heading()

    def restore_heading(self):
        print("returning to starting position")
        if self.turn_track > 0:
            val = abs(self.turn_track)
            self.encL(val)
        elif self.turn_track < 0:
            val = abs(self.turn_track)
            self.encR(val)



    #YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        # 7=quarter
        # 15=half
        # 30=full
        self.sprinkler()
        self.chacha()
        self.sprinkler()
        self.chacha2()
        #self.back_it_up()

    def shimmy(self):
        print('shimmy')
        for x in range(3):
            self.servo(30)
            self.servo(140)
            self.servo(30)


    def chacha(self):
        print('chacha')
        for x in range(2):
            self.encL(4)
            self.encF(15)
            time.sleep(.25)
            self.encR(4)
            self.encL(7)
            self.encR(4)
            self.encR(30)
            self.encB(15)
            time.sleep(.25)
            self.encB(15)
            time.sleep(.25)
            self.encR(4)
            self.encL(7)
            self.encR(4)
            self.encR(30)
            self.encF(15)
            time.sleep(.25)
        for x in range(3):
            self.encR(30)

    def chacha2(self):
        self.encR(15)
        for x in range(2):
            self.encL(4)
            self.encF(15)
            time.sleep(.25)
            self.encR(4)
            self.encL(7)
            self.encR(4)
            self.encR(30)
            self.encB(15)
            time.sleep(.25)
            self.encB(15)
            time.sleep(.25)
            self.encR(4)
            self.encL(7)
            self.encR(4)
            self.encR(30)
            self.encF(15)
            time.sleep(.25)
        for x in range(3):
            self.encR(30)

    def sprinkler(self):
        print('sprinkler')
        for x in range(3):
            for x in range(20,160,20):
                self.servo(x)




    ########################
    ### MAIN LOGIC LOOP - the core algorithm of my navigation
    ### (kind of a big deal)
    ########################

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"

    def encR(self, enc):
        pigo.Pigo.encR(self, enc)
        self.turn_track += enc

    def encL(self, enc):
        pigo.Pigo.encL(self, enc)
        self.turn_track -= enc


####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

try:
    g = GoPiggy()
except (KeyboardInterrupt, SystemExit):
    from gopigo import *
    stop()
