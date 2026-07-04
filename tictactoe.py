import streamlit as st
import random

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Tic-Tac-Toe",
    page_icon="🎮",
    layout="centered",
)

# -----------------------------
# Session State Initialization
# -----------------------------
def init_state():
    if "board" not in st.session_state:
        st.session_state.board = [""] * 9
    if "current_player" not in st.session_state:
        st.session_state.current_player = "X"
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "mode" not in st.session_state:
        st.session_state.mode = "Two Player"
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}
    if "winning_cells" not in st.session_state:
        st.session_state.winning_cells = []

init_state()

# -----------------------------
# Helper Functions
# -----------------------------
WINNING_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),              # diagonals
]

def check_winner(board):
    """Return 'X', 'O', 'Draw', or None."""
    for combo in WINNING_COMBOS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], list(combo)
    if all(cell for cell in board):
        return "Draw", []
    return None, []

def minimax(board, depth, is_maximizing, ai_player="O", human_player="X"):
    """Minimax algorithm for unbeatable AI."""
    result, _ = check_winner(board)
    if result == ai_player:
        return 1
    elif result == human_player:
        return -1
    elif result == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = ai_player
                score = minimax(board, depth + 1, False, ai_player, human_player)
                board[i] = ""
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = human_player
                score = minimax(board, depth + 1, True, ai_player, human_player)
                board[i] = ""
                best_score = min(best_score, score)
        return best_score

def get_ai_move(board, ai_player="O", human_player="X"):
    """Get the best move for the AI using minimax."""
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = ai_player
            score = minimax(board, 0, False, ai_player, human_player)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.winning_cells = []

# -----------------------------
# UI: Title & Sidebar
# -----------------------------
st.title("🎮 Tic-Tac-Toe")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Game Settings")
    mode = st.radio(
        "Game Mode",
        ["Two Player", "Play vs AI (Easy)", "Play vs AI (Unbeatable)"],
        index=0,
    )

    if mode != st.session_state.mode:
        st.session_state.mode = mode
        reset_game()

    st.markdown("---")
    st.header("📊 Scoreboard")
    st.markdown(f"**❌ Player X:** {st.session_state.scores['X']}")
    st.markdown(f"**⭕ Player O:** {st.session_state.scores['O']}")
    st.markdown(f"**🤝 Draws:** {st.session_state.scores['Draws']}")

    if st.button("🔄 Reset Scores", use_container_width=True):
        st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}
        st.rerun()

    st.markdown("---")
    st.markdown("### 📜 How to Play")
    st.markdown(
        """
        1. Player **X** always goes first.
        2. Click any empty cell to make your move.
        3. Get **three in a row** (horizontal, vertical, or diagonal) to win!
        """
    )

# -----------------------------
# UI: Status Banner
# -----------------------------
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.success("🤝 It's a Draw!")
    else:
        emoji = "❌" if st.session_state.winner == "X" else "⭕"
        st.success(f"🏆 Player {st.session_state.winner} ({emoji}) Wins!")
else:
    emoji = "❌" if st.session_state.current_player == "X" else "⭕"
    label = "Your" if mode != "Two Player" else "Player"
    st.info(f"🎲 {label} {st.session_state.current_player} ({emoji}) — your turn!")

# -----------------------------
# UI: Game Board (3x3 Grid)
# -----------------------------
def make_move(idx):
    """Handle a player's move."""
    if st.session_state.game_over or st.session_state.board[idx] != "":
        return

    st.session_state.board[idx] = st.session_state.current_player
    winner, winning_cells = check_winner(st.session_state.board)

    if winner:
        st.session_state.game_over = True
        st.session_state.winner = winner
        st.session_state.winning_cells = winning_cells
        if winner == "Draw":
            st.session_state.scores["Draws"] += 1
        else:
            st.session_state.scores[winner] += 1
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# Render board using columns
for row in range(3):
    cols = st.columns(3)
    for col_idx in range(3):
        idx = row * 3 + col_idx
        cell = st.session_state.board[idx]

        # Determine button label and styling
        if cell == "X":
            label = "❌"
        elif cell == "O":
            label = "⭕"
        else:
            label = "　"

        # Highlight winning cells
        is_winning = idx in st.session_state.winning_cells

        with cols[col_idx]:
            if st.button(
                label,
                key=f"cell_{idx}",
                use_container_width=True,
                disabled=st.session_state.game_over or cell != "",
            ):
                make_move(idx)

                # AI Move (if applicable)
                if (
                    not st.session_state.game_over
                    and mode != "Two Player"
                    and st.session_state.current_player == "O"
                ):
                    if mode == "Play vs AI (Easy)":
                        empty_cells = [i for i in range(9) if st.session_state.board[i] == ""]
                        if empty_cells:
                            ai_move = random.choice(empty_cells)
                            make_move(ai_move)
                    elif mode == "Play vs AI (Unbeatable)":
                        ai_move = get_ai_move(st.session_state.board)
                        if ai_move is not None:
                            make_move(ai_move)

                st.rerun()

# -----------------------------
# UI: Reset Button
# -----------------------------
st.markdown("---")
if st.button("🆕 New Game", use_container_width=True, type="primary"):
    reset_game()
    st.rerun()

# -----------------------------
# UI: Reset Button
# -----------------------------
st.markdown("---")
if st.button("🆕 New Game", use_container_width=True, type="primary"):
    reset_game()
    st.rerun()
