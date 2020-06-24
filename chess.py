import sys
from string import digits
from random import choice

class Square:
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

  def clear(self):
    self.piece = None

  def whoControls(self):
    pass

  def setPiece(self, piece):
    self.piece = piece

  def containsPiece(self):
    if self.piece:
      return True
    else:
      return False

class Piece:
  def __init__(self, color, square):
    assert color in ['black', 'white']
    self.color = color
    self.square = square

  def moveTo(self, square):
    self.square.clear()
    self.square = square
    self.square.setPiece(self)
    
  def wakeUp(self):
    print("The", self.color, type(self).__name__, "wakes up");
    #print(self.square.name)
    #print(self.square.neighbours)
    
    # feel/listen: sense what squares are a no-go
    options = []
    for i in self.square.neighbours:
      # ask who controls the square
      options.append(self.square.neighbours[i])
      #print(i,self.square.neighbours[i].name)
    
    # make a move
    #print(options)
    r = choice(options)
    print("Moving to", r.name)
    self.moveTo(r)

class King(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'K'
    else:
      return 'k'

  def wakeUp(self):
    Piece.wakeUp(self)

  def announcePresence(self):
    pass
    
class Queen(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'Q'
    else:
      return 'q'
  
  def wakeUp(self):
    Piece.wakeUp(self)

class Chessboard:
  pieces = {'k': King, 'q': Queen}
  # Squares
  #board = [[Square()]*8 for i in range(8)]
  
  # only the white king: '8/8/8/8/8/8/8/4K3 w - - 0 1' (with quotes)
  # Standard chess setup: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
  def __init__(self, fen='3qk3/8/8/8/8/8/8/3QK3 w - - 0 1'):
    self.squares = [[Square() for i in range(8)] for j in range(8)]
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
    self.blackPieces = []

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
            self.squares[x][j].setPiece(King('white', self.squares[x][j])) # bind the King to the square
            
          if i=='k':
            print('i==k') # debug
            self.squares[x][j].setPiece(King('black', self.squares[x][j])) # bind the King to the square
            
          if i=='Q':
            print('i==Q') # debug
            self.squares[x][j].setPiece(Queen('white', self.squares[x][j])) # bind the Queen to the square

          if i=='q':
            print('i==q') # debug
            self.squares[x][j].setPiece(Queen('black', self.squares[x][j])) # bind the Queen to the square

          x += 1

    # Assign the white and black pieces to their respective armies
    for j in range(2): # idee: getPiece().getColor() gebruiken, zodat we slechts één for-loop nodig hebben voor alle stukken
      x = 0
      for i in lines[7-j]:
        if i in digits:
          x += int(i)
        else:
          self.whitePieces.append(self.squares[x][j].getPiece())
          x += 1

    for j in range(0,2):
      x = 0
      for i in lines[7-j]:
        if i in digits:
          x += int(i)
        else:
          self.blackPieces.append(self.squares[x][7-j].getPiece())
          x += 1


  def dayBreak(self):
    for p in self.whitePieces:
      p.wakeUp()

  def nightFall(self):
    for p in self.blackPieces:
      p.wakeUp()

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
  board = Chessboard(sys.argv[1]) # e.g. '4k3/8/8/8/8/8/8/4K3 w - - 0 1' (kings only)
else:
  board = Chessboard()
board.print()

while True :
  input("Press enter to continue day/night cycle.");
  print("")

  if board.color == 'w':
    print("White to move")
    board.dayBreak()
  else:
    print("Black to move")
    board.nightFall()

  board.print()
  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'


