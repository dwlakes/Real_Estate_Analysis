#!/usr/bin/env python3

import sys

VERSION = "0.0.1"
VersionDate = "2023-3-5"

rows = 20
cols = 20
x_pos = rows // 2
y_pos = cols // 2

def print_help():
    print("This program prints out a box depending on how many rows and columns you want.")
    print("Example:")
    print('  "file_name" x/row y/column')
    print("  ./box.py 10 5")
    print("+--------+")
    print("|        |")
    print("|        |")
    print("|        |")
    print("+--------+")

def print_version():
    print(f"{VERSION}")
    print(VersionDate)

def character(char):
    print(x_pos, y_pos)
    print(char)

def rowcol(rows, cols):
    global x_pos, y_pos
    for y in range(rows):
        for x in range(cols):
            if x_pos == x and y_pos == y:
                print("*", end="")
            elif x == 0 and y == 0: # top left
                print("+", end="")
            elif x == 0 and y == rows - 1: # bottom left
                print("+", end="")
            elif x == cols - 1 and y == 0: # top right
                print("+", end="")
            elif x == cols - 1 and y == rows - 1: # bottom right
                print("+", end="")
            elif y == 0 or y == rows - 1:
                print("-", end="")
            elif x == 0 or x == cols - 1:
                print("|", end="")
            else:
                print(" ", end="")
        print()

def move(direction, steps):
    global x_pos, y_pos
    if direction == "u":
        y_pos -= steps
    elif direction == "d":
        y_pos += steps
    elif direction == "l":
        x_pos -= steps
    elif direction == "r":
        x_pos += steps

def main():
    global x_pos, y_pos, rows, cols
    if len(sys.argv) > 1:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
        x_pos = rows // 2
        y_pos = cols // 2
    rowcol(rows, cols)

    while True:
        args = input("Enter command (e.g., 'u1', 'd3', 'l2', 'r4') or 'q' to quit: ").strip().lower()

        if args == 'q':
            print("Exiting...")
            break

        if args in ['-h', '--help']:
            print_help()
            continue

        if args in ['-v', '--version']:
            print_version()
            continue

        if args[0] in ['u', 'd', 'l', 'r'] and args[1:].isdigit():
            direction = args[0]
            steps = int(args[1:])
            move(direction, steps)
            rowcol(rows, cols)
        else:
            print("Invalid command. Please use 'u', 'd', 'l', 'r' followed by a number.")

if __name__ == "__main__":
    main()
