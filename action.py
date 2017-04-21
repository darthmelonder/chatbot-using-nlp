from decimal import Decimal

import nltk
import os
import filecheck

from filecheck import *

#set0 refers to items that may have one or more than one arguments, like close, open
#set1 refers to items that require two arguments only, like copy, paste
set0 = set()
set1 = set()
set2 = set()
set3 = set()
set4 = set()

list0 = ['open','close','shut','exit']
list1 = ['copy','cut','move','duplicate']
list2 = ['run','execute']
list3 = ['change']
list4 = ['make','create']

set0 = set(list0)
set1 = set(list1)
set2 = set(list2)
set3 = set(list3)
set4 = set(list4)

openProcess = {}
extensions = {}
files=set()
directories=set()
commands = []

extensions = {}

#extension function loader

f = open('extensions','r')
for line in f:
    line_chunks = line.split('->')
    command = line_chunks[0]
    command = command.strip()
    ext = line_chunks[1]
    ext = ext.strip()
    if ',' in ext:
        ext_arr = ext.split(',')
        n = len(ext_arr)
        for i in range(0,n):
            ext_arr[i] = ext_arr[i].strip()
            extensions[ext_arr[i]] = command
    else:
        extensions[ext] = command

#print(extensions)


def openDir(dirName):
    os.system('nautilus '+dirName+' &')

def appChecker():
    f = open('appnames.txt','r')
    for line in f:
        if '=>' in line:
            line_chunks = line.split('=>')
            n = len(line_chunks)
            for i in range(0,n-1):
                command = line_chunks[n-1].rstrip('\n')
                if '%' in command:
                    position = command.find('%')
                    command = command[0:position]
                commands.append(command.strip())
    f.close()

def openProcessRefresher():
    os.system("ps -A -o pid>temp")
    f = open('temp','r')
    processList = []
    for line in f:
        processList.append(line.strip())
    #print processList
    for key in openProcess:
        if openProcess[key] not in processList:
            'remove it from the chart because it is not an active process'
            del openProcess[key]
        
'''
def fileNamesLoader():
    status = []
    fileDirs = []
    os.system('ls -lv > chooser')
    files.clear()
    directories.clear()
    f = open('chooser','r')
    for line in f:
        if line[0]=='-':
            status.append('f')
        elif line[0]=='d':
            status.append('d')
    f.close()
    os.system('ls > names')
    f = open('names','r')
    for line in f:
        line = line.strip().rstrip('\n')
        fileDirs.append(line)
    f.close()
    for i in range(0,len(status)):
        if status[i]=='f':
            files.add(fileDirs[i])
        elif status[i]=='d':
            directories.add(fileDirs[i])
'''


def openFiles(appName):
    if '.' not in appName:
        os.system('gedit '+appName+ '&')
    else:
        dotpos = appName.find('.')
        extn = appName[dotpos:len(appName)]
        if extn in extensions:
            os.system(extensions[extn]+' '+appName+' &')

def actionSequence(Verb,Args,fileMode):
    Verb = Verb.lower()
    if Verb in set0:#open and close related
        if Verb == 'open' and fileMode == True:
            Apps = Args
            appChecker()
            for i in range(0,len(Apps)):
                appName = Apps[i]['AN'][0].strip()
                if appName in commands:
                    os.system(appName+" & echo $!>temp 2>error")
                    f = open('temp','r')
                    for line in f:
                        openProcess[appName] = line.rstrip('\n').strip()
                    os.system('rm temp')
                else:
                    #check if it has a dot or not, if no dot, then file, otherwise open it specially
                    l = checkIfInHome(appName)
                    if len(l) == 0:
                        print("Oops! Seems like there is no file like this!")
                    elif len(l) == 1:
                        #print(l)
                        openFiles(l[0])
                    else:
                        print("Seems like there is more than one file with this name")
                        print("Please select an option to select one :")
                        for i in range(0,len(l)):
                            print(str(i+1)+' '+l[i])
                        choice = raw_input().strip()
                        choice = int(choice)
                        if choice in range(1,len(l)+1):
                            openFiles(l[choice-1])
                        else:
                            print("")
    
        elif Verb == 'open' and fileMode == False:
            for i in range(0,len(Args)):
                dirName = Args[i]['AN'][0]
                l = checkIfInHomeDir(dirName)
                if len(l) == 0:
                    print("Oops! Seems like there is no folder like this!")
                elif len(l) == 1:
                    openDir(l[0])
                else:
                    print("Seems like there is more than one folder with this name")
                    print("Please select an option to select one :")
                    for i in range(0,len(l)):
                        print(str(i+1)+' '+l[i])
                    choice = raw_input().strip()
                    choice = int(choice)
                    if choice in range(1,len(l)+1):
                        openDir(l[choice-1])
                    else:
                        print("")
        
             
        elif Verb.strip() in ['close','exit','shut']:
            Apps = Args
            openProcessRefresher()
        
            for i in range(0,len(Apps)):
                appName = Apps[i]['AN'][0].strip()
                  #print(appName)
                                
                    #k=str(pid)
                                #print(k)
                os.system('pkill ' +appName)
                print("Application successfully closed " )

                        '''        print(openProcess)
                if appName in openProcess:
                    os.system('sudo kill -9 '+openProcess[appName])
                    print("Application successfully closed " )

                else:
                    print("Oops! This process is not active " + appName)
'''
                    

def createSequence(Verb,Args,NameRHS):
    if Verb in set4: #make a directory
        rhs = NameRHS.split('->')[1]
        rhs = rhs.split('|')
        for i in range(0,len(rhs)):
            rhs[i] = rhs[i].strip()
        Args = Args[0]['NAME'][0]
        for word in rhs:
            if word in Args:
                #print(Args)
                os.system('mkdir '+Args[word][0])
                print("Successfully created the folder named "+Args[word][0])
                break

def checkFileInFolder(fn,folder):
    os.system('find '+folder+' -type f -name '+fn+' 2>/dev/null |cat>fname')
    os.system('wc -l<fname>lengthf')
    f = open('lengthf','r')
    exist=''
    for line in f:
        exist = line.rstrip('\n')
    exist = int(exist)
    return exist

def checkFolderInDir(fn,folder):
    os.system('find '+folder+' -type d -name '+fn+' 2>/dev/null |cat>dname')
    os.system('wc -l<dname>lengthd')
    f = open('lengthd','r')
    exist=''
    for line in f:
        exist = line.rstrip('\n')
    exist = int(exist)
    return exist

def cutCopy(Verb,filename,source,dest):
    filename = filename['AN'][0]
    source = source['AN'][0]
    dest = dest['AN'][0]
    os.system('find /home -type d -name '+source+' 2>/dev/null |cat>src')
    os.system('wc -l<src >srcL')
    f = open('srcL','r')
    for line in f:
        countS = line.rstrip('\n')
    f.close()
    countS = int(countS)
    os.system('rm srcL')

    os.system('find /home -type d -name '+dest+' 2>/dev/null |cat>dest')
    os.system('wc -l<dest > destL')
    f = open('destL','r')
    for line in f:
        countD = line.strip('\n')
    f.close()
    countD = int(countD)
    os.system('rm destL')
    
    if countS == 1 and countD == 1:
        f = open('src','r')
        for line in f:
            source = line.rstrip('\n')
        f.close()
        f = open('dest','r')
        for line in f:
            dest = line.strip('\n')
        f.close()
        doesFileExist = checkFileInFolder(filename,source)
        doesDirExist = checkFolderInDir(filename,source)
        if doesFileExist == 0:
            #print("Oops! Seems like there is no file named this in the folder")
            print("")
        elif doesFileExist == 1:
            f = open('fname','r')
            line = ''
            for line in f:
                line = line.rstrip('\n')
            cutCopyFun(Verb,line,source,dest)
            f.close()
        if doesDirExist == 0:
            #print("Oops! Seems like there is no sub-folder named this in the folder")
            print("")
        elif doesDirExist == 1:
            f = open('dname','r')
            line = ''
            for line in f:
                line = line.rstrip('\n')
            cutCopyFunDir(Verb,line,source,dest)
            f.close()
            
    else:
        f = open('src','r')
        source = []
        for line in f:
            source.append(line.rstrip('\n'))
        f.close()
        dest = []
        f = open('dest','r')
        for line in f:
            dest.append(line.rstrip('\n'))
        f.close()
        print("Seems like there is either more then one source or destination")
        print("Choose a source...")
        for i in range(0,len(source)):
            print(str(i+1)+" "+source[i])
        choice = raw_input().strip()
        choice = int(choice)
        if choice in range(1,len(source)+1):
            source = source[choice-1]
        else:
            print("Wrong choice!")
            return

        print("Choose a destination...")
        for i in range(0,len(dest)):
            print(str(i+1)+" "+dest[i])
        choice = raw_input().strip()
        choice = int(choice)
        if choice in range(1,len(dest)+1):
            dest = dest[choice-1]
        else:
            print("Wrong choice!")
            return

        doesFileExist = checkFileInFolder(filename,source)
        if doesFileExist == 0:
            #print("Oops! Seems like there is no file named this in the folder")
            print("")
        elif doesFileExist == 1:
            f = open('fname','r')
            line = ''
            for line in f:
                line = line.rstrip('\n')
            cutCopyFun(Verb,line,source,dest)
            f.close()
        if doesDirExist == 0:
            #print("Oops! Seems like there is no sub-folder named this in the folder")
            print("")
        elif doesDirExist == 1:
            f = open('dname','r')
            line = ''
            for line in f:
                line = line.rstrip('\n')
            cutCopyFunDir(Verb,line,source,dest)
            f.close()
            
    #else:
    
    os.system('rm src')
    os.system('rm dest')
    os.system('rm fname')

def cutCopyFun(Verb,line,source,dest):
    if Verb in ['copy','duplicate']:
        os.system('cp '+line+' '+dest)
    elif Verb in ['cut','move']:
        os.system('mv '+line+' '+dest)
        
def cutCopyFunDir(Verb,line,source,dest):
    if Verb in ['copy','duplicate']:
        os.system('cp -r '+line+' '+dest)
    elif Verb in ['cut','move']:
        os.system('mv -r '+line+' '+dest)

def changeWallpaper(Verb,fileName):
    fileName = fileName['AN'][0]
    extensions = ['.png','.jpg','.jpeg','.bmp','.gif']
    foundExt = False
    for i in range(0,len(extensions)):
        if extensions[i] in fileName:
            foundExt = True
    if foundExt == False:
        print("Oops.. Seems like it is not a valid image!")
        return
    else:
        imageList = checkIfInHome(fileName)
        if len(imageList) == 0:
            print("Oops! Seems like a file like this doesn't exist!")
        elif len(imageList) == 1:
            print(fileName)
            imageList = imageList[0]
        else:
            print("Seems like there are more than one image with the same name")
            print("Which one do you want to set as?")
            for i in range(0,len(imageList)):
                print(str(i+1)+' '+imageList[i])
            choice = raw_input().strip()
            choice = int(choice)
            if choice in range(1,len(imageList)+1):
                imageList = imageList[choice-1]
            else:
                print("Wrong choice!")
                return
        os.system('gsettings set org.gnome.desktop.background picture-uri file://'+imageList)

def counter(fileName,obj):
    if obj.lower() in ['lines','sentences','sentence','line']:
        l = checkIfInHome(fileName)
        if len(l) == 0:
            print("Oops! Seems like there is no file like this!")
        elif len(l) == 1:
            printLines(l[0])
        else:
            print("Seems like there is more than one file with this name")
            print("Please select an option to select one :")
            for i in range(0,len(l)):
                print(str(i+1)+' '+l[i])
            choice = raw_input().strip()
            choice = int(choice)
            if choice in range(1,len(l)+1):
                printLines(l[choice-1])
    elif obj.lower() in ['words']:
        l = checkIfInHome(fileName)
        if len(l) == 0:
            print("Oops! Seems like there is no file like this!")
        elif len(l) == 1:
            printWords(l[0])
        else:
            print("Seems like there is more than one file with this name")
            print("Please select an option to select one :")
            for i in range(0,len(l)):
                print(str(i+1)+' '+l[i])
            choice = raw_input().strip()
            choice = int(choice)
            if choice in range(1,len(l)+1):
                printWords(l[choice-1])

def printLines(fileName):
    os.system('wc -l <'+fileName+'>ctr')
    f = open('ctr','r')
    ctr = 0
    for line in f:
        ctr = int(line.rstrip('\n'))
    f.close()
    print(fileName+' has '+str(ctr)+' lines')

def printWords(fileName):
    os.system('wc -w <'+fileName+'>ctr')
    f = open('ctr','r')
    ctr = 0
    for line in f:
        ctr = int(line.rstrip('\n'))
    f.close()
    print(fileName+' has '+str(ctr)+' words')
