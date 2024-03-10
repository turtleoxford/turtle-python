from turtle_oxford import *
from random import randint
from math import sqrt
import heapq

WIDTH = 1000
LENGTH = 1000
N = 7

open = []

def push(element: list[int]):
    open.append(element)
    position = len(open)-1
    while open[position][0] < open[(position-1)//2][0]:
        x = open[(position-1)//2]
        open[(position-1)//2] = open[position]
        open[position] = x
        position = (position - 1) // 2

def pop() -> list[int]:
    root = open[0]
    open[0] = open[len(open) - 1]
    open = open.pop()
    position = 0
    l = len(open)
    while (position * 2 + 1 < l and open[position][0] > open[position * 2 + 1][0]) or (
        position * 2 + 2 < l and open[position][0] > open[position * 2 + 2][0]):
        smallestchild = position * 2 + 1
        if (position * 2 + 2 < l and open[position * 2 + 2][0] < open[smallestchild][0]):
            smallestchild = position * 2 + 2
        
        # swap current node with its smallest child 
        x = open[position]
        open[position] = open[smallestchild]
        open[smallestchild] = x 

        position = smallestchild
    return root

    

def draw_nodes() -> list[tuple[int]]:
    coords = []
    colour("black")
    for i in range(N):
        x = randint(10, WIDTH - 10)
        y = randint(10, LENGTH - 10)
        setxy(x, y)
        blot(5)
        setxy(x + 7, y)
        display(chr(ord('A') + i))
        coords.append((x, y))
    return coords

def distance(c1: tuple[int], c2: tuple[int]):
    return int(sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2))

def draw_edges(coords: list[tuple[int]]) -> list[tuple[int]]:
    MAX = maxint()
    distances = [[MAX for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            if randint(0, 1):
                continue
            weight = distance(coords[i], coords[j])
            distances[i][j] = weight
            distances[j][i] = weight
            (x, y) = coords[i]
            setxy(x, y)
            xdist = coords[j][0] - x
            ydist = coords[j][1] - y
            drawxy(xdist, ydist)
            setxy(x + xdist / 2, y + ydist/ 2)
            display(str(weight))
    return distances

def reconstruct_path(parents, source, destination):
    if source == destination:
        return [source]
    return reconstruct_path(parents, source, parents[destination]) + [destination]


def astar(source: str, destination: str, coords: list[tuple[int]], distances: list[tuple[int]]):
    open = []
    scores = [maxint()] * N
    scores[source] = 0
    parents = list(range(N))
    node = source
    push([0, source])
    while node != destination and open:
        l = pop()
        score = l[0]
        node = l[1]
        setxy(*coords[node])
        colour("blue")
        blot(5)
        if score != scores[node]:
            continue
        for n in range(0, N):
            if distances[node][n] != maxint() and distances[node][n] + score < scores[n]:
                setxy(*coords[n])
                colour("red")
                blot(5)
                scores[n] = distances[node][n] + score
                push([scores[n], n])
                parents[n] = node


    if node == destination:
        print("Path found")
        path = reconstruct_path(parents, source, destination)
        print(f"{[chr(ord('A') + i) for i in path]}")
        for i in range(1, len(path)):
            setxy(*coords[path[i-1]])
            xdist = coords[path[i]][0] - coords[path[i-1]][0]
            ydist = coords[path[i]][1] - coords[path[i-1]][1]
            thickness(4)
            colour("green")
            drawxy(xdist, ydist)
        

with turtle_canvas(0, 0, WIDTH, LENGTH) as t:
    coords = draw_nodes()
    print(coords)
    distances = draw_edges(coords)
    source = input("Please enter a source point:")
    destination = input("Please enter a destination point:")
    try :
        source = ord(source) - ord('A')
        destination = ord(destination) - ord('A')
    except TypeError:
        print("Source or destination point invalid")
        halt()
    astar(source, destination, coords, distances)
