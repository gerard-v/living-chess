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
      print(oldPiece.color + ' ' + type(oldPiece).__name__ + ' on ' + self.name + ' captured')
    self.piece = piece

  def exploreRange(self, piece):
    if isinstance(piece, King):
      options = []
      for d in self.neighbours:
        if len(d) < 3:
          options.append(self.neighbours[d])
      return options
    if isinstance(piece, Queen):
      options = []
      for d in self.neighbours:
        if len(d) < 3:
          options.append(self.neighbours[d])
      return options
    if isinstance(piece, Knight):
      options = []
      for d in self.neighbours:
        if len(d) == 3:
          options.append(self.neighbours[d])
      return options
    if isinstance(piece, Bishop):
      options = []
      for d in self.neighbours:
        if len(d) == 2:
          options.append(self.neighbours[d])
      return options
    if isinstance(piece, Rook):
      options = []
      for d in self.neighbours:
        if len(d) == 1:
          options.append(self.neighbours[d])
      return options

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
    #print("The", self.color, type(self).__name__, "wakes up");
    # feel/listen: sense what squares are a no-go
    options = self.square.exploreRange(self)
    
    r = [o for o in options if o.piece and o.piece.color != self.color]
    if r:
      return [2,self,choice(r)]
    else:
      r = [o for o in options if not o.piece or o.piece.color != self.color]
      if r:
        return [1,self,choice(r)]
      else:
        return [0,self,None]

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
      
class Queen(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'Q'
    else:
      return 'q'

class Knight(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'N'
    else:
      return 'n'

class Bishop(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'B'
    else:
      return 'b'

class Rook(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if (self.color=='white'):
      return 'R'
    else:
      return 'r'


class Chessboard:
  pieces = {'k': King, 'q': Queen, 'n': Knight, 'b': Bishop, 'r': Rook}
  # These directions are used to connect the squares
  directions = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
  
  # only the white king: '8/8/8/8/8/8/8/4K3 w - - 0 1' (with quotes)
  # Standard chess setup: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
  def __init__(self, fen='rbnqknbr/8/8/8/8/8/8/RBNQKNBR w - - 0 1'):
    
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
          assert c.lower() in self.pieces, "Unknown piece: '" + c + "'"
          
          if c.isupper():
            color = 'white'
          else:
            color = 'black'
            
          self.squares[i][j].setPiece(self.pieces[c.lower()](color, self.squares[i][j]))
          
          if color == 'white':
            self.whitePieces.append(self.squares[i][j].getPiece())
          else:
            self.blackPieces.append(self.squares[i][j].getPiece())
          
          j += 1


  def dayBreak(self):
    biddings = []
    for p in self.whitePieces:
      biddings.append(p.wakeUp())
    return biddings

  def nightFall(self):
    biddings = []
    for p in self.blackPieces:
      biddings.append(p.wakeUp())
    return biddings
  
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
  print(biddings)
  best = -1
  bestIndex = None
  for i in range(len(biddings)):
    if biddings[i][0] > best:
      best = biddings[i][0]
      bestIndex = i
  print (biddings[bestIndex])
  
  biddings[bestIndex][1].moveTo(biddings[bestIndex][2])
  
  #print(str(self).upper()+str(self.square.name)+"-"+destination.name)
  #self.moveTo(destination)


  board.print()
  # Switch between black and white
  if board.color == 'b':
    board.color = 'w'
  else:
    board.color = 'b'


