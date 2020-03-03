import re
import os #used to mannage file
import pickle
from calendar import monthrange
import datetime

passwordRules="Password must have the following:\n\
\t 1.More than 8 characters\n\
\t 2.Contain at least one uppercase and lower case\n\
\t 3.Contain at least one digit and special symbol\n\
\t 4.Must not contain username"

#functionality:Collects username, password, doB
#input:Nil
#output:list=[userName, password,doB]
#functions used:
#   checkPassword(userName)
#   checkUserName()
#   checkDoB()
def CreateAccFunction(userName, password,doB):
    print(passwordRules)
    ErrorStr=''
    ErrorStr+=checkUserName(userName)
    ErrorStr+=checkPassword(userName,password)
    ErrorStr+=checkDoB(doB)
    print(ErrorStr)
    return ErrorStr,{(userName):[userName,password,doB,0]}

##################################################################
#functionality:Collect Password and check for compliance with rules
#input:userName
#output:Password
def checkPassword(userName,password):
    ErrorStr=''

    length_regex = re.compile(r'.{8,}')
    uppercase_regex = re.compile(r'[A-Z]')
    lowercase_regex = re.compile(r'[a-z]')
    digit_regex = re.compile(r'[0-9]')
    special_regex=re.compile(r'[@#$%&+=!,.?]')
    if (length_regex.search(password) is not None
        and uppercase_regex.search(password) is not None
        and lowercase_regex.search(password) is not None
        and digit_regex.search(password) is not None
        and special_regex.search(password)is not None
        and (userName in password)is not True):
        print("Valid:",password)

    else:
        if(len(password)<8):
            ErrorStr+="NOTE: Password must be more than 8 characters\n"
        if(uppercase_regex.search(password) is None):
            ErrorStr+="NOTE: Password must contain at least one uppercase\n"
        if(lowercase_regex.search(password) is None):
            ErrorStr+="NOTE: Password must contain at least one lower case\n"
        if(digit_regex.search(password)is None):
            ErrorStr+="NOTE: Password must contain at least one digit\n"
        if(special_regex.search(password)is None):
            ErrorStr+="NOTE: Password must contain at least one special symbol\n"
        if userName in password:
            ErrorStr+="NOTE: Password must not contain username\n"
        print(ErrorStr)
    return ErrorStr
##################################################################
#functionality:Collect Username and check for existance on Database
#input:Nil
#output:userName
def checkUserName(userName):
    ErrorStr=''
    try:
        aFile=open("accounts.out","r+b")
        info=pickle.load(aFile)
        aFile.close()
        if userName in info:
            print(info)
            print("Username Error: Username taken.\n")
            ErrorStr+="Username Error: Username taken.\n"
            return ErrorStr
        else:
            return ErrorStr
    except Exception as e:
        print(e)
        ErrorStr+=""
        return ErrorStr

#functionality:Collect DoB check for validity
#input:Nil
#output:DoB
def checkDoB(doB):
    ErrorStr=''
    #doB=input("Date of Birth\nDDMMYYYY:")
    if(doB.isdigit()==False or len(doB)!=8):
        ErrorStr+="DoB Error: Invalid Date of Birth.\n"

    else:
        now=datetime.datetime.now()
        y=int(doB[4:8])
        m=int(doB[2:4])
        d=int(doB[0:2])
        if y>now.year or \
            (y==now.year and m>now.month) or \
            y==now.year and m==now.month and d>now.day:
            ErrorStr+="DoB Error: Future Date\n"
        if 0>m or m>12:
            ErrorStr+="DoB Error: Month is out of bounds\n"
        elif d>(monthrange(y,m))[1]:
            ErrorStr+="DoB Error: Day is out of bounds\n"

    print(doB)
    print(ErrorStr)
    return ErrorStr
