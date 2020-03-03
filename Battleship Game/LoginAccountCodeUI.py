import pickle
import os
import CreateAccountCodeUI
LoginFail=3

#functionality:check UserName, Password and Tries 
#input:userName, password
#output:ErrorStr and Userinfo=[userName,Password,Dob ,Tries=1]
#functions used :
#           loadInformation(userName,password)
def loginAccountFunction(userName, password):
    ErrorStr=''
    #press enter button
    userInfo=loadInformation(userName,password)
    print(userInfo)
    ####1: User does not exist
    if userInfo==False:
        print("User does not exist")
        ErrorStr+="User does not exist\n"
    ######################################################
    ####2: Account Tries not up
    elif userInfo[3]<3:
        #### 2.1: Correct password
        if userInfo[1]==password:
            userInfo[3]=0
            try:
                aFile=open("accounts.out","r+b")
                info=pickle.load(aFile)
                print(info)
                aFile.close()
                info[userName]=userInfo
                print("Check USERS")
                print(info)
            except:
                info=Userinfo

            aFile=open("accounts.out","w+b")
            pickle.dump(info, aFile)
            aFile.close()

            return ErrorStr,userInfo
    ######################################################
        ####2.2: Wrong password
        else:

            userInfo[3]+=1
            ErrorStr+="Wrong Password\n"
            
            try:
                    aFile=open("accounts.out","r+b")
                    info=pickle.load(aFile)
                    print(info)
                    aFile.close()
                    info[userName]=userInfo
                    print("Check USERS")
                    print(info)
            except:
                    info=userinfo

            aFile=open("accounts.out","w+b")
            pickle.dump(info, aFile)
            aFile.close()
        print(ErrorStr)
        return  ErrorStr,userInfo
    ######################################################
    ####3: User ResetPassword Ties used up userInfo[3]==3
    elif userInfo[3]==3:
        if userInfo[1]==password:
            print("Login Successful")
        print("Account been unsuccessfully accessed 3 times.")
        ErrorStr+="Account been unsuccessfully accessed 3 times.\n"

        #ResetPassword(userInfo)
        return  ErrorStr,userInfo
    ######################################################
    ####4: User Locked userInfo[3]==4
    elif userInfo[3]==4:
        print("Account Locked")
        ErrorStr+="Account Locked\n"
        return  ErrorStr,userInfo
    return  ErrorStr,userInfo

#functionality:open pickle file and load specified userinfomation
#input:userName, password
#output:list=[userName,Password,Dob ,Tries=1]
def loadInformation(userName,password):
    ###############################################
    try:
        aFile=open("accounts.out",'r+b')
        userInfo=pickle.load(aFile)
        print(userInfo)
        aFile.close()
        if userName in userInfo:
            print("Load user info")
            print(userInfo.get(userName))
            return userInfo.get(userName)
        else:
            return False
    except:
        return False
    ################################################
    
#functionality: using user input
#               1. Check Dob
#               2. Check Password Validity
#               3. Check Confirm Password and password
#input:userName,UserdoB, UserPassword,ConfirmNewPassword, Tries
#output:ErrorStr, Tries
#functions used:
#    checkPassword() form CreateAccountCode.py
def ResetPassword(userName,UserdoB, UserPassword,ConfirmNewPassword, Tries):
    print("Reset Password")
    userInfo=loadInformation(userName,UserPassword)
    AccdoB=userInfo[2]
    userName=userInfo[0]
    ErrorStr=""

    #used checkDoB() form CreateAccountCode.py
    ErrorStr+=CreateAccountCodeUI.checkDoB(UserdoB)
    ######################################################
    ####1: wrong DoB
    if AccdoB!=UserdoB:
        print("Wrong DoB.",str(Tries)," tries left.")
        ErrorStr+="Wrong DoB."+str(Tries)+" tries left.\n"
        ####1.1: NO Tries left
        if(Tries==0):
            ##FILE
            userInfo[3]=4
            try:
                    aFile=open("accounts.out","r+b")
                    info=pickle.load(aFile)
                    print(info)
                    aFile.close()
                    info[userName]=userInfo
                    print("Check USERS")
                    print(info)
            except:
                    info=Userinfo

            aFile=open("accounts.out","w+b")
            pickle.dump(info, aFile)
            aFile.close()

        Tries-=1
        return ErrorStr,Tries
    ###################################################################
    ####2: correct DoB
    elif(AccdoB==UserdoB):
        #used checkPassword() form CreateAccountCode.py
        ErrorStr+=CreateAccountCodeUI.checkPassword(userName,UserPassword)
        #ConfirmNewPassword=input("Confirm Password:")
        print(ConfirmNewPassword)
        ###Choose another Password
        ####2.1: No input
        if ConfirmNewPassword=='':
            pass
        
        ####2.2: successful reset
        if(UserPassword==ConfirmNewPassword)and ErrorStr =='':
            userInfo[1]=UserPassword
            userInfo[3]=0
            try:
                    aFile=open("accounts.out","r+b")
                    info=pickle.load(aFile)
                    print(info)
                    aFile.close()
                    info[userName]=userInfo
                    print("Check USERS")
                    print(info)
            except:
                    info=Userinfo

            aFile=open("accounts.out","w+b")

            pickle.dump(info, aFile)
            aFile.close()
            return ErrorStr,3
        
        ####2.3: unsuccessful reset
        else:
            print("Password Does not match")
            print("press enter to choose new password")
            ErrorStr+="Password Does not match\n"
            return ErrorStr,3
    #########################################################################




#aFile=open('BLIM048.out','r+b')
#userInfo=pickle.load(aFile)


#aFile.close()
#print(userInfo)

#loginAccountFunction()
