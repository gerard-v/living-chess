import sys
from getopt import getopt
from stage import *
from players import *

(opts, fen) = getopt(sys.argv[1:],'u:')
print(opts)
print(fen)

if opts:
  if 'w' in opts[0][1]:
    whitePieces.possess()
  if 'b' in opts[0][1]:
    blackPieces.possess()

if len(sys.argv)>2:
  board = Chessboard(sys.argv[2]) # e.g. '4k3/8/8/8/8/8/8/4K3 w - - 0 1' (kings only)
else:
  board = Chessboard()
board.print()
# board.emitVibrations()

whiteScore = 0
blackScore = 0

while True:

  if whitePieces.playMode == 'computer' and blackPieces.playMode == 'computer':
    input("Press enter to continue day/night cycle.")
    print("")

  board.clearVibrations()
  board.emitVibrations()

  if board.color == 'w':
    print("White to move")
    move = whitePieces.wakeUp()
  else:
    print("Black to move")
    move = blackPieces.wakeUp()

  # Let the chess piece move
  try:
    board.status()
    captureScore = move[1].moveTo(move[2])
    print(captureScore)
    # TODO: detect check

    if board.color == 'w':
      whiteScore += captureScore
    else:
      blackScore += captureScore

    print("White score: " + str(whiteScore))
    print("Black score: " + str(blackScore))

  except AttributeError:
    print("Stalemate")
    exit()

  # Emit vibrations by both armies
  board.clearVibrations()
  board.emitVibrations()
  board.print()
  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'


