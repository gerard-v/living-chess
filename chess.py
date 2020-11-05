import sys
from string import digits
from random import choice

class Square:
  def __init__(self, name, board):
    self.piece = None
    self.name = name
    self.neighbours = {}
    self.board = board

  def __str__(self):
    if self.piece:
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
    oldPiece = self.getPiece()
    if oldPiece:
      if oldPiece.color=='white':
        self.board.whitePieces.remove(oldPiece)
      if oldPiece.color=='black':
        self.board.blackPieces.remove(oldPiece)
      print('piece captured, color: ' + oldPiece.color)
    self.piece = piece

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
    # Roll-call
    print("The", self.color, type(self).__name__, "wakes up");
    # feel/listen: sense what squares are a no-go
    options = self.getOptions()
    
    r = choice([o for o in options if not o.piece or o.piece.color != self.color])
    print(str(self).upper()+str(self.square.name)+"-"+r.name)
    self.moveTo(r)

class King(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.options = []

  def __str__(self):
    if (self.color=='white'):
      return 'K'
    else:
      return 'k'

  def announcePresence(self):
    pass
    
  def getOptions(self):
    self.options = []
    for d in self.square.neighbours:
      if len(d) < 3:
        self.options.append(self.square.neighbours[d])
    return self.options
      
class Queen(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'Q'
    else:
      return 'q'

  def getOptions(self):
    self.options = []
    for d in self.square.neighbours:
      if len(d) < 3:
        self.options.append(self.square.neighbours[d])
    return self.options

class Chessboard:
  pieces = {'k': King, 'q': Queen}
  # These directions are used to connect the squares
  directions = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

  # Squares
  #board = [[Square()]*8 for i in range(8)]
  
  # only the white king: '8/8/8/8/8/8/8/4K3 w - - 0 1' (with quotes)
  # Standard chess setup: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
  def __init__(self, fen='3qk3/8/8/8/8/8/8/3QK3 w - - 0 1'):
    
    self.squares = [[Square("abcdefgh"[j]+"12345678"[i], self) for j in range(8)] for i in range(8)]
    for i in range(8):
      for j in range(8):
        for d in self.directions:
          deltai = d.count("N") - d.count("S")
          deltaj = d.count("E") - d.count("W")
          if 0<=i+deltai<8 and 0<=j+deltaj<8:
            self.squares[i][j].neighbours[d] = self.squares[i+deltai][j+deltaj]
    
    self.whitePieces = []
    self.blackPieces = []

    # Split FEN record into fields
    fields = fen.split(' ')
    # Set color of player to move
    self.color = fields[1]
    # Setup position
    lines = fields[0].split('/')
    for i in range(8):
      j = 0
      for c in lines[7-i]:
        if c in digits:
          j += int(c)
        else:
          
          if c=='K':
            self.squares[i][j].setPiece(King('white', self.squares[i][j])) # bind the King to the square
            
          if c=='k':
            self.squares[i][j].setPiece(King('black', self.squares[i][j])) # bind the King to the square
            
          if c=='Q':
            self.squares[i][j].setPiece(Queen('white', self.squares[i][j])) # bind the Queen to the square

          if c=='q':
            self.squares[i][j].setPiece(Queen('black', self.squares[i][j])) # bind the Queen to the square

          j += 1

    # Assign the white and black pieces to their respective armies
    for i in range(2): # idee: getPiece().getColor() gebruiken, zodat we slechts één for-loop nodig hebben voor alle stukken
      j = 0
      for c in lines[7-i]:
        if c in digits:
          j += int(c)
        else:
          self.whitePieces.append(self.squares[i][j].getPiece())
          j += 1

    for i in range(0,2):
      j = 0
      for c in lines[7-i]:
        if c in digits:
          j += int(c)
        else:
          self.blackPieces.append(self.squares[7-i][j].getPiece())
          j += 1


  def dayBreak(self):
    #for p in self.whitePieces: # TODO: pieces should compete for who is to move
      choice(self.whitePieces).wakeUp()

  def nightFall(self):
    #for p in self.blackPieces: # TODO: pieces should compete for who is to move
      choice(self.blackPieces).wakeUp()

  def print(self):
    print()
    for rank in range(8):
      for square in self.squares[7-rank]: # from 7 to 0, to print top rank first
        print(square, end=' ')
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


