import sys
from string import digits

class chessboard:
  # Squares
  board = [['.']*8 for i in range(8)]

  def __init__(self, setup='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
    # Add the pieces
    lines = setup.split('/')
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
  board = chessboard(sys.argv[1])
else:
  board = chessboard() # 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
board.print()
color = 'w'
print("White to move")

while True :
  origin = input("Move from: ")
  origin = ('87654321'.index(origin[1]),'abcdefgh'.index(origin[0]))
  destination = input("Move to: ")
  destination = ('87654321'.index(destination[1]),'abcdefgh'.index(destination[0]))

  board.move(origin,destination)
  board.print()
  # Switch between black and white
  if color == 'b':
    color = 'w'
    print("White to move")
  else:
    color = 'b'
    print("Black to move")





