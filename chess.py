import sys
from getopt import getopt
from stage import *
from players import *

# Process command line arguments
(opts, fen) = getopt(sys.argv[1:],'u:')

for o in opts:
  if o[0] == '-u':
    if 'w' in o[1]:
      whitePieces.possess()
      print("User plays white.")
    if 'b' in o[1]:
      blackPieces.possess()
      print("User plays black.")

if fen:
  print("starting position:","'"+fen[0]+"'")
  board = Chessboard(fen[0]) # e.g. '4k3/8/8/8/8/8/8/4K3 w - - 0 1' (kings only)
else:
  board = Chessboard()

whiteScore = 0
blackScore = 0

# Main game loop
while True:
  # Emit vibrations by both armies
  board.clearVibrations()
  board.emitVibrations()
  board.print()

  if whitePieces.playMode == 'computer' and blackPieces.playMode == 'computer':
    input("Press enter to continue day/night cycle.")
    print("")

  if board.color == 'w':
    # Daybreak
    print("White to move")
    move = whitePieces.wakeUp()
  else:
    # Nightfall
    print("Black to move")
    move = blackPieces.wakeUp()

  # Let the chess piece move
  try:
    #board.status()
    captureScore = move[1].moveTo(move[2])
    print(captureScore)

    if board.color == 'w':
      whiteScore += captureScore
    else:
      blackScore += captureScore

    print("White score: " + str(whiteScore))
    print("Black score: " + str(blackScore))

  except AttributeError:
    print("Stalemate")
    exit()

  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'
  # Alternative formulations:
  # board.color = 'w' if board.color = 'b' else 'b'
  # board.color = 'bw'['bw'.index(board.color)-1]


