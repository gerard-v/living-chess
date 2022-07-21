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
    self.piece = piece
    self.active = True

    if oldpiece:
      if oldpiece.color == 'white':
        if isinstance(oldpiece, GhostPawn) and isinstance(piece, Pawn):
          whitePieces.removePiece(oldpiece.parent)
          oldpiece.parent.square.clear()
        whitePieces.removePiece(oldpiece)
      if oldpiece.color == 'black':
        if isinstance(oldpiece, GhostPawn) and isinstance(piece, Pawn):
          blackPieces.removePiece(oldpiece.parent)
          oldpiece.parent.square.clear()
        blackPieces.removePiece(oldpiece)
      if oldpiece.color != piece.color:
        print(oldpiece.color + ' ' + oldpiece.getName() + ' on ' + self.name + ' captured by a ' + piece.getName())
        if isinstance(oldpiece, King):
          self.board.print()  # to investigate, king still visible
          print(piece.color, "wins!")
          exit()


  def promotePawn(self, piece):
    # Replace pawn by queen
    self.setPiece(Queen(piece.color, self))
    # Enlist
    if piece.color == 'white':
      whitePieces.addPiece(self.piece)
    else:
      blackPieces.addPiece(self.piece)
    print(piece.color, piece.getName(), "on", self.name, "promoted to", self.piece.getName())

  def storeVibration(self, piece):
    self.vibrations.append(piece)

  def clearVibrations(self):
    self.vibrations = []

  def control(self):
    count = 0
    for p in self.vibrations:
      if p.color == 'white':
        count += 1
      else:
        count -= 1
    if count > 0:
      return 'white'
    elif count < 0:
      return 'black'
    else:
      return None

  def gain(self, color):
    sum = 0
    for p in self.vibrations:
      if p.color == color:
        sum -= p.value
      else:
        sum += p.value
    return sum

  def isUnderAttack(self, piece):
    for p in self.vibrations:
      if p.color != piece.color:
        return True
    return False

  def propagate(self, direction, piece):
    self.vibrations.append(piece)
    if (direction in self.neighbours and
        (not self.piece
        or isinstance(self.piece, GhostPawn)
        or isinstance(self.piece, King))):
      self.neighbours[direction].propagate(direction, piece)

  def propagateVibrations(self, piece):
    for d in piece.directions:
      if d in self.neighbours:
        if piece.range == 'long':
          self.neighbours[d].propagate(d, piece)
        else:
          self.neighbours[d].storeVibration(piece)

  def exploreRange(self, piece):
    options = []
    # Pawn
    if isinstance(piece, Pawn):
      # Forward moves: one square...
      forward = piece.forward
      if forward in self.neighbours and not self.neighbours[forward].piece:
        options.append(self.neighbours[forward])
        # ...and two squares
        if (self.name[1] == piece.startingRow
            and not self.neighbours[forward].neighbours[forward].piece):
          options.append(self.neighbours[forward].neighbours[forward])
      # Capture moves
      for d in piece.directions:
        if (d in self.neighbours
            and self.neighbours[d].piece
            and self.neighbours[d].piece.color != piece.color):
          options.append(self.neighbours[d])
      return options
    # Other pieces
    for d in piece.directions:
      if d in self.neighbours:
        if piece.range == 'long':
          options.extend(self.neighbours[d].explore(d))
        else:
          options.append(self.neighbours[d])
    return options

  def explore(self, direction):
    if self.piece and not isinstance(self.piece, GhostPawn):
      return [self]
    lyst = [self]
    if direction in self.neighbours:
      lyst.extend(self.neighbours[direction].explore(direction))
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
          if square.control() == 'white':
            print(colors.GREEN + str(square) + colors.ENDC, end=' ')
          elif square.control() == 'black':
            print(colors.BLUE + str(square) + colors.ENDC, end=' ')
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

