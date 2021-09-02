from random import choice

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
          reachableSquares = p.square.exploreRange(p)
          for r in reachableSquares:
            #print(r.name)
            if r.name == moveParams[1]:
              return [0, p, r]
      print('I can\'t work with this. Please try again.')


  def addPiece(self, piece):
    self.pieces.append(piece)

  def removePiece(self, piece):
    self.pieces.remove(piece)

  def wakeUp(self):
    if self.playMode == 'user':
      return self.askMove()

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
    return biddings[bestIndex]

whitePieces = Army('white')
blackPieces = Army('black')

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

pieces = {'k': King, 'q': Queen, 'n': Knight, 'b': Bishop, 'r': Rook, 'p': Pawn}

