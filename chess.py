# Build the board
board = [['. ']*8 for i in range(8)]

# Add the pieces
lineUp = "RNBQKBNR"
board[0] = [x+'b' for x in lineUp]
board[1] = ['Pb']*8
board[6] = ['Pw']*8
board[7] = [x+'w' for x in lineUp]

def printboard():
  print()
  for i in range(8):
    for j in range(8):
      print(board[i][j], end=' ')
    print()
  print()

def move(origin, destination):
  board[destination[0]][destination[1]] = board[origin[0]][origin[1]]
  board[origin[0]][origin[1]] = '. '

def isvalidpawnmove(origin, destination, color):
  #TODO: attacking moves, move limit 1 for moves from the 3rd rank and up (or 6th and down), taking "en passant"
  if color == 'w' and board[origin[0]][origin[1]][1] == color and origin[1]==destination[1] and origin[0]>destination[0] and origin[0]<=destination[0]+2:
    return True
  else:
    if color == 'b' and board[origin[0]][origin[1]][1] == color and origin[1]==destination[1] and origin[0]<destination[0] and origin[0]>=destination[0]-2:
      return True
    else:
      return False

def isvalidmove(origin, destination, color):
  # origin empty ('. ')
  if board[origin[0]][origin[1]] == '. ':
    return False
  if board[origin[0]][origin[1]][0] == 'P':
    return isvalidpawnmove(origin,destination,color)
  
  return True
  
printboard()
color = 'w'
print("White to move")

while True :
  origin = input("Move from: ")
  origin = ('87654321'.index(origin[1]),'abcdefgh'.index(origin[0]))
  #print(origin[0])
  #print(origin[1])

  destination = input("Move to: ")
  destination = ('87654321'.index(destination[1]),'abcdefgh'.index(destination[0]))
  #print(destination[0])
  #print(destination[1])

  if isvalidmove(origin,destination,color):
    move(origin,destination)
    printboard()
	  # Switch between black and white
    if color == 'b':
      color = 'w'
      print("White to move")
    else:
      color = 'b'
      print("Black to move")
  else:
    print("Invalid move")






