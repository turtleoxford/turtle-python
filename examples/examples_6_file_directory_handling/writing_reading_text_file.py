import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    def writefile():
        if not os.path.exists(myfilename):
            handle=fopen(myfilename,3) #3 = OPEN FOR WRITING
            print(myfilename+' has been opened for writing ...')
            fwriteline(handle,'This is the first line to be written.')
            fwriteline(handle,'This is the second line to be written.')
            fwriteline(handle,'This is the third line to be written.')
            fclose(handle) #write lines to the file, then close it
        else: #if file already exists, open for appending instead
            print(myfilename+' could not be opened for writing')
            handle=fopen(myfilename,2) #2 = OPEN FOR APPENDING
            if handle: #handle means file opening has succeeded and hence file already exists
                print(myfilename+' has been opened for appending ...')
                fwriteline(handle,'This is the first line to be appended.')
                fwriteline(handle,'This is the second line to be appended.')
                fwriteline(handle,'This is the third line to be appended.')
                fclose(handle) #write lines to the file, then close it
            else: #means there's been some error, e.g. illegal filename
                print('Nor could it be opened for appending')

    def readfile():
        if os.path.exists(myfilename):
            handle=fopen(myfilename,1) #1 = OPEN FOR READING
            print('Contents read from '+myfilename+':')
            while not eof(handle):    #while not end of file, ...
                s=freadline(handle) #read the next line from the file,
                print('  '+s)         #and write it to the output display
            fclose(handle) #on reaching the end of file, close it
        else:
            print(myfilename + ' could not be opened for reading')

    myfilename='TestFile.txt' #specify chosen filename
    writefile()                 #write three lines to the file
    print('') #blank line to output display
    readfile() #read the file, displaying contents to output