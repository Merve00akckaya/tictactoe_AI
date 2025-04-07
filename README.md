# Tic-Tac-Toe AI 🤖

Play the classic game of Tic-Tac-Toe against an intelligent AI opponent powered by a Large Language Model (LLM) via the Groq API! This AI doesn't just make a move; it analyzes the board and provides its reasoning. 🤔

## ✨ Features

*   **Classic Tic-Tac-Toe Gameplay:** Standard 3x3 grid rules.
*   **Human vs. AI:** Play as 'X' against the AI 'O'.
*   **LLM-Powered AI:** Utilizes Groq's fast inference API with the `qwen-2.5-32b` model for strategic decision-making.
*   **AI Reasoning:** The AI explains *why* it chose a specific move, offering insights into its strategy. 🧠
*   **Randomized Start:** Either the Human ('X') or the AI ('O') can start the game randomly.
*   **Clear CLI:** Simple and intuitive command-line interface.
*   **Input Validation:** Prevents invalid moves by the human player.
*   **Win/Tie Detection:** Automatically detects and announces game outcomes. 🏆🤝

## 🛠️ Tech Stack

*   **Python 🐍:** Core programming language.
*   **Langchain (`langchain_groq`) 🦜🔗:** Framework for interacting with the LLM.
*   **Groq API ⚡:** Provides fast LLM inference capabilities.
*   **Pydantic 🤖:** Used for defining the structured output format expected from the LLM.

## ⚙️ Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd tictactoe_AI
    ```

2.  **Install Dependencies:**
    Make sure you have Python 3 installed. Then, install the required packages:
    ```bash
    pip install langchain_groq pydantic groq
    ```
    *(Note: `groq` might be needed directly or as a dependency of `langchain_groq`)*

3.  **Configure API Key 🔑:**
    *   Sign up and get an API key from [GroqCloud](https://console.groq.com/keys).
    *   Open the file `tictactoe_AI/player.py`.
    *   Find the line: `API_KEY="enter your Groq api-key"`
    *   Replace `"enter your Groq api-key"` with your actual Groq API key.
    *   **Important:** Keep your API key secure and do not commit it directly into public repositories. Consider using environment variables or a `.env` file for better security practices in larger projects.

## ▶️ How to Play

1.  **Run the Game:**
    Navigate to the project's root directory (`tictactoe_AI`) in your terminal and run:
    ```bash
    python tictactoe_game.py
    ```

2.  **Follow Prompts:**
    *   The game will display the numbered board layout (1-9).
    *   It will announce whether you ('X') or the Computer ('O') starts.
    *   When it's your turn, enter the number (1-9) corresponding to the empty square where you want to place your 'X'.
    *   When it's the AI's turn, it will pause briefly to think, then print the position it chose and its detailed reasoning.
    *   The game board updates after each move.

3.  **Game End:**
    The game continues until a player gets three in a row (horizontally, vertically, or diagonally) or the board is full (resulting in a tie). The outcome will be announced. 🎉

## 💡 How the AI Works

The AI's logic resides in `player.py`:

1.  **Board Analysis:** The current state of the Tic-Tac-Toe board is formatted.
2.  **Available Moves:** Empty squares are identified as potential moves.
3.  **Prompt Engineering:** A detailed system prompt is constructed and sent to the Groq LLM. This prompt instructs the AI on the rules of Tic-Tac-Toe, its objective ('O'), winning/blocking strategies, and the desired output format (move number and reasoning).
4.  **LLM Interaction:** The `ChatGroq` client (using Langchain) sends the prompt and current game state to the specified LLM (`qwen-2.5-32b`).
5.  **Structured Output:** The LLM is asked to return its response in a specific JSON structure (defined using Pydantic), containing the chosen `move` (1-9) and the `reasoning`.
6.  **Move Execution:** The game script receives the AI's move and reasoning, updates the board, and displays the information to the user.
7.  **Fallback:** Basic error handling is included. If the LLM call fails, the AI defaults to picking the first available move.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.

## 📄 License

This project is likely licensed under the MIT License (or specify your chosen license). You can add a `LICENSE` file to the repository for details.

---

Enjoy playing against the AI!
