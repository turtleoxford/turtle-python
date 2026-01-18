import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    subdir='testsubdir'
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
    code=checkdir(format(code, '08b'),subdir)
    code=int(code, 2)  # Convert binary string back to integer
    print('Code on exit = $'+hex(code))
    if code and tonentry>0:
        print('Subdirectory existed on entry')
    else:
        print('No subdirectory on entry')
    print('')
    showresult(mkdir(subdir),'mkdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    showresult(mkdir(subdir),'mkdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    showresult(rmdir(subdir),'rmdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    showresult(rmdir(subdir),'rmdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    showresult(mkdir(subdir),'mkdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    showresult(mkdir(subdir),'mkdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    if int(checkfile('00000010', subdir+'A_File.txt'), 2)>127:
        print('File has been created')
    else:
        print('File could not be created')
    showresult(rmdir(subdir),'rmdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')
    print('')
    if int(checkfile('00000001', subdir+'A_File.txt'), 2)<128:
        print('File has been deleted')
    else:
        print('File could not be deleted')
    showresult(rmdir(subdir),'rmdir('+subdir+')')
    showresult(isdir(subdir),'direxists('+subdir+')')