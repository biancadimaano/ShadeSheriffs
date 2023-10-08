# Each tube will be able to contain 4 colours -> fixed
# Players will be able to choose 
# Each game will have two free/empty tubes -> also fixed

'''

SHADE SHERIFFS BY YONKA
- Inspired by the popular WaterSort game
    - Numerous shades have been mixed up into different tubes! Organize each shade into its own separate tube to win!

- Hard coded elements:
    - Each tube will contain 4 colors max
    - Players are able to choose to play with 3-10 colors
    - Each game will start off with two extra (empty) tubes

Created Francesca Bianca Dimaano
Completed/Last Modified 10/5/2023

'''

import random
import pygame
import copy
import asyncio
pygame.init()

# CONSTANTS
MINTUBES = 3
MAXTUBES = 10
SCREENWIDTH = 1600
SCREENHEIGHT = 1000
WIDTH = 100
HEIGHT = 50
MARGINS = WIDTH/10

# Tuple for the tube background hex code.
tubeBackground = (92,15,10)
# Array of tuples containing hex codes of 10 available colors to be chosen from for the game.
colorBank = [(255,176,124), (255,227,111), (177,238,135), (0,26,175), (192,221,240), (234,92,92), (255,125,229), (129,32,238), (161,141,210), (32,144,44)]
#            Orange         Yellow         Sage Green     Dark Blue    Powder Blue    Red          Pink           Purple       Seafoam Green  Pine Green
# Array of tuples containing:
# [0] - The number of shades the player chooses to organize (number in the image shown)
# [1] - Left-most X coordinate of the number in the image shown
# [2] - Right-most X coordinate ...
# [3] - Top-most Y coordinate ... 
# [4] - Bottom-most Y coordinate ...
numTubeCoords = [(3,525,605,337,460),(4,680,770,337,460),(5,845,925,337,460),(6,998,1080,337,460),
                (7,506,585,525,650),(8,660,738,525,650),(9,810,896,525,650),(10,972,1111,525,650)]
#                (NUMBER CHOICE, X1, X2, Y1, Y2)

# Changes the pygame window text
pygame.display.set_caption("YONKA'S SHADE SHERIFFS")

# Changes the pygame window icon
gameIcon = pygame.image.load("logo.png")
pygame.display.set_icon(gameIcon)

# Setting up the main display for the game
gameScreen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

'''

Creates a display with an image background and loads it over top the current display.
PARAMATERS:
    - surface: current pygame display to load the new display onto
    - image: image to load onto the display
PRECONDITIONS:
    - image is a valid image file type (png, jpg, gif, bmp)

'''

def drawScreen(surface, image):
    screen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    screenImage = pygame.image.load(image)
    screen.blit(screenImage,(0,0))
    surface.blit(screen,(0,0))

'''

Loads an image and draws it onto the specified display, at the coordinate (x,y)
PARAMETERS:
    - surface: pygame display to load the image onto
    - image: image to load onto the display
    - x: x coordinate
    - y: y coordinate
PRECONDITIONS:
    - image is a valid image file type (png, jpg, gif, bmp)
    - x and y are of type int

'''

def drawImage(surface, image, x, y):
    image = pygame.image.load(image)
    surface.blit(image,(x,y))

'''

Checks if the tube is empty
PARAMETERS:
    - tube: an array containing four elements, representing colors in the tube

'''

def tubeIsEmpty(tube):
    return tube[3] == ''

'''

Returns the top most index of the tube THAT CONTAINS A COLOR
PARAMETERS:
    - tube: an array containing four elements, representing colors in the tube

'''

def findTop(tube):
    
    for i in range(4,0,-1):
        if tube[i-1] == '':
            return i
    return -1

'''
Returns an array containing the indices of tube that are a range of the same color, starting from the top of tube.
ex: If the tube we are pouring from = ['',red,red,blue] then rangeOfPour = [1,2]
PARAMETERS:
    - tube: an array containing four elements, representing colors in the tube
    - pourFrom: index of the entire tube array we are pouring from
    - pourFromIndex: index of the specific color being poured (topmost element of pourFrom)
PRECONDITIONS:
    - pourFrom is a valid tube
    - pourFromIndex is a valid index containing a color in pourFrom
'''

def rangeOfPour(tube, pourFrom, pourFromIndex):
    pourRange = [pourFromIndex]

    if pourFromIndex != 3:
        for i in range(pourFromIndex,3):
            if tube[pourFrom[1]][i] == tube[pourFrom[1]][i+1]:
                pourRange.append(i+1)
            else:
                break
    return pourRange

'''

Creates and returns an array of arrays, of length numTubes + 2 (numTubes + 2 empty tubes)
The arrays contained will have numTubes FULLY COMPLETED tubes (sorted already)
PARAMTERS:
    - availableColors: array of color hex codes that are able to be chosen
    - numTubes: number of tubes/shades the user chooses to play with
PRECONDITIONS:
    - length of availableColors >= max numTubes able to be chosen
    
'''

def createTubes(availableColors, numTubes):
    
    tubeArray = []
    colorChoices = copy.deepcopy(availableColors)

    # Append two empty tubes
    tubeArray.append(['','','',''])
    tubeArray.append(['','','',''])

    # Create a random list of colors for the game.
    for i in range(numTubes):
        currentColor = random.choice(colorChoices)
        tubeArray.append([currentColor for i in range(4)])
        colorChoices.remove(currentColor)

    return tubeArray

'''

Unsorts the sorted tubes for the user to sort. 
Returns an array of mixed tubes.
* Created a function to mix up tubes instead of randomly choosing colors in each tube to ensure
  that it is 100% possible for the tubes to be sorted.

'''

def mixTubes(tubeArrays, numTubes):

    tubeOneFull = False
    tubeTwoFull = False
    mixTracker = [0 for i in range(numTubes)]
    mixedTubes = []
    while True:

        emptyTubeCount = 0


        while True:
            swapFrom = random.randint(0,numTubes+1)
            if tubeIsEmpty(tubeArrays[swapFrom]): continue
            else: 
                break
    
        while True:
            swapTo = random.randint(0,numTubes+1)
            if (findTop(tubeArrays[swapTo]) == -1): continue
            if (swapFrom == swapTo): continue
            else: 
                break
    
        swapFromIndex = findTop(tubeArrays[swapFrom])
        if swapFromIndex == -1: swapFromIndex = 0


        tubeArrays[swapTo][findTop(tubeArrays[swapTo])-1] = tubeArrays[swapFrom][swapFromIndex]
        tubeArrays[swapFrom][swapFromIndex] = ''

        if ((swapFromIndex == 2 or swapFromIndex == 3) and swapFrom > 1): 
            mixTracker[swapFrom-2] = mixTracker[swapFrom-2] + 1

        if sum(mixTracker) < numTubes: continue

        for i in range(numTubes+2):
            if tubeIsEmpty(tubeArrays[i]): 
                emptyTubeCount+=1
        
        # Allows the algorithm to completely fill up the first and second tubes.
        # If this was not included, there is a possibility of moving one color to the first empty tube and moving it back,
        # resulting in no mixture of colors at all.
        if tubeArrays[0][0] != '': tubeOneFull = True
        if tubeArrays[1][0] != '': tubeTwoFull = True

        # print("Updated tubes: ", tubeArrays)

        if(emptyTubeCount == 2 and (tubeOneFull and tubeTwoFull)): 

            for i in range(len(tubeArrays)):
                if tubeIsEmpty(tubeArrays[i]): 
                    continue
                mixedTubes.append(tubeArrays[i])

            mixedTubes.append(['','','',''])
            mixedTubes.append(['','','',''])

            # print("tubeArrays: ", tubeArrays)
            # print("mixedTubes: ", mixedTubes)
            return mixedTubes

'''
Draws the tubes to the pygame screen using the pygame.draw.rect() function
Returns an array of Rect objects so we can use methods of the Rect class (from pygame) in the main game function.
PARAMETERS:
    - tubeArrays: array of arrays of the mixed tubes, containing color hex codes, to be drawn to the screen
    - numTubes: number of tubes/shades the user chooses to play with
    - surface: pygame display to draw on
    - width: width of the surface
    - height: height of the surface
    - margins: how many pixels thick the tube outlines will be
    - x,y: (x,y) coordinate where the tubes will be drawn
    - tubeCol: color of the tube outlines
PRECONDITIONS:
    - x >= 0 and x <= screen width, y >= 0 and y <= screen height
    - tubeCol is a valid color name or hex code
'''

def drawTubes(tubeArrays, numTubes, surface, width, height, margins, x ,y, tubeCol):

    drawScreen(surface,"gamebackground.png")

    yOriginal = y
    xOriginal = x
    tubesDrawn = 0
    gameTubes = []
    
    # Find number of rows in the first row:
    if numTubes % 2 == 0:
        tubesInFirstRow = (numTubes + 2) // 2
    else:
        tubesInFirstRow = ((numTubes + 2) // 2) + 1
    # Draw first row of tubes

    for i in range(numTubes+2):
        y = yOriginal
        gameTubes.append(pygame.draw.rect(surface, tubeCol, pygame.Rect(x-margins, y-height, width+(2*margins), (5*height)+margins)))
        y = yOriginal

        for k in range(4):
            if tubeArrays[i][k] == '':
                y+=height
                continue
            pygame.draw.rect(surface, tubeArrays[i][k], pygame.Rect(x, y, width, height))
            y += height
        x+=2*width
        tubesDrawn += 1
        if tubesDrawn == tubesInFirstRow:
            yOriginal += height*7
            
            if numTubes % 2 == 0:
                x = xOriginal
            else:
                x = xOriginal + width

    pygame.display.update()
    return gameTubes 

'''

Checks if the player has won the game or not
Returns true (won) or false (haven't won yet)

'''

def checkWinner(tubeArrays, numTubes):
    organizedTubesCount = 0
    sameColorInTube = 0
    for i in range(numTubes+2):
        if tubeIsEmpty(tubeArrays[i]):
            continue
        else:
            for j in range(4):
                if tubeArrays[i][0] == tubeArrays[i][j]:
                    sameColorInTube += 1
                    if sameColorInTube == 4:
                        organizedTubesCount += 1
        sameColorInTube = 0
    return organizedTubesCount == numTubes

'''

Manipulates and updates the array of tubes to update the player's choices
Returns an updated array of tubes
PRECONDITIONS:
    - pourFrom, pourTo is a valid tube index
    - currentTubeTop is the index of the top-most element of the current tube chosen
        - 0 <= currentTubeTop <= 3
    - clickCount is either 0,1, or 2

'''

def playGame(surface, tubesToSort, pourFrom, pourTo, currentTubeTop, clickCount):

    gameTubes = tubesToSort

    if pourFrom[0] == '':
        # Will draw an image that says " "
        drawImage(surface, "errorEmptyTube.png", 130,830)
        return False
    if pourFrom[1] == pourTo[1]:
        drawImage(surface, "errorSameTube.png", 130,830)
        return False
    if gameTubes[pourTo[1]][0] != '':
        drawImage(surface, "errorFullTube.png", 130,830)
        return False
    if pourTo[0] != '' and pourFrom[0] != pourTo[0]:
        drawImage(surface, "errorColorMatch.png", 130,830)
        return False
    
    pourFromIndex = findTop(gameTubes[pourFrom[1]])
    if pourFromIndex <= -1: pourFromIndex = 0

    pourToIndex = findTop(gameTubes[pourTo[1]]) - 1
    pourRange = rangeOfPour(gameTubes, pourFrom, pourFromIndex)

    for i in range(len(pourRange)):
        if clickCount == 2:
            if currentTubeTop == 0:
                currentTubeTop = 4
            if (4-currentTubeTop + len(pourRange)) > 4:
                drawImage(surface, "errorOverflow.png", 130,830)
                return False
        gameTubes[(pourTo[1])][pourToIndex-i] = gameTubes[(pourFrom[1])][pourRange[i]]
        gameTubes[(pourFrom[1])][pourRange[i]] = ''

    return gameTubes

'''

Function to call the game loop and pygame event handler
PARAMETERS:
    - gameStartedStatus: boolean type, True or False if the game has already been started before 

'''

async def main(gameStartedStatus):
    fromTubeSelected = None
    toTubeSelected = None
    clickCount = 0 
    numTubesChosen = False
    gameStarted = gameStartedStatus
    starterTubesDrawn = False
    restarted = False
    won = False

    while True:
        mousePos = pygame.mouse.get_pos()
        
        if won:
            for event in pygame.event.get():    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mousePos[1] >= 857 and mousePos[1] <= 926:
                        # Play Again        
                            if mousePos[0] >= 72 and mousePos[0] <= 525:
                                won = False
                                game(True)
                                
                        # Exit
                            if mousePos[0] >= 1376 and mousePos[0] <= 1540:
                                pygame.quit()
                                quit() 


           
        if not gameStarted:
            drawScreen(gameScreen, "shadesheriffs.png")
            for event in pygame.event.get():
                if (mousePos[0] >= 505 and mousePos[0] <= 1087) and (mousePos[1] >= 695 and mousePos[1] <= 770):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            gameStarted = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit() 

        else:
            if not numTubesChosen:
                for event in pygame.event.get():
                    drawScreen(gameScreen, "shades to sort.png")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for i in range(len(numTubeCoords)):
                                if (mousePos[1] >= numTubeCoords[i][3] and mousePos[1] <= numTubeCoords[i][4]) and (mousePos[0] >= numTubeCoords[i][1] and mousePos[0] <= numTubeCoords[i][2]):
                                    numTubes = numTubeCoords[i][0]
                                    numTubesChosen = True
                            
                                    x = ((SCREENWIDTH - (((numTubes+1)*(WIDTH)))) // 2) - 2*MARGINS
                                    y = HEIGHT*4
                                    mixedTubes = mixTubes(createTubes(colorBank, numTubes), numTubes)
                                    originalTubes = copy.deepcopy(mixedTubes)


                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit() 

            else:
                for event in pygame.event.get():
                    if not starterTubesDrawn:
                        gameTubes = drawTubes(originalTubes, numTubes, gameScreen, WIDTH, HEIGHT, MARGINS, x, y, tubeBackground)
                        if restarted:
                            mixedTubes = originalTubes
                            restarted = False
                        pygame.display.update()
                        starterTubesDrawn = True


                    elif (mousePos[0] >= 796 and mousePos[0] <= 1050) and (mousePos[1] >= 911 and mousePos[1] <= 972):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                starterTubesDrawn = False
                                restarted = True

                    else:
                        for j in range(len(gameTubes)):
                            if gameTubes[j].collidepoint(mousePos):
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if event.button == 1:
                                        clickCount += 1
                                        
                                        top = findTop(mixedTubes[j])
                                        if top <= -1 or top > 3: 
                                            top = 0
                                        if clickCount == 1:
                                            fromTubeSelected = (mixedTubes[j][top],j)
                                        elif clickCount == 2:
                                            toTubeSelected = (mixedTubes[j][top],j)
                                            updatedMixedTubes = playGame(gameScreen, mixedTubes, fromTubeSelected, toTubeSelected, top, clickCount)

                                            if updatedMixedTubes == False: 
                                                updatedMixedTubes = playGame(gameScreen, mixedTubes, fromTubeSelected, toTubeSelected, top, clickCount)
                                                clickCount = 0
                                                continue
                                            else: 
                                                drawTubes(updatedMixedTubes, numTubes, gameScreen, WIDTH, HEIGHT, MARGINS, x, y, tubeBackground)
                                            
                                            clickCount = 0
                                            fromTubeSelected = None
                                            toTubeSelected = None
                                            
                                            if checkWinner(updatedMixedTubes, numTubes): 
                                                drawScreen(gameScreen, "winscreen.png")
                                                won = True
                                        pygame.display.update() 
                await asyncio.sleep(0)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit() 
        pygame.display.update()

asyncio.run(main(False))

