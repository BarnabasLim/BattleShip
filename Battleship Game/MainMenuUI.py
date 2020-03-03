#========================================================================
#1.MainMenu Parameters
#2.MainMenu Functions
#3.MainMenu Variables
#4.MainMenu Main Loops

#please Run this File
import pygame
import random
#input box module
from inputTest import *
import tkinter
from tkinter import messagebox
import pickle
from UtilityUI import *
import CreateAccountCodeUI
import LoginAccountCodeUI
import gameMainUI

login_img = pygame.image.load('battleship.png')

pygame.init()
#========================================================================
#------------------------
#1.MainMenu Parameters
#------------------------
#display
display_width=800
display_height=520

#color dictionary
colours = { 'black':(0,0,0),'grey':(40,40,40),'white':(255,255,255),'red':(200,0,0),'bright_red':(255,0,0),'green':(0,200,0),'bright_green':(0,255,0),'block_color':(53,115,255)}

#fonts
largeText=pygame.font.SysFont(None,115)
mediumText=pygame.font.SysFont(None,50)
smallText=pygame.font.SysFont(None,32)
verysmallText=pygame.font.SysFont(None,20)


#creating a surface object
gameDisplay=pygame.display.set_mode((display_width, display_height))
clock=pygame.time.Clock()

#========================================================================
#------------------------
#2.MainMenu Functions
#------------------------
#tkinter for pop up message
#function: generate error message window
#input: message
#https://www.youtube.com/watch?v=4McKSuuUQ-0
def error_message(msg):
    my_window=tkinter.Tk()
    my_window.eval('tk::PlaceWindow %s center'% my_window.winfo_toplevel())
    my_window.withdraw()

    tkinter.messagebox.showinfo("Invalid",msg)
    my_window.deiconify()
    my_window.destroy()
    my_window.quit()


#Function:
#1)check validity of username, password, dob
#2)generate Error Message board
#input:username, password, dob
#return:ErrorStr
def CreateAccCheck():
    userName=input_box1.text
    password=input_box2.text
    doB=input_box3.text
    print(userName)
    print(password)
    print(doB)
    if userName=='' or password=='' or doB=='':
        ErrorStr='Empty Inputs!'
    else:
        #1. Test username availability
        #2. Test password validity
        ErrorStr,userInfo=CreateAccountCodeUI.CreateAccFunction(userName, password, doB)
    if ErrorStr=='' or ErrorStr is None:
        pass
    else:
        error_message(ErrorStr)
    return ErrorStr

#Function:
#1)check login password and username
#input: username, password
#output:ErrorStr
def LoginAccCheck():
    userName=input_box1.text
    password=input_box2.text
    print(userName)
    print(password)
    if userName=='' or password=='':
        ErrorStr='Empty Inputs!'
    else:
        #1. Test username availability
        #2. Test password validity
        ErrorStr,userInfo=LoginAccountCodeUI.loginAccountFunction(userName, password)
    if ErrorStr=='' or ErrorStr is None:
        pass
    else:
        error_message(ErrorStr)
    return ErrorStr

#Function returns string 'reset'
#required to work with the button() function
def ResetPasswordCheck():
    return 'Reset'
#========================================================================
#------------------------
#3.MainMenu Variables
#------------------------

input_box1 = InputBox(400, 250, 140, 32)
input_box2 = InputBox(400, 300, 140, 32, isPassword=True)
input_box3 = InputBox(400, 350, 140, 32, isDoB=True)

input_boxes = [input_box1, input_box2,input_box3]

#Input Box for Reset Password Screen
input_box_reset1 = InputBox(400, 250, 140, 32, isDoB=True)
input_box_reset2 = InputBox(400, 300, 140, 32, isPassword=True)
input_box_reset3 = InputBox(400, 350, 140, 32, isPassword=True)

input_boxes_reset = [input_box_reset1, input_box_reset2, input_box_reset3]

#========================================================================
#------------------------
#4.MainMenu Main Loops
#------------------------
def SignUp():
    pygame.time.delay(200)
    Signup=True
    while Signup:
        #Handle Event----------------------------------------------------------------------------------------------------#
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            ##INPUT BOXES
            #handles events on inputboxes
            #clear remnants from previous usage of the inputBox objects
            for box in input_boxes:
                box.handle_event(event)

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    print(input_box1.text)
                    print(input_box2.text)
                    print(input_box3.text)


        #Draw----------------------------------------------------------------------------------------------------#
        #Fill entire display
        #gameDisplay.fill(white)
        gameDisplay.blit(login_img,[0,0])
        ##INPUT BOXES
        ##renders input boxes
        for box in input_boxes:
            box.update()
        for box in input_boxes:
            box.draw(gameDisplay)
        ##


        #Text
        #1)render the font
        #2)blit the font
        #3)display update
        message_display("Create Account",smallText,colours['black'],(display_width/2),200,colours['white'])
        message_display("Date of Birth:",smallText,colours['black'],240,356,colours['white'],True)
        display_common_text()

        #button
        ErrorStr=button("Create",150,450,100,50,colours['green'],colours['bright_green'],CreateAccCheck)

        #Error String Handling(Variable)----------------------------------------------------------------------------------------------------#
        #if no Error Message was returned from CreateAccCheck
        if ErrorStr==''and ErrorStr is not None:
            print("success")
            userName=input_box1.text
            password=input_box2.text
            doB=input_box3.text
            Userinfo={(userName):[userName,password,doB,0]}
            #####################
            try:
                aFile=open("accounts.out","r+b")
                info=pickle.load(aFile)
                print(info)
                aFile.close()
                info.update(Userinfo)
                print("Check USERS")
                #print(info)
            except:
                info=Userinfo

            aFile=open("accounts.out","w+b")
            pickle.dump(info, aFile)
            aFile.close()
            login()
            intro=False
        ###################################
        else:
            pass

        button("Login",550,450,100,50,colours['red'],colours['bright_red'],login)
        pygame.display.update()
        #15 fps
        clock.tick(15)

def login():
    pygame.time.delay(200)
    loginSeq=True
    while loginSeq:
        #Handle Event----------------------------------------------------------------------------------------------------#
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            ##INPUT BOXES
            ##inputboxs events
            for box in input_boxes[0:2]:
                box.handle_event(event)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    print(input_box1.text)
                    print(input_box2.text)
                    print(input_box3.text)
            ##
        #Draw----------------------------------------------------------------------------------------------------#
        #Fill entire display
        #gameDisplay.fill(white)
        gameDisplay.blit(login_img,[0,0])
        ##INPUT BOXES
        #renders input boxes
        for box in input_boxes[0:2]:
            box.update()
        for box in input_boxes[0:2]:
            box.draw(gameDisplay)
        ##


        #Text
        #1)render the font
        #2)blit the font
        #3)display update
        display_common_text()
        message_display("Login",smallText,colours['black'],(display_width/2),200,colours['white'])
        #Button
        #renders buttons
        button("Signup",550,450,100,50,colours['red'],colours['bright_red'],SignUp)
        ErrorStr=button("Enter",150,450,100,50,colours['green'],colours['bright_green'],LoginAccCheck)
        #Error String Handling(Variable)----------------------------------------------------------------------------------------------------#
        if ErrorStr==''and ErrorStr is not None:
            #add game code function here
            print("success")
            userName=input_box1.text
            password=input_box2.text
            doB=input_box3.text
            #display_width=1320
            #display_height=660
            #gameDisplay=pygame.display.set_mode((display_width, display_height))
            gameMainUI.set_sub_on_board()
        elif ErrorStr=='Account been unsuccessfully accessed 3 times.\n':
            userName=input_box1.text
            resetPasswordUI(userName)
            break

        pygame.display.update()
        #15 fps
        clock.tick(15)

def resetPasswordUI(userName):
    pygame.time.delay(200)
    loginSeq=True
    tries=2
    ###INPUT BOXES
    while loginSeq:
        #Handle Event----------------------------------------------------------------------------------------------------#
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            ##INPUT BOXES
            #reset input boxes parameters for recording passwords and dob
            for option in input_boxes_reset:
                option.handle_event(event)
                if event == pg.MOUSEBUTTONDOWN:print(event.pos)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    print(input_box_reset1.text)
                    print(input_box_reset2.text)
                    print(input_box_reset3.text)
            ##

        #Draw----------------------------------------------------------------------------------------------------#
        #Fill entire display
        gameDisplay.blit(login_img,[0,0])
        ##INPUT BOXES
        #renders input boxes
        for box in input_boxes_reset:
            box.update()
        for box in input_boxes_reset:
            box.draw(gameDisplay)
        ##


        #Text
        #1)render the font
        #2)blit the font
        #3)display update
        message_display("BATTLE SHIP",largeText,colours['black'],(display_width/2),100,colours['white'])
        message_display("Reset Password for: "+userName,smallText,colours['black'],display_width/2,200,colours['white'])
        message_display("Date of Birth:",smallText,colours['black'],180,256,colours['white'],True)
        message_display("Password:",smallText,colours['black'],180,306,colours['white'],True)
        message_display("Confirm Password:",smallText,colours['black'],180,356,colours['white'],True)
        ErrorStr=button("Go",150,450,100,50,colours['green'],colours['bright_green'],ResetPasswordCheck)
        button("Signup",550,450,100,50,colours['red'],colours['bright_red'],SignUp)
        #Error String(Variable) Handling----------------------------------------------------------------------------------------------------#
        if ErrorStr=='Reset'and ErrorStr is not None:
            doB=input_box_reset1.text
            password=input_box_reset2.text
            newPassword=input_box_reset3.text

            if newPassword=='' or password=='' or doB=='':
                ErrorStr="Empty inputs!"
            else:
                ErrorStr,tries=LoginAccountCodeUI.ResetPassword(userName,doB,password,newPassword, tries)
                print(tries)
                if tries==-1:
                    error_message("Account Locked!")
                    SignUp()
            if ErrorStr!='':
                error_message(ErrorStr)




        if ErrorStr==""and ErrorStr is not None:
            #reset input boxes to default
            input_box1.isDoB = False
            input_box2.isPassword = True
            input_box3.isDoB = True
            input_box3.isPassword = False
            login()
            pass


        pygame.display.update()
        #15 fps
        clock.tick(15)

#========================================================================

SignUp()
