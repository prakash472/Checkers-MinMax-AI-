from .constants import WHITE,BLACK,RED,GREY,SQUARE_SIZE,CROWN
import pygame
class Pieces:
    PADDING=10
    OUTLINE=2
    def __init__(self,row,col,color):
        self.row=row
        self.col=col
        self.color=color
        self.king=False
        self.x=0
        self.y=0
        self.calc_position()
    
    def calc_position(self):
        self.x=SQUARE_SIZE*self.col+SQUARE_SIZE//2
        self.y=SQUARE_SIZE*self.row+SQUARE_SIZE//2

    def make_king(self):
        self.king=True
    
    def draw(self,window):
        radius=SQUARE_SIZE//2-self.PADDING
        pygame.draw.circle(window,GREY,(self.x,self.y),radius+self.OUTLINE)
        pygame.draw.circle(window,self.color,(self.x,self.y),radius)
        if self.king:
            window.blit(CROWN,(self.x-CROWN.get_width()//2,self.y-CROWN.get_height()//2))

    """
    Here the below function is used when we move the piece object. If, the particular instance of the Piece object or 
    a specific piece is moved from one place to another place, then the below function will update the piec position
    which is its row and column. It will also adjust the current position of the piece after movement along with updating
    its row and column.
    """    
    def move(self,row,col):
        self.row=row
        self.col=col
        self.calc_position() 

    def __repr__(self):
        return str(self.color)