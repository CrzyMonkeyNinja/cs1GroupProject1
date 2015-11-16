import runWorld as rw
import drawWorld as dw
import pygame as pg
from random import randint

################################################################

# This program is an interactive simulation/game. A cat starts
# to move across the screen. The direction of movement is reversed
# on each "mouse down" event.
#
# The state of the cat is represented by a tuple (pos, delta-pos).
# The first element, pos, represents the x-coordinate of the cat.
# The second element, delta-pos, represents the amount that the
# position changes on each iteration of the simulation loop.
#
# For example, the tuple (7,1) would represent the cat at x-coord,
# 7, and moving to the right by 1 pixel per "clock tick."
# 
# The initial state of the cat in this program is (0,1), meaning that the cat
# starts at the left of the screen and moves right one pixel per tick.
#
# Pressing a mouse button down while this simulation run updates the cat state
# by leaving pos unchanged but reversing delta-pos (changing 1 to -1 and vice
# versa). That is, pressing a mouse key reverses the direction of the
# cat.
#
# The simulation ends when the cat is allowed to reach either the left
# or the right edge of the screen.

################################################################

# Initialize world
name = "Cat Fun. Press the mouse (but not too fast)!"
width = 1200
height = 800
rw.newDisplay(width, height, name)

################################################################

# Display the state by drawing a cat at that x coordinate
rightTorso = dw.loadImage("T_R.png")
rightHigh = dw.loadImage("R_H.png")  # -150, +255
rightLow = dw.loadImage("R_L.png")  # -150, -100

leftTorso = dw.loadImage("T_L.png")
leftHigh = dw.loadImage("L_H.png")  # 200, +225
leftLow = dw.loadImage("L_L.png")  # 200, -100

rightArm = (rightHigh, - 100)
leftArm = (leftLow, 225)

# state -> image (IO)
# draw the cat halfway up the screen (height/2) and at the x
# coordinate given by the first component of the state tuple


def updateDisplay(state):
    dw.fill(dw.black)
    dw.draw(rightArm[0], (state[2] - 150, state[3] + rightArm[1]))
    dw.draw(leftArm[0], (state[0] + 200, state[1] + leftArm[1]))
    dw.draw(rightTorso, (state[2], state[3]))
    dw.draw(leftTorso, (state[0], state[1]))


################################################################

# Change pos by delta-pos, leaving delta-pos unchanged
# Note that pos is accessed as state[0], and delta-pos
# as state[1]. Later on we'll see how to access state
# components by name (as we saw with records in Idris).
#
# state -> state
def updateState(state):
    return((state[0] + 1, state[1] + 1, state[2] - 1, state[3] - 1))

################################################################

# Terminate the simulation when the x coord reaches the screen edge,
# that is, when pos is less then zero or greater than the screen width
# state -> bool


def endState(state):
    leftWid = state[0] - 150
    leftHi = state[1] + 225
    rightWid = state[2] - 150
    rightHi = state[3] + 225

    if ((leftWid > width or leftWid < 0) or (leftHi > width or leftHi < 0)) or ((rightWid > height or rightWid < 0) or (rightHi > height or rightHi < 0)):
        return True
    else:
        return False


################################################################

# We handle each event by printing (a serialized version of) it on the console
# and by then responding to the event. If the event is not a "mouse button down
# event" we ignore it by just returning the current state unchanged. Otherwise
# we return a new state, with pos the same as in the original state, but
# delta-pos reversed: if the cat was moving right, we update delta-pos so that
# it moves left, and vice versa. Each mouse down event changes the cat
# direction. The game is to keep the cat alive by not letting it run off the
# edge of the screen.
#
# state -> event -> state
#
def handleEvent(state, event):  
#    print("Handling event: " + str(event))
        return(state)

################################################################

# World state will be single x coordinate at left edge of world

# The cat starts at the left, moving right 
initState = (randint(350, 550), randint(11, 277), randint(750, 950), randint(11, 277))

# Run the simulation no faster than 60 frames per second
frameRate = 60

# Run the simulation!
rw.runWorld(initState, updateDisplay, updateState, handleEvent,
            endState, frameRate)
