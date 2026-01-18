import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    methods=4  # sorting methods to be compared
    n=100      # items to be sorted
    cols=10    # columns for display
    trials=10  # number of trials (for averaging)
    check=True # whether to check for correct sorting
    A=[0]*(n)  # integer list to be sorted - initially all zeros
    caption=['Bubblesort:','Selectionsort:','Insertionsort:','Quicksort:']
    comptotal=[0]*methods # list to count comparisons per method
    swaptotal=[0]*methods # list to count swaps per method
    comps=0    # comparison counter
    swaps=0    # swap counter

    # Tests whether x<y, and increments comparison count
    def lessthan(x,y):
        global comps
        comps+=1
        return (x<y)

    # Swaps A[x] and A[y], and increments swap count
    def swap(x,y):
        global A,swaps
        swaps+=1
        t=A[x]
        A[x]=A[y]
        A[y]=t

    # Tests whether the A list is fully ordered
    def ordered():
        for i in range(n-1):
            if A[i]>A[i+1]:
                return False
        return True

    # Displays entire A list in columns
    def listthem():
        print('    ', end='')
        for i in range(n):
            print(pad(str(A[i]),' ',3), end=' ')
            if (i+1)%cols==0:
                print()
                print('    ', end='')
        print()

    # Randomises order of A list
    def randomise():
        global swaps
        for i in range(n):
            j=randrange(n)
            swap(i,j)

    # Performs BUBBLESORT
    def bubblesort():
        changed=True
        # repeat bubble sequence until no change
        while changed:
            changed=False
            for i in range(n-1):
                if lessthan(A[i+1],A[i]):
                    swap(i,i+1)
                    changed=True

    # Performs SELECTIONSORT
    def selectionsort():
        for i in range(n-1):
            # find lowest value between A[i] and A[n-1]
            lowsofar=i
            for j in range(i+1,n):
                if lessthan(A[j],A[lowsofar]):
                    lowsofar=j
            # swap it into position A[i]
            if lowsofar!=i:
                swap(i,lowsofar)

    # Performs INSERTIONSORT
    def insertionsort():
        # extend sorted range upwards, starting from  A[0]..A[1]
        for i in range(1,n):
            # make j=i and swap A[j] down until it's in position
            j=i
            while lessthan(A[j],A[j-1]):
                swap(j-1,j)
                if j>1:
                    j-=1 # if j>1, continue down the list

    # Performs QUICKSORT
    def quicksort():

        # recursively sort list from A[left] to A[right]
        def qsort(left,right):
            # nothing to do unless left<right
            if left<right:
                # M will be sorted position of A[left]
                m=left
                for i in range(left+1,right+1):
                    # if A[i] is less than A[left],
                    if lessthan(A[i],A[left]):
                        # increment M and swap A[i] down
                        m+=1
                        swap(m,i)
                # swap A[left] into its new position
                swap(left,m)
                # sort the left-hand remainder
                qsort(left,m-1)
                # sort the right=hand remainder
                qsort(m+1,right)

        # sort entire list from A[0] to A[n-1]
        qsort(0,n-1)

    # Calls one of the sorting methods
    def sort(method):
        global comps,swaps
        # initialise the comparison and swap counts
        comps=0
        swaps=0
        # call the specified sorting method
        if method==0:
            bubblesort()
        elif method==1:
            selectionsort()
        elif method==2:
            insertionsort()
        else:
            quicksort()
        # neatly display the number of comparisons and swaps required
        print(pad(caption[method],' ',-17)+pad(str(comps),' ',4)+' comparisons', end='')
        print(pad(str(swaps),' ',6)+' swaps')
        # optionally check that the sorting has been successful
        if check:
            if not(ordered()):
                print('     Sort failed:')
                listthem()
                halt()

    # Display the output panel and explanatory text
    print(str(methods)+' sorting methods will be compared, each of them being used to')
    print('sort randomised lists of '+str(n)+' items ('+str(trials)+' times), while keeping')
    print('track of the numbers of comparisons and swaps required.')
    if check:
        print('If sorting fails, the program will halt and show the list.')
    print()

    # initialise the A list (will be randomly ordered before each sort)
    for i in range(n):
        A[i]=i

    # conduct the specified number of trials
    for round in range(trials):
        # test each method in turn
        for m in range(methods):
            # randomise the A list of integers
            randomise()
            # sort the list using the relevant method
            sort(m)
            # keep track of the cumulative totals of comparsions and swaps
            comptotal[m]=comptotal[m]+comps
            swaptotal[m]=swaptotal[m]+swaps
        print()

    # Display the final average results
    print('Averages from sorting '+str(n)+' items, over '+str(trials)+' trials')
    print()
    print('               COMPARISONS    SWAPS')
    for m in range(methods):
        print(pad(caption[m],' ',-17)+pad(qstr(comptotal[m],trials,1),' ',7), end='')
        print(pad(qstr(swaptotal[m],trials,1),' ',11))
    print()
    print('Items sorted were:')
    listthem()