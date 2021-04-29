from random import choice

class Piece:
  def __init__(self, color, square):
    assert color in ['black', 'white']
    self.color = color
    self.square = square

  def getName(self):
    return type(self).__name__ + " (" + str(self.value) + ")"

  def moveTo(self, square):
    # print("White control score: ", self.square.whiteVibrations)
    # print("Black control score: ", self.square.blackVibrations)
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
    reachableSquares = self.square.exploreRange(self)
    for r in reachableSquares:
      r.storeVibration(self)

  def wakeUp(self):
    options = self.square.exploreRange(self)

    # TODO: Sense vibrations on the current square (are you in danger?)

    r = [o for o in options if o.piece and o.piece.color != self.color]
    if r:
      c = max(r, key=lambda s: s.piece.value)
      # Idea: modify bid if more enemy vibrations than friendly vibrations

      print("bid by " + self.getName() + " on " + self.square.name + ": " + str(1 + c.piece.value / self.value))
      return [1 + c.piece.value / self.value, self, c]
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

  def __str__(self):
    if self.color == 'white':
      return 'K'
    else:
      return 'k'


class Queen(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 9

  def __str__(self):
    if self.color == 'white':
      return 'Q'
    else:
      return 'q'


class Knight(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 3

  def __str__(self):
    if self.color == 'white':
      return 'N'
    else:
      return 'n'


class Bishop(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 3

  def __str__(self):
    if self.color == 'white':
      return 'B'
    else:
      return 'b'

class Rook(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 5

  def __str__(self):
    if self.color == 'white':
      return 'R'
    else:
      return 'r'

class Pawn(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.value = 1

  def __str__(self):
    if self.color == 'white':
      return 'P'
    else:
      return 'p'
