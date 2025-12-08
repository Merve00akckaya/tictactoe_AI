from langchain_groq import ChatGroq
from typing import Optional
from pydantic import BaseModel, Field


API_KEY="enter your Groq api-key"


class Output(BaseModel):
    reasoning: str = Field(description="The entire reasoning of why you provide this move")
    move: int = Field(description="The number of your selected move.")
    

llm = ChatGroq(
    model="qwen-2.5-32b",
    temperature=0.6,
    max_tokens=32768,
    api_key=API_KEY
)

def computer_move(board, difficulty="easy"):
    """
    Computer move with difficulty levels
    easy: Uses LLM for moves (original version)
    hard: Uses strategic AI (unbeatable)
    """
    if difficulty == "hard":
        return computer_move_hard(board)
    else:
        return computer_move_easy(board)

def computer_move_easy(board):
    """Original LLM-based version (easy mode)"""
    # Convert board to consistent string representation, handling empty strings
    game_state = []
    for cell in board:
        if isinstance(cell, str):
            stripped = cell.strip()
            if stripped in ('X', 'O'):
                game_state.append(stripped)
            else:
                game_state.append(' ')  # Treat empty string or other values as empty space
        else:
            game_state.append(' ')  # Treat non-string values as empty space
    
    # Get available moves (1-9 where position is empty)
    available_moves = [i+1 for i, cell in enumerate(game_state) if cell == ' ']
    if not available_moves:
        return -1, "No available moves"
    
    # Create the system prompt
    system_prompt = f"""# Tic-Tac-Toe AI Agent ('O') - Optimal Move Generator
    
## Objective
You are an AI that plays Tic-Tac-Toe as 'O' against human 'X'. Analyze the board and return the optimal move (1-9) to win, block, or force a draw.

## Rules
1. Board positions ({available_moves}):
   1 | 2 | 3
   ---------
   4 | 5 | 6
   ---------
   7 | 8 | 9
2. Only suggest empty positions (check carefully!)
3. Available moves: {available_moves}

## Game Fundamentals
### Winning Conditions (for you or opponent):
A player wins by getting 3 of their marks in a row:
- Horizontal: Rows 1-3 (positions 1-3, 4-6, 7-9)
- Vertical: Columns 1-3 (positions 1-4-7, 2-5-8, 3-6-9)
- Diagonal: Two possible (positions 1-5-9 or 3-5-7)

### Blocking Rules:
- If opponent ('X') has 2 in a row with third spot empty, MUST block
- If opponent could create multiple threats, prioritize most dangerous

## Perform a complete strategic analysis:
1. First check for immediate winning moves for O
2. Then check for immediate blocking needs against X
3. Evaluate potential forks and counter-forks
4. Consider optimal positional strategy
5. Select the move with highest strategic value
6. Provide detailed reasoning for your choice and alternatives considered


## Output Format
{{
    "reasoning": "think deeply and provide that thought",
    "your_move": {available_moves}
}}

## Important
- NEVER suggest an occupied position
- Current available moves: {available_moves}
- If board is full, return -1
- Your reasoning should be large and it should cover all the edge cases.
"""
    messages = [
        ("system", system_prompt),
        ("human", f"Current board (X's turn was last):\n"
                  f"{game_state[0]} | {game_state[1]} | {game_state[2]}\n"
                  f"---------\n"
                  f"{game_state[3]} | {game_state[4]} | {game_state[5]}\n"
                  f"---------\n"
                  f"{game_state[6]} | {game_state[7]} | {game_state[8]}"
                  f"\n\nProvide your move from these available moves: {available_moves}. "
                  "Don't provide any move (number) beyond these available moves. "
                  "Think deeply and make a proper plan, then provide the move and the reasoning.")
    ]

    try:
        structured_llm = llm.with_structured_output(Output)
        response = structured_llm.invoke(messages)
        return response.move, response.reasoning
    except Exception as e:
        # Fallback to first available move if LLM fails
        return available_moves[0], f"Error in AI decision: {str(e)}. Using first available move."

def computer_move_hard(board):
    """Strategic AI (hard mode - nearly unbeatable)"""
    # Convert board to consistent string representation
    game_state = []
    for cell in board:
        if isinstance(cell, str):
            stripped = cell.strip()
            if stripped in ('X', 'O'):
                game_state.append(stripped)
            else:
                game_state.append(' ')
        else:
            game_state.append(' ')
    
    available_moves = [i+1 for i, cell in enumerate(game_state) if cell == ' ']
    if not available_moves:
        return -1, "No available moves"
    
    # STRATEGIC MOVE SELECTION - Much smarter AI
    def get_winning_move(player):
        """Check if player can win in next move"""
        wins = [(0,1,2), (3,4,5), (6,7,8),  # rows
                (0,3,6), (1,4,7), (2,5,8),  # columns  
                (0,4,8), (2,4,6)]           # diagonals
        
        for a, b, c in wins:
            if game_state[a] == game_state[b] == player and game_state[c] == ' ':
                return c + 1
            if game_state[a] == game_state[c] == player and game_state[b] == ' ':
                return b + 1
            if game_state[b] == game_state[c] == player and game_state[a] == ' ':
                return a + 1
        return None
    
    def get_fork_move(player):
        """Look for fork opportunities (creating two winning threats)"""
        # Center is key for forks
        if game_state[4] == ' ' and player == 'O':
            return 5
        
        # Corner forks
        corners = [0, 2, 6, 8]
        empty_corners = [c for c in corners if game_state[c] == ' ']
        if len(empty_corners) >= 2:
            for corner in empty_corners:
                # Check if this corner creates multiple threats
                temp_board = game_state.copy()
                temp_board[corner] = player
                threats = 0
                for a, b, c in [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]:
                    line = [temp_board[a], temp_board[b], temp_board[c]]
                    if line.count(player) == 2 and line.count(' ') == 1:
                        threats += 1
                if threats >= 2:
                    return corner + 1
        return None
    
    # 1. WIN: Check if computer can win immediately
    winning_move = get_winning_move('O')
    if winning_move:
        return winning_move, "HARD MODE: I can win the game with this move! 🎯"
    
    # 2. BLOCK: Check if player can win and block them
    block_move = get_winning_move('X')
    if block_move:
        return block_move, "HARD MODE: I need to block your winning move! 🛡️"
    
    # 3. FORK: Create a fork (two winning opportunities)
    fork_move = get_fork_move('O')
    if fork_move:
        return fork_move, "HARD MODE: Creating a fork - now I have two ways to win! 🎯"
    
    # 4. BLOCK FORK: If player is about to create a fork
    player_fork = get_fork_move('X')
    if player_fork:
        # Force them into a defensive move
        edges = [1, 3, 5, 7]
        available_edges = [e for e in edges if game_state[e-1] == ' ']
        if available_edges:
            move = available_edges[0]
            return move, "HARD MODE: Blocking your potential fork with strategic edge move! 🤔"
    
    # 5. CENTER: Take center if available
    if game_state[4] == ' ':
        return 5, "HARD MODE: Taking the center position - most strategic spot! 🎯"
    
    # 6. OPPOSITE CORNER: If player has corner, take opposite
    corners = [(0,8), (2,6), (6,2), (8,0)]
    for player_corner, opposite_corner in corners:
        if game_state[player_corner] == 'X' and game_state[opposite_corner] == ' ':
            return opposite_corner + 1, "HARD MODE: Taking opposite corner from your move! 🔄"
    
    # 7. EMPTY CORNER: Take any empty corner
    empty_corners = [0, 2, 6, 8]
    for corner in empty_corners:
        if game_state[corner] == ' ':
            return corner + 1, "HARD MODE: Taking an empty corner position! 📍"
    
    # 8. EMPTY EDGE: Take any empty edge
    edges = [1, 3, 5, 7]
    for edge in edges:
        if game_state[edge] == ' ':
            return edge + 1, "HARD MODE: Taking an edge position as last option! 📏"
    
    # Fallback (should never reach here)
    return available_moves[0], "HARD MODE: Using first available move as fallback."