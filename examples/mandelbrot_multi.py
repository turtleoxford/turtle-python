from turtle_oxford import *
from time import time

# STARTPROMPT offers the user either to display the entire Mandelbrot set or to
# zoom in on a small "lake" within it, with three possible speeds/resolutions 
def startprompt():
    global xcentre,ycentre
    global scale,pixels
    print("MANDELBROT SET DISPLAY PROGRAM")
    print()
    print('Select Whole set, or Zoom on mini "lake" at -0.1592,-1.0330 (W/Z)', end="")
    det = ""
    while (det!="w") and (det!="z"):
        det=input()
    if det=="w":
        xcentre=-500000
        ycentre=0
    else:
        xcentre=-159200
        ycentre=-1033000
    if ycentre==0:
        print("Select Fast/Medium/Slow, giving resolution 300/750/1500: (F/M/S) ", end="")
    else:
        print("Select Fast/Medium/Slow, giving resolution 300/600/1200: (F/M/S) ", end="")
    while (det!="f") and (det!="m") and (det!="s"):
        det=input()
    print(det)
    if ycentre==0:
        if det=="f":
            scale=100
        elif det=="m":
            scale=250
        else:
            scale=500
        pixels=scale*3
    else:
        if det=="f":
            scale=10000
        elif det=="m":
            scale=20000
        else:
            scale=40000
        pixels=scale//100*3

# This version allows up to 40 iterations to test how quickly points in the plane "diverge"
maxcol = 40 # each iteration is represented by a different colour, so 40 colours altogether
colmult = 0xffffff // 40
startprompt()
xstart = int(xcentre / 1000000 * scale) - pixels // 2 # DIVMULT provides optimal integer arithmetic,
ystart = int(ycentre / 1000000 * scale) - pixels // 2 # avoiding intermediate rounding errors
xfinish = xstart + pixels
yfinish = ystart + pixels
print("Mandelbrot will be plotted over the following real range:")
print(str(xstart / scale)+" < x < "+str(xfinish / scale), end="    ")
print(str(ystart / scale)+" < y < "+str(yfinish / scale))
print("Scaling factor: "+str(scale)+"    Image resolution: "+str(pixels)+'x'+str(pixels))

with turtle_canvas(xstart, ystart, pixels, pixels) as t:
    resolution(pixels, pixels)           # Resolution depends on the speed chosen
    t = time()
    for a in range(xstart, xfinish):
        noupdate()
        for b in range(ystart, yfinish):   # Count through points (a,b) in the region ...
            x = a                             # Generate series of points (x,y) starting from (a,b)
            y = b
            iterations = 0                    # Count iterations up to MAXCOL
            while (math.hypot(x,y)<2*scale) and (iterations<=maxcol):  # Series diverges if distance of
                temp = (x+y) / scale * (x-y)                           # (x,y) from origin reaches 2
                y = (2*x) / scale * y + b
                x = temp + a                      # Otherwise, calculate next point (x,y) in series
                iterations += 1
            if iterations > maxcol:           # If series hasn't diverged after MAXCOL, point, then
                pixset(a,b,"black")             # (a,b) - the starting point - is coloured black
            else:
                pixset(a,b,iterations*colmult) # Otherwise, it's colour shows how quickly it diverged
        update()
    print("Time taken: " + str(time() - t) + " seconds.")