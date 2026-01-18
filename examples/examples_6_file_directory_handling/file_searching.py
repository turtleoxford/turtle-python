import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    dhandle=0
    fhandle = []
    thisdir=finddir('*.*',fhandle)

    def showdir(d):
        if d=='':
            print('Base directory:')
        else:
            print('Directory "'+d+'":')
        chdir(d)
        fhandle=0
        thisfile=findfirst('*.*',fhandle)
        if thisfile=='':
            print('  <no files>')
        else:
            while thisfile!='':
                print('  '+thisfile)
                thisfile=findnext(fhandle)
        print('')

    print('Turtle directories (up to first level) and their files ...')
    print('')
    showdir('')
    while thisdir!='':
        showdir(thisdir)
        thisdir=findnext(dhandle)