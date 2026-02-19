import random
from modules import variables as var

#code de https://inventwithpython.com/recursion/chapter11.html

WIDTH = 21  # Width of the maze (must be odd).
HEIGHT = 17  # Height of the maze (must be odd).
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

# Use these characters for displaying the maze:
EMPTY = ' '
WALL = chr(9608)  # █
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'


def generate_maze(posx, posy):
  # Create the maze filled with walls
  maze = []
  for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
      row.append(WALL)
    maze.append(row)

  def printMaze(maze):
    for y in range(HEIGHT):
      for x in range(WIDTH):
        print(maze[y][x], end='')
      print()

  def visit(x, y):

    maze[y][x] = EMPTY

    while True:
      unvisitedNeighbors = []

      if y > 1 and (x, y - 2) not in hasVisited:
        unvisitedNeighbors.append(NORTH)
      if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
        unvisitedNeighbors.append(SOUTH)
      if x > 1 and (x - 2, y) not in hasVisited:
        unvisitedNeighbors.append(WEST)
      if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
        unvisitedNeighbors.append(EAST)

      if not unvisitedNeighbors:
        return

      direction = random.choice(unvisitedNeighbors)

      if direction == NORTH:
        maze[y - 1][x] = EMPTY
        nextX, nextY = x, y - 2

      elif direction == SOUTH:
        maze[y + 1][x] = EMPTY
        nextX, nextY = x, y + 2

      elif direction == WEST:
        maze[y][x - 1] = EMPTY
        nextX, nextY = x - 2, y

      elif direction == EAST:
        maze[y][x + 1] = EMPTY
        nextX, nextY = x + 2, y

      hasVisited.append((nextX, nextY))
      visit(nextX, nextY)

  hasVisited = [(1, 1)]
  visit(1, 1)
  maze[HEIGHT - 1][1] = EMPTY

  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i][j] == WALL:
        var.game_map[posy + i][posx + j] = 77
      else:
        var.game_map[posy + i][posx + j] = random.randint(1, 16)
  var.game_map[posy + 1][posx + 1] = 28
  var.game_map[posy + HEIGHT - 1][posx + 1] = 25
