import pygame
pygame.init()

#colors
# black=(0,0,0)
# grey=(40,40,40)
# white=(255,255,255)
# red=(200,0,0)
# bright_red=(255,0,0)
# green=(0,200,0)
# bright_green=(0,255,0)
# block_color=(53,115,255)
colours = { 'black':(0,0,0),'grey':(40,40,40),'white':(255,255,255),'red':(200,0,0),'bright_red':(255,0,0),'green':(0,200,0),'bright_green':(0,255,0),'block_color':(53,115,255)}


#display
display_width=800
display_height=520

#fonts
largeText=pygame.font.SysFont(None,115)
mediumText=pygame.font.SysFont(None,50)
smallText=pygame.font.SysFont(None,32)
verysmallText=pygame.font.SysFont(None,20)

#creating a surface object
gameDisplay=pygame.display.set_mode((display_width, display_height))
clock=pygame.time.Clock()

#For Text
#to reduce opacity of surface - https://nerdparadise.com/programming/pygameblitopacity
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)
#function:display text in pygame surface object
#input:(text, font, color, x, y, background colour of text, keepLeft)
#For Text
#function:display text in pygame surface object
#input:(text, font, color, x_center, y_center)
def message_display(text, font, colour, x, y, bgdcolour = None, keepLeft = False):
    #1)Render
    textSurface = font.render(text, True, colour)
    #2)blit the font
    #creates a new font object
    TextRect=textSurface.get_rect()
    #to position the text
    if keepLeft == False:
        TextRect.center=(x,y)
    else: TextRect.topleft = (x,y)
    #to add background colour
    if bgdcolour != None:
        bgd_surface = pygame.Surface((TextRect.width, TextRect.height))
        bgd_surface.fill(bgdcolour)
        blit_alpha(gameDisplay,bgd_surface,TextRect,150)
    gameDisplay.blit(textSurface,TextRect)
    #3)update
    #pygame.display.update()


def display_common_text():
    message_display("BATTLE SHIP",largeText,colours['black'],(display_width/2),100,colours['white'])
    message_display("UserName:",smallText,colours['black'],240,256,colours['white'],True)
    message_display("Password:",smallText,colours['black'],240,306,colours['white'],True)
    message_display("Go to",verysmallText,colours['black'],600,445)


#For Buttons
#function:
#1)display buttons
#2)changes button color when mouse hover
#3)execute function (action()) when button clocked
#input:(message, x, y,width,height,inactive color,
#active color, action function(default none))
#return ErrorStr
#https://www.youtube.com/watch?v=P-UuVITG7Vg&t=677s

def button(msg,x,y,w,h,ic,ac,action=None):
    #returns a tuple of (x,y)
    mouse=pygame.mouse.get_pos()
    #returns a tuple of (left mouse, scroll, right mouse)0, 1 clicked
    click=pygame.mouse.get_pressed()
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        #pygame.draw.rect(surfaceObj,color,(xpos,ypos,width,height))
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0]==1 and action!= None:
            print(msg)
            ErrorStr=action()
            return ErrorStr
    else:

        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    message_display(msg,smallText,colours['black'],x+w/2,y+h/2)
