import random
from player import computer_move

def print_board(board):
    print("\n")
    for i in range(3):
        print(f" {board[i*3]} │ {board[i*3+1]} │ {board[i*3+2]} ")
        if i < 2:
            print("───┼───┼───")
    print("\n")

def check_winner(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != " ":
            return board[i]
    
    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != " ":
            return board[i]
    
    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]
    
    return None

def is_board_full(board):
    return " " not in board

def tic_tac_toe():
    board = [" "] * 9
    
    # Randomly choose who starts (X or O)
    current_player = random.choice(["X", "O"])
    
    print("\n" + "="*40)
    print(" " * 10 + "TIC-TAC-TOE")
    print("="*40)
    print("\nEnter a number (1-9) to make your move:")
    print_board(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    print("Let's begin!\n")
    
    # Announce who starts
    if current_player == "X":
        print("You (X) will play first!")
    else:
        print("Computer (O) will play first!")
    
    while True:
        print_board(board)
        
        if current_player == "X":
            print(f"\nYour turn (X)")
            while True:
                try:
                    move = int(input("Enter your move (1-9): ")) - 1
                    if 0 <= move <= 8 and board[move] == " ":
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 1 and 9.")
            board[move] = current_player
        else:
            # O's turn - call the computer_move function
            print("\nComputer's turn (O)")
            move, reasoning = computer_move(board)
            board[move-1] = "O"
            print(f"\nComputer chooses position {move}")
            print("\nComputer's reasoning:")
            print("-"*40)
            print(reasoning)
            print("-"*40)
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "X":
                print("\n⭐️ You win! ⭐️")
            else:
                print("\n💻 Computer wins! 💻")
            break
        
        if is_board_full(board):
            print_board(board)
            print("\n🤝 It's a tie! 🤝")
            break
        
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    tic_tac_toe()