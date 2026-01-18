import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    art=0
    adj=1
    col=2
    noun=3
    verb=4
    maxwords=10
    subdir='sentences'
    handle=[0]*5
    fname=['']*5
    wstr=['']*5
    numwords=[0]*5
    word=[]
    toadd=['']*maxwords
    for i in range(5):
        word.append(toadd)

    def setup():
        fname[art]='articles'
        fname[adj]='adjectives'
        fname[col]='colours'
        fname[noun]='nouns'
        fname[verb]='verbs'
        wstr[art]='the,a'
        wstr[adj]='hungry,quick,lazy,slow'
        wstr[col]='black,brown,grey,white'
        wstr[noun]='cat,dog,fox,monkey,rabbit'
        wstr[verb]='chases,jumps over,runs away from,watches'

    def writewordfiles():
        for i in range(5):
            handle[i]=fopen(subdir+'\\'+fname[i]+'.txt',3)
            s=wstr[i]
            count=1
            posn=s.find(',')
            while (posn>-1) and (count<5):
                count+=1
                fwriteline(handle[i], s[:posn])
                s=s[posn+1:]
                posn=s.find(',')
            fwriteline(handle[i], s)
            print('File "'+subdir+'\\'+fname[i]+'.txt" has been created, with '+str(count)+' lines')
            fclose(handle[i])
        print('')

    def readwordfiles():
        for i in range(5):
            handle[i]=fopen(subdir+'\\'+fname[i]+'.txt',1)
            if handle[i]:
                numwords[i]=0
                while not(eof(handle[i])) and (numwords[i]<maxwords):
                    word[i][numwords[i]]=freadline(handle[i])
                    numwords[i]+=1
            print(str(numwords[i])+' lines have been read from file "'+subdir+'\\'+fname[i]+'.txt"')
            fclose(handle[i])
        print('')

    def generate(n):

        def rand(n):
            return word[n][randrange(numwords[n])]

        print('Now up to '+str(n)+' random sentences will be generated using')
        print('these words. The generation will stop if a well-known target')
        print('sentence is achieved before the maximum has been reached.')
        print('')
        fhandle=fopen(subdir+'\\'+str(n)+'_sentences.txt',3)
        i=0
        first=True
        s=rand(art)+' '+rand(adj)+' '+rand(col)+' '+rand(noun)+' '+rand(verb)+' '+rand(art)+' '+rand(adj)+' '+rand(noun)+'.'
        s=chr(ord(s[0])-32)+s[1:]
        while first or ((i!=n) and (s!='The quick brown fox jumps over the lazy dog.')):
            first=False
            s=rand(art)+' '+rand(adj)+' '+rand(col)+' '+rand(noun)+' '+rand(verb)+' '+rand(art)+' '+rand(adj)+' '+rand(noun)+'.'
            s=chr(ord(s[0])-32)+s[1:]
            fwriteline(fhandle,s)
            i+=1
        fclose(fhandle)
        if i==(n):
            print(str(i)+' sentences written to "'+subdir+'\\'+str(n)+'_sentences.txt'+'".')
        else:
            if frename(subdir+'\\'+str(n)+'_sentences.txt',subdir+'\\'+str(i)+'_sentences.txt'):
                print(str(i)+' sentences written to "'+subdir+'\\'+str(i)+'_sentences.txt'+'"')
            else:
                print(str(i)+' sentences written to "'+subdir+'\\'+str(n)+'_sentences.txt'+'"')
                print('For some reason, this file could not be renamed.')
        if i<n:
            print('')
            print('  Loop terminated early, having written:')
            print('  "The quick brown fox jumps over the lazy dog."')
        if i<n/2:
            print('')
            if fmove(subdir+'\\'+str(i)+'_sentences.txt',str(i)+'_sentences.txt'):
                print('File moved to base directory.')
                if fcopy(str(i)+'_sentences.txt',subdir+'Latest_Good_Example.txt'):
                    print('File then copied back as "Latest_Good_Example.txt".')
                else:
                    print('But it could not be copied back as "Latest_Good_Example.txt" ...')
                    if fremove(subdir+'Latest_Good_Example.txt'):
                        if fcopy(str(i)+'_sentences.txt',subdir+'Latest_Good_Example.txt'):
                            print('... until the existing file with that name was deleted.')
                        else:
                            print('... for some reason unknown.')
                    else:
                        print('... and the existing file with that name could not be deleted.')
            else:
                print('For some reason, the file "'+subdir+'\\'+str(i)+'_sentences.txt" could not be moved to the base directory.')

    if mkdir(subdir):
        setup()
        writewordfiles()
        readwordfiles()
        generate(100000)
    else:
        print('Subdirectory '+subdir+' could not be created.')