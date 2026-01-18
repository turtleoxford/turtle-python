import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    def readfile(fname):
        handle=fopen(fname,1) #"file handle" assigned for accessing file - 1 = OPEN FOR READING
        if handle: #handle means file opening has succeeded and hence file already exists
            print('Contents read from '+fname+':')
            while not eof(handle):      #while not end of file
                s=freadline(handle)   #read the next line
                print('  '+s)
            fclose(handle)              #close the file
        else:
            print('  '+fname+' could not be opened for reading')

    origfname='TestFile.txt'  #original filename (created by previous example program)
    newfname='TestRename.txt' #new filename to be given
    for i in range(1,4):
        print('LOOP '+str(i)+' ...')
        print('')
        print('ABOUT TO TRY TO READ '+origfname+' ...')
        readfile(origfname)
        print('')
        print('ABOUT TO TRY TO READ '+newfname+' ...')
        readfile(newfname)
        print('')
        if i==1:
            print('RENAMING '+origfname+' TO '+newfname)
            if frename(origfname,newfname):
                print('  succeeded')
            else:
                print('  failed')
            print('')
        elif i==2:
            print('DELETING '+newfname)
            if fremove(newfname):
                print('  file no longer exists')
            else:
                print('  failed')
            print('')