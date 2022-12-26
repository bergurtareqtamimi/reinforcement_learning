# game environment influenced by Shaun Halverson
import random
from mcts import monte_carlo_tree_search

print("Welcome to Connect Four")
print("-----------------------")

possibleLetters = ["A","B","C","D","E","F","G"]
gameBoard = [["","","","","","",""], ["","","","","","",""], ["","","","","","",""], ["","","","","","",""], ["","","","","","",""], ["","","","","","",""]]

rows = 6
cols = 7

def printGameBoard():
  print("\n     A    B    C    D    E    F    G  ", end="")
  for x in range(rows):
    print("\n   +----+----+----+----+----+----+----+")
    print(x, " |", end="")
    for y in range(cols):
      if(gameBoard[x][y] == "🔵"):
        print("",gameBoard[x][y], end=" |")
      elif(gameBoard[x][y] == "🔴"):
        print("", gameBoard[x][y], end=" |")
      else:
        print(" ", gameBoard[x][y], end="  |")
  print("\n   +----+----+----+----+----+----+----+")

def checkForWinner(chip):
  ### Check horizontal spaces
  for y in range(rows):
    for x in range(cols - 3):
      if gameBoard[y][x] == chip and gameBoard[y][x+1] == chip and gameBoard[y][x+2] == chip and gameBoard[y][x+3] == chip:
        print("\nGame over", chip, "wins! Thank you for playing :)")
        return True

  ### Check vertical spaces
  for y in range(rows-3):
    for x in range(cols):
      if gameBoard[y][x] == chip and gameBoard[y+1][x] == chip and gameBoard[y+2][x] == chip and gameBoard[y+3][x] == chip:
        print("\nGame over", chip, "wins! Thank you for playing :)")
        return True

  ### Check upper right to bottom left diagonal spaces
  for x in range(rows - 3):
    for y in range(3, cols):
      if gameBoard[x][y] == chip and gameBoard[x+1][y-1] == chip and gameBoard[x+2][y-2] == chip and gameBoard[x+3][y-3] == chip:
        print("\nGame over", chip, "wins! Thank you for playing :)")
        return True

  ### Check upper left to bottom right diagonal spaces
  for x in range(rows - 3):
    for y in range(cols - 3):
      if gameBoard[x][y] == chip and gameBoard[x+1][y+1] == chip and gameBoard[x+2][y+2] == chip and gameBoard[x+3][y+3] == chip:
        print("\nGame over", chip, "wins! Thank you for playing :)")
        return True
  return False

def coordinateParser(inputString:str) -> int:
  if(inputString.lower() == "a"):
    return 0
  elif(inputString.lower() == "b"):
    return 1
  elif(inputString.lower() == "c"):
    return 2
  elif(inputString.lower() == "d"):
    return 3
  elif(inputString.lower() == "e"):
    return 4
  elif(inputString.lower() == "f"):
    return 5
  elif(inputString.lower() == "g"):
    return 6
  else:
    print("Invalid")
    return -1


def isSpaceAvailable(column: int):
  if gameBoard[0][column] == "": return True
  return False

def do_move(move: int, piece: str) -> None:
    for current_row in range(rows - 1, -1, -1):
        if gameBoard[current_row][move] == "":
            gameBoard[current_row][move] = piece
            return



##########################################################

leaveLoop = False
player_color = input("blue (b) or read(r)?: ")
turnCounter = 0 if  player_color == "b" else 1
while(leaveLoop == False):
  if(turnCounter % 2 == 0):
    printGameBoard()
    while True:
      spacePicked = input("\nChoose a space: ")
      print(spacePicked)
      coordinate = coordinateParser(spacePicked)
      try:
        ### Check if the space is available
        if(isSpaceAvailable(coordinate)):
          do_move(coordinate, '🔵' if player_color == "b" else '🔴')
          break
        else:
          print("Not a valid coordinate")
      except:
        print("Error occured. Please try again.")
    winner = checkForWinner('🔵' if player_color == "b" else '🔴')
    turnCounter += 1
  ### It's the computers turn
  else:
    while True:
      mcts = monte_carlo_tree_search(gameBoard, '🔴' if player_color == "b" else '🔵')
      mcts.run(2000)
      cpuCoordinate = mcts.pick_move()
      if(isSpaceAvailable(cpuCoordinate)):
        do_move(cpuCoordinate, '🔴' if player_color == "b" else '🔵')
        break
    turnCounter += 1
    winner = checkForWinner('🔴' if player_color == "b" else '🔵')

  if(winner):
    printGameBoard()
    break






