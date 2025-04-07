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

def computer_move(board):
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