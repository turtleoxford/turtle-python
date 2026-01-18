import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    # generates the reverse of a string
    def reverse(s):
        result=''
        for posn in range(len(s)):
            result=s[posn]+result
        return result

    # generates the reverse of a string recursively
    def reverseRecursive(s):
        if (s==''):
            return s
        return reverseRecursive(s[1:len(s)])+s[0]

    # tests whether a character is uppercase (1), lowercase (0), or neither (-1)
    def testCase(c):
        if ((ord(c)>=ord('A')) and (ord(c)<=ord('Z'))):
            return 1
        if ((ord(c)>=ord('a')) and (ord(c)<=ord('z'))):
            return 0
        return -1

    # capitalises first letter of each word, leaving other letters unchanged and
    # treating any non-letter as a word separator; the native TITLE function
    # treats only spaces as word separators, making subsequent letters lowercase
    def initCaps(s):
        newword=True
        result=''
        for posn in range(len(s)):
            c=s[posn]
            if (newword and (testCase(c)==0)):
                c=chr(ord(s[posn])-32)
            result=result+c
            newword=(testCase(c)==-1)
        return result

    # generates the Caesar cipher of a string
    def caesar(s,n):
        result=''
        for posn in range(len(s)):
            c=s[posn]
            if (testCase(c)==1):
                c=chr(ord(c)+n)
                if (ord(c)>ord('Z')):
                    c=chr(ord(c)-26)
            else:
                if (testCase(c)==0):
                    c=chr(ord(c)+n)
                    if (ord(c)>ord('z')):
                        c=chr(ord(c)-26)
            result=result+c
        return result

    # shows the results of applying the above functions to a string
    def process(s):
        print('')
        print('ORIGINAL STRING:               "'+s+'"')
        print('REVERSED (by iteration):       "'+reverse(s)+'"')
        print('REVERSED (by recursion):       "'+reverseRecursive(s)+'"')
        print('INITIAL CAPITAL ALL WORDS:     "'+initCaps(s)+'"')
        print('REVERSED THEN INITIAL CAPITAL: "'+initCaps(reverse(s))+'"')
        print('CAESAR CIPHER (1 letter):      "'+caesar(s,1)+'"')
        print('CAESAR DECRYPT (1+25 = 26):    "'+caesar(caesar(s,1),25)+'"')
        print('CAESAR CIPHER (4 letters):     "'+caesar(s,4)+'"')
        print('CAESAR DECRYPT (4+22 = 26):    "'+caesar(caesar(s,4),22)+'"')

    # show the output
    print('Some User-Defined String Functions')
    # process some example strings
    process('CREATING is better than LEARNING')
    process('indeed it\'s the Essence of Life!')