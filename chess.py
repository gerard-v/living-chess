import sys
from stage import *
from players import *

if len(sys.argv)>1:
  board = Chessboard(sys.argv[1]) # e.g. '4k3/8/8/8/8/8/8/4K3 w - - 0 1' (kings only)
else:
  board = Chessboard()
board.print()

while True :

  if not board.blackPieces:
    print("White wins!")
    exit()

  if not board.whitePieces:
    print("Black wins!")
    exit()

  input("Press enter to continue day/night cycle.");
  print("")

  if board.color == 'w':
    print("White to move")
    biddings = board.dayBreak()

  else:
    print("Black to move")
    biddings = board.nightFall()

  # Honor the best bid
  #print(biddings)
  best = -1
  bestIndex = None
  results = []
  for i in range(len(biddings)):
    if biddings[i][0] == best:
      results.append(i)

    if biddings[i][0] > best:
      results = [i]
      best = biddings[i][0]

  # In case of a tie, pick a random bid out of the results
  bestIndex = choice(results)
  # Let the chess piece move
  try:
    biddings[bestIndex][1].moveTo(biddings[bestIndex][2])
  except AttributeError:
    print("Stalemate")

  board.print()
  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'


