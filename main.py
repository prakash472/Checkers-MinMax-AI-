import pygame
from checkers.constants import HEIGHT,WIDTH,SQUARE_SIZE,WHITE
from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax

FPS=60
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Checkers")

"""
We know the get_position method provides the position of the mouse selected. But it will be the pixel of the window
Here, the leftmost corner is (0,0) and the pixel goes on incresing as we move right and downwards. The right bottom
has pixel (600,600). Now since the get_position gives this value we have convert it into numeric rows and columns.
E.g row=5 and col=5 to find the exact position of the piece. Here, we have square_size=100
If x=350 and x//square_size= 350//100=3.5 . It means we are at 3rd row and likewise we can identify column. 
Finally we can find the board piece as board[row][col].
"""
def get_row_col_from_mouse(pos):
    x,y=pos
    row= y // SQUARE_SIZE
    col= x // SQUARE_SIZE
    return row,col

def main():
    run=True
    clock=pygame.time.Clock()
    board= Board()
    game=Game(WINDOW)
    # Here we create the board instance. Now, it operates the default consturctor __init__ of board class. Let's go to board class.
    
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value,new_board=minimax(game.get_board(),3,WHITE,game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos() #This returns the position of the selected piece in tuple form (350(row pixel),200(column pixel))
                row,col=get_row_col_from_mouse(pos) # Here the position was on the tuple form e.g(350,200). It returns the 
                                                    # equivalent rows and position of the piece e.g row=3, col=2    
            #    piece=board.get_piece(row,col)
            #    board.move(piece,4,3)   # We move the selected piece to this position.
                game.select(row,col)
                #Here we know go to game.select(say for (5,0)-->Goes to game class of select method.)
      #  board.draw(WINDOW)
      #  pygame.display.update()
        game.update()
    pygame.quit()

main()