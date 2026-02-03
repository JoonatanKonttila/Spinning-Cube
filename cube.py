# classic spinning cube by AJK
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-

import math as m
import time as t

# Play around with to customise size and perspective :)
width = 40
height = 20
fov = 150
distance = 25

buffer = [[' ' for x in range(width)] for y in range(height)]

verts = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
]

def rot_x(point, angle):
    x, y, z = point
    new_y = y * m.cos(angle) - z * m.sin(angle)
    new_z = y * m.sin(angle) + z * m.cos(angle)
    return [x, new_y, new_z]

def rot_y(point, angle):
    x, y, z = point
    new_x = x * m.cos(angle) + z * m.sin(angle)
    new_z = -x * m.sin(angle) + z * m.cos(angle)
    return [new_x, y, new_z]

def rot_z(point, angle):
    x, y, z = point
    new_x = x * m.cos(angle) - y * m.sin(angle)
    new_y = x * m.sin(angle) + y * m.cos(angle)
    return [new_x, new_y, z]


def TwoDeeProject(point, width, height, fov, distance):
    x, y, z = point

    # perspective
    factor = fov / (distance + z)

    # 2d
    screen_x = x * factor + width / 2
    screen_y = -y * factor + height / 2

    return [int(screen_x), int(screen_y)]

def drawLines(start, end, buffer, char='<'): # change the character the cube consists of-
    x1, y1 = start
    x2, y2 = end

    # calculate the diff
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    # no dividing by zero please
    if steps == 0:
        if 0 <= x1 < len(buffer[0]) and 0 <= y1 < len(buffer):
            buffer[y1][x1] = char
        return
    
    # calculate the increment for steps
    x_incre = dx / steps
    y_incre = dy /steps

    # draw the line
    x, y = x1, y1
    for i in range(steps + 1):
        # rounding
        px = int(round(x))
        py = int(round(y))

        # check bounds befcore draw
        if 0 <= px < len(buffer[0]) and 0 <= py < len(buffer):
            buffer[py][px] = char
        
        # new pos
        x += x_incre
        y += y_incre

# initial rot angle
angle_x = 0
angle_y = 0
angle_z = 0

# anim loop
try:
    while True:
        # clears screen and moves cursor to top left, ANSI [\033[2J] for screen clear and [\033[H] to move cursor--
        print('\033[2J\033[H')

        # reset buffer
        buffer = [[' ' for x in range(width)] for y in range(height)]

        # inc rot angles
        angle_x += 0.05
        angle_y += 0.05
        angle_z += 0.02

        # rot and project all verts
        projected_verts = []
        for vert in verts:
            # apply rots
            rotated = rot_x(vert, angle_x)
            rotated = rot_y(rotated, angle_y)
            rotated = rot_z(rotated, angle_z)

            # proj to 2d
            projected = TwoDeeProject(rotated, width, height, fov, distance)
            projected_verts.append(projected)

        # draw all edges
        for edge in edges:
            start = projected_verts[edge[0]]
            end = projected_verts[edge[1]]
            drawLines(start, end, buffer)

        # print buffer
        for row in buffer:
            print(''.join(row))

        # small pause
        t.sleep(0.03)
except KeyboardInterrupt:
    print("\nAnimation interrupted")