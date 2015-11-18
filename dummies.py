import runWorld as rw
import drawWorld as dw
import pygame as pg
from random import randint

################################################################

# This program is an interactive simulation/game. Two characters move
# across the screen (controlled by WASD and IJKL for a multiplayer
# game) and can slap each other backwards with another key command.
#
# The state of the torso is represented by a tuple (x position, y
# position, state of arm, for both players).
#
# A slap initiated outside of a certain region will have no affect on
# the other character's location, but the arm will still swing.
#
# The simulation ends when either player leaves the "ring" by fleeing
# or by being pushed out by the other player's slaps. 

################################################################

# Initialize world
name = "SMACK"
width = 1200
height = 800
rw.newDisplay(width, height, name)

################################################################

# Display the state by drawing two torsos with arms.
rightTorso = dw.loadImage("T_R.png")
rightHigh = dw.loadImage("R_H.png")  # -150, +255
rightLow = dw.loadImage("R_L.png")  # -150, -100

leftTorso = dw.loadImage("T_L.png")
leftHigh = dw.loadImage("L_H.png")  # 200, +225
leftLow = dw.loadImage("L_L.png")  # 200, -100


def updateDisplay(state):
    dw.fill(dw.black)
    if (state[4] == 1):
        dw.draw(leftHigh,(state [0] + 200, state[1] - 100))
    else:
        dw.draw(leftLow, (state[0] + 200, state[1] + 225))
    if (state[5] == 1):
        dw.draw(rightHigh, (state[2] - 150, state[3] - 100))
    else:
        dw.draw(rightLow, (state[2] - 150, state[3] + 225))

    dw.draw(rightTorso, (state[2], state[3]))
    dw.draw(leftTorso, (state[0], state[1]))



################################################################
# state -> state
def updateState(state):
    print("frame", state[7])
    return(state[0], state[1], state[2], state[3], state[4], state[5], state[6] - 1, state[7] - 1)

################################################################

# Terminate the simulation when the x coord reaches the screen edge,
# that is, when pos is less then zero or greater than the screen width
# state -> bool, or when y coord reaches screen edge for either image.


def endState(state):

    result = False

    leftWid = state[0] + 150
    leftHi = state[1] + 225
    rightWid = state[2] + 150
    rightHi = state[3] + 225

    if (leftWid > width or leftWid < 0) or (leftHi > height or leftHi < 0):
        result = True
        print("Player 2 Wins! (That's the guy on the right)")

    elif (rightWid > width or rightWid < 0) or (rightHi > height or rightHi < 0):
        result = True
        print("Player 1 Wins! (That's the guy on the left)")

    else:
        result = False

    return result

################################################################

# state -> event -> state
#
def handleEvent(state, event):
#        print("Handling event: " + str(event))
    state0mod = 0
    state1mod = 0
    state2mod = 0
    state3mod = 0

    state4 = state [4]
    state5 = state [5]

    state6mod = 0
    state7mod = 0

    if (event.type == pg.KEYDOWN):
        if (event.key == 119):
            state1mod -= 10
        if (event.key == 97):
            state0mod -= 10
        if (event.key == 115):
            state1mod += 10
        if (event.key == 100):
            state0mod += 10
        if (event.key == 106):
            state2mod -= 10
        if (event.key == 105):
            state3mod -= 10
        if (event.key == 107):
            state3mod += 10
        if (event.key == 108):
            state2mod += 10

        if(event.key == 99 or event.key == 120) and (state[6] < 0):
            state4 = (1 + state[4]) % 2
            state6mod += 30
            if(0<=(state[2]-state[0])<=400) and (abs(state[3]-state[1])<=300):
                state2mod += 75

        if(event.key == 44 or event.key == 46) and (state[7] < 0):
            state5 = (1 + state[5]) % 2
            state7mod += 30
            if(0<=(state[2]-state[0])<=400) and (abs(state[3]-state[1])<=300):
                state0mod -= 75

    return(state[0] + state0mod, state[1] + state1mod, state[2] + state2mod, state[3] + state3mod, state4, state5, state[6] + state6mod, state[7] + state7mod)

################################################################

initState = (100, 175, 900, 175, randint(0, 1), randint(0, 1), 120, 120)

# Run the simulation no faster than 60 frames per second
frameRate = 60

# Run the simulation!
rw.runWorld(initState, updateDisplay, updateState, handleEvent,
            endState, frameRate)
