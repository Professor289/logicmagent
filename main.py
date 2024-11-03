from elemant import Ball, Magnet, Target
from Magnet_Game import LogicMagnet

def setup_boards():
    boards = [
        {
            #1
            "n": 4,
            "max_steps": 3,
            "magnets": [Magnet(1, 3, "-")],
            "balls": [Ball(2, 1)],
            "targets": [Target(1, 1),Target(3, 1)]
        },
        {
            #2
            "n": 5,
            "max_steps": 5,
            "magnets": [Magnet(0, 4, "-"),],
            "balls": [Ball(1, 2), Ball(2, 1),Ball(3, 2),Ball(2, 3)],
            "targets": [Target(0, 2), Target(2, 0),Target(2, 2),Target(2, 4),Target(4, 2)]
        },
        {
            #3
            "n": 4,
            "max_steps": 5,
            "magnets": [Magnet(0, 2, "-")],
            "balls": [Ball(2, 1)],
            "targets": [Target(3, 0), Target(3, 2)]
        },
        {
            #4
            "n": 5,
            "max_steps": 5,
            "magnets": [Magnet(2, 2, "-"),],
            "balls": [Ball(3, 1),Ball(3, 3)],
            "targets": [Target(4, 0), Target(2, 0),Target(3, 4)]
        },
    ]
    return boards

def select_board(boards):
    print("Choose a board number:")
    for i in range(len(boards)):
        board = boards[i]
        print(f"Board {i + 1}: Grid {board['n']}x{board['n']}, Steps to Win: {board['max_steps']}")
        # print(len(boards))
    choice = int(input("Enter the board number: ")) - 1
    if 0 <= choice < len(boards):
        selected_board = boards[choice]
        return selected_board
    else:
        print("invalid number board")
        return boards[0]


if __name__ == "__main__":
    boards = setup_boards()
    selected_board = select_board(boards)

    game = LogicMagnet(
        n=selected_board["n"],
        full_steps=selected_board["max_steps"]
    )

    game.magnets = selected_board["magnets"]
    game.balls = selected_board["balls"]
    game.targets = selected_board["targets"]

    game.game_loop()