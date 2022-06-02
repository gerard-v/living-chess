from random import choice
# The following imports to access the directions from class Chessboard
#   in module stage.py don't work:
# from stage import Chessboard (ImportError: cannot import name 'Chessboard')
# from stage import Chessboard as Schaakbord (same message)
# from stage import * (NameError: name 'stage' is not defined)
# import Chessboard (ImportError: No module named 'Chessboard')
import stage # for directions in class Chessboard

class Army:
  playMode = 'computer'

  def __init__(self, color):
    assert color in ['black', 'white']
    self.color = color
    self.pieces = []

  def possess(self):
    self.playMode = 'user'

  def askMove(self):
    while (True):
      moveString = input("Please enter move: ")
      moveParams = moveString.split(' ')

      for p in self.pieces:
        if p.square.name == moveParams[0]:
          reachableSquares = p.square.exploreRange(p) # TODO: p.exploreRange()
          for r in reachableSquares:
            # print(r.name)
            if r.name == moveParams[1]:
              return [0, p, r]
      print('I can\'t work with this. Please try again.')

  def addPiece(self, piece):
    self.pieces.append(piece)

  def removePiece(self, piece):
    self.pieces.remove(piece)

  def wakeUp(self):
    # Remove ghost pawn, if any
    for p in self.pieces:
      if isinstance(p, GhostPawn):
        p.square.clear()
        self.pieces.remove(p)
        break
    biddings = []
    for p in self.pieces:
      biddings.append(p.wakeUp())

    # Honor the best bid
    best = -1
    bestIndex = None
    results = []
    for i in range(len(biddings)):
      if biddings[i][0] == best:
        results.append(i)

      if biddings[i][0] > best:
        results = [i]
        best = biddings[i][0]
    # In case of a tie, pick a random bid out of the results
    bestIndex = choice(results)

    if self.playMode == 'user':
      return self.askMove()
    else:
      return biddings[bestIndex]


whitePieces = Army('white')
blackPieces = Army('black')


class Piece:
  def __init__(self, color, square):
    assert color in ['black', 'white']
    self.color = color
    self.square = square
    for r in pieces:
      if isinstance(self,pieces[r]):
        self.symbol = r if self.color == 'black' else r.upper()

  def __str__(self):
    return self.symbol

  def getName(self):
    return type(self).__name__ + " (" + str(self.value) + ")"

  def moveTo(self, square):
    print(self, self.square.name, "-", square.name)
    self.square.clear()
    self.square = square
    if self.square.getPiece():
      score = self.square.getPiece().value
    else:
      score = 0
    square.setPiece(self)
    # Promote pawn if possible
    if isinstance(self, Pawn) and self.forward not in square.neighbours:
      square.promotePawn(self)
    return score

  def vibrate(self):
    self.square.propagateVibrations(self)

  def wakeUp(self):
    options = self.square.exploreRange(self)
    # Remove squares occupied by own pieces
    options = [o for o in options if not o.piece or o.piece.color != self.color]

    # Remove squares where King can be captured
    if isinstance(self, King):
      print("Options for King before trimming:", [o.name for o in options])
      options = [o for o in options if not o.isUnderAttack(self)]
      print("Options for King after trimming:", [o.name for o in options])
      # Sense vibrations on the current square (are you in danger?)
      if self.square.isUnderAttack(self):
        print(str(self) + ": I'm in check!")
        if len(options):
          return [self.value, self, choice(options)]

    # Can you capture a piece of the opponent?
    r = [o for o in options if o.piece and o.piece.color != self.color]
    if r:
      c = max(r, key=lambda s: s.piece.value)
      # Idea: modify bid if more enemy vibrations than friendly vibrations

      if 1 + c.piece.value / self.value >= 2:
        print("bid by " + self.getName() + " on " + self.square.name + ": " + str(1 + c.piece.value / self.value))
        return [1 + c.piece.value / self.value, self, c]
      else:
        if c.control() == self.color and c.gain(self.color) > 0:
          print("bid by " + self.getName() + " on " + self.square.name + ": " + str(1 + c.piece.value / self.value))
          return [1 + c.piece.value / self.value, self, c]
        return [0.1, self, c]
    else:
      r = [o for o in options if not o.piece or o.piece.color != self.color]
      if r:
        return [1, self, choice(r)]
      else:
        return [0, self, None] # no moves available


class King(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 100
    self.directions = [d for d in stage.Chessboard.directions if len(d) < 3]
    self.range = 'short'


class Queen(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 9
    self.directions = [d for d in stage.Chessboard.directions if len(d) < 3]
    self.range = 'long'


class Knight(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 3
    self.directions = [d for d in stage.Chessboard.directions if len(d) == 3]
    self.range = 'short'


class Bishop(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 3
    self.directions = [d for d in stage.Chessboard.directions if len(d) == 2]
    self.range = 'long'


class Rook(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 5
    self.directions = [d for d in stage.Chessboard.directions if len(d) == 1]
    self.range = 'long'


class Pawn(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 1
    self.range = 'short'
    self.forward = 'N' if self.color == 'white' else 'S'
    self.directions = [self.forward + d for d in 'EW']
    self.startingRow = '2' if self.color == 'white' else '7'

  def moveTo(self, square):
    if square not in [self.square.neighbours[d] for d in self.square.neighbours]:
      print('Giant step forward by pawn, skipped square: ' + self.square.neighbours[self.forward].name)
      ghost = GhostPawn(self, self.color, self.square.neighbours[self.forward])
      if self.color == 'white':
        whitePieces.addPiece(ghost)
      else:
        blackPieces.addPiece(ghost)
      self.square.neighbours[self.forward].setPiece(ghost)
    return Piece.moveTo(self, square)


# Virtual piece for enabling en passant capture
# Not enlisted in the army
class GhostPawn(Piece):
  def __init__(self, parent, color, square):
    Piece.__init__(self, color, square)
    self.value = 1
    self.parent = parent
    self.symbol = 'x'
    self.directions = []


pieces = {'k': King, 'q': Queen, 'n': Knight, 'b': Bishop, 'r': Rook, 'p': Pawn}

