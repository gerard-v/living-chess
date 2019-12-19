import sys
from string import digits
from random import choice

class square:
  def __init__(self):
    self.piece = None
    self.name = ""
    self.neighbours = {}

  def __str__(self):
    if self.getPiece():
      return str(self.piece)
    else:
      return '.'


  def getPiece(self):
    return self.piece

  def setKing(self, king):
    self.piece = king

  def containsPiece(self):
    return False;

class king:
  def __init__(self, color, square):
    assert color in ['black', 'white']
    self.color = color
    self.square = square

  def __str__(self):
    if (self.color=='white'):
      return 'K'
    else:
      return 'k'

  def wakeUp(self):
    print("The %s king wakes up" %self.color);
    print(self.square.name)
    print(self.square.neighbours)
    
    # feel/listen: sense what squares are a no-go
    options = []
    for i in self.square.neighbours:
      options.append(self.square.neighbours[i])
      #print(i,self.square.neighbours[i].name)
    
    # make a move
    print(options)
    r = choice(options)
    print(r.name)

class chessboard:
  # Squares
  #board = [[square()]*8 for i in range(8)]
  
  # only the white king: '8/8/8/8/8/8/8/4K3 w - - 0 1' (with quotes)
  def __init__(self, fen='8/8/8/8/8/8/8/4K3 w - - 0 1'): # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    self.squares = [[square() for i in range(8)] for j in range(8)]
    for i in range(8):
      for j in range(8):
        self.squares[i][j].name = "abcdefgh"[i]+"12345678"[j]
    
    for i in range(8):
      for j in range(7):
        self.squares[i][j].neighbours["N"] = self.squares[i][j+1]
    
    for i in range(7):
      for j in range(8):
        self.squares[i][j].neighbours["E"] = self.squares[i+1][j]
    
    for i in range(8):
      for j in range(1,8):
        self.squares[i][j].neighbours["S"] = self.squares[i][j-1]

    for i in range(1,8):
      for j in range(8):
        self.squares[i][j].neighbours["W"] = self.squares[i-1][j]
    
    for i in range(7):
      for j in range(7):
        self.squares[i][j].neighbours["NE"] = self.squares[i+1][j+1]
    
    for i in range(7):
      for j in range(1,8):
        self.squares[i][j].neighbours["SE"] = self.squares[i+1][j-1]
    
    for i in range(1,8):
      for j in range(1,8):
        self.squares[i][j].neighbours["SW"] = self.squares[i-1][j-1]
    
    for i in range(1,8):
      for j in range(7):
        self.squares[i][j].neighbours["NW"] = self.squares[i-1][j+1]
    
    
    self.whitePieces = []
    print(fen);
    # Split FEN record into fields
    fields = fen.split(' ')
    # Set color of player to move
    self.color = fields[1]
    # Setup position
    lines = fields[0].split('/')
    for j in range(8):
      x = 0
      for i in lines[7-j]:
        print(i)
        if i in digits:
          x += int(i)
        else:
          #self.board[j][x] = i
          if i=='K':
            print('i==K') # debug
            self.squares[x][j].setKing(king('white', self.squares[x][j])) # bind the King to the square
            self.whitePieces.append(self.squares[x][j].getPiece()) # add white king to collection of white pieces
          x += 1

  #  self.whitePieces = []
  #  for line in self.board:
  #    for i in line:
  #      if str(i) in ['RNBQKBNR']:
  #        self.whitePieces.append(i)


  def dayBreak(self):
    for p in self.whitePieces:
      p.wakeUp()

  def nightFall(self):
    pass

  def print(self):
    print()
    for rank in range(7,-1,-1): # from 7 to 0, to print top rank first
      for file in self.squares:
        print(file[rank], end=' ')
      print()
    print()

  def getAccessibleSquares(self, piece):
    squares = []
    if (piece.x > 1):
      squares.append((piece.x-1, piece.y))
    return squares

  def move(self, origin, destination):
    self.board[destination[0]][destination[1]] = self.board[origin[0]][origin[1]]
    self.board[origin[0]][origin[1]] = '.'

if len(sys.argv)>1:
  board = chessboard(sys.argv[1]) # e.g. '4k3/8/8/8/8/8/8/4K3 w - - 0 1' (kings only)
else:
  board = chessboard()
board.print()

while True :
  input("Press enter to continue day/night cycle.");

  if board.color == 'w':
    print("White to move")
    board.dayBreak()
  else:
    print("Black to move")
    board.nightFall()

  #origin = input("Move from: ")
  #origin = ('87654321'.index(origin[1]),'abcdefgh'.index(origin[0]))
  #destination = input("Move to: ")
  #destination = ('87654321'.index(destination[1]),'abcdefgh'.index(destination[0]))

  #board.move(origin,destination)
  board.print()
  for piece in board.whitePieces:
    print(piece)
  #print(board.whitePieces)
  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'


