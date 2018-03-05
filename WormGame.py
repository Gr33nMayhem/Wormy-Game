#!/usr/bin/python
#
# Copyright (C) 2018 Azhar Ali Khaked <gr33nmayhem@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import gettext as _
from sugar3.graphics.xocolor import XoColor
from sugar3 import profile
import pygame
import sys
from pygame.locals import *
from random import randint
import random
from gi.repository import Gtk
import locale


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
darkColor = (0, 255, 0)
DARKdarkColor = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK
BROWN = (200, 128, 0)
GREY = (100, 100, 100)


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
FPSCLOCK = None
DISPLAYSURF = None
BASICFONT = None
HEAD = 0


def main():

    pygame.init()

    game = wormgame()

    game.run()


class wormgame():
    def __init__(self):
        pass

    def run(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, WINDOWWIDTH, WINDOWHEIGHT, FPS, CELLWIDTH, CELLHEIGHT, CELLSIZE, appleImg, introImg, wormCoords, fontObj, megaFont, answer, game, lightColor, darkColor, gameover
        XO1, XO2 = profile.get_color().to_string().split(',')
        lightColor = hex_to_rgb(XO2)
        darkColor = hex_to_rgb(XO1)

        infoObject = pygame.display.Info()
        WINDOWWIDTH = infoObject.current_w
        WINDOWHEIGHT = infoObject.current_h

        FPS = 15

        CELLSIZE = WINDOWHEIGHT / 40

        CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
        CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

        fontObj = pygame.font.Font('freesansbold.ttf', 32)
        megaFont = pygame.font.Font('freesansbold.ttf', 70)

        introImg = pygame.image.load('WormyIntro.png')
        introImg = pygame.transform.scale(
            introImg, (WINDOWWIDTH - 200, WINDOWHEIGHT - 200))

        appleImg = pygame.image.load('apple.png')
        appleImg = pygame.transform.scale(
            appleImg, (CELLSIZE * 3, CELLSIZE * 3))

        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Wormy')

        FPSCLOCK = pygame.time.Clock()
        showStartScreen()
        introScreen()
        while(1):
            gameover = False

            startx = random.randint(2, CELLWIDTH - 6)
            starty = random.randint(1, 4)
            wormCoords = [{'x': startx, 'y': starty},
                          {'x': startx - 1, 'y': starty},
                          {'x': startx - 2, 'y': starty}]
            direction = RIGHT
            DISPLAYSURF.fill(WHITE)
            answer, question, typeOfAnswer = randomQuery()

            appleEaten = 10  # set to any value not equal to 0, 1, 2 or 3
        # pick a random location for the answer
            if typeOfAnswer == 2:
                answerApple = random.randint(0, 2)
            else:
                answerApple = random.randint(0, 3)
        # The part where we generate appropriate random options
        #######################################################################
            if typeOfAnswer == 0:
                wrongAnswer0 = answer + (1) * (-1)**randint(1, 2)
                wrongAnswer1 = answer + (2) * (-1)**randint(1, 2)
                wrongAnswer2 = answer + (3) * (-1)**randint(1, 2)
                randomOptions = [wrongAnswer0, wrongAnswer2, wrongAnswer1]

            elif typeOfAnswer == 1:
                if answer == '+':
                    shuffle = random.randint(0, 2)
                    if shuffle == 0:
                        randomOptions = ['-', 'x', '/']
                    elif shuffle == 1:
                        randomOptions = ['x', '-', '/']
                    elif shuffle == 2:
                        randomOptions = ['/', 'x', '-']
                elif answer == '-':
                    shuffle = random.randint(0, 2)
                    if shuffle == 0:
                        randomOptions = ['+', 'x', '/']
                    elif shuffle == 1:
                        randomOptions = ['x', '+', '/']
                    elif shuffle == 2:
                        randomOptions = ['/', 'x', '+']
                elif answer == 'x':
                    shuffle = random.randint(0, 2)
                    if shuffle == 0:
                        randomOptions = ['+', '-', '/']
                    elif shuffle == 1:
                        randomOptions = ['-', '+', '/']
                    elif shuffle == 2:
                        randomOptions = ['/', '-', '+']
                elif answer == '/':
                    shuffle = random.randint(0, 2)
                    if shuffle == 0:
                        randomOptions = ['+', 'x', '-']
                    elif shuffle == 1:
                        randomOptions = ['x', '+', '-']
                    elif shuffle == 2:
                        randomOptions = ['-', 'x', '+']

            elif typeOfAnswer == 2:
                if answer == '=':
                    shuffle = random.randint(0, 1)
                    if shuffle == 0:
                        randomOptions = ['<', '>']
                    elif shuffle == 1:
                        randomOptions = ['>', '<']
                if answer == '<':
                    shuffle = random.randint(0, 1)
                    if shuffle == 0:
                        randomOptions = ['=', '>']
                    elif shuffle == 1:
                        randomOptions = ['>', '=']
                if answer == '>':
                    shuffle = random.randint(0, 1)
                    if shuffle == 0:
                        randomOptions = ['<', '=']
                    elif shuffle == 1:
                        randomOptions = ['=', '<']

        #######################################################################
            # Start the apple in a random place.
            apple0x, apple0y = getRandomLocation(0)
            apple1x, apple1y = getRandomLocation(1)
            apple2x, apple2y = getRandomLocation(2)
            apple3x, apple3y = getRandomLocation(3)

            while True:  # game game loop
                DISPLAYSURF.fill(WHITE)
                while Gtk.events_pending():
                    Gtk.main_iteration()
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN:

                        if (event.key == K_LEFT or event.key ==
                                K_a) and direction != RIGHT:
                            direction = LEFT
                        elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                            direction = RIGHT
                        elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                            direction = UP
                        elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                            direction = DOWN
                        elif event.key == K_ESCAPE:
                            terminate()

                for wormBody in wormCoords[1:]:
                    if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                        # game Over
                        gameover = showGameOverScreen(len(wormCoords) - 3)

                        is_true = True
                        while is_true:
                            while Gtk.events_pending():
                                Gtk.main_iteration()
                            for event in pygame.event.get():

                                if event.type == pygame.KEYDOWN:

                                    startx = random.randint(5, CELLWIDTH - 10)
                                    starty = random.randint(29, CELLHEIGHT - 2)
                                    wormCoords = [{'x': startx, 'y': starty},
                                                  {'x': startx - 1, 'y': starty},
                                                  {'x': startx - 2, 'y': starty}]
                                    direction = RIGHT
                                    apple0x, apple0y = getRandomLocation(0)
                                    apple1x, apple1y = getRandomLocation(1)
                                    apple2x, apple2y = getRandomLocation(2)
                                    apple3x, apple3y = getRandomLocation(3)
                                    is_true = False
                # check if worm has eaten an apply

                # check apple eaten 0
                if checkAppleEaten(apple0x, apple0y, 0, answerApple):
                    appleEaten = 0
                    # don't remove worm's tail segment
                    apple0x, apple0y = getRandomLocation(0)
                    apple1x, apple1y = getRandomLocation(1)
                    apple2x, apple2y = getRandomLocation(2)
                    apple3x, apple3y = getRandomLocation(3)

                    answer, question, typeOfAnswer = randomQuery()
                    # pick a random location for the answer
                    if typeOfAnswer == 2:
                        answerApple = random.randint(0, 2)
                    else:
                        answerApple = random.randint(0, 3)
                        # The part where we generate appropriate random options
                        #######################################################
                    if typeOfAnswer == 0:
                        wrongAnswer0 = answer + (1) * (-1)**randint(1, 2)
                        wrongAnswer1 = answer + (2) * (-1)**randint(1, 2)
                        wrongAnswer2 = answer + (3) * (-1)**randint(1, 2)
                        randomOptions = [
                            wrongAnswer0, wrongAnswer2, wrongAnswer1]

                    elif typeOfAnswer == 1:
                        if answer == '+':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['-', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '-', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '-']
                        elif answer == '-':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '+']
                        elif answer == 'x':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', '-', '/']
                            elif shuffle == 1:
                                randomOptions = ['-', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', '-', '+']
                        elif answer == '/':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '-']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '-']
                            elif shuffle == 2:
                                randomOptions = ['-', 'x', '+']

                    elif typeOfAnswer == 2:
                        if answer == '=':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '<']
                        if answer == '<':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['=', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '=']
                        if answer == '>':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '=']
                            elif shuffle == 1:
                                randomOptions = ['=', '<']

                    DISPLAYSURF.fill(WHITE)

                # check apple eaten 1

                
                elif checkAppleEaten(apple1x, apple1y, 1, answerApple):
                    appleEaten = 1
                    # don't remove worm's tail segment
                    apple0x, apple0y = getRandomLocation(0)
                    apple1x, apple1y = getRandomLocation(1)
                    apple2x, apple2y = getRandomLocation(2)
                    apple3x, apple3y = getRandomLocation(3)
                    DISPLAYSURF.fill(WHITE)
                    answer, question, typeOfAnswer = randomQuery()
                    # pick a random location for the answer
                    if typeOfAnswer == 2:
                        answerApple = random.randint(0, 2)
                    else:
                        answerApple = random.randint(0, 3)
                        # The part where we generate appropriate random options
                        #######################################################
                    if typeOfAnswer == 0:
                        wrongAnswer0 = answer + (1) * (-1)**randint(1, 2)
                        wrongAnswer1 = answer + (2) * (-1)**randint(1, 2)
                        wrongAnswer2 = answer + (3) * (-1)**randint(1, 2)
                        randomOptions = [
                            wrongAnswer0, wrongAnswer2, wrongAnswer1]

                    elif typeOfAnswer == 1:
                        if answer == '+':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['-', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '-', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '-']
                        elif answer == '-':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '+']
                        elif answer == 'x':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', '-', '/']
                            elif shuffle == 1:
                                randomOptions = ['-', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', '-', '+']
                        elif answer == '/':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '-']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '-']
                            elif shuffle == 2:
                                randomOptions = ['-', 'x', '+']

                    elif typeOfAnswer == 2:
                        if answer == '=':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '<']
                        if answer == '<':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['=', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '=']
                        if answer == '>':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '=']
                            elif shuffle == 1:
                                randomOptions = ['=', '<']

                    DISPLAYSURF.fill(WHITE)

                # check apple eaten 2

                
                elif checkAppleEaten(apple2x, apple2y, 2, answerApple):
                                    # don't remove worm's tail segment
                    apple0x, apple0y = getRandomLocation(0)
                    apple1x, apple1y = getRandomLocation(1)
                    apple2x, apple2y = getRandomLocation(2)
                    apple3x, apple3y = getRandomLocation(3)

                    answer, question, typeOfAnswer = randomQuery()
                    # pick a random location for the answer
                    if typeOfAnswer == 2:
                        answerApple = random.randint(0, 2)
                    else:
                        answerApple = random.randint(0, 3)
                        # The part where we generate appropriate random options
                        #######################################################
                    if typeOfAnswer == 0:
                        wrongAnswer0 = answer + (1) * (-1)**randint(1, 2)
                        wrongAnswer1 = answer + (2) * (-1)**randint(1, 2)
                        wrongAnswer2 = answer + (3) * (-1)**randint(1, 2)
                        randomOptions = [
                            wrongAnswer0, wrongAnswer2, wrongAnswer1]

                    elif typeOfAnswer == 1:
                        if answer == '+':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['-', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '-', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '-']
                        elif answer == '-':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '+']
                        elif answer == 'x':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', '-', '/']
                            elif shuffle == 1:
                                randomOptions = ['-', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', '-', '+']
                        elif answer == '/':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '-']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '-']
                            elif shuffle == 2:
                                randomOptions = ['-', 'x', '+']

                    elif typeOfAnswer == 2:
                        if answer == '=':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '<']
                        if answer == '<':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['=', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '=']
                        if answer == '>':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '=']
                            elif shuffle == 1:
                                randomOptions = ['=', '<']

                    DISPLAYSURF.fill(WHITE)

                # check if apple eaten 3, alos check if the operation is of
                # equality or not.

                
                elif typeOfAnswer != 2 and checkAppleEaten(apple3x, apple3y, 3, answerApple):
                                    # don't remove worm's tail segment
                    apple0x, apple0y = getRandomLocation(0)
                    apple1x, apple1y = getRandomLocation(1)
                    apple2x, apple2y = getRandomLocation(2)
                    apple3x, apple3y = getRandomLocation(3)

                    answer, question, typeOfAnswer = randomQuery()
                    # pick a random location for the answer
                    if typeOfAnswer == 2:
                        answerApple = random.randint(0, 2)
                    else:
                        answerApple = random.randint(0, 3)
                    # The part where we generate appropriate random options
                    ###########################################################
                    if typeOfAnswer == 0:
                        wrongAnswer0 = answer + (1) * (-1)**randint(1, 2)
                        wrongAnswer1 = answer + (2) * (-1)**randint(1, 2)
                        wrongAnswer2 = answer + (3) * (-1)**randint(1, 2)
                        randomOptions = [
                            wrongAnswer0, wrongAnswer2, wrongAnswer1]

                    elif typeOfAnswer == 1:
                        if answer == '+':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['-', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '-', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '-']
                        elif answer == '-':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '/']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', 'x', '+']
                        elif answer == 'x':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', '-', '/']
                            elif shuffle == 1:
                                randomOptions = ['-', '+', '/']
                            elif shuffle == 2:
                                randomOptions = ['/', '-', '+']
                        elif answer == '/':
                            shuffle = random.randint(0, 2)
                            if shuffle == 0:
                                randomOptions = ['+', 'x', '-']
                            elif shuffle == 1:
                                randomOptions = ['x', '+', '-']
                            elif shuffle == 2:
                                randomOptions = ['-', 'x', '+']

                    elif typeOfAnswer == 2:
                        if answer == '=':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '<']
                        if answer == '<':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['=', '>']
                            elif shuffle == 1:
                                randomOptions = ['>', '=']
                        if answer == '>':
                            shuffle = random.randint(0, 1)
                            if shuffle == 0:
                                randomOptions = ['<', '=']
                            elif shuffle == 1:
                                randomOptions = ['=', '<']

                    DISPLAYSURF.fill(WHITE)

                else:
                    del wormCoords[-1]  # remove worm's tail segment

                # move the worm by adding a segment in the direction it is
                # moving
                if wormCoords[HEAD]['x'] == CELLWIDTH:
                    wormCoords[HEAD]['x'] = 0

                if wormCoords[HEAD]['x'] == -1:
                    wormCoords[HEAD]['x'] = CELLWIDTH

                if wormCoords[HEAD]['y'] == CELLHEIGHT:
                    wormCoords[HEAD]['y'] = 0

                if wormCoords[HEAD]['y'] == -1:
                    wormCoords[HEAD]['y'] = CELLHEIGHT

                if direction == UP:
                    newHead = {
                        'x': wormCoords[HEAD]['x'],
                        'y': wormCoords[HEAD]['y'] - 1}
                elif direction == DOWN:
                    newHead = {
                        'x': wormCoords[HEAD]['x'],
                        'y': wormCoords[HEAD]['y'] + 1}
                elif direction == LEFT:
                    newHead = {
                        'x': wormCoords[HEAD]['x'] - 1,
                        'y': wormCoords[HEAD]['y']}
                elif direction == RIGHT:
                    newHead = {
                        'x': wormCoords[HEAD]['x'] + 1,
                        'y': wormCoords[HEAD]['y']}
                wormCoords.insert(0, newHead)

                if gameover:
                    break
                drawWorm(wormCoords)

                drawApple(
                    apple0x,
                    apple0y,
                    apple1x,
                    apple1y,
                    apple2x,
                    apple2y,
                    apple3x,
                    apple3y,
                    typeOfAnswer)
                drawOptions(
                    WINDOWHEIGHT / 40 * apple0x,
                    WINDOWHEIGHT / 40 * apple0y,
                    WINDOWHEIGHT / 40 * apple1x,
                    WINDOWHEIGHT / 40 * apple1y,
                    WINDOWHEIGHT / 40 * apple2x,
                    WINDOWHEIGHT / 40 * apple2y,
                    WINDOWHEIGHT / 40 * apple3x,
                    WINDOWHEIGHT / 40 * apple3y,
                    answer,
                    typeOfAnswer,
                    answerApple,
                    randomOptions)
                drawScore(len(wormCoords) - 3)

                # draw the question
                texSurfaceObj = fontObj.render(question, True, BLACK)
                texRectObj = texSurfaceObj.get_rect()
                texRectObj.center = (WINDOWWIDTH / 2, 20)
                DISPLAYSURF.blit(texSurfaceObj, texRectObj)

                pygame.display.update()
                FPSCLOCK.tick(FPS)

            showNextGameScreen()


def checkAppleEaten(applex, appley, checkApple, answerApple):
    global gameover
    for i in range(3):
        for j in range(3):
            if wormCoords[HEAD]['x'] - \
                    i == applex and wormCoords[HEAD]['y'] - j == appley:
                if checkApple == answerApple:
                    return True
                else:
                    gameover = showGameOverScreen(len(wormCoords) - 3)
    return False


def checkForKeyPress():

    for event1 in pygame.event.get():

        if event1.type == pygame.KEYUP:

            return True


def showGameOverScreen(score):
    flicker = 0
    while True:

        flicker += 1
        DISPLAYSURF.fill(lightColor)
        texSurfaceObj = megaFont.render(_("GAME OVER!"), True, darkColor)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        texSurfaceObj = megaFont.render(
            _("You Scored = %d") %
            (score), True, BLACK)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 90)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)

        if(flicker < 7):
            texSurfaceObj = fontObj.render(
                _("Press any key to continue"), True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        if(flicker == 15):
            flicker = 0
        while Gtk.events_pending():
            Gtk.main_iteration()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return True
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def introScreen():
    flicker = 0
    while True:
        flicker += 1
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(introImg, (100, 100))
        if(flicker < 15):
            texSurfaceObj = fontObj.render(
                _("Press any key to continue"), True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        if(flicker == 30):
            flicker = 0
        while Gtk.events_pending():
            Gtk.main_iteration()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return ()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showStartScreen():
    flicker = 0
    while True:
        flicker += 1
        DISPLAYSURF.fill(lightColor)
        texSurfaceObj = megaFont.render(("Wormy Game !"), True, darkColor)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)

        if(flicker < 15):
            texSurfaceObj = fontObj.render(
                _("Press any key to continue"), True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        if(flicker == 30):
            flicker = 0
        while Gtk.events_pending():
            Gtk.main_iteration()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return ()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showNextGameScreen():
    DISPLAYSURF.fill(GREY)
    texSurfaceObj = megaFont.render(_("3"), True, BLACK)
    texRectObj = texSurfaceObj.get_rect()
    texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
    pygame.display.update()
    pygame.time.wait(1000)
    DISPLAYSURF.fill(GREY)
    texSurfaceObj = megaFont.render(_("2"), True, BLACK)
    texRectObj = texSurfaceObj.get_rect()
    texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
    pygame.display.update()
    pygame.time.wait(1000)
    DISPLAYSURF.fill(GREY)
    texSurfaceObj = megaFont.render(_("1"), True, BLACK)
    texRectObj = texSurfaceObj.get_rect()
    texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
    pygame.display.update()
    pygame.time.wait(1000)
    DISPLAYSURF.fill(GREY)
    texSurfaceObj = megaFont.render(_("GO!"), True, BLACK)
    texRectObj = texSurfaceObj.get_rect()
    texRectObj.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
    pygame.display.update()
    pygame.time.wait(1500)


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation(c):
    if c == 0:
        while True:
            p = random.randint(3, CELLWIDTH / 2 - 3)
            q = random.randint(3, CELLHEIGHT / 2 - 3)
            if (wormCoords[HEAD]['x'] -
                3 > p or wormCoords[HEAD]['x'] +
                3 < p) and (wormCoords[HEAD]['y'] -
                            3 > q or wormCoords[HEAD]['y'] +
                            3 < q):
                break
        return p, q
    if c == 1:
        while True:
            p = random.randint(CELLWIDTH / 2, (CELLWIDTH - 7))
            q = random.randint(CELLHEIGHT / 2, (CELLHEIGHT - 7))
            if (wormCoords[HEAD]['x'] -
                3 > p or wormCoords[HEAD]['x'] +
                3 < p) and (wormCoords[HEAD]['y'] -
                            3 > q or wormCoords[HEAD]['y'] +
                            3 < q):
                break
        return p, q
    if c == 2:
        while True:
            p = random.randint(CELLWIDTH / 2, CELLWIDTH - 7)
            q = random.randint(3, CELLHEIGHT / 2 - 3)
            if (wormCoords[HEAD]['x'] -
                3 > p or wormCoords[HEAD]['x'] +
                3 < p) and (wormCoords[HEAD]['y'] -
                            3 > q or wormCoords[HEAD]['y'] +
                            3 < q):
                break
        return p, q
    if c == 3:
        while True:
            p = random.randint(3, CELLWIDTH / 2 - 3)
            q = random.randint(CELLHEIGHT / 2, CELLHEIGHT - 7)
            if (wormCoords[HEAD]['x'] -
                3 > p or wormCoords[HEAD]['x'] +
                3 < p) and (wormCoords[HEAD]['y'] -
                            3 > q or wormCoords[HEAD]['y'] +
                            3 < q):
                break
        return p, q


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, darkColor, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
            x + 3, y + 3, CELLSIZE - 6, CELLSIZE - 6)
        pygame.draw.rect(DISPLAYSURF, lightColor, wormInnerSegmentRect)


def drawOptions(
        apple0x,
        apple0y,
        apple1x,
        apple1y,
        apple2x,
        apple2y,
        apple3x,
        apple3y,
        answer,
        typeOfAnswer,
        answerApple,
        randomOptions):
    if typeOfAnswer == 0:
        count = 0
        c = 0
        for i in range(4):
            if i == answerApple:
                if count == 0:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple0x+CELLSIZE*2, apple0y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 1:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple1x+CELLSIZE*2, apple1y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 2:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple2x+CELLSIZE*2, apple2y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 3:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple3x+CELLSIZE*2, apple3y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                count = count + 1
            else:
                if count == 0:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple0x+CELLSIZE*2, apple0y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 1:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple1x+CELLSIZE*2, apple1y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 2:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple2x+CELLSIZE*2, apple2y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 3:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple3x+CELLSIZE*2, apple3y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                c = c + 1
                count = count + 1

    elif typeOfAnswer == 1:
        count = 0
        c = 0
        for i in range(4):
            if i == answerApple:
                if count == 0:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple0x+CELLSIZE*2, apple0y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 1:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple1x+CELLSIZE*2, apple1y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 2:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple2x+CELLSIZE*2, apple2y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 3:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple3x+CELLSIZE*2, apple3y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                count = count + 1
            else:
                if count == 0:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple0x+CELLSIZE*2, apple0y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 1:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple1x+CELLSIZE*2, apple1y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 2:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple2x+CELLSIZE*2, apple2y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 3:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple3x+CELLSIZE*2, apple3y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                c = c + 1
                count = count + 1

    elif typeOfAnswer == 2:
        count = 0
        c = 0
        for i in range(3):
            if i == answerApple:
                if count == 0:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple0x+CELLSIZE*2, apple0y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 1:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple1x+CELLSIZE*2, apple1y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                elif count == 2:
                    texSurfaceObj = fontObj.render(str(answer), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple2x+CELLSIZE*2, apple2y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                count = count + 1
            else:
                if count == 0:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple0x+CELLSIZE*2, apple0y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                    c = c + 1
                elif count == 1:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple1x+CELLSIZE*2, apple1y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                    c = c + 1
                elif count == 2:
                    texSurfaceObj = fontObj.render(
                        str(randomOptions[c]), True, BLACK)
                    texRectObj = texSurfaceObj.get_rect()
                    texRectObj.center = (apple2x+CELLSIZE*2, apple2y+CELLSIZE*2)
                    DISPLAYSURF.blit(texSurfaceObj, texRectObj)
                    c = c + 1
                count = count + 1


def drawApple(
        apple0x,
        apple0y,
        apple1x,
        apple1y,
        apple2x,
        apple2y,
        apple3x,
        apple3y,
        choice):
    x = apple0x * CELLSIZE
    y = apple0y * CELLSIZE
    DISPLAYSURF.blit(appleImg, (x, y))
    x = apple1x * CELLSIZE
    y = apple1y * CELLSIZE
    DISPLAYSURF.blit(appleImg, (x, y))
    x = apple2x * CELLSIZE
    y = apple2y * CELLSIZE
    DISPLAYSURF.blit(appleImg, (x, y))
    if (choice != 2):
        x = apple3x * CELLSIZE
        y = apple3y * CELLSIZE
        DISPLAYSURF.blit(appleImg, (x, y))


def randomQuery():
    rand = random.randint(0, 2)
    if rand == 0:
        answer, question = createEquation(rand)
        return answer, question, rand
    elif rand == 1:
        answer, question = createEquation(rand)
        return answer, question, rand
    elif rand == 2:
        answer, question = createEquation(rand)
        return answer, question, rand


def createEquation(selection):
    # there can only be a total of 5 charcater groups in total
    operationType = random.randint(0, 3)
    if operationType == 0:
        firstOperand = random.randint(30, 90)
        secondOperand = random.randint(30, 90)
        answerOperand = firstOperand + secondOperand
        # returns an answer, which would be one of the three operand
        return additinOperation(
            firstOperand,
            secondOperand,
            answerOperand,
            selection)
    elif operationType == 1:
        firstOperand = random.randint(30, 90)
        secondOperand = random.randint(30, 90)
        answerOperand = firstOperand - secondOperand
        # returns an answer, which would be one of the three operand
        return subtractionOperation(
            firstOperand,
            secondOperand,
            answerOperand,
            selection)
    elif operationType == 2:
        firstOperand = random.randint(5, 12)
        secondOperand = random.randint(5, 12)
        answerOperand = firstOperand * secondOperand
        # returns an answer, which would be one of the three operand
        return multiplicationOperation(
            firstOperand, secondOperand, answerOperand, selection)
    elif operationType == 3:
        secondOperand = random.randint(5, 12)
        firstOperand = secondOperand * random.randint(5, 12)
        answerOperand = firstOperand / secondOperand
        # returns an answer, which would be one of the three operand
        return divisionOperation(
            firstOperand,
            secondOperand,
            answerOperand,
            selection)


def additinOperation(a, b, ans, s):
    if s == 0:
        r = random.randint(0, 2)
        if r == 0:
            question = _("%d + %d = __") % (a, b)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return ans, question
        elif r == 1:
            question = _("%d + __ = %d") % (a, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return b, question
        elif r == 2:
            question = _("__ + %d = %d") % (b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return a, question

    elif s == 1:
        question = _("%d __ %d = %d") % (a, b, ans)
        texSurfaceObj = fontObj.render(question, True, BLACK)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, 20)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        return '+', question

    elif s == 2:
        randomEquality = random.randint(0, 2)
        if randomEquality == 0:
            question = _("%d + %d __ %d") % (a, b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '=', question
        elif randomEquality == 1:
            randomIncrement = random.randint(1, 9)
            question = _("%d + %d __ %d") % (a, b, ans + randomIncrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '<', question
        elif randomEquality == 2:
            randomDecrement = random.randint(1, 9)
            question = _("%d + %d __ %d") % (a, b, ans - randomDecrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '>', question


def subtractionOperation(a, b, ans, s):
    if s == 0:
        r = random.randint(0, 2)
        if r == 0:
            question = _("%d - %d = __") % (a, b)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return ans, question
        elif r == 1:
            question = _("%d - __ = %d") % (a, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return b, question
        elif r == 2:
            question = _("__ - %d = %d") % (b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return a, question

    elif s == 1:
        question = _("%d __ %d = %d") % (a, b, ans)
        texSurfaceObj = fontObj.render(question, True, BLACK)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, 20)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        return '-', question

    elif s == 2:
        randomEquality = random.randint(0, 2)
        if randomEquality == 0:
            question = _("%d - %d __ %d") % (a, b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '=', question
        elif randomEquality == 1:
            randomIncrement = random.randint(1, 9)
            question = _("%d - %d __ %d") % (a, b, ans + randomIncrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '<', question
        elif randomEquality == 2:
            randomDecrement = random.randint(1, 9)
            question = _("%d - %d __ %d") % (a, b, ans - randomDecrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '>', question


def multiplicationOperation(a, b, ans, s):
    if s == 0:
        r = random.randint(0, 2)
        if r == 0:
            question = _("%d x %d = __") % (a, b)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return ans, question
        elif r == 1:
            question = _("%d x __ = %d") % (a, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return b, question
        elif r == 2:
            question = _("__ x %d = %d") % (b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return a, question

    elif s == 1:
        question = _("%d __ %d = %d") % (a, b, ans)
        texSurfaceObj = fontObj.render(question, True, BLACK)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, 20)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        return 'x', question

    elif s == 2:
        randomEquality = random.randint(0, 2)
        if randomEquality == 0:
            question = _("%d x %d __ %d") % (a, b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '=', question
        elif randomEquality == 1:
            randomIncrement = random.randint(1, 9)
            question = _("%d x %d __ %d") % (a, b, ans + randomIncrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '<', question
        elif randomEquality == 2:
            randomDecrement = random.randint(1, 9)
            question = _("%d x %d __ %d") % (a, b, ans - randomDecrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '>', question


def divisionOperation(a, b, ans, s):
    if s == 0:
        r = random.randint(0, 2)
        if r == 0:
            question = _("%d / %d = __") % (a, b)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return ans, question
        elif r == 1:
            question = _("%d / __ = %d") % (a, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return b, question
        elif r == 2:
            question = _("__ / %d = %d") % (b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return a, question

    elif s == 1:
        question = _("%d __ %d = %d") % (a, b, ans)
        texSurfaceObj = fontObj.render(question, True, BLACK)
        texRectObj = texSurfaceObj.get_rect()
        texRectObj.center = (WINDOWWIDTH / 2, 20)
        DISPLAYSURF.blit(texSurfaceObj, texRectObj)
        return '/', question

    elif s == 2:
        randomEquality = random.randint(0, 2)
        if randomEquality == 0:
            question = _("%d / %d __ %d") % (a, b, ans)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '=', question
        elif randomEquality == 1:
            randomIncrement = random.randint(1, 9)
            question = _("%d / %d __ %d") % (a, b, ans + randomIncrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '<', question
        elif randomEquality == 2:
            randomDecrement = random.randint(1, 9)
            question = _("%d / %d __ %d") % (a, b, ans - randomDecrement)
            texSurfaceObj = fontObj.render(question, True, BLACK)
            texRectObj = texSurfaceObj.get_rect()
            texRectObj.center = (WINDOWWIDTH / 2, 20)
            DISPLAYSURF.blit(texSurfaceObj, texRectObj)
            return '>', question


def hex_to_rgb(value):
    """Return (red, darkColor, lightColor) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


if __name__ == '__main__':
    main()
