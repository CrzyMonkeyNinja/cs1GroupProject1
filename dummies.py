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
#ddc
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
    if (state.player1arm == 1):
        dw.draw(leftHigh,(state.player1x + 200, state.player1y - 100))
    else:
        dw.draw(leftLow, (state.player1x + 200, state.player1y + 225))
    if (state.player2arm == 1):
        dw.draw(rightHigh, (state.player2x - 150, state.player2y - 100))
    else:
        dw.draw(rightLow, (state.player2x - 150, state.player2y + 225))

    if (state.player1slaps>=0):
        slapNumberLeft="0"
    else:
        slapNumberLeft=str(-state.player1slaps//30)

    if (state.player2slaps>=0):
        slapNumberRight="0"
    else:
        slapNumberRight=str(-state.player2slaps//30)
        
    slapCounterLeft=dw.makeLabel(slapNumberLeft,"Times New Roman, Ariel", 72, dw.white)
    slapCounterRight=dw.makeLabel(slapNumberRight,"Times New Roman, Ariel", 72, dw.white)

    dw.draw(rightTorso, (state.player2x, state.player2y))
    dw.draw(leftTorso, (state.player1x, state.player1y))
    dw.draw(slapCounterLeft, (50, 650))
    dw.draw(slapCounterRight, (1100,650))


################################################################
# state -> state
def updateState(state):
    state.player1slaps -= 1
    state.player2slaps -= 1
    return state

################################################################

# Terminate the simulation when the x coord reaches the screen edge,
# that is, when pos is less then zero or greater than the screen width
# state -> bool, or when y coord reaches screen edge for either image.


def endState(state):

    result = False

    leftWid = state.player1x + 150
    leftHi = state.player1y + 225
    rightWid = state.player2x + 150
    rightHi = state.player2y + 225

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

    if (event.type == pg.KEYDOWN):
        if (event.key == 119):
            state.player1y -= 10
        if (event.key == 97):
            state.player1x -= 10
        if (event.key == 115):
            state.player1y += 10
        if (event.key == 100):
            state.player1x += 10
        if (event.key == 106):
            state.player2x -= 10
        if (event.key == 105):
            state.player2y -= 10
        if (event.key == 107):
            state.player2y += 10
        if (event.key == 108):
            state.player2x += 10

        if(event.key == 99 or event.key == 120) and (state.player1slaps < 0):
            state.player1arm = (1 + state.player1arm) % 2
            state.player1slaps += 30
            if(0<=(state.player2x-state.player1x)<=400) and (abs(state.player2y-state.player1y)<=300):
                state.player2x += 75

        if(event.key == 44 or event.key == 46) and (state.player2slaps < 0):
            state.player2arm = (1 + state.player2arm) % 2
            state.player2slaps += 30
            if(0<=(state.player2x-state.player1x)<=400) and (abs(state.player2y-state.player1y)<=300):
                state.player1x -= 75

    return(state)

################################################################
class State(object):
    def __init__(self):
        self.player1x = 100
        self.player1y = 175
        self.player2x = 900
        self.player2y = 175
        self.player1arm = randint(0, 1)
        self.player2arm = randint(0, 1)
        self.player1slaps = -120
        self.player2slaps = -120
    
initState = State()

# Run the simulation no faster than 60 frames per second
frameRate = 60

# Run the simulation!
rw.runWorld(initState, updateDisplay, updateState, handleEvent,
            endState, frameRate)
