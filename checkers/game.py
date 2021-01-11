import pygame
from .constants import  RED,WHITE, BLUE,SQUARE_SIZE
from .board import  Board
class Game:
    def __init__(self,win):
        self._init()
        self.win=win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    """
    Here, we simply create the _init protected method because, while updating and restarting we have to perform the
    same task twice. However, we simply distinguish between reset and initializing the board.
    """
    def _init(self):
        self.selected=None
        self.board=Board()
        self.turn=RED
        self.valid_moves={}
    
    def winner(self):
        return self.board.winner()
    
    
    def reset(self):
        self._init()

    """
    Here, the select method is used to see if the valid moves are possibles. Here, we get the value of row,col as
    (5,0). Since, the game object is only instaniated we, have self.select=False at first. We just called our select
    method. Here, we are making the functions in such way that, at first the users select a piece and we provide 
    the valid positions for that piece, and if the user selects the valid positions for a piece than move.

    Here, at first(5,0) is passed to select. Since this was just selected and the game class has no previous value
    of selected. We first find its moves and display back to the users in a blue cirlce. Here, since at first 
    nothing is selected 
    we move to line piece=self.board.get_piece(row,col)->(5,0): We give the get the piece=(5,0,RED). We check if 
    the selected piece is valid and it is the players turn. If it is valid, we select the piece. i.e.
    self.selected=piece. and we calculate the valid moves. We return True if the selection was correct and False
    if it is wrong. Then the first event is completed in our main program. Now, we again iterate through our 
    event loop. Let's we again press a valid move. We again reach game.select(row, col) with the position
    where we need to move.
    If the move is valid than we move else not. Here, again when we reach this method after selecting a move.
    We, have self.selected=TRUE(5,0,RED). So, we move inside the if condition. Then, we move the piece. If the
    move was successful then the result is TRUE else FALSE. Let's say if the move was not correct and we click on
    the random position which was not a valid move(valid was (4,1), but we clicked (5,6)), then we make 
    self.selected=None. That means no piece was selected and we again do a recursive call with select(5,6).
    Since, we returned back to the function, Now, self.select=False. so we check for the piece at position
    5,6. Since(5,6) has no piece board.get_piece(5,6)=0.So, we return False. Here, since the function is over. Now,
    again we move to main function and check for new event. 

    This whole process repeats and like this way the below function works.
    """
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:  # Insures that piece is valid and turn is for red and change accordingly.
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    """
    Let's see how the below function works. First of all, if the move is valid then we move a piece.
    Here, from select function, if a piece is already selected and then we calculate the valid moves and if the 
    move is not valid then we return the False.
    Here the valid moves produdes the result in the form of the dictonary. Eg. We get the output of 
    get valid moves as: 
    get_valid_moves={(2,5):[(3,4,WHITE),(6,3,WHITE)],(1,3):[]}. We get output in this form. Here the key(2,5) and
    (1,3) are final valid positions for our previous piece. It was stored while in valid moves while we were 
    calculating for it. If the key has no value, then it means the next move for the piece did not contain any 
    piece to capture. E.g. it means a piece can move to either position(2,5) or position(1,3) but the concequenses
    will be different. Here, while moving to the final position (2,5) from a red_piece we skip from 2 white piece
    (3,4,WHITE) and (6,3,WHITE) i.e. double hop we can capture 2 white pieces. However, if we chose the position
    (1,3) then it means we did not capture any white piece and the next move for our piece was blank. In short, the
    key value represents the final move position and the values in a list represent the numbers of pieces skipped.

    Now, if we have skipped the pieces, then we remove those pieces from the board and change the turn. Like this
    way below function works.
    """
    def _move(self,row, col):
        piece=self.board.get_piece(row,col)
        if self.selected and piece==0 and (row,col) in self.valid_moves:
            self.board.move(self.selected,row,col)
            skipped=self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    
    # Simply draws a blue cirle to the valid moves present.
    def draw_valid_moves(self,moves):
        for move in moves:
            row,col=move
            pygame.draw.circle(self.win,BLUE,(col*SQUARE_SIZE+SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2),15)

    # Here, it simply changes the turn. We have to be careful because while changing turn we select the new piece 
    # different color and say next is white then we have to clear the valid moves from the previously strored value.
    def change_turn(self):
        self.valid_moves={}
        if self.turn==RED:
            self.turn=WHITE
        else:
            self.turn=RED

    def get_board(self):
        return self.board
    
    def ai_move(self,board):
        self.board=board
        self.change_turn()

