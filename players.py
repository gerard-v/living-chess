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
    self.square.setPiece(self)
    return score

  def vibrate(self):
    self.square.propagateVibrations(self)

  def wakeUp(self):
    options = self.square.exploreRange(self)
    for o in options:
      if o.piece and o.piece.color == self.color:
        options.remove(o)

    # Sense vibrations on the current square (are you in danger?)
    if isinstance(self, King) and self.square.isUnderAttack(self):
      print(str(self) + ": I'm in check!")
      for o in options:
        print(o.name)
        if o.isUnderAttack(self):
          options.remove(o)
          print("Removed: " + o.name)
      if len(options):
        return [self.value, self, choice(options)]

    # Can you capture a piece of the opponent?
    r = [o for o in options if o.piece and o.piece.color != self.color]
    if r:
      c = max(r, key=lambda s: s.piece.value)
      # Idea: modify bid if more enemy vibrations than friendly vibrations

      print("bid by " + self.getName() + " on " + self.square.name + ": " + str(1 + c.piece.value / self.value))
      if 1 + c.piece.value / self.value >= 2:
        return [1 + c.piece.value / self.value, self, c]
      else: # TODO: look at the target's defense, is it protected?
        return [0, self, None]
    else:
      r = [o for o in options if not o.piece or o.piece.color != self.color]
      if r:
        return [1, self, choice(r)]
      else:
        return [0, self, None]


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


pieces = {'k': King, 'q': Queen, 'n': Knight, 'b': Bishop, 'r': Rook, 'p': Pawn}

