from elemant import MAGNET, Ball, Taraget
from Magnet_Game import MagnetBRo

def Sboard():
    boards =[
         {
            #1
            "n": 4,
            "allStep": 5,
            "magnets": [MAGNET(1, 3, "-")],
            "balls": [Ball(2, 1)],
            "Taragets": [Taraget(1, 1),Taraget(3, 1)]
        },
        {
            #2
            "n": 5,
            "allStep": 5,
            "magnets": [MAGNET(0, 4, "-"),],
            "balls": [Ball(1, 2), Ball(2, 1),Ball(3, 2),Ball(2, 3)],
            "Taragets": [Taraget(0, 2), Taraget(2, 0),Taraget(2, 2),Taraget(2, 4),Taraget(4, 2)]
        },
        {
            #3
            "n": 4,
            "allStep": 5,
            "magnets": [MAGNET(0, 2, "-")],
            "balls": [Ball(2, 1)],
            "Taragets": [Taraget(3, 0), Taraget(3, 2)]
        },
        {
            #4
            "n": 5,
            "allStep": 5,
            "magnets": [MAGNET(2, 2, "-"),],
            "balls": [Ball(3, 1),Ball(3, 3)],
            "Taragets": [Taraget(4, 0), Taraget(2, 0),Taraget(3, 4)]
        },
        {
            #5
            "n": 4,
            "allStep": 5,
            "magnets": [MAGNET(3, 3, "+"),],
            "balls": [Ball(0, 2),Ball(0, 3),Ball(3, 0)],
            "Taragets": [Taraget(0,1), Taraget(1, 2),Taraget(2, 1),Taraget(2, 2)]
        },
        {
            #6
            "n": 5,
            "allStep": 2,
            "magnets": [MAGNET(2, 1, "-"),MAGNET(2, 2, "+"),],
            "balls": [Ball(1, 0),Ball(3, 0)],
            "Taragets": [Taraget(0, 0), Taraget(2, 0),Taraget(4, 1),Taraget(4, 2)]
        },
         {
            #7
            "n": 5,
            "allStep": 5,
            "magnets": [MAGNET(2, 0, "-"),MAGNET(2, 2, "+"),],
            "balls": [Ball(1, 0),Ball(3, 0),Ball(1, 4),Ball(3, 4)],
            "Taragets": [Taraget(0, 1), Taraget(1, 2),Taraget(0, 3),Taraget(2, 3),Taraget(4, 1),Taraget(4, 3)]
        },
        {
            #8
            "n": 6,
            "allStep": 5,
            "magnets": [MAGNET(2, 4, "+"),MAGNET(3, 4, "-"),],
            "balls": [Ball(3, 0),Ball(0, 2),Ball(5, 2)],
            "Taragets": [Taraget(5, 2), Taraget(3, 1),Taraget(3, 2),Taraget(2, 2),Taraget(1 , 2)]
        },
        {
            #9
            "n": 5,
            "allStep": 5,
            "magnets": [MAGNET(2, 0, "-"),MAGNET(2, 2, "+"),],
            "balls": [Ball(1, 0),Ball(3, 0),Ball(1, 4),Ball(3, 4)],
            "Taragets": [Taraget(0, 1), Taraget(0, 3),Taraget(1, 2),Taraget(2, 3),Taraget(4 , 1),Taraget(4 , 3)]
        },
        
    ]
    return boards

def selecte_boards(boards):
    print("choose number boards:")
    for i in range(len(boards)):
        board= boards[i]
        print(f"board {i + 1}: grid {board['n']}x{board['n']}, steps to Win: {board['allStep']}")
        
    choice= int(input("enter the number boards Bro:")) - 1
    if 0 < choice < len(boards):
        select_board= boards[choice] 
        return select_board
    else:
        print("invalid number board")
        return boards[0]
    
if __name__ == "__main__":
    board= Sboard()
    select_board=selecte_boards(board)
    
    game=MagnetBRo(n=select_board["n"],allStep=select_board["allStep"])

    game.magnets=select_board["magnets"]
    game.balls=select_board["balls"]
    game.targets=select_board["Taragets"]
    game.game_loop()
        

        
    