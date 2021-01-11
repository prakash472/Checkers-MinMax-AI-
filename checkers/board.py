import pygame
from .pieces import Pieces
from .constants import BLACK,ROWS,COLS,WHITE,RED,SQUARE_SIZE

#Here from main we are now at board class. It initializaes the following method. 
"""
Since the board is our class. We first look what objects board can have? First of all, the board itslef has board
variable which stores the list. Here, it keeps track of the each position(square) of the board. Here, it keeps 
track of each of the squares of the checkers board. Eg. [[0, (0, 1, 'White'), 0, (0, 3, 'White'), 0, (0, 5, 'White')],
                                                         [0, (1, 1, 'White'), 0, (1, 3, 'White'), 0, (1, 5, 'White')]]
Here the list is a 2d array. each row is an list of the total checkers board. Here 0 means no pieces are placed.
And if the pieces are present in that square. Then we have to find, what is the position and color of the piece.So,
we store the information of rows position, column position and color of the piece. Here (0,3,"White") means a white 
piece is present in the checkers board at row 0 and column 3.

- We keep the track of if the piece is selected. If it is selected, we could so the possible next valid steps and 
  many other operations. So, we keep track of it also.
- We keep the track of the pieces present on the checkers board for both red and white. Initially both of them have 
  12 pieces at begining. So, while initializing we initialize them to 0.
- We also keep the track of the kings in the checkers board. A piece is said to be a king, if it travels to the last 
  row of the opponent board. Then we make them king. We also keep track of the king. Likewise, initally we have 0 
  king so initialize both red and white kings to zero.
- After all this we create our board.
"""
class Board:
    def __init__(self):
        self.board = []
        self.selected_piece=None # To check which piece is selected
        self.red_left=self.white_left=12 #Total number of pieces remaining at first will be 12 for both red and white. And we subtract 1 from pieces
        self.red_kings=self.white_kings=0 # The kings
        self.create_board()

    """
         0-   |---1(R)--|--2(B)----|--3(R)----|
         1-   |---4(B)--|---5(R)---|--6(B)----|
         2-   |---7(R)--|---8(B)---|--9(R)----|
            
            Let's above is the checkers board. Initially when we draw the window in our main file, it was totally
            black. We have to make it to red-black pattern. So, we simply put the red squares in such a way that
            a pattern is formed in red-black. Here we go through each row and alternatively placed red squares. If 
            the row is even(say 0, it should be r-b-r). So we place the red sqaures in even positions(i.e 0 ,2,4).
            
            Here when we do rows%2, for rows=2, then we go have loop of cols as 
            st.position=2%2=0, final_position=ROWS=8(not rows),step=2. 
            We draw red square at 0. Incrase by step 2 to 0-2-4-6

            Here when we do rows%2, for rows=1, then we go have loop of cols as 
            st.position=1%2=1, final_position=ROWS=8(not rows),step=2. 
            We draw red square at 1. Incrase by step 2 to 1-3-5-7.

            Like this way with the help of mod 2(%2), we can print the board with red and black.
    """
    # This method helps to draw the red and black pattern of the checkers.
    def draw_squares(self,window):
        window.fill(BLACK) # Fills entire window by black
        for rows in range(ROWS):
            for col in range(rows%2,ROWS,2):
                pygame.draw.rect(window, RED,(rows*SQUARE_SIZE, col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))


    def get_piece(self,row,col):
        return self.board[row][col]
    
    """
    The below method is used when we select the piece and move into the new row and col position.
    Here row and col is the new position(4,3) and piece object contains (0,1, WHITE) information of the piece to be 
    moved.Here, we swap the position of board[piece.row][piece.column] i.e board[0][1] with board[4][3]. Previously 
    board[4][3]=0 and board[0][1]=(0,1,WHITE). Now it is replaced. i.e board[4][3]=(0,1,WHITE) and board[0][1]=0.
    Now we also have to make the changes to the piece also. Until now, only board part was done.
    Here we sent pieces.move(4,3). Here the piece object=(0,1,WHITE) and it is moved to new position. When,
    we do (0,1,WHITE).move(4,3). In the pieces the object (0,1,WHITE) will change its position to self.row=row i.e 
    row=4 and self.col=col i.e previous 1= 5. Now the instance of previous piece (0,1,WHITE)=(4,3,WHITE)
    """
    def move(self,piece,row,col):
        self.board[piece.row][piece.col],self.board[row][col]=self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)

        if row==ROWS or row==0:
            piece.make_king()
            if piece.color== WHITE:
                self.white_kings+=1
            else:
                self.red_kings+=1
    """
    Here, we create the board or place the pieces of the board and store them in our board. So, we store the 
    information of the each square of the board in the board as described above.
    Eg. [[0, (0, 1, 'White'), 0, (0, 3, 'White'), 0, (0, 5, 'White')],
         [0, (1, 1, 'White'), 0, (1, 3, 'White'), 0, (1, 5, 'White')]]
    """
    def create_board(self):
        for rows in range(ROWS):
            self.board.append([])
            #creates [[],[],[],[]]
            """Here the board pieces are placed according to the rows. In checkers, pieces are placed as:
            All the white and red pieces are onlu placed at the black background or at the 
            row0=white_pieces(not red background, but black background)=1,3,5,7 or row[0][1],row[0][3],row[0][5],row[0][7]
            So, first we develop the logic to place the pieces. 
            Here, if cols%2 == (rows+1)%2, we place the piece. 
            Eg. for row[0][0], cols%2(=0),and (rows+1)%2(=1), they are not equal so we don't place the piece.
            Eg. for row[0][1], cols%2(=1),and (rows+1)%2(=1), they are equal so we place the piece.
            This logic helps to place the piece. It helps to find the odd positions for placing pieces.
            
            0-   |---0(R)--|--1(B)----|--2(R)----|--3(R)----|
            1-   |---0(B)--|---1(R)---|--2(B)----|--3(R)----|
            2-   |---0(R)--|---1(B)---|--2(R)----|--3(R)----|
            
            """
            for cols in range(COLS):
                if cols % 2== ((rows + 1) % 2):
                    if rows < 3: # We place white at row 0, row 1 and 2 so.
                        """
                        Here we append ((Piece(rows,cols,WHITE))). Piece class is instantiated. 
                        The instance of the piece class or the object of the Piece class is the  above value.
                        For let's say  self.board[rows].append(Pieces(0,1,WHITE)), it points the object that has
                        value (0,1,"White"). The class piece points the object that has the value of piece.
                        self.board[row][cols]==Piece. Eg.
                        self.board[row].append(Pieces(0,1,White))=[0,[0,1,White],...]
                        self.board[0][1] points to the Piece object. So, we can use the method draw of the piece 
                        because self.board[row][cols] points to the object of the piece.
                        """
                        self.board[rows].append(Pieces(rows,cols,WHITE))
                        # At first, it will look like for first piece. [[0, (0, 1, 'White')]. Because at board[0][0] no piece can be placed.
                    elif rows>4:
                        self.board[rows].append(Pieces(rows,cols,RED))
                        # At first red we have. [[0,(0,1,'White'),...(0,7,'White')],[(1,0,"White"),....],[(5,0,"RED")]]
                    else:
                        self.board[rows].append(0)
                        # At begining the other rows i.e 3,4 the pieces are black.
                else:
                    # The else part is needed because for the remaining part of the rows 0,1,2 and 5,6,7, some of them have empty spaces and they are denoted with 0.
                    self.board[rows].append(0)
    
    
    #This method is used to draw the board and place the pieces
    def draw(self,win):
        self.draw_squares(win)
        for rows in range(ROWS):
            for cols in range(COLS):
                piece=self.board[rows][cols]
                """The above value of piece returns the piece value for each location. 
                [[0, (0, 1, 'White'), 0, (0, 3, 'White'), 0, (0, 5, 'White')],
                 [0, (1, 1, 'White'), 0, (1, 3, 'White'), 0, (1, 5, 'White')],....]
                 Here for board[0][0], piece=0 i.e we do not have a piece. So, we do not draw piece. 
                 Here for board[0][1],piece=(0,1,"White"), it is not 0, so we draw the piece.
                """
                if piece!=0:
                    piece.draw(win) 
    
    # It simply removes the piece.
    def remove(self, pieces):
            for piece in pieces:
                self.board[piece.row][piece.col] = 0
                if piece != 0:
                    if piece.color == RED:
                        self.red_left -= 1
                    else:
                        self.white_left -= 1
        
    """
    Check the image to find the reference.
    The below function might seem to be a bit tricky. Here, we get the piece object whose valid moves we want. 
    Say piece=(6,1,RED). Now, we calculate the possible moves in moves dictionary i.e move={}.
    Here, since the valid moves for a checkers are diagonal only. We first find the left and right of the current
    piece. However, the row may varie depending upon the turn of the checkers. If, the checker is red, then 
    valid moves are upper diagonal(either left diagonals or right diagonals) and if the checkers is white, then
    valid moves are lower diagonal(either left or right.).So, we only find the left and right for the piece because
    they are same for red and white. For, row we keep it same and while traversing we traverse according to the 
    color of checkers.
    ---------valid_move(WHITE)=[left_diagonal(upper)=(left,row+1) and right_diagonal(upper)=(right,row+1)]-------------------
    ---------valid_move(RED)=[left_diagonal(lower)=(left,row-1) and right_diagonal(upper)=(right,row-1)]-------------------
    
    It is because red comes down and white goes up.
    -------------------------------------------RED----------------------------------------------------------
    Now, if the piece is red, the we find the moves. Here, we use the traverse_left method.
     moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
    Initially moves={}
    Here, in self._traverse_left() we have row-1(since it is a red piece and red moves up. In python the upper 
    most sqare is (0,0) and right bottom one is (7,7). Since red moves up, next move have to decrease row by 1.)
    (6,1,RED)
    We have row-1=>6-1=5, left=>col-1    , right=>col+1       ,piece.color=red
                              =>1-1 =0          =>1+1  =2
    In _traverse_left(self, start, stop, step, color, left, skipped=[])
    where start=5, stop=max(row-3,-1), step=-1 color=red, skipped=[]

    Here, we place the start as the 5 for the piece(6,1,WHITE) because its diagonal is the next valid position.
    Here, if the diagonal consists of a piece then we have to check if its diagonal is empty. Eg. For a piece
    (6,1,WHITE). It's valid position in right is (5,2,WHITE). Since it has a piece, we have to check if we can skip 
    that piece. For that piece(5,2,WHITE) to caputre the diagonal of (5,2,WHITE) i.e (4,3) should be empty. Here, 
    if the first diagonal is empty then automatically it is a valid position. However, if the diagonal consists of 
    other piece and if we can capture then we have to again look for the diagonal of captured piece. Overall,
    we have to go through 2 steps ahead(or above) to check if the move is valid.
    Hence the stopping criteria will be (row-1) or for (6,1,WHITE) it will be 6-3= 3. Here, we start with its 
    diagonal so, starting will be row-1 i.e 5. and its diagonal is 4. We check for row 5 and 4.

    Let's check for left then, we get  moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
    Here, self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left) generates output as {(5,0):[]} and 
    while doing moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left) makes moves as 
    moves={(5,0):[]}

    Now the  moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right)). Here,  
    self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right) generates the output as 
    {(2,5):[(3,4,WHITE),(6,3,WHITE)]. Now the moves. update method will give output as:
    moves={(5,0):[],(2,5):[(3,4,WHITE),(6,3,WHITE)}. Now, we return the moves. Here, it is properly explained in
    the game class comment section.However, how they are generated are discussed below. We discuss for the right
    side because it covers the concept of double hop.
    """    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    """
    (6,1,WHITE)
    Here when self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right) method is called we have,
    ----> row-1=5m max(3,-1), step=-1 and piece.color=red and right=2
    moves={}-> to store the valid right moves.
    last=[]
    
    Now, we check the valid for value of r for 5 and 4. Tow steps are required if we need to skip.
    ----------------------------For r=5----------------------------------------------------------
    current=self.board[r][right]=>self.board[5][2]=>(5,2,WHITE)
    Here current is not equal to zero. So, we execute the else part. current is not equal to zero means the 
    first checking position for valid position consists of a piece. if the current.color==color, it means it is 
    the red one here and we have no valid position. However, if the current one is of different color then we can
    skip through it. In our case it is white, so we have 
    last=[current] i.e last=[(5,2,WHITE)]
    Now, since it consits of a piece, we have to look for its diagonal. For that we have to go right and move upwards.
    In loop, we already put stop for 5,4. Since 5 is completed the value of r becomes 4. Since, we are looking diagonal
    for (5,2,WHITE) piece, we have to go one more right. So, we increase the value of right. Now, we execute the 
    next iteration with value as : r=4 and right= 3
    -----------------------------------------------For r=4---------------------------------------------------
    current=self.board[r][right]=(4,3)=0
    
    Here current=0, so we go for the branching conditions. Here skipped=[] so skip if and elif part. Now, in
    else part we have moves[(r,right)]=last i.e moves[(4,3):(5,2,WHITE)].

    we have last, so we go inside if last: Here, if last had some value then we have to check if double hop is 
    possible. It is same as if the last position is the new position and we check if there is a valid position 
    from this new position. Since we check for the valid position from this one, check for its upper diagonal.
    We do the same process, row=row-1 (moving upwards means row-1.).

    For==>> if last: 
                if step=-1 (Ture because example is for red. Now, we go to find its valid position)
                row=max(row-3,0)  (Here, we go to 2 steps ahead for finding so.) row=max(4-3,0)=>1.
                    row=1.
    Here, we also update the moves from this position if its possible .It is possible if it is a double hop. 


    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
     we recursively call the same function. Here, recursion is used because we are repeating the same process. But
     only the parameters change not the process.

     Here now,(--------------------------recursion from r=4)
     start=r+step=>4-1=>3 and stop=row=1 step=-1 color=red, right=4, skipped=[(5,2,WHITE)].
    
    Here we do loop for 3 and 2.
          -----------------------------------------3----------------------------------
          (skipped=[(5,2,WHITE)])
          current=[3][4]=(3,4,WHITE)
          current is not zero. so we go to else part and last=[(3,4,WHITE)]
          right=right+1=5

          -------------------------------------------2-------------------------------
          current=[2][5]=0
          current =zero.
          we have last so if skipped and not last: branching is ignored. Now, we have elif skipped:  
           ---> Now moves[(r,right)]=last+skipped:
                    moves[(2,5)]=[(3,4,WHITE)]+[(5,2,WHITE)]
                    moves[(2,5)]=[(3,4,WHITE),(5,2,WHITE)]  
          Now since we have last we checked if another position can be made from the last(3,4,WHITE). Here, we 
          repeat the process and again do a recursive call. In the next call we have current=[1][6]=(1,6,WHITE).
          Since current!= 0 , we repeat above process and again look for its diagonal. Now, the current[0][7] is 
          not = 0. we execute else part(two times consequitively). We finish the part. Return back to our function.
        ---------------------------------------------------------------------------------------------------------- 
          In the same part of the function for loop r=4, we have done for right side. The result of the left side
          i.e moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last)) was:
          moves[(r,left)]=last+skipped:
          moves[(2,1)]=[(3,2,WHITE)]+[(5,2,WHITE)]
          (2,1):[(3,2,WHITE),(5,2,WHITE)]
          Now, after moves.upadte(right)={(2,1):[(3,2,WHITE),(5,2,WHITE),(3,4):[(3,4,WHITE),(5,2,WHITE)]]
          and then we return it.
        -------------------------------------------------------------------------------------------------------- 

    """
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves


    def winner(self):
        if self.red_left<=0:
            return WHITE
        elif self.white_left<=0: 
            return RED
        return None
   
    def evaluate(self):
         return self.white_left-self.red_left+(self.white_kings*0.5-self.red_kings*0.5)

    def get_all_piece(self,color):
        pieces=[]
        for row in self.board:
            for piece in row:
                if piece!=0 and piece.color==color:
                    pieces.append(piece)
        return pieces

  