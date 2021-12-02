from players import *
from string import digits


class colors:
  BLUE = '\033[94m'
  CYAN = '\033[96m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  ENDC = '\033[0m'


class Square:
  def __init__(self, name, board):
    self.piece = None
    self.active = False
    self.name = name
    self.neighbours = {}
    self.board = board
    self.vibrations = []

  def __str__(self):
    if self.piece:
      return str(self.piece)
    else:
      return '.'

  def getPiece(self):
    return self.piece

  def clear(self):
    self.piece = None

  def setPiece(self, piece):
    oldpiece = self.getPiece()
    if oldpiece:
      if oldpiece.color == 'white':
        whitePieces.removePiece(oldpiece)
      if oldpiece.color == 'black':
        blackPieces.removePiece(oldpiece)
      print(oldpiece.color + ' ' + oldpiece.getName() + ' on ' + self.name + ' captured by a ' + piece.getName())
      if isinstance(oldpiece, King):
        print(piece.color, "wins!")
        exit()
    self.piece = piece
    self.active = True

  def storeVibration(self, piece):
    self.vibrations.append(piece)

  def clearVibrations(self):
    self.vibrations = []

  def isUnderAttack(self, piece):
    for p in self.vibrations:
      if p.color != piece.color:
        return True
    return False

  def propagate(self, direction, piece):
    self.vibrations.append(piece)
    if not self.piece and direction in self.neighbours:
      self.neighbours[direction].propagate(direction, piece)

  def propagateVibrations(self, piece):
    if isinstance(piece, King):
      for d in self.neighbours:
        if len(d) < 3:
          self.neighbours[d].storeVibration(piece)
    if isinstance(piece, Knight):
      for d in self.neighbours:
        if len(d) == 3:
          self.neighbours[d].storeVibration(piece)
    if isinstance(piece, Pawn):
      if piece.color == 'white':
        forward = 'N'
      else:
        forward = 'S'
      if forward+'W' in self.neighbours:
        self.neighbours[forward+'W'].storeVibration(piece)
      if forward+'E' in self.neighbours:
        self.neighbours[forward+'E'].storeVibration(piece)

    # Long range pieces
    # TODO: refactor, make shorter
    if isinstance(piece, Queen):
      for d in self.neighbours:
        if len(d) < 3: # if len(d) <operator for: Queen> <number for: Queen>:
          self.neighbours[d].propagate(d, piece)
    if isinstance(piece, Bishop):
      for d in self.neighbours:
        if len(d) == 2:
          self.neighbours[d].propagate(d, piece)
    if isinstance(piece, Rook):
      for d in self.neighbours:
        if len(d) == 1:
          self.neighbours[d].propagate(d, piece)

  def exploreRange(self, piece):
    # Short range pieces
    if isinstance(piece, King):
      return [self.neighbours[d] for d in self.neighbours if len(d) < 3]
    if isinstance(piece, Knight):
      return [self.neighbours[d] for d in self.neighbours if len(d) == 3]
    if isinstance(piece, Pawn):
      if piece.color == 'white':
        forward = 'N'
        opponent = 'black'
        startingRow = '2'
      else:
        forward = 'S'
        opponent = 'white'
        startingRow = '7'
      options = []
      if forward in self.neighbours and not self.neighbours[forward].piece:
        options.append(self.neighbours[forward])
      if (piece.square.name[1] == startingRow
          and not self.neighbours[forward].piece
          and not self.neighbours[forward].neighbours[forward].piece):
        options.append(self.neighbours[forward].neighbours[forward])
      if forward + "E" in self.neighbours and self.neighbours[forward + "E"].piece and self.neighbours[
        forward + "E"].piece.color == opponent:
        options.append(self.neighbours[forward + "E"])
      if forward + "W" in self.neighbours and self.neighbours[forward + "W"].piece and self.neighbours[
        forward + "W"].piece.color == opponent:
        options.append(self.neighbours[forward + "W"])
      return options
    # Long range pieces
    lyst = []
    if isinstance(piece, Queen):
      lyst.extend([self.neighbours[d].explore(d, piece) for d in self.neighbours if len(d) < 3])
      return [item for sublist in lyst for item in sublist]
    if isinstance(piece, Bishop):
      lyst.extend([self.neighbours[d].explore(d, piece) for d in self.neighbours if len(d) == 2])
      return [item for sublist in lyst for item in sublist]
    if isinstance(piece, Rook):
      lyst.extend([self.neighbours[d].explore(d, piece) for d in self.neighbours if len(d) == 1])
      return [item for sublist in lyst for item in sublist]

  def explore(self, direction, piece):
    if self.piece:
      return [self]
    lyst = [self]
    if direction in self.neighbours:
      lyst.extend(self.neighbours[direction].explore(direction, piece))
    return lyst

class Chessboard:
  # These directions are used to connect the squares
  directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

  # Only the white king: '8/8/8/8/8/8/8/4K3 w - - 0 1' (with quotes)
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
          assert c.lower() in pieces, "Unknown piece: '" + c + "'"

          if c.isupper():
            color = 'white'
          else:
            color = 'black'

          self.squares[i][j].setPiece(pieces[c.lower()](color, self.squares[i][j]))
          self.squares[i][j].active = False

          if color == 'white':
            whitePieces.addPiece(self.squares[i][j].getPiece())
          else:
            blackPieces.addPiece(self.squares[i][j].getPiece())

          j += 1

  def dayBreak(self):
    biddings = []
    for p in whitePieces:
      biddings.append(p.wakeUp())
    return biddings

  def nightFall(self):
    biddings = []
    for p in blackPieces:
      biddings.append(p.wakeUp())
    return biddings

  def emitVibrations(self):
    for p in whitePieces.pieces + blackPieces.pieces:
      p.vibrate()

  def clearVibrations(self):
    for row in self.squares:
      for square in row:
        square.clearVibrations()

  def print(self):
    print()
    for rank in range(8):
      for square in self.squares[7 - rank]:  # from 7 to 0, to print top rank first
        if square.active:
          print(colors.RED + str(square) + colors.ENDC, end=' ')
          square.active = False
        else:
          print(square, end=' ')
      print()
    print()

  def status(self):
    for row in self.squares:
      for square in row:
        if square.vibrations:
          print(square.name, end=": ")
          for piece in square.vibrations:
            print(piece, end=" ")
          print()

