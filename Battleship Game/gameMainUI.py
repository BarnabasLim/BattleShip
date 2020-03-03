import pygame
from UtilityUI import message_display
from UtilityUI import button
from random import randint
import random
from time import sleep
#shu Fang
#from ship import *

#========================================================================
#------------------------
#1.Game Parameters
#------------------------

#Windows Size
display_width = 800
display_height = 520

#Initialise pygame
pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

#Number of ships
number_of_carrier=1
number_of_sub=1

#Images
background = pygame.image.load("Images/board.jpg")
win_img = pygame.image.load("Images/win_game.png")
lose_img = pygame.image.load("Images/lose_game.png")
carrier_img = pygame.image.load('Images/carrier.png').convert_alpha()
submarine_img = pygame.image.load('Images/submarine.png').convert_alpha()
cross_img = pygame.image.load('Images/cross.png').convert_alpha()
bluecross_img = pygame.image.load('Images/blueCross.png').convert_alpha()
rect = carrier_img.get_rect(topleft=(0, 40))


#Various Colors
black = (0,0,0)
grey = (40,40,40)
white = (255,255,255)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)
block_color = (53,115,255)

#Fonts
largeText = pygame.font.SysFont(None,115)
mediumText = pygame.font.SysFont(None,50)
smallText = pygame.font.SysFont(None,32)
verysmallText = pygame.font.SysFont(None,20)

#Width of grid on board
width = display_width/20

#shape - 'sub', 'carrier', 'bomb'
#orientation - 'vert','hori'

#========================================================================
#------------------------
#2.Game Controls
#------------------------

#Layout
###2.1 Draw Functions
###2.2 Check Boundary Funcions
###2.3 Generate Coordinates Functions
###2.4 Comp Actions Functions
###2.5 Button Functions

###2.6 Important VARIABLES

#2.1 Draw Functions
#--------------------------------------------------------------------------------------------#
#Function: creates the game board interface and
#          colour the grids grey and outline red when the mouse hovers a ship or a bomb over the board,
#          and colour the grids red when the object is out of bound.
#          loops through j-width i-height and either:
#          1. generate grid
#          2. generate red box (show collision)
#          3. generate red box with boundary(tentative ship/bomb positon)
#Input: Mouse position, shape=("sub","carrier","bomb"),orientation=("vert","hori")
#Return: Colour the grids grey and outline red when the mouse hovers a ship or a bomb over the board
def drawBoard(position,shape,orientation,ship_pos,bomb_central_pos,state=None):
    x_pos = position[0]
    y_pos = position[1]
    #Mouse Position 
    y_int = int((y_pos-40)//width)
    x_int = int((x_pos)//width)
    #loop through i and j to draw grid on board
    for i in range(10):
        y_grid = i*width+40
        for j in range (22):
            x_grid = j*width
            #Mouse on board
            if(0 <= x_int <= 19 and 0 <= y_int <= 9):
                #Carrier and Sub has different attributes
                #Carrier cant be placed on subsurface
                if shape == 'sub':
                    #changes orientation condition
                    #condi1 checks x coordinate for drawing
                    #condi2 checks y coordinate for drawing
                    #IMPORTANT 1 and 2 for drawing boxes of length
                    #condi3 checks if boundary ships collides with boundary
                    
                    if orientation == 'vert':
                        condi1 = (x_int == j)
                        condi2 = (y_int+2 >= i >= y_int)
                        condi3 = (y_int+2 >= 10)
                    elif orientation == 'hori':
                        condi2 = (y_int == i)
                        condi3 = (x_int+2 >= 20) or (8 <= x_int <= 9)
                        if(condi3):
                            if (8 <= x_int <= 9):
                                condi1 = (9 >= j >= x_int)
                            elif (x_int+2 >= 20):
                                condi1 = (19 >= j >= x_int)
                        else:
                            condi1 = (x_int+2 >= j >= x_int)
                    
                    #notice condition changes with the one above
                    #condi1 and condi2 describes the range of i and j when ship is on 
                    if condi1 and condi2:
                        #condi3 returns true if no collision with board
                        if condi3:
                            pygame.draw.rect(gameDisplay,red,(x_grid,y_grid,width,width))
                            pygame.draw.rect(gameDisplay, red, [x_grid, y_grid, width, width], 2)
                        else:
                            pygame.draw.rect(gameDisplay,grey,(x_grid,y_grid,width,width))
                            pygame.draw.rect(gameDisplay, red, [x_grid, y_grid, width, width], 2)
                    #else just generate empty grid
                    else:
                        pygame.draw.rect(gameDisplay, green, [x_grid, y_grid, width, width], 2)

                elif shape == 'carrier':
                    if x_int < 10:
                        #changes orientation condition
                        #condi1 checks x coordinate for drawing
                        #condi2 checks y coordinate for drawing
                        #IMPORTANT 1 and 2 for drawing boxes of length
                        #condi3 checks if boundary ships collides with boundary
                        if orientation == 'vert':
                            condi1 = (x_int == j)
                            condi2 = (y_int+3 >= i >= y_int)
                            condi3 = (y_int+3 >= 10)
                        elif orientation == 'hori':
                            condi2 = (y_int == i)
                            condi3 = (x_int+3 >= 20) or (7 <= x_int <= 9)
                            if(condi3):
                                condi1 = (9 >= j >= x_int)
                            else:
                                condi1 = (x_int+3 >= j >= x_int)

                        #notice condition changes with the one above
                        if condi1 and condi2:
                            if condi3:
                                pygame.draw.rect(gameDisplay,red,(x_grid,y_grid,width,width))
                                pygame.draw.rect(gameDisplay, red, [x_grid, y_grid, width, width], 2)
                            else:
                                pygame.draw.rect(gameDisplay,grey,(x_grid,y_grid,width,width))
                                pygame.draw.rect(gameDisplay, red, [x_grid, y_grid, width, width], 2)
                        else:
                            pygame.draw.rect(gameDisplay, green, [x_grid, y_grid, width, width], 2)

                    #else just generate empty grid
                    else:
                        pygame.draw.rect(gameDisplay, green, [x_grid, y_grid, width, width], 2)

                elif shape == 'bomb':
                    #x_int==9 and x_int==10 takes care of the boundary in the middle of the board
                    if x_int == 9:
                        condi1 = x_int >= j >= x_int-1
                        condi2 = y_int+1 >= i >= y_int-1
                    elif x_int == 10:
                        condi1 = x_int+1 >= j >= x_int
                        condi2 = y_int+1 >= i >= y_int-1
                    else:
                        condi1 = x_int+1 >= j >= x_int-1
                        condi2 = y_int+1 >= i >= y_int-1
                    if condi1 and condi2:
                        pygame.draw.rect(gameDisplay,grey,(x_grid,y_grid,width,width))
                        pygame.draw.rect(gameDisplay, red, [x_grid, y_grid, width, width], 2)
                    else:
                        pygame.draw.rect(gameDisplay, green, [x_grid, y_grid, width, width], 2)

                #else if Variable shape has nothing
                else:
                    pygame.draw.rect(gameDisplay, green, [x_grid, y_grid, width, width], 2)
            #else if x_int and y_int are not on grid
            else:
                pygame.draw.rect(gameDisplay, green, [x_grid, y_grid, width, width], 2)


#Function: To display the ships image
#Input: ship coord
#Return: The coordinate on board are display with the ship images
def drawship(ship_coord):
    board = ship_coord[0][0]
    y_int = ship_coord[0][1]
    x_int = ship_coord[0][2]
    w = 40
    length = len(ship_coord)
    if board == 1:
        x_int += 10
    #gameMainUI.py drawship(ship_coord)
    #[(0,0,0),(0,0,1),(0,0,2)]
    #if Vertical
    if ship_coord[0][2] == ship_coord[1][2]:
        rotation = 270
        crop = (0,0,w,length*w)
    #if Horizontal
    elif ship_coord[0][1] == ship_coord[1][1]:
        rotation = 0
        crop = (0,0,length*w,w)

    if length == 4:
        image = carrier_img
    elif length == 3:
        image = submarine_img

    surf = pygame.transform.rotate(image, rotation)
    subsurf = surf.subsurface(crop)
    gameDisplay.blit(subsurf,(x_int*w,y_int*w+40))

#Function: To display bombed ships image
#Input: ship coord, bomb_list, state
#Return: ship image are revealed on bombed coordinate on board
def draw_bombedship(ship_coord, bomb_list,state):
    global compShip_bombed_list
    global ship_bombed_list
    w = 40
    length = len(ship_coord)
    #check orientation
    #vericle
    if ship_coord[0][2] == ship_coord[1][2]:
        rotation = 270
        #Crop selection for verticle
        #used to crop parts of image depending on which part is bombed
        #crop input (crop_begining_x,crop_begining_y, crop_to_x, )
        crop = [(0,0,w,w),(0,w,w,w),(0,2*w,w,w),(0,3*w,w,w)]
    #horizontal
    elif ship_coord[0][1] == ship_coord[1][1]:
        rotation = 0
        #Crop selection for horizonal
        crop = (0,0,w,w),(w,0,w,w),(2*w,0,w,w),(3*w,0,w,w)
    #check shape
    if length == 4:
        image = carrier_img
    elif length == 3:
        image = submarine_img
    #loops through ship_coord and
    #if ship in bombed_list
    #display specific of ship that is bombed
    for coord in ship_coord:
        if coord in bomb_list:
            #part_ship gets the index of section of ship that is bombed
            #used to determine which image crop to use
            part_ship = ship_coord.index(coord)
            board = coord[0]
            y_int = coord[1]
            x_int = coord[2]
            if board == 1:
                x_int += 10
            x_grid,y_grid=x_int*w,y_int*w+40
            pygame.draw.rect(gameDisplay,green,(x_grid,y_grid,width,width))

            surf = pygame.transform.rotate(image, rotation)
            #Crops part of ship
            subsurf = surf.subsurface(crop[part_ship])
            gameDisplay.blit(subsurf,(x_int*w,y_int*w+40))

            pygame.draw.rect(gameDisplay, red, [x_grid,y_grid, width, width], 2)
            surf = pygame.transform.rotate(cross_img,0)
            gameDisplay.blit(surf,(x_grid,y_grid))
            if state == "P attack Comp" and coord not in compShip_bombed_list:
                compShip_bombed_list.append(coord)
            elif state == "Comp attack P" and coord not in ship_bombed_list:
                ship_bombed_list.append(coord)

#Function: To display bombed area on board
#Input: bomb coord, central
#Return: bombed coordinate are marked with cross
def draw_bomb(bomb_coord, central):
    board = bomb_coord[0]
    y_int = bomb_coord[1]
    x_int = bomb_coord[2]
    w = 40
    if board == 1:
        x_int += 10
    if (bomb_coord in central):
        surf = pygame.transform.rotate(bluecross_img,0)
        gameDisplay.blit(surf,(x_int*w,y_int*w+40))
    else:
        surf = pygame.transform.rotate(cross_img,0)
        gameDisplay.blit(surf,(x_int*w,y_int*w+40))


#2.2 Check Boundary Funcions
#--------------------------------------------------------------------------------------------#
#Function: Check boundary of board
#          Check if ship coolides with board
#Input: target=(0,x_int,y_int), shape="sub","carrier","bomb" Orientation="vert","hori"
#Return: True, if hit boundary
#        False, if does not hit boundary
def check_boundary(target,shape,orientation):
    y_int = target[1]
    x_int = target[0]*10 + target[2]

    if(0 <= x_int <= 19 and 0 <= y_int <= 9):
        if shape == 'sub':
            #condi3 checks boundary condition
            if orientation == 'vert':
                condi3 = (y_int+2 >= 10)
            elif orientation == 'hori':
                condi3 = (x_int+2 >= 20) or (8 <= x_int <= 9)

            if condi3:
                print("sub out of bound")
                return True
            else:
                print("sub pos Valid")
                return False

        elif shape == 'carrier':
            if x_int < 10:
                #condi3 checks boundary condition
                if orientation == 'vert':
                    condi3 = (y_int+3 >= 10)
                elif orientation == 'hori':
                    condi3 = (x_int+3 >= 20) or (7 <= x_int <= 9)

                if condi3:
                    print("carrier out of bound")
                    return True
                else:
                    print("carrier pos Valid")
                    return False

            #else just generate empty grid
            else:
                print("carrier out of bound")
                return True

        elif shape == 'bomb':
            if (y_int < 0) or (y_int > 9):
                print("bomb out of bound")
                return True
            else:
                print("bomb pos Valid")
                return False

#Function: Check if ship collides with existing ship
#Input: 1) temp_ship=[(0,0,0),(0,0,1),(0,0,2)]
#       coordinates of one ship to be added
#       2)temp_ship=list of Ships coordinate already added
#Return: True , if collide
def check_collision(ship_pos,temp_ship):
    for ship in ship_pos:
        for temp_coordinate in temp_ship:
            if temp_coordinate in ship:
                print("Collide")
                return True
                break
    return False

#Function: Check if bomb collides with existing bomb
#Input: 1)target = center coordinate of one bomb to be added
#       2)bomb_central_pos=list of bomb's centre coordinate already added
#Return: True , if collide
def check_bomb_central(target,bomb_central_pos):
    print (target,bomb_central_pos)
    if target in bomb_central_pos:
        print("Collide")
        return True
    else:
        return False

#Functions: Checks if target is on a ship already added
#Input: 1)target = coordinate of mouse in (board,y_int,x_int) form
#       2)ship_pos = list of ship coordinates
#Return: Return index of ship which contains target
def delete_ship(target, ship_pos):
    #Convert user selection to tuple because coordinate are stored as tuple
    target_tup = (target[0],target[1],target[2])
    for i in range(len(ship_pos)):
        if target_tup in ship_pos[i]:
            return i
    return None


#2.3 Generate Coordinates Functions
#--------------------------------------------------------------------------------------------#

#Functions: Generates a list of valid coordinates for one ship
#Input: target=(0,x_int,y_int), shape="sub","carrier", Orientation="vert","hori"
#Return: eg[(0,0,0),(0,0,1),(0,0,2)]
def ship_coordinates(target,shape,orientation):
    y_int = target[1]
    x_int = target[2]
    board = target[0]
    ship_coordinates = []
    if shape == 'sub':
        if orientation == 'vert':
            for i in range(3):
                ship_coordinates.append((board, y_int+i,x_int))

        elif orientation == 'hori':
            for i in range(3):
                ship_coordinates.append((board, y_int,x_int+i))
    if shape == 'carrier':
        if orientation == 'vert':
            for i in range(4):
                ship_coordinates.append((board, y_int+i,x_int))

        elif orientation == 'hori':
            for i in range(4):
                ship_coordinates.append((board, y_int,x_int+i))

    return ship_coordinates

#Functions: Generates a list of valid coordinates for one bomb
#Input: target=(0,x_int,y_int), shape="bomb"
#Return: List of bomb coordinates
def bomb_coordinates(target,shape):
    y_int,x_int = target[1],target[2]
    board = target[0]
    bomb_coordinates = []
    if shape == 'bomb':
        #At column 1
        if x_int == 0:
            #At A1, append 4 board coordinates
            if y_int == 0:
                for x in range(0,2):
                    for y in range(0,2):
                        bomb_coordinates.append((board,y_int+y,x_int+x))
            #At J1, append 4 board coordinates
            elif y_int == 9:
                for x in range(0,2):
                    for y in range(-1,1):
                        bomb_coordinates.append((board,y_int+y,x_int+x))
            #At other boxes, append 6 board coordinates
            else:
                for x in range(0,2):
                    for y in range(-1,2):
                        bomb_coordinates.append((board,y_int+y,x_int+x))

        #At column 10
        elif x_int == 9:
            #At A10, append 4 board coordinates
            if y_int == 0:
                for x in range(-1,1):
                    for y in range(0,2):
                        bomb_coordinates.append((board,y_int+y,x_int+x))
            #At J10, append 4 board coordinates
            elif y_int == 9:
                for x in range(-1,1):
                    for y in range(-1,1):
                        bomb_coordinates.append((board,y_int+y,x_int+x))
            #At other boxes, append 6 board coordinates
            else:
                for x in range(-1,1):
                    for y in range(-1,2):
                        bomb_coordinates.append((board,y_int+y,x_int+x))

        #At row A, append 6 board coordinates
        elif y_int == 0:
            for x in range(-1,2):
                for y in range(0,2):
                    bomb_coordinates.append((board,y_int+y,x_int+x))

        #At row J, append 6 board coordinates
        elif y_int == 9:
            for x in range(-1,2):
                for y in range(-1,1):
                    bomb_coordinates.append((board,y_int+y,x_int+x))

        #At other boxes, append 9 board coordinates
        else:
            for x in range(-1,2):
                for y in range(-1,2):
                    bomb_coordinates.append((board,y_int+y,x_int+x))

    return bomb_coordinates



#2.4 Comp Actions Functions
#--------------------------------------------------------------------------------------------#

#Function: Generate random ship position for Computer
#Input: number of Carrier, number of sub
#Return: List of all ship positions of Computer
def compShip(no_carrier, no_sub):
    compCarrier_pos = []
    #computer randomly selects carrier
    while len(compCarrier_pos) != no_carrier:
        #random selection
        target = (0,randint(0,9),randint(0,9))
        orientation = random.choice(["hori","vert"])
        shape = "carrier"
        #reused ship_coordinates() ,check_boundary() and check_collision()
        #1)generate ship coord
        temp_ship = ship_coordinates(target,shape, orientation)
        #2)check boundary collision
        boundary_collision = check_boundary(target,shape,orientation)
        #3)check ship collision
        ship_collision = check_collision(compCarrier_pos,temp_ship)
        #add carrier coordinates if all check return False(no collision)
        if boundary_collision == False and ship_collision == False:
            compCarrier_pos.append(temp_ship)
            print(compCarrier_pos)
    compShipT_pos = []
    compShipT_pos += compCarrier_pos
    while len(compShipT_pos) != no_sub+ no_carrier:
        #random selection
        target = (randint(0,1),randint(0,9),randint(0,9))
        orientation = random.choice(["hori","vert"])
        shape = "sub"
        #reused ship_coordinates() ,check_boundary() and check_collision()
        #1)generate ship coord
        temp_ship = ship_coordinates(target,shape, orientation)
        #2)check boundary collision
        boundary_collision = check_boundary(target,shape,orientation)
        #3)check ship collision
        ship_collision = check_collision(compShipT_pos,temp_ship)
        #add sub coordinates if all check return False(no collision)
        if boundary_collision == False and ship_collision == False:
            compShipT_pos.append(temp_ship)
            print(compSub_pos)
    return compShipT_pos

#Function: Generate random bomb position for Computer and bomb display randomly on board
#          Randomly generate bomb position
#Input: NIL
#Return: Append bombed coordinates in list
def compBomb():
    #global compBomb_pos
    global compBomb_list
    global compBomb_central_pos
    global ship_pos
    no_of_bomb = len(compBomb_central_pos)

    while len(compBomb_central_pos) != no_of_bomb+1:
        #randomly select no. of times to loop
        j=randint(2,15)
        for i in range (0,j):
            #rand select 
            mouse=(randint(0,800),randint(40,440))
            target=UserSelection(mouse)
            #target = (randint(0,1),randint(0,9),randint(0,9))
            #displays random selection
            gameDisplay.blit(background, [0,0])
            drawBoard(mouse,"bomb",None,ship_pos,compBomb_central_pos,"Comp attack P")
            message_display("Surface",largeText,black,(display_width*0.25),100)
            message_display("Subsea",largeText,black,(display_width*0.75),100)
            pygame.display.update()
            sleep(0.1)

        shape = "bomb"
        orientation = 'vert'
        #bomb_central_pos
        bomb_place = bomb_coordinates(target,shape)
        boundary_collision = check_boundary(target,shape,orientation)
        bomb_collision = check_bomb_central(target,compBomb_central_pos)
        if boundary_collision == False and bomb_collision == False:
            compBomb_central_pos.append(target)
            compBomb_list.extend(bomb_place)

#2.5 Button Functions
#--------------------------------------------------------------------------------------------#

def sub():
    return "sub"

def carrier():
    return "carrier"

def bomb():
    return "bomb"

def orientate():
    if orientation == "vert":
        return 'hori'
    else:
        return 'vert'

#Function: Capture user's mouse position on board
#Input: mouse position
#Return: mouse position converted to board coordinates
def UserSelection(mouse):
    position_x = mouse[0]
    position_y = mouse[1]
    board = int(position_x//(display_width/2))
    y_int = int((position_y-40)//width)
    x_int = int((position_x)//width)
    if board == 1:
        x_int -= 10
    return(board, y_int, x_int)

#Function: To clear all lists when "Play again" button is selected
def play_again():
    ship_pos.clear()
    sub_pos.clear()
    ship_bombed_list.clear()
    bomb_list.clear()
    bomb_central_pos.clear()
    compShip_pos.clear()
    compSub_pos.clear()
    compBomb_list.clear()
    compBomb_central_pos.clear()
    compShip_bombed_list.clear()
    set_sub_on_board()
    
###2.6 Important VARIABLES
#--------------------------------------------------------------------------------------------#

orientation="vert"

#Various lists to store information of Game Loop
ship_pos = [] #used for draw_ship
sub_pos = [] #used to count number of submarine and manage game flow
ship_bombed_list = [] #used in draw_bombedship
bomb_list = [] #used in draw_bomb
bomb_central_pos = [] #used for check bomb collision

compShip_pos = []#used for computer draw_ship
compSub_pos = []#used to count number of computer submarine and manage game flow
compBomb_list = []#used in draw_bombedship(for computer)
compBomb_central_pos = []#used in draw_bomb(for computer)
compShip_bombed_list = []#used for check bomb collision(for computer)

#========================================================================
#------------------------
#3.Game Loops
#------------------------

# User DISPLAY board 1 to set submarine
def set_sub_on_board():
    shape = 'None'
    global orientation
    pygame.time.delay(200)
    setboard = True
    while setboard:
        #Handle Event----------------------------------------------------------------------------------------------------#
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target=UserSelection(mouse)

                #temporary ship
                #User Target
                temp_ship = ship_coordinates(target,shape, orientation)
                #1.check boundary collision
                boundary_collision = check_boundary(target,shape,orientation)
                #2.check ship collision
                ship_collision = check_collision(ship_pos,temp_ship)
                #3.check if user targeted exisiting ship
                #  if so delete ship
                remove_ship_index = delete_ship(target,ship_pos)

                if boundary_collision == False and ship_collision == False and len(sub_pos) < number_of_sub:
                    ship_pos.append(temp_ship)
                    sub_pos.append(temp_ship)

                if remove_ship_index is not None:
                    if len(ship_pos[remove_ship_index]) == 3:
                        sub_pos.remove(ship_pos[remove_ship_index])
                    ship_pos.pop(remove_ship_index)

        for event in pygame.event.get():
            print(event)
        #Draw----------------------------------------------------------------------------------------------------#
        #Background display
        gameDisplay.fill(white)
        gameDisplay.blit(background, [0,0])

        #Text
        #1)render the font
        #2)blit the font
        #3)display update
        message_display("Surface",largeText,black,(display_width*0.25),100)
        message_display("Subsea",largeText,black,(display_width*0.75),100)

        #Buttons
        sub_clicked = button("sub",520,460,80,40,red,bright_red,sub)
        orientation_clicked = button(orientation,650,460,80,40,red,bright_red,orientate)

        #once all ships are placed
        if len(sub_pos) == number_of_sub:
            orientation_clicked = button("Confirm",650,460,80,40,red,bright_red,set_carrier_on_board)

        if sub_clicked != None:
            shape = sub_clicked
        else:
            pass

        if orientation_clicked!=None:
            orientation = orientation_clicked
            pygame.time.delay(200)
        else:
            pass

        #Display message
        message_display("Click sub to put sub on any board.",smallText,white, 10,450, keepLeft = True)
        message_display("Click vert/hori to change orientation.",smallText,white,10,470, keepLeft = True)
        message_display("Reset by clicking on the submarine.",smallText,white,10,490, keepLeft = True)
        drawBoard(mouse,shape, orientation,ship_pos,None,None)

        for ship in ship_pos:
            drawship(ship)
        pygame.display.update()
        #------------------------------------------------------------------------------------------------------#
        #15 fps
        clock.tick(60)


# User DISPLAY board 2 to set carrier
def set_carrier_on_board():
    setboard = True
    shape = 'None'
    global orientation
    pygame.time.delay(200)
    ###INPUT BOXES
    while setboard:
        if len(sub_pos) < number_of_sub:
            set_sub_on_board()
        #Handle event----------------------------------------------------------------------------------------------------#
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target = UserSelection(mouse)
                #temporary ship
                #User Target
                temp_ship = ship_coordinates(target,shape, orientation)
                #1.check boundary collision
                boundary_collision = check_boundary(target,shape,orientation)
                #2.check ship collision
                ship_collision = check_collision(ship_pos,temp_ship)
                #3.check if user targeted exisiting ship
                #  if so delete ship
                remove_ship_index = delete_ship(target,ship_pos)
                
                if boundary_collision == False and ship_collision == False and len(ship_pos)<(number_of_sub+number_of_carrier):
                    ship_pos.append(temp_ship)
                    print(ship_pos)
                if remove_ship_index is not None:
                    print(ship_pos[remove_ship_index])
                    print(sub_pos)
                    if len(ship_pos[remove_ship_index]) == 3:
                        sub_pos.remove(ship_pos[remove_ship_index])
                    ship_pos.pop(remove_ship_index)

        for event in pygame.event.get():
            print(event)
        #Draw----------------------------------------------------------------------------------------------------#
        #Background display
        gameDisplay.fill(white)
        gameDisplay.blit(background, [0,0])
        message_display("Surface",largeText,black,(display_width*0.25),100)
        message_display("Subsea",largeText,black,(display_width*0.75),100)

        #Buttons
        carrier_clicked = button("carrier",520,460,80,40,red,bright_red,carrier)
        orientation_clicked = button(orientation,650,460,80,40,red,bright_red,orientate)
        #once all ships are placed
        if len(ship_pos) == (number_of_sub+number_of_carrier):
            button("Confirm",650,460,80,40,red,bright_red,comp_set_ships)

        if carrier_clicked != None:
            shape = carrier_clicked
        else:
            pass
        if orientation_clicked != None:
            orientation = orientation_clicked
            pygame.time.delay(200)
        else:
            pass

        #Message
        message_display("Click on carrier to put carrier on surface",smallText,white,10,450,keepLeft = True)
        message_display("Click hori/vert to change orientation.",smallText,white,10,470, keepLeft = True)
        message_display("Reset any ship by clicking on it.",smallText,white,10,490,keepLeft = True)

        drawBoard(mouse,shape, orientation,ship_pos,None,None)
        for ship in ship_pos:
            drawship(ship)
        pygame.display.update()
        #-------------------------------------------------------------------------------------------------------#
        clock.tick(60)

#Function: Computer set ships before User begins to set bombs
#Input: NIL
#Returns: Append Computer ship positions to compShip_pos list and proceed to user_targetBoard()
def comp_set_ships():
    global compShip_pos
    compShip_pos = compShip(number_of_carrier, number_of_sub)
    user_targetBoard()

#Function: user set bombs
#Input: NIL
#Returns: Shows result of user bombs on computer ships
def user_targetBoard():
    user_targetBoard = True
    shape = 'None'
    no_bomb = len(bomb_central_pos)
    global orientation
    global ship_pos
    global compShip_pos
    pygame.time.delay(200)
    ###INPUT BOXES
    while user_targetBoard:
        #Handle Event--------------------------------------------------------------------------------------------------#
        mouse = pygame.mouse.get_pos()
        #print(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target=UserSelection(mouse)

                bomb_place = bomb_coordinates(target,shape)
                boundary_collision=check_boundary(target,shape,orientation)
                bomb_collision=check_bomb_central(target,bomb_central_pos)
                if boundary_collision==False and bomb_collision==False:
                    #bomb_pos.append(bomb_place)
                    bomb_central_pos.append(target)
                    bomb_list.extend(bomb_place)

        for event in pygame.event.get():
            print(event)
        #Draw--------------------------------------------------------------------------------------------------#
        #Background display
        gameDisplay.fill(white)
        gameDisplay.blit(background, [0,0])
        message_display("Surface",largeText,black,(display_width*0.25),100)
        message_display("Subsea",largeText,black,(display_width*0.75),100)

        #Buttons
        bomb_clicked = button("bomb",550,460,80,40,red,bright_red,bomb)
        if bomb_clicked != None:
            shape = bomb_clicked
        else:
            pass

        drawBoard(mouse,shape,orientation,ship_pos,bomb_central_pos,"P attack Comp")

        #If computer bomb = user ships, goes to win page
        for ship in compShip_pos:
            draw_bombedship(ship, bomb_list,"P attack Comp")
        for bomb_coord in bomb_list:
            draw_bomb(bomb_coord, bomb_central_pos)
        if len(compShip_bombed_list) == (number_of_sub*3+number_of_carrier*4):
            message_display("You Win!",smallText,white,240,475)
            button("Win",550,460,80,40,red,bright_red,win_lose)
            shape = None
        elif len(bomb_central_pos) == no_bomb+1:
            button("Next",550,460,80,40,red,bright_red,user_resultBoard)
            shape = None
        else:
            message_display("Your battleships has been deployed!",smallText,white,240,470)
            message_display("Click to deploy bombs on enemy ships-->",smallText,white,240,490)
        #-------------------------------------------------------------------------------------------------------#
        pygame.display.update()
        clock.tick(60)

#Comp TARGET board & User RESULT board
#Comp TARGET board: computer sets random bombs
#User RESULT board: shows result of computer bomb on user ships
def user_resultBoard():
    user_resultBoard = True
    shape = 'None'
##    no_compbomb=len(compBomb_pos)
    compBomb()
    global orientation
    global ship_pos
    global compShip_pos
    pygame.time.delay(200)
    
    while user_resultBoard:
        mouse = pygame.mouse.get_pos()
        #Handle event--------------------------------------------------------------------------------------------------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target = UserSelection(mouse)
        for event in pygame.event.get():
            print(event)
        #Drawing--------------------------------------------------------------------------------------------------#
        #Background display
        gameDisplay.fill(white)
        gameDisplay.blit(background, [0,0])
        message_display("Surface",largeText,black,(display_width*0.25),100)
        message_display("Subsea",largeText,black,(display_width*0.75),100)

        drawBoard(mouse,shape,orientation,ship_pos,compBomb_central_pos,"Comp attack P")

        #If user bomb = computer ships, goes to lose page
        for ship in ship_pos:
            drawship(ship)
        for ship in ship_pos:
            draw_bombedship(ship, compBomb_list,"Comp attack P")
        for bomb_coord in compBomb_list:
            draw_bomb(bomb_coord, compBomb_central_pos)
        if len(ship_bombed_list) == (number_of_sub*3+number_of_carrier*4):
            message_display("You Lose!",smallText,white,240,475)
            button("Lose",550,460,80,40,red,bright_red,win_lose)
        else:
            message_display("The enemy retaliates!",smallText,white,240,480)
            button("Next",550,460,80,40,red,bright_red,user_targetBoard)

        pygame.display.update()
        #-------------------------------------------------------------------------------------------------------#
        clock.tick(60)

# Win Game/ Lose Game page
def win_lose():
    win_lose = True
    global orientation
    global ship_pos
    global compShip_pos
    pygame.time.delay(200)
    ###INPUT BOXES
    while win_lose:
        mouse = pygame.mouse.get_pos()
        #Handle Event-------------------------------------------------------------------------------------------------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target=UserSelection(mouse)
        for event in pygame.event.get():
            print(event)
        #Draw--------------------------------------------------------------------------------------------------#
        #Background display
        gameDisplay.fill(white)

        #win condition
        if len(compShip_bombed_list) == (number_of_sub*3 + number_of_carrier*4):
            result_screen = win_img
        #lose condition
        elif len(ship_bombed_list) == (number_of_sub*3 + number_of_carrier*4):
            result_screen = lose_img

        gameDisplay.blit(result_screen, [0,0])

        button("Play again",((display_width//2)-70),340,140,50,green,bright_green,play_again)
        button("Quit",((display_width//2)-50),400,100,50,red,bright_red,quit)

        pygame.display.update()
        clock.tick(60)

#========================================================================

#set_sub_on_board()
