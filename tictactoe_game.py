import random
from player import computer_move

def print_board(board):
    print("\nCurrent Board:")
    for i in range(3):
        # Create display row - show numbers for empty spaces, X/O for occupied
        display_row = []
        for j in range(3):
            pos = i * 3 + j
            if board[pos] == " ":
                display_row.append(str(pos + 1))  # Show position number
            else:
                display_row.append(board[pos])    # Show X or O
        
        print(f" {display_row[0]} │ {display_row[1]} │ {display_row[2]} ")
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

def play_single_game():
    board = [" "] * 9
    
    # Choose difficulty level
    print("\n" + "="*40)
    print(" " * 10 + "TIC-TAC-TOE")
    print("="*40)
    print("\nChoose difficulty level:")
    print("1. Easy - Fun AI opponent")
    print("2. Hard - Nearly unbeatable AI")
    
    while True:
        try:
            choice = input("Enter 1 or 2: ").strip()
            if choice in ['1', '2']:
                difficulty = "easy" if choice == '1' else "hard"
                break
            else:
                print("Please enter 1 for Easy or 2 for Hard")
        except:
            print("Invalid input. Please enter 1 or 2")
    
    # Randomly choose who starts (X or O)
    current_player = random.choice(["X", "O"])
    
    print(f"\nDifficulty: {difficulty.upper()} mode")
    print("Enter a number (1-9) to make your move:")
    print_board(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    print("Let's begin!\n")
    
    # Announce who starts
    if current_player == "X":
        print("You (X) will play first!")
    else:
        print(f"Computer (O) will play first!")
    
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
            # O's turn - call the computer_move function with difficulty
            print(f"\nComputer's turn (O) - {difficulty.upper()} mode")
            move, reasoning = computer_move(board, difficulty)
            if move == -1:
                print("No moves available - game should end!")
                break
            board[move-1] = "O"
            print(f"\nComputer chooses position {move}")
            print(f"\nComputer's reasoning ({difficulty.upper()} mode):")
            print("-"*40)
            print(reasoning)
            print("-"*40)
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "X":
                print("\n⭐️ You win! ⭐️")
            else:
                print(f"\n💻 Computer wins! 💻")
                if difficulty == "hard":
                    print("  (Hard mode is tough! 💪)")
            return winner
        
        if is_board_full(board):
            print_board(board)
            print("\n🤝 It's a tie! 🤝")
            return "tie"
        
        current_player = "O" if current_player == "X" else "X"

def tic_tac_toe():
    print("\n" + "="*50)
    print(" " * 15 + "TIC-TAC-TOE GAME")
    print("="*50)
    
    games_played = 0
    player_wins = 0
    computer_wins = 0
    ties = 0
    
    while True:
        games_played += 1
        print(f"\n🎮 Starting Game #{games_played}")
        
        result = play_single_game()
        
        # Update statistics
        if result == "X":
            player_wins += 1
        elif result == "O":
            computer_wins += 1
        elif result == "tie":
            ties += 1
        
        # Display current statistics
        print(f"\n📊 Game Statistics:")
        print(f"   Games played: {games_played}")
        print(f"   Your wins: {player_wins}")
        print(f"   Computer wins: {computer_wins}")
        print(f"   Ties: {ties}")
        
        # Ask if player wants to play again
        print("\n" + "="*40)
        print("What would you like to do next?")
        print("1. Play again")
        print("2. Quit")
        
        while True:
            try:
                choice = input("Enter 1 or 2: ").strip()
                if choice in ['1', '2']:
                    break
                else:
                    print("Please enter 1 to play again or 2 to quit")
            except:
                print("Invalid input. Please enter 1 or 2")
        
        if choice == '2':
            print(f"\n🎉 Thanks for playing!")
            print(f"📊 Final Statistics:")
            print(f"   Total games: {games_played}")
            print(f"   Your wins: {player_wins}")
            print(f"   Computer wins: {computer_wins}")
            print(f"   Ties: {ties}")
            
            if player_wins > computer_wins:
                print("🏆 You're the overall winner! 🏆")
            elif computer_wins > player_wins:
                print("💻 Computer is the overall winner! 💻")
            else:
                print("🤝 It's an overall tie! 🤝")
                
            print("\nGoodbye! 👋")
            break
        else:
            print("\n" + "="*50)
            print(" " * 15 + "NEW GAME")
            print("="*50)

if __name__ == "__main__":
    tic_tac_toe()