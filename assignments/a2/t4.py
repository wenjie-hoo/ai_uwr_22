from random import choice
from collections import deque

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def solve_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                commando = [i, j]
                break

    target_points = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'G':
                target_points.append((i, j))
    paths = []
    for target in target_points:
        path = (maze, [target])
        paths.append(path)
        commando[0], commando[1] = target
    for path in paths:
        for move in path:
            print(move, end='')

maze = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', ' ', '#', 'G', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#'],
]
