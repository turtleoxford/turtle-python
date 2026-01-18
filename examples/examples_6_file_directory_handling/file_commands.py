import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    testfile1='testfile1.txt'
    testfile2='testfile2.txt'
    enquire=0
    delete=1
    create=2
    recreate=3
    tnotify=4
    fnotify=16
    tonentry=64
    tonexit=128
    todo=create

    def showresult(b,n):
        if b:
            print(n.upper()+' returns TRUE')
        else:
            print(n.upper()+' returns FALSE')

    code=todo+tnotify+fnotify
    print('Code on entry = $'+hex(code))
    print('The initial CHECKFILE command will invoke a message window ...')
    code=checkfile(format(code, '08b'),testfile1)
    code=int(code, 2)
    print('Code on exit = $'+hex(code))
    if code&tonentry>0:
        print('File existed on entry')
    else:
        print('No file on entry')
    if code&tonexit>0:
        print('File existed on exit')
    else:
        print('No file on exit')
    print('')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    print('')
    showresult(fremove(testfile1),'deletefile('+testfile1+')')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    print('')
    if int(checkfile('00000010',testfile1), 2)>127:
        print('File "'+testfile1+'" has been created')
    else:
        print('File "'+testfile1+'" could not be created')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    showresult(isfile(testfile2),'fileexists('+testfile2+')')
    print('')
    if fcopy(testfile1,testfile2):
        print('File "'+testfile1+'" has been copied to "'+testfile2+'"')
    else:
        print('File "'+testfile1+'" could not be copied to "'+testfile2+'"')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    showresult(isfile(testfile2),'fileexists('+testfile2+')')
    print('')
    if int(checkfile('00000001',testfile1), 2)<128:
        print('File "'+testfile1+'" has been deleted')
    else:
        print('File "'+testfile1+'" could not be deleted')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    print('')
    showresult(fremove(testfile1),'deletefile('+testfile1+')')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    print('')
    showresult(isfile(testfile2),'fileexists('+testfile2+')')
    if frename(testfile2,testfile1):
        print('File "'+testfile2+'" has been renamed "'+testfile1+'"')
    else:
        print('File "'+testfile2+'" could not be renamed "'+testfile1+'"')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')
    showresult(isfile(testfile2),'fileexists('+testfile2+')')
    print('')
    showresult(fremove(testfile1),'deletefile('+testfile1+')')
    showresult(isfile(testfile1),'fileexists('+testfile1+')')