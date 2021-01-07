from players import *


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
      if oldPiece.color == 'white':
        self.board.whitePieces.remove(oldPiece)
      if oldPiece.color == 'black':
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
    if isinstance(piece, Pawn):
      options = []
      if piece.color == 'white':
        if "N" in self.neighbours and not self.neighbours["N"].piece:
          options.append(self.neighbours["N"])
        elif "NE" in self.neighbours and self.neighbours["NE"].piece:
          options.append(self.neighbours["NE"])
        elif "NW" in self.neighbours and self.neighbours["NW"].piece:
          options.append(self.neighbours["NW"])
      else: # black
        if "S" in self.neighbours and not self.neighbours["S"].piece:
          options.append(self.neighbours["S"])
        elif "SE" in self.neighbours and self.neighbours["SE"].piece:
          options.append(self.neighbours["SE"])
        elif "SW" in self.neighbours and self.neighbours["SW"].piece:
          options.append(self.neighbours["SW"])
      return options

class Chessboard:
  pieces = {'k': King, 'q': Queen, 'n': Knight, 'b': Bishop, 'r': Rook, 'p': Pawn}
  # These directions are used to connect the squares
  directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

  # only the white king: '8/8/8/8/8/8/8/4K3 w - - 0 1' (with quotes)
  # Standard chess setup: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
  def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1'):

    self.squares = [[Square("abcdefgh"[j] + "12345678"[i], self) for j in range(8)] for i in range(8)]
    for i in range(8):
      for j in range(8):
        for d in self.directions:
          deltai = d.count("N") - d.count("S")
          deltaj = d.count("E") - d.count("W")
          if 0 <= i + deltai < 8 and 0 <= j + deltaj < 8:
            self.squares[i][j].neighbours[d] = self.squares[i + deltai][j + deltaj]

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
      for c in lines[7 - i]:
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
      for square in self.squares[7 - rank]:  # from 7 to 0, to print top rank first
        print(square, end=' ')
      print()
    print()

  def getAccessibleSquares(self, piece):
    squares = []
    if (piece.x > 1):
      squares.append((piece.x - 1, piece.y))
    return squares
