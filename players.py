from string import digits
from random import choice, randint


class Piece:
  def __init__(self, color, square):
    assert color in ['black', 'white']
    self.color = color
    self.square = square
    self.selfishness = 1

  def moveTo(self, square):
    self.square.clear()
    self.square = square
    self.square.setPiece(self)

  def wakeUp(self):
    # Roll-call
    # print("The", self.color, type(self).__name__, "wakes up");

    # set/unset selfish mode
    if self.selfishness == 2:
      r = randint(1, 5)
      if r == 1:
        self.selfishness = 1
        print("The", self.color, type(self).__name__, "stopped being selfish")
    else:
      r = randint(1, 50)
      if r == 1:
        self.selfishness = 2
        print("The", self.color, type(self).__name__, "is in a selfish mood!")

    # feel/listen: sense what squares are a no-go
    options = self.square.exploreRange(self)

    r = [o for o in options if o.piece and o.piece.color != self.color]
    if r:
      return [2*self.selfishness, self, choice(r)]
    else:
      r = [o for o in options if not o.piece or o.piece.color != self.color]
      if r:
        return [1*self.selfishness, self, choice(r)]
      else:
        return [0, self, None]


class King(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)
    self.options = []

  def __str__(self):
    if self.color == 'white':
      return 'K'
    else:
      return 'k'

  def announcePresence(self):
    pass


class Queen(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if self.color == 'white':
      return 'Q'
    else:
      return 'q'


class Knight(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if self.color == 'white':
      return 'N'
    else:
      return 'n'


class Bishop(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if self.color == 'white':
      return 'B'
    else:
      return 'b'


class Rook(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if self.color == 'white':
      return 'R'
    else:
      return 'r'


class Pawn(Piece):
  def __init__(self, color, square):
    Piece.__init__(self, color, square)

  def __str__(self):
    if self.color == 'white':
      return 'P'
    else:
      return 'p'
