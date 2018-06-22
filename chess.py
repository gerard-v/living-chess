import sys
from string import digits

class chessboard:
  # Squares
  board = [['.']*8 for i in range(8)]

  def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    # Split FEN record into fields
    fields = fen.split(' ')
    # Set color of player to move
    self.color = fields[1]
    # Setup position
    lines = fields[0].split('/')
    for i in range(8):
      x = 0
      for j in lines[i]:
        if j in digits:
          x += int(j)
        else:
          self.board[i][x] = j
          x += 1

  def print(self):
    print()
    for rank in self.board:
      for square in rank:
        print(square, end=' ')
      print()
    print()

  def move(self, origin, destination):
    self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
    self.board[origin[0]][origin[1]] = '.'

if len(sys.argv)>1:
  board = chessboard(sys.argv[1]) # e.g. '4k3/8/8/8/8/8/8/4K3 w - - 0 1' (kings only)
else:
  board = chessboard()
board.print()

while True :
  if board.color == 'w':
    print("White to move")
  else:
    print("Black to move")

  origin = input("Move from: ")
  origin = ('87654321'.index(origin[1]),'abcdefgh'.index(origin[0]))
  destination = input("Move to: ")
  destination = ('87654321'.index(destination[1]),'abcdefgh'.index(destination[0]))

  board.move(origin,destination)
  board.print()
  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'


