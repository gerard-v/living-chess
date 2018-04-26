class chessboard:
  # Squares
  b = [['. ']*8 for i in range(8)]

  def __init__(self):
    # Add the pieces
    lineUp = "RNBQKBNR"
    self.b[0] = [x+'b' for x in lineUp]
    self.b[1] = ['Pb']*8
    self.b[6] = ['Pw']*8
    self.b[7] = [x+'w' for x in lineUp]

  def print(self):
    print()
    for i in range(8):
      for j in range(8):
        print(self.b[i][j], end=' ')
      print()
    print()

  def move(self, origin, destination):
    self.b[destination[0]][destination[1]] = self.b[origin[0]][origin[1]]
    self.b[origin[0]][origin[1]] = '. '

board = chessboard()
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





