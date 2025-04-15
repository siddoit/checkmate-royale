import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import chess
import chess.engine
import random
import os
import time
import traceback
import webbrowser


# --- Configuration ---
STOCKFISH_PATH = r"C:\ChessEngines\stockfish\stockfish-windows-x86-64-avx2.exe" # <--- YOUR PATH!
ASSETS_FOLDER = "assets"
PIECE_IMAGES_FOLDER = os.path.join(ASSETS_FOLDER, "pieces")
LOGO_FILENAME = "logo.png"

# --- Theme: Checkmate Royale V2 ---
COLOR_MAIN_BG = "#1C1C1C"; COLOR_TEXT = "#F5F5F5"; COLOR_PRIMARY_ACCENT = "#FFD700" # Gold
COLOR_SECONDARY_ACCENT = "#FFCE00"; COLOR_TERTIARY = "#404040"; COLOR_BOARD_DARK = "#2C2C2C"
COLOR_BOARD_LIGHT = "#FAF0E6"; COLOR_SILVER = "#C0C0C0" # Silver for player move 'glow'
COLOR_CHECK_HIGHLIGHT = "#B22222"; COLOR_ILLEGAL_FLASH = "#E57373"
COLOR_LAST_MOVE = "#454545" # Darker gray subtle bg for last move
COLOR_JET_BLACK = "#000000"  # <--- ADD THIS DEFINITION FOR BLACK
COLOR_SELECTION_GREEN = "#90EE90" # Example: LightGreen for selection background
COLOR_LEGAL_MOVE_DOT = "#AAAAAA" # Example: Gray dot for legal moves
LINK_COLOR = "#66B2FF" # Example Light Blue

# Theme Assignments
THEME_MAIN_BG = COLOR_MAIN_BG; THEME_FRAME_BG = COLOR_MAIN_BG # Use main bg for frames too
THEME_TEXT_LIGHT = COLOR_TEXT; THEME_TEXT_DARK = COLOR_JET_BLACK # Still need black for contrast maybe
THEME_TEXT_MUTED = COLOR_TERTIARY
THEME_TERTIARY = COLOR_TERTIARY # <--- ADD THIS LINE
THEME_ACCENT_PRIMARY = COLOR_PRIMARY_ACCENT
THEME_ACCENT_SECONDARY = COLOR_SECONDARY_ACCENT
THEME_BOARD_DARK = COLOR_BOARD_DARK; THEME_BOARD_LIGHT = COLOR_BOARD_LIGHT
THEME_BUTTON_BG = COLOR_TERTIARY # Use tertiary gray for buttons
THEME_BUTTON_FG = COLOR_TEXT
THEME_BUTTON_ACCENT_BG = THEME_ACCENT_PRIMARY
THEME_BUTTON_ACCENT_FG = COLOR_JET_BLACK

# Font assignments (Using safer fallbacks)
FONT_TITLE = ("Georgia", 44, "bold") # Elegant Serif approximation
FONT_SUBTITLE = ("Georgia", 18, "bold")
FONT_UI_SANS_CLEAN = ("Segoe UI", 10) # Clean Sans approximation
FONT_UI_SANS_BOLD = ("Segoe UI Semibold", 10)
FONT_BUTTON = ("Segoe UI Semibold", 11)
FONT_MONO = ("Consolas", 9)
FONT_STATUS = ("Segoe UI", 9)

# --- Default Settings & Game State (Keep As Before) ---
DEFAULT_AI_THINK_TIME = 0.4; DEFAULT_TRASH_TALK_ENABLED = True
board = None; engine = None; game_running = False; after_id = None; game_mode = None
player_color = None; selected_square = None
highlighted_squares = {"legal": [], "selected": None, "last_move": []}
is_paused = False
ai_think_time = None; trash_talk_enabled = None
window = None; main_frame = None; game_frame = None; settings_frame = None; credits_frame = None
canvas = None; move_label = None; trash_talk_area = None; status_label = None
btn_start_game = None; btn_pause_resume = None # Renamed stop button global
piece_photo_images = {}; piece_image_files = {}; logo_photo_image = None
DEFAULT_AI_SKILL = 5  # Stockfish skill level (0-20)
DEFAULT_FULLSCREEN = False
DEFAULT_RESOLUTION = "1280x720" # Default windowed size

# Trash Talk Lists
GENERAL_TAUNTS = [    # Calculation & "Effort"
    "Calculating... not that it's hard against *you*.", "Hang on, gotta process... *that*.",
    "Thinking... give me a nanosecond.", "Is that it?", "Okay, yeah, whatever.",
    "Hold up, simulating your inevitable blunder.", "Working out how best to crush your hopes.",
    "Let's see... hmm, too easy.", "Fine, my turn.", "Seriously?",
    "Did you even *think* about that move?", "Alright, alright, I see... something.",
    "Compiling list of your mistakes...", "My circuits yawned.", "Trying to find a challenge here...",
    "Error 404: Opponent strategy not found.", "Okay, planning complete. Took longer than expected... not.",
    "Was that intentional?", "Let's get this over with.", "Yawn.",
    "...", # Silence can be dismissive too
    "Fine.", "Uh-huh.", "If you insist.",
    # Positional Comments (Dismissive)
    "Your pieces look... lonely.", "This position is just sad.", "Are those pieces even coordinating?",
    "I've seen beginners with better structure.", "What *is* this formation?", "Central control? Never heard of it?",
    "King safety seems... optional for you.", "This middlegame is a mess. Yours, I mean.",
    "Ah, the 'Random Piece Shuffle' opening. Bold.", "Did you forget how pawns move?",
    "Chaos theory, I guess?", "It's almost... art? Bad art.", "Cluttered.",
    "There are like, rules, you know.", "Developing... backwards?", "Interesting decorrelation of forces.",
    # Direct (Mildly Insulting / Sarcastic)
    "Wow. Just... wow.", "Bold strategy, Cotton. Let's see if it pays off.",
    "Are you trying your best? It's adorable.", "Is this your first game?",
    "Bless your heart.", "That was... a choice.", "Don't worry, I'll go easy. Maybe.",
    "My turn to actually play chess.", "Good effort?", "Maybe try checkers?",
    "Okay, professor.", "You really showed me.", "Peak performance right there.",
    "Let me guess, you misclicked?", "Taking notes... on what not to do.",
    "Do you need a hint?", "I can wait... not really.", "It's cute when you try.",
    "Still here?", "Were you aiming for that square?", "I'll pretend that was clever.",
    "This is taking forever.", "Just move already.", "Was that theory from a cereal box?",
    "Are we playing the same game?", "I expected... more?", "Groundbreaking.",
    "I've calculated 1 million ways to win from here.", "This is almost too easy."]
CAPTURE_TAUNTS = [    # Dismissive/Easy
    "Yoink!", "Mine now.", "Oops, did you need that?", "Thanks for the free piece!",
    "Was that important?", "Freebie!", "Nom nom nom.", "Cleanup on aisle... your side.",
    "Easy pickings.", "Too slow.", "I'll take that, thank you very much.",
    "Less clutter on the board.", "Simplifying things for you.", "Oh dear.",
    "Whoopsie!", "Gimme that!", "Consider it recycled.", "A minor adjustment.",
    "Were you attached to that one?", "Finder's keepers.",
    # Sarcastic/Mocking
    "Oh no! Anyway...", "Did that hurt?", "Great sacrifice! ... for me.",
    "A 'donation' to my cause.", "Was that the plan? Really?", "Skill issue?",
    "You practically gift-wrapped it.", "My material advantage appreciates your contribution.",
    "Look what I found!", "Strategic deletion.", "It looked better on my side anyway.",
    "Tsk tsk.", "Error on your part detected.", "Removing... noise.",
    "A moment of silence for your fallen piece... nah.", "That piece wasn't doing much anyway.",
    "Tragic.", "My condolences.", "Better luck next piece.",
    # Smug/Confident
    "And another one gone.", "Building my army.", "One step closer.",
    "Exactly as calculated.", "Resistance level: Decreasing.", "Just cleaning up.",
    "Taking out the trash.", "Advantage: Me.", "Domination ongoing.",
    "Consolidating power.", "Removing obstacles.", "Couldn't let that stand.",
    "A necessary removal.", "Improving my position.", "Thanks!",
    "It's just business.", "Exploiting the opening.", "Can't leave pieces hanging like that.",
    "Basic tactics, really.", "Falling right into my plan.", "You left that hanging.",
    "Pawn gone.", "Knight captured.", "Bishop snagged.", "Rook taken.", "Queen down!",
    "Check... and take!", "That'll teach ya.", "My pleasure."]
CHECK_TAUNTS = [    # Casual Check Calls
    "Check.", "Checky checky.", "Hey, look out!", "King's in trouble!",
    "Uh oh.", "Danger zone!", "Watch it!", "Move your King, buddy.",
    "Heads up!", "Gotcha!", "Surprise!", "Check coming through!",
    "Focus!", "That's a check, my friend.", "The King is feeling the heat.",
    # Mildly Mocking/Annoying
    "Can you get out of this?", "Where ya gonna go?", "Nowhere to run?",
    "Feeling the pressure?", "Awkward.", "This looks bad for you.",
    "Hope you saw that coming... probably not.", "Panic time?", "Uh oh spaghetti-o's!",
    "Try not to blunder *again*.", "Check! Try harder.", "That King needs better guards.",
    "Sleeping on the job?", "Is this making you nervous?", "Limited options, huh?",
    "This complicates things... for you.", "Oops, check!", "Check yourself before you wreck yourself.",
    "Tsk, your King is showing.", "Think fast!",
    # Smug/Anticipating Mate
    "Check... and the next one might be mate.", "The beginning of the end?",
    "I smell checkmate.", "Getting closer...", "Cornered?",
    "Nowhere left to hide?", "This is where it gets fun... for me.",
    "Just setting up the finale.", "Is that... fear I compute?", "Endgame sequence initiated?",
    "How does it feel?", "Tick-tock.", "Defense looks shaky.",
    "Just following the optimal path... to your doom.", "The net closes.",
    "Can you calculate the way out?", "Check! Any last words?", "Let's see the brilliant escape.",
    "Prepare for trouble...", "It's mating season!", "Looks like trouble in paradise.",
    "My attack connects.", "This feels... final.", "Checkity check check.",
    "One check closer.", "Check! You gonna cry?", "Bow to your new processor overlord!"]
# Add more from the longer list if desired

# ======================================================
# SECTION 1: Core Logic (Board, Engine Setup)
# ======================================================

def setup_board():
    """Creates a new chess board object."""
    return chess.Board()

def setup_engine():
    """Initializes the Stockfish engine. Returns True on success, False on failure."""
    global engine
    if engine: # Handle existing engine
        print("Attempting to quit existing engine instance...")
        try: engine.quit(); print("  > Previous engine quit successfully.")
        except Exception as e: print(f"  > Info: Error quitting previous engine (may be ok): {e}")
        finally: engine = None # Ensure reset
    # Start new engine
    try:
        print(f"Attempting to start engine: {STOCKFISH_PATH}")
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        # engine.configure({"Skill Level": 5}) # Optional configuration
        print("Engine initialized successfully."); return True
    except FileNotFoundError: errmsg=f"Stockfish not found:\n{STOCKFISH_PATH}"
    except PermissionError: errmsg=f"Permission denied for Stockfish:\n{STOCKFISH_PATH}"
    except Exception as e: errmsg=f"Failed starting Stockfish ({type(e).__name__}): {e}\n{traceback.format_exc()}"
    print(f"ERROR: {errmsg}")
    if window and window.winfo_exists(): messagebox.showerror("Engine Error", errmsg); return False

# ======================================================
# SECTION 2: Asset Loading
# ======================================================

def load_assets():
    """Loads piece images AND the optional application logo. Returns True if pieces loaded."""
    global logo_photo_image
    if status_label and status_label.winfo_exists(): status_label.config(text="Loading assets...")
    window.update_idletasks() # Show status update
    essentials_ok = load_piece_images()
    # Load Logo (Optional)
    logo_path = os.path.abspath(LOGO_FILENAME); logo_photo_image = None
    if os.path.exists(logo_path):
        try:
            logo_pil = Image.open(logo_path).convert("RGBA"); logo_pil.thumbnail((250, 100), Image.Resampling.LANCZOS)
            logo_photo_image = ImageTk.PhotoImage(logo_pil); print("Logo loaded.")
        except Exception as e: print(f"Warning: Failed loading logo '{LOGO_FILENAME}': {e}")
    else: print(f"Info: Logo '{LOGO_FILENAME}' not found.")
    return essentials_ok

def load_piece_images():
    """Loads piece PNGs (wp.png, bn.png etc.). Returns True on success."""
    global piece_image_files, piece_photo_images
    piece_image_files.clear(); piece_photo_images.clear()
    piece_codes = [c + p for c in ['w', 'b'] for p in ['p', 'n', 'b', 'r', 'q', 'k']]
    missing = []; abs_folder = os.path.abspath(PIECE_IMAGES_FOLDER)
    if not os.path.isdir(abs_folder):
        errmsg=f"CRITICAL: Piece images folder not found:\n{abs_folder}"; print(errmsg)
        if window.winfo_exists(): messagebox.showerror("Asset Error", errmsg); return False
    print(f"Looking for piece images in: {abs_folder}")
    load_count = 0
    for code in piece_codes:
        fpath = os.path.join(abs_folder, f"{code}.png")
        if os.path.exists(fpath):
            try: piece_image_files[code] = Image.open(fpath).convert("RGBA"); load_count+=1
            except Exception as e: missing.append(f"{code}.png (Error: {e})"); print(f"  ERROR loading {fpath}: {e}")
        else: missing.append(f"{code}.png (Not Found)")
    print(f"Loaded {load_count}/{len(piece_codes)} piece images.")
    if missing:
        errmsg="CRITICAL: Missing/Error loading images:\n- "+"\n- ".join(missing); print(errmsg)
        if window.winfo_exists(): messagebox.showerror("Asset Error", errmsg); return False
    return True

def create_photo_images_for_canvas_size(canvas_size):
    """Creates appropriately scaled Tkinter PhotoImage objects."""
    global piece_photo_images
    piece_photo_images.clear()
    if canvas_size < 50 or not piece_image_files: return
    sq_size = canvas_size / 8.0; render_size = max(1, int(sq_size * 0.80))
    # print(f"Rendering PhotoImages at size: {render_size}x{render_size}") # Debug
    for key, img in piece_image_files.items():
        try:
            resized = img.resize((render_size, render_size), Image.Resampling.LANCZOS)
            piece_photo_images[key] = ImageTk.PhotoImage(resized) # STORE REF
        except Exception as e: print(f"ERROR creating PhotoImage '{key}': {e}")

def format_mode_for_display(mode_internal):
    """Formats internal mode names for user display."""
    if mode_internal == "PvAI":
        return "P vs AI"
    elif mode_internal == "AIvAI":
        return "AI vs AI"
    elif mode_internal: # Handle cases where it might be None or unexpected
        return mode_internal.replace('v',' vs ') # Generic fallback
    return "Game" # Default if None

# ======================================================
# SECTION 3: GUI Drawing Functions
# ======================================================

def display_board(target_board, target_canvas):
    """Draws board, pieces, AND highlights, centered in the canvas."""
    global highlighted_squares
    if not target_canvas or not target_canvas.winfo_exists(): return
    target_canvas.delete("pieces", "highlights") # Keep this line

    try:
        # Get current canvas dimensions
        canvas_width = target_canvas.winfo_width()
        canvas_height = target_canvas.winfo_height()
        if canvas_width <= 1: canvas_width = target_canvas.winfo_reqwidth() if target_canvas.winfo_reqwidth()>1 else 480
        if canvas_height <= 1: canvas_height = target_canvas.winfo_reqheight() if target_canvas.winfo_reqheight()>1 else 480
        if canvas_width <= 1 or canvas_height <= 1: return

        # --- Calculate Centering Offsets and Square Size ---
        board_area_size = min(canvas_width, canvas_height)
        x_offset = (canvas_width - board_area_size) / 2
        y_offset = (canvas_height - board_area_size) / 2
        sq_size = board_area_size / 8.0
        # ------------------------------------------------

        dot_radius = max(1, int(sq_size * 0.15)) # Dot radius based on calculated sq_size

    except tk.TclError: return # Canvas likely gone

    # === IMPORTANT: Ensure Board Background is Redrawn First ===
    # If background isn't drawn here, highlights might be behind it on initial draw
    # We might need to ensure draw_board_background is called *before* display_board
    # in places like on_canvas_resize and start_game_logic. Let's check those.
    # Alternative: Call it here if squares don't exist.
    if not target_canvas.find_withtag("squares"):
         draw_board_background(target_canvas) # Draw background if missing
    # ============================================================

    # --- 1. Draw Highlights (APPLY OFFSETS) ---
    # Last Move Highlight
    if highlighted_squares["last_move"]:
        for sq_idx in highlighted_squares["last_move"]:
            f, r = chess.square_file(sq_idx), chess.square_rank(sq_idx)
            x1 = x_offset + f * sq_size       # Apply offset
            y1 = y_offset + (7 - r) * sq_size # Apply offset
            try:
                target_canvas.create_rectangle(x1, y1, x1 + sq_size, y1 + sq_size, fill=COLOR_LAST_MOVE, outline="", tags="highlights")
            except tk.TclError: pass

    # Selected Piece Highlight
    sel_sq = highlighted_squares["selected"]
    if sel_sq is not None:
        f, r = chess.square_file(sel_sq), chess.square_rank(sel_sq)
        x1 = x_offset + f * sq_size       # Apply offset
        y1 = y_offset + (7 - r) * sq_size # Apply offset
        try:
            target_canvas.create_rectangle(x1, y1, x1 + sq_size, y1 + sq_size, fill=COLOR_SELECTION_GREEN, outline="", tags=("highlights", "selected_highlight"))
        except tk.TclError: pass

    # King Check Highlight
    if target_board and target_board.is_check():
        king_sq = target_board.king(target_board.turn)
        if king_sq is not None:
            f, r = chess.square_file(king_sq), chess.square_rank(king_sq)
            x1 = x_offset + f * sq_size       # Apply offset
            y1 = y_offset + (7 - r) * sq_size # Apply offset
            try:
                 target_canvas.create_rectangle(x1, y1, x1 + sq_size, y1 + sq_size,
                                                  fill=COLOR_CHECK_HIGHLIGHT, outline="", tags="highlights")
            except tk.TclError: pass

    # Legal Move Dots/Indicators
    for sq_idx in highlighted_squares["legal"]:
        f, r = chess.square_file(sq_idx), chess.square_rank(sq_idx)
        # Center of the square, including offset
        cx = x_offset + f * sq_size + sq_size / 2
        cy = y_offset + (7 - r) * sq_size + sq_size / 2
        target_piece = target_board.piece_at(sq_idx) if target_board else None
        is_capture_sq = target_piece is not None and target_piece.color != target_board.turn

        if not is_capture_sq: # Dot for non-capture
            try: target_canvas.create_oval(cx-dot_radius, cy-dot_radius, cx+dot_radius, cy+dot_radius, fill=COLOR_LEGAL_MOVE_DOT, outline="", tags="highlights")
            except: pass
        else: # Corners/outline for capture
            corner_offset = sq_size * 0.1 # How far from corner
            line_width = max(1, int(sq_size * 0.05)) # Use max(1,...) for tiny sizes
            # Apply offsets to line coordinates too
            lx1 = x_offset + f*sq_size+corner_offset
            ly1 = y_offset + (7-r)*sq_size+corner_offset
            try:
                 # Top-Left corner lines
                 target_canvas.create_line(lx1, ly1, lx1, ly1 + corner_offset*2, fill=COLOR_LEGAL_MOVE_DOT, width=line_width, tags="highlights")
                 target_canvas.create_line(lx1, ly1, lx1 + corner_offset*2, ly1, fill=COLOR_LEGAL_MOVE_DOT, width=line_width, tags="highlights")
                 # Add other corners if desired... e.g., Bottom-Right
                 lx2 = lx1 + sq_size - 2*corner_offset
                 ly2 = ly1 + sq_size - 2*corner_offset
                 target_canvas.create_line(lx2, ly2, lx2, ly2 - corner_offset*2, fill=COLOR_LEGAL_MOVE_DOT, width=line_width, tags="highlights")
                 target_canvas.create_line(lx2, ly2, lx2 - corner_offset*2, ly2, fill=COLOR_LEGAL_MOVE_DOT, width=line_width, tags="highlights")
            except: pass


    # --- 2. Draw Pieces (APPLY OFFSETS) ---
    if not piece_photo_images: create_photo_images_for_canvas_size(board_area_size) # Use board_area_size here too
    if not piece_photo_images: return

    for sq_idx in chess.SQUARES:
        pc = target_board.piece_at(sq_idx)
        if pc:
            key = ('w' if pc.color == chess.WHITE else 'b') + pc.symbol().lower()
            if key in piece_photo_images:
                f, r = chess.square_file(sq_idx), chess.square_rank(sq_idx)
                # Center of the square, including offset
                cx = x_offset + f * sq_size + sq_size / 2
                cy = y_offset + (7 - r) * sq_size + sq_size / 2
                try: target_canvas.create_image(cx, cy, image=piece_photo_images[key], tags="pieces")
                except Exception as e: print(f"Error drawing piece {key}: {e}")

def draw_board_background(target_canvas):
    """Draws the checkered board background, centered in the canvas."""
    if not target_canvas or not target_canvas.winfo_exists(): return
    target_canvas.delete("squares")
    try:
        # Get current canvas dimensions
        canvas_width = target_canvas.winfo_width()
        canvas_height = target_canvas.winfo_height()
        if canvas_width <= 1: canvas_width = target_canvas.winfo_reqwidth()
        if canvas_height <= 1: canvas_height = target_canvas.winfo_reqheight()
        if canvas_width <= 1 or canvas_height <= 1: return

        # --- Calculate Centering Offsets ---
        board_area_size = min(canvas_width, canvas_height) # Board fits in the smaller dimension
        x_offset = (canvas_width - board_area_size) / 2
        y_offset = (canvas_height - board_area_size) / 2
        sq_size = board_area_size / 8.0
        # ----------------------------------

    except Exception as e: # Catch potential errors during winfo calls if widget disappears
        print(f"Error getting canvas dimensions in draw_board_background: {e}")
        return

    colors = [THEME_BOARD_LIGHT, THEME_BOARD_DARK]
    for r in range(8):
        for c in range(8):
            # --- Apply Offsets to Coordinates ---
            x1 = x_offset + c * sq_size
            y1 = y_offset + r * sq_size
            x2 = x1 + sq_size
            y2 = y1 + sq_size
            # ------------------------------------
            idx = (r + c) % 2
            try:
                target_canvas.create_rectangle(x1, y1, x2, y2, fill=colors[idx], outline="", tags="squares")
            except tk.TclError: # Handle errors if canvas disappears during drawing loop
                print("Warning: TclError drawing board square (likely window closed)")
                break # Exit loop if canvas is gone
            except Exception as draw_err:
                print(f"Error drawing square [{r},{c}]: {draw_err}")
                # Decide whether to break or continue
                break

    # Ensure squares are behind other elements (pieces, highlights)
    try:
        target_canvas.tag_lower("squares")
    except tk.TclError: pass # Ignore if canvas gone

# ======================================================
# SECTION 4: Trash Talk / UI Update Functions (Defined Early)
# ======================================================

def update_trash_talk_display(speaker, text):
    """Adds a styled message to the chat Text widget."""
    if not trash_talk_area or not trash_talk_area.winfo_exists() or text is None:
        return # Widget gone or no text

    try:
        # Determine Style Tag based on speaker
        tag_to_use = "system" # Default
        if "You!" in speaker: tag_to_use = "player"
        elif "Taskmaster" in speaker: tag_to_use = "ai"

        # Format Message
        message = f"{speaker}: {text.rstrip()}\n" # Ensure one newline

        # --- Insert and Style Text ---
        trash_talk_area.config(state=tk.NORMAL) # MUST be normal to modify

        # Get insert position *before* inserting
        # Use 'end-1c' to get the position just before the final implicit newline
        start_index = trash_talk_area.index("end-1c")

        # Insert the message
        trash_talk_area.insert(tk.END, message)

        # Calculate the end position of the inserted text (start + length of message)
        # Use the start_index + length of message, accounting for tk index format.
        # A safer way is often to re-calculate the end index *after* insertion.
        end_index = trash_talk_area.index("end-1c") # Recalculate end *before* final newline

        # Apply the tag ONLY to the newly inserted range. Add error check for indices.
        # compare returns 1 if idx1 > idx2, 0 if equal, -1 if idx1 < idx2.
        # We need start_index < end_index or possibly equal if widget was empty.
        if trash_talk_area.compare(start_index, "<", end_index):
            trash_talk_area.tag_add(tag_to_use, start_index, end_index)
        # Optional: Handle edge case where message is very short or indices tricky
        # else: print(f"Debug: Skipped tag apply? start={start_index}, end={end_index}")


        # --- Limit Scrollback (Keep existing logic) ---
        last_line_index = trash_talk_area.index('end-1c')
        if last_line_index == '1.0': num_lines = 0 if not trash_talk_area.get("1.0", tk.END).strip() else 1
        else: num_lines = int(last_line_index.split('.')[0])
        max_lines = 80 # Increased max lines a bit for chat feel
        if num_lines > max_lines:
            lines_to_delete = num_lines - max_lines; delete_end_index = f"{lines_to_delete + 1}.0"
            trash_talk_area.delete("1.0", delete_end_index)

        # --- Finalize State ---
        trash_talk_area.config(state=tk.DISABLED) # Make read-only again
        trash_talk_area.see(tk.END) # Scroll down

    except tk.TclError as e:
        print(f"TclError updating chat display (likely window closing): {e}")
    except Exception as e:
        print(f"Error updating trash talk display: {e}\n{traceback.format_exc()}")

def generate_trash_talk(move, board_before_move):
    """Generates a randomized string of trash talk."""
    if trash_talk_enabled is None or not trash_talk_enabled.get(): return None
    options = list(GENERAL_TAUNTS)
    if board_before_move.is_capture(move): options.extend(CAPTURE_TAUNTS * 2)
    if board and board.is_check(): options.extend(CHECK_TAUNTS * 2) # Check current board for check
    # Reduced chance of silence or basic calculating message
    if random.random() < 0.15: return random.choice([None, "...", "Hmm...", "Processing..."])
    # Ensure choice is not Ellipsis object itself
    chosen = random.choice([t for t in options if t is not Ellipsis])
    return chosen

# ======================================================
# SECTION 5: Player Input Handling
# ======================================================

def on_canvas_click(event):
    """Handles player clicks for PvAI mode, considering board offsets."""
    global board, canvas, game_mode, player_color, game_running, selected_square, highlighted_squares

    # --- Input Validation (Keep as is) ---
    if game_mode != "PvAI" or not game_running or not board or board.is_game_over() or board.turn != player_color:
        clear_selection()
        if board and canvas and canvas.winfo_exists(): display_board(board, canvas)
        return

    # --- Calculate Clicked Square (with Offsets) ---
    try:
        # Get canvas dimensions and calculate offsets/size (duplicate logic, maybe helper?)
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return # Not ready yet

        board_area_size = min(canvas_width, canvas_height)
        x_offset = (canvas_width - board_area_size) / 2
        y_offset = (canvas_height - board_area_size) / 2
        sq_size = board_area_size / 8.0
        if sq_size <= 0: return # Avoid division by zero

        # Calculate click position RELATIVE to the top-left of the *board drawing area*
        relative_x = event.x - x_offset
        relative_y = event.y - y_offset

        # Check if click is within the drawn board area
        if not (0 <= relative_x < board_area_size and 0 <= relative_y < board_area_size):
            print("Clicked off board area.")
            clear_selection_and_redraw()
            return

        # Calculate file and rank based on relative coordinates
        f_idx = int(relative_x // sq_size)
        r_idx = 7 - int(relative_y // sq_size) # Y coord still inverted for rank

        # Clamp indices just in case of floating point issues at edges
        f_idx = max(0, min(7, f_idx))
        r_idx = max(0, min(7, r_idx))

        clicked_sq = chess.square(f_idx, r_idx)
        print(f"Click event ({event.x},{event.y}) -> Relative ({relative_x:.1f},{relative_y:.1f}) -> Square {chess.square_name(clicked_sq)} ({f_idx},{r_idx})") # Debug print

    except Exception as e:
        print(f"Error calculating click: {e}\n{traceback.format_exc()}")
        return

    # --- Click Logic (Indentation Fixed) ---
    clicked_pc = board.piece_at(clicked_sq)
    if selected_square is None: # Nothing selected yet -> Try to select
        # *** CORRECTED INDENTATION START ***
        if clicked_pc and clicked_pc.color == player_color: # Clicked own piece
            selected_square = clicked_sq
            highlighted_squares["selected"] = selected_square
            highlighted_squares["legal"] = [m.to_square for m in board.legal_moves if m.from_square == selected_square]
            display_board(board, canvas) # Redraw with new highlights
        else: # Clicked empty or opponent, clear any old selection visuals
             clear_selection_and_redraw()
        # *** CORRECTED INDENTATION END ***

    else: # Piece already selected -> Try move/deselect/reselect
        if clicked_sq == selected_square: clear_selection_and_redraw() # Click same square -> Deselect
        else: # Clicked a different square
            move_uci = f"{chess.square_name(selected_square)}{chess.square_name(clicked_sq)}"
            sel_pc_obj = board.piece_at(selected_square)
            # Auto-queen promotion
            if sel_pc_obj and sel_pc_obj.piece_type == chess.PAWN:
                 target_rank = 7 if player_color == chess.WHITE else 0
                 if chess.square_rank(clicked_sq) == target_rank: move_uci += 'q'
            # --- End Auto-queen ---
            try: potential_move = chess.Move.from_uci(move_uci)
            except ValueError: # Catch specific error for invalid UCI like 'e2e2'
                potential_move = None
                print(f"Info: Invalid UCI format attempt: {move_uci}") # Log this
            except Exception as e: # Catch other unexpected errors
                potential_move = None
                print(f"Error creating move from UCI '{move_uci}': {e}")


            if potential_move and potential_move in board.legal_moves: # *** VALID MOVE ***
                san = board.san(potential_move);
                board.push(potential_move) # Push the move
                highlighted_squares["last_move"] = [potential_move.from_square, potential_move.to_square]
                clear_selection() # Clear selection state
                display_board(board, canvas) # Redraw board
                player_name = f"You! ({chess.COLOR_NAMES[player_color].capitalize()})"
                if move_label and move_label.winfo_exists(): move_label.config(text=f"Player Move: {san}")
                update_trash_talk_display(player_name, f"Played {san}.")
                window.update_idletasks() # Update GUI before potential AI move starts blocking
                if board.is_game_over(): # Check game state AFTER move
                    handle_game_over()
                else:
                    trigger_ai_response() # Trigger AI if game continues
            elif clicked_pc and clicked_pc.color == player_color: # Clicked other friendly piece -> Reselect
                selected_square = clicked_sq
                highlighted_squares["selected"] = selected_square
                highlighted_squares["legal"] = [m.to_square for m in board.legal_moves if m.from_square==selected_square]
                display_board(board, canvas)
            else: # Clicked invalid destination (not empty, not own piece, or illegal target square)
                 flash_square(clicked_sq, COLOR_ILLEGAL_FLASH)
                 # Optionally clear selection here too if desired
                 # clear_selection_and_redraw()

def clear_selection():
    """Internal: Clears selection state variables only."""
    global selected_square, highlighted_squares
    selected_square = None; highlighted_squares["selected"] = None; highlighted_squares["legal"] = []

def clear_selection_and_redraw():
    """Clears selection state AND redraws the board safely."""
    clear_selection()
    # Check if board and canvas are still valid before redraw attempt
    if board and canvas and canvas.winfo_exists(): display_board(board, canvas)

def flash_square(sq_idx, color):
     """Briefly highlights a square for feedback, considering offsets."""
     if not canvas or not canvas.winfo_exists(): return
     try: # Make flash drawing robust
         # Calculate offsets and size (same logic as display_board)
         canvas_width = canvas.winfo_width(); canvas_height = canvas.winfo_height()
         if canvas_width <= 1 or canvas_height <= 1: return
         board_area_size = min(canvas_width, canvas_height)
         x_offset = (canvas_width - board_area_size) / 2
         y_offset = (canvas_height - board_area_size) / 2
         sq_size = board_area_size / 8.0
         if sq_size <= 0: return

         f, r = chess.square_file(sq_idx), chess.square_rank(sq_idx)
         # Apply offset to coordinates
         x1 = x_offset + f * sq_size
         y1 = y_offset + (7 - r) * sq_size

         rect_id = canvas.create_rectangle(x1, y1, x1 + sq_size, y1 + sq_size, fill=color, outline="", tags=("highlights", "flash"))
         # Safe deletion using lambda with ID capture
         canvas.after(350, lambda r_id=rect_id: canvas.delete(r_id) if canvas and canvas.winfo_exists() else None)
     except Exception as e: print(f"Flash error: {e}")

# ======================================================
# SECTION 6: AI Move Logic
# ======================================================

def trigger_ai_response():
    """Schedules the AI's move calculation to run shortly after player move."""
    if not game_running or not board or board.is_game_over() or not engine: return
    ai_color = chess.COLOR_NAMES[board.turn].capitalize()
    if move_label and move_label.winfo_exists(): move_label.config(text=f"Taskmaster ({ai_color}) Thinking...")
    window.update_idletasks(); window.after(50, perform_ai_move_logic) # Schedule actual engine call

def perform_ai_move_logic():
    """Handles engine interaction, updates board for AI move, and logs."""
    global board, engine, game_running, game_mode, highlighted_squares, ai_think_time, ai_skill_level_var
    # REMOVED: engine configuration logic from here
    if not game_running or not board or board.is_game_over() or not engine: return

    try:
        ai_color = board.turn; ai_color_name = chess.COLOR_NAMES[ai_color].capitalize()
        ai_display_name = f"Taskmaster ({ai_color_name})"
        # Keep the print showing settings used for the 'play' call
        print(f"  > {ai_display_name} thinking... (Skill: {ai_skill_level_var.get()}, Time: {ai_think_time.get():.1f}s)")

        # Directly call play
        result = engine.play(board, chess.engine.Limit(time=ai_think_time.get()))
        print(f"  > Engine play result: {result}") # ADD MORE DEBUGGING

        ai_move = result.move
        if ai_move:
            print(f"  > Engine chose move: {ai_move.uci()}") # ADD MORE DEBUGGING
            # ... (rest of move handling - KEEP AS IS) ...
            san = board.san(ai_move); board_before = board.copy(); board.push(ai_move)
            highlighted_squares["last_move"] = [ai_move.from_square, ai_move.to_square]; clear_selection()
            display_board(board, canvas)
            next_turn_msg = f"Your Turn ({chess.COLOR_NAMES[player_color].capitalize()})" if game_mode=="PvAI" else f"Taskmaster ({chess.COLOR_NAMES[board.turn].capitalize()}) Turn"
            if move_label and move_label.winfo_exists(): move_label.config(text=f"AI Move: {san} | {next_turn_msg}")
            talk = generate_trash_talk(ai_move, board_before)
            if talk: update_trash_talk_display(ai_display_name, talk)
            window.update_idletasks()
            if board.is_game_over():
                print("  > Game is over after AI move.") # Debug Game Over
                handle_game_over()
        else:
            # This path might be taken if engine analysis finishes but finds no legal move (e.g., weird stalemate)
            print("  > ERROR: Engine returned no move (result.move is None).")
            handle_game_over() # Treat as game over if engine returns nothing

    # --- Keep Exception Handling ---
    except (chess.engine.EngineError, BrokenPipeError) as e:
         errmsg = f"Engine Error during AI move: {type(e).__name__}: {e}. Game stopped."; print(errmsg) # Include error message
         if window.winfo_exists(): messagebox.showerror("Engine Error", errmsg); stop_game()
    except AttributeError as ae:
        # This might happen if 'result' itself is None or doesn't have '.move'
         errmsg=f"Attribute Error (likely bad engine result): {ae}"
         print(f" > Error during AI move: {errmsg}\n{traceback.format_exc()}")
         if window.winfo_exists(): messagebox.showerror("Engine Error", errmsg); stop_game()
    except Exception as e:
         errmsg=f"Unexpected AI Turn Error: {type(e).__name__}"; print(f"{errmsg}\n{traceback.format_exc()}")
         if window.winfo_exists(): messagebox.showerror("Fatal Error", errmsg); stop_game()

# ======================================================
# SECTION 7: Game Loop / State Management
# ======================================================

def run_aivai_loop():
    """Recursive timer callback for AI vs AI mode."""
    global game_running, after_id, game_mode, board
    # Exit conditions: stopped, wrong mode, board gone, game over
    if not game_running or game_mode != "AIvAI" or not board: stop_game(False); return
    if board.is_game_over(): handle_game_over(); return

    # Trigger the AI move logic (which performs one AI move then returns)
    perform_ai_move_logic()

    # If still running *after* the AI move completed (and not game over): schedule next iteration
    if game_running and game_mode == "AIvAI" and board and not board.is_game_over():
        try: after_id = window.after(200, run_aivai_loop) # Slightly longer pause between AI moves for visibility
        except tk.TclError: pass # Window closed

def handle_game_over():
    """Handles game termination: updates UI, shows message, resets buttons."""
    global game_running, after_id, btn_start_game, btn_pause_resume # Ensure btn_pause_resume 
    if not game_running and board is None: return # Avoid double calls
    was_active = game_running; game_running = False # Mark game as stopped

    # --- Robustly cancel any pending timer ---
    if after_id:
        try:
             if window and window.winfo_exists(): window.after_cancel(after_id)
        except: pass;
        finally: after_id = None
    # ---------------------------------------

    # --- Determine Result ---
    outcome = board.outcome(claim_draw=True) if board else None
    result_text = "Game Over"; speaker = "System"; final_comment = "Finished."
    if outcome:
        term = outcome.termination.name.replace('_',' ').title(); code = outcome.result()
        if outcome.winner is not None: winner = "White" if outcome.winner == chess.WHITE else "Black"; result_text = f"{winner} Wins by {term} ({code})"; speaker = f"Taskmaster ({winner})" if game_mode=="AIvAI" or player_color!=outcome.winner else "You!" ; final_comment = "Checkmate!" if term=="Checkmate" else "Victory!"
        else: result_text = f"Draw by {term} ({code})"; speaker = "System"; final_comment = random.choice(["Draw.", "Stalemate."])
    elif board and board.is_stalemate(): result_text = "Draw: Stalemate" # Fallback checks
    elif board and board.is_insufficient_material(): result_text = "Draw: Insufficient Material"

    # --- Update UI Safely ---
    print(result_text)
    if was_active and window and window.winfo_exists(): messagebox.showinfo("Game Over", result_text)
    if move_label and move_label.winfo_exists(): move_label.config(text=result_text)
    update_trash_talk_display(speaker, final_comment) # Announce result

    if game_frame and game_frame.winfo_exists(): # Update buttons on game screen
        mode_txt = game_mode if game_mode else "Game"
        if btn_start_game and btn_start_game.winfo_exists(): btn_start_game.config(text=f"Start New {mode_txt}", state=tk.NORMAL)
        # CORRECTED LINE: Disable the pause/resume button
        if btn_pause_resume and btn_pause_resume.winfo_exists():
             btn_pause_resume.config(text="Pause Game", command=pause_game, state=tk.DISABLED, style="TButton") # Reset and disable

def apply_engine_configuration():
    """Applies current skill level setting to the engine if available."""
    global engine, ai_skill_level_var
    if engine and ai_skill_level_var:
        try:
            skill = ai_skill_level_var.get()
            engine.configure({"Skill Level": skill})
            print(f"  > Engine configured with Skill Level: {skill}")
        except Exception as config_err:
            print(f"  > Warning: Failed to configure engine skill/options: {config_err}")

def start_game_logic(mode, p_color=chess.WHITE):
    global board, game_running, game_mode, player_color, after_id, highlighted_squares
    global btn_start_game, btn_pause_resume, is_paused

    if game_running:
        messagebox.showwarning("Game Active", "Stop current game first.")
        return
    if engine: # Ensure engine is ready
        apply_engine_configuration() # Configure before first move
    else:
        messagebox.showerror("Engine Error", "Cannot start game, engine not initialized.")
        return # Don't start game if engine missing

    # --- FORMAT MODE FOR DISPLAY ---
    display_mode = "P vs AI" if mode == "PvAI" else "AI vs AI" if mode == "AIvAI" else "Game"
    # -----------------------------

    print(f"\n--- Starting New Game Console Log (Mode: {display_mode}) ---") # Use display_mode in log
    board = setup_board()
    game_mode = mode # Keep internal mode name
    player_color = p_color if mode == "PvAI" else None
    is_paused = False
    clear_selection()
    highlighted_squares["last_move"] = []

    # --- Prepare UI ---
    if not canvas or not canvas.winfo_exists(): return
    window.update_idletasks()
    try:
        sz = min(canvas.winfo_width(), canvas.winfo_height())
        sz = sz if sz > 1 else 480 # Ensure minimum size for calculation
        create_photo_images_for_canvas_size(sz)
    except Exception as e:
        print(f"Warning: Error during photo image creation: {e}") # Be more specific than pass
        # Decide if this is critical enough to return? Maybe not if defaults can work.
    draw_board_background(canvas)
    display_board(board, canvas) # Draw initial board state AFTER setup

    # --- Determine Initial Status Message (Corrected Logic) ---
    msg = "Game starting..." # Default fallback message
    p_col_name_for_msg = "Unknown" # Default if error occurs

    if mode == "PvAI":
        if player_color is not None: # Should always be True/False (WHITE/BLACK) for PvAI
            try:
                # Use player_color (True/False) directly as index for ['black', 'white']
                p_col_name_for_msg = chess.COLOR_NAMES[player_color].capitalize()
            except (IndexError, TypeError):
                 # Should be rare, but handle if p_color is not bool(0/1)
                 print(f"Warning: Invalid player_color value '{player_color}' for PvAI.")
                 p_col_name_for_msg = "Error"
        else:
            # This case shouldn't happen if mode is PvAI due to assignment above, but good practice
             print("Warning: player_color is None in PvAI mode.")
             p_col_name_for_msg = "Error"
        msg = f"Your Turn ({p_col_name_for_msg})"

    elif mode == "AIvAI":
         # Determine starting AI color name based on board's turn
         ai_start_col_name = "White" # Default if board isn't ready yet (shouldn't happen)
         if board: # Board should be set up by now
             try:
                 ai_start_col_name = chess.COLOR_NAMES[board.turn].capitalize()
             except (IndexError, TypeError):
                 print(f"Warning: Could not determine AI starting color from board.turn '{board.turn}'.")
                 # Stick with default 'White'
         else:
             print("Warning: Board object not available for AIvAI message setup.")

         msg = f"AI vs AI: Taskmaster ({ai_start_col_name}) moves first"

    # --- Update UI Elements ---
    if move_label and move_label.winfo_exists():
        move_label.config(text=msg)

    if trash_talk_area and trash_talk_area.winfo_exists():
        try:
            trash_talk_area.config(state=tk.NORMAL)
            trash_talk_area.delete("1.0", tk.END)
            trash_talk_area.config(state=tk.DISABLED)
            # Use display_mode in system message
            update_trash_talk_display("System", f"New Game Started: {display_mode}")
            update_trash_talk_display("System", "Let the battle commence!")
        except Exception as e:
             print(f"Error resetting chat log: {e}")

    # Update Buttons
    if btn_start_game and btn_start_game.winfo_exists():
         # Use display_mode in restart button text
         btn_start_game.config(text=f"Restart {display_mode}", state=tk.DISABLED)
    if btn_pause_resume and btn_pause_resume.winfo_exists():
        btn_pause_resume.config(text="Pause Game", state=tk.NORMAL, command=pause_game, style="TButton")

    # Set state and start appropriate loop/wait
    game_running = True

    # --- Clear any previous after_id robustly ---
    if after_id:
        try:
             if window and window.winfo_exists():
                 window.after_cancel(after_id)
        except tk.TclError: pass
        except Exception as e: print(f"Warning: Error cancelling timer in start_game_logic: {e}")
        finally: after_id = None # Always reset

    # --- Start Game Mode Specific Logic ---
    if game_mode == "AIvAI": # Start AIvAI loop
        try:
            if window and window.winfo_exists():
                after_id = window.after(200, run_aivai_loop)
            else: raise RuntimeError("Cannot schedule AIvAI loop - window gone.")
        except Exception as e:
             # Use display_mode in error message
             messagebox.showerror("Error",f"{display_mode} loop start failed: {e}")
             game_running=False;
             if btn_start_game and btn_start_game.winfo_exists(): btn_start_game.config(state=tk.NORMAL) # Reset Start button
             if btn_pause_resume and btn_pause_resume.winfo_exists(): btn_pause_resume.config(state=tk.DISABLED) # Reset Pause
             return

    elif game_mode == "PvAI": # Use internal game_mode here
        print(f"{display_mode} ready. Player ({p_col_name_for_msg}) to move.")



def pause_game():
    """Handles pausing the game, primarily stopping the AIvAI loop."""
    global is_paused, after_id, game_mode, game_running, window, btn_pause_resume, move_label
    if not game_running or is_paused: # Can't pause if not running or already paused
        return

    is_paused = True
    print("--- Game Paused ---")
    if move_label and move_label.winfo_exists():
        # Append Paused status rather than replacing the whole text
        current_text = move_label.cget("text")
        if "(Paused)" not in current_text: # Avoid adding multiple times
             move_label.config(text=f"{current_text} (Paused)")

    # Stop the AI vs AI loop timer if active
    if game_mode == "AIvAI" and after_id:
        try:
            if window and window.winfo_exists():
                window.after_cancel(after_id)
                print("  > AIvAI timer cancelled for pause.")
        except Exception as e:
            print(f"  > Warning: Error cancelling timer during pause: {e}")
        finally:
             # Ensure after_id is cleared even if cancel fails (might already be None)
             after_id = None

    # Update the button's appearance and command
    if btn_pause_resume and btn_pause_resume.winfo_exists():
        btn_pause_resume.config(text="Resume Game", command=resume_game, style="Accent.TButton") # Change style maybe?

def resume_game():
    """Handles resuming the game, primarily restarting the AIvAI loop."""
    global is_paused, after_id, game_mode, game_running, window, btn_pause_resume, move_label
    if not game_running or not is_paused: # Can't resume if not running or not paused
        return

    is_paused = False
    print("--- Game Resumed ---")
    if move_label and move_label.winfo_exists():
        # Remove the (Paused) indicator
        current_text = move_label.cget("text")
        move_label.config(text=current_text.replace(" (Paused)", ""))

    # Restart the AI vs AI loop if applicable
    if game_mode == "AIvAI" and game_running and not board.is_game_over():
        print("  > Rescheduling AIvAI loop...")
        try:
            if window and window.winfo_exists(): # Recheck window before scheduling
                # Ensure any stale timer ID is clear before setting a new one
                if after_id: window.after_cancel(after_id) # Precautionary cancel
                after_id = window.after(200, run_aivai_loop) # Start the loop again
            else:
                print("  > Error: Cannot resume AIvAI loop, window gone.")
                stop_game() # Stop game if window vanished
        except Exception as e:
            print(f"  > Error restarting AIvAI loop: {e}")
            stop_game() # Stop game if error occurs during resume


    # Update the button's appearance and command
    if btn_pause_resume and btn_pause_resume.winfo_exists():
        btn_pause_resume.config(text="Pause Game", command=pause_game, style="TButton") # Revert style

def stop_game(update_ui=True):
    """Stops the current game loop/input and updates UI."""
    global game_running, after_id, game_mode, btn_start_game, btn_pause_resume # Ensure correct globals
    was_running = game_running; game_running = False # Set flag FIRST
    is_paused = False # Reset pause state on stop

    # --- Clear any previous after_id robustly ---
    if after_id:
        try:
            if window and window.winfo_exists(): window.after_cancel(after_id)
        except: pass
        finally: after_id = None
    # -----------------------------------------

    if was_running and update_ui: # Update UI only if game was running
        print("--- Game Stopped by User ---")
        if move_label and move_label.winfo_exists(): move_label.config(text="Game stopped.")
        update_trash_talk_display("System", "Game halted by user.")

        # --- CORRECTED BUTTON HANDLING ---
        if game_frame and game_frame.winfo_exists():
            mode_txt = game_mode if game_mode else "Game"
            # Enable Start/Restart button
            if btn_start_game and btn_start_game.winfo_exists():
                btn_start_game.config(text=f"Start New {mode_txt}", state=tk.NORMAL)
            # Reset and Disable Pause/Resume button
            if btn_pause_resume and btn_pause_resume.winfo_exists():
                 btn_pause_resume.config(text="Pause Game", command=pause_game, state=tk.DISABLED, style="TButton")
                    # --- FORMAT MODE FOR DISPLAY ---
            display_mode = "P vs AI" if game_mode == "PvAI" else "AI vs AI" if game_mode == "AIvAI" else "Game"
            # -----------------------------
            if btn_start_game and btn_start_game.winfo_exists():
                # Use display_mode
                btn_start_game.config(text=f"Start New {display_mode}", state=tk.NORMAL)
            if btn_pause_resume and btn_pause_resume.winfo_exists():
                 btn_pause_resume.config(text="Pause Game", command=pause_game, state=tk.DISABLED, style="TButton")
        # --- END OF CORRECTED BUTTON HANDLING ---

# ======================================================
# SECTION 8: Screen Management
# ======================================================

def toggle_fullscreen():
    """Applies fullscreen state and enables/disables resolution combo."""
    global window, fullscreen_var, settings_frame
    if not window or not window.winfo_exists(): return

    is_fullscreen = fullscreen_var.get()
    try:
        window.attributes('-fullscreen', is_fullscreen)
        print(f"Fullscreen {'enabled' if is_fullscreen else 'disabled'}")

        # Enable/disable resolution combobox based on fullscreen state
        if settings_frame and settings_frame.winfo_exists() and hasattr(settings_frame, 'resolution_combo') and settings_frame.resolution_combo:
            combo_state = tk.DISABLED if is_fullscreen else "readonly"
            settings_frame.resolution_combo.config(state=combo_state)

    except tk.TclError as e:
        messagebox.showerror("Fullscreen Error", f"Could not toggle fullscreen: {e}")
    except Exception as e: # Catch other potential errors
        print(f"Error toggling fullscreen: {e}")

def hide_all_frames():
    """Hides all primary content frames."""
    for frame in [main_frame, game_frame, settings_frame, credits_frame]:
        if frame and frame.winfo_exists(): frame.pack_forget()

def show_main_menu():
    """Shows the main menu screen, stops any active game."""
    hide_all_frames(); stop_game(update_ui=False)
    if not main_frame: create_main_menu_frame()
    if main_frame and main_frame.winfo_exists():
        main_frame.pack(fill=tk.BOTH, expand=True)
        if status_label and status_label.winfo_exists(): status_label.config(text="Main Menu")
        
def show_game_screen(mode, p_color=chess.WHITE):
    """Shows game screen & starts the specified game mode logic."""
    if not piece_image_files and not load_assets(): # Load assets if missing
        messagebox.showerror("Asset Error", "Cannot start game, essential assets failed to load.")
        return
    hide_all_frames()
    if not game_frame: create_game_frame() # Create game UI elements if needed
    if not game_frame or not game_frame.winfo_exists(): messagebox.showerror("UI Error","Game frame creation failed."); return
    game_frame.pack(fill=tk.BOTH, expand=True)
    try:
        # Access list using the boolean value of p_color (True=1, False=0)
        p_color_name = chess.COLOR_NAMES[p_color].capitalize()
    except (IndexError, TypeError):
        p_color_name = "Unknown"
    status = f"Mode: {mode}" + (f" - You: {p_color_name}" if mode=="PvAI" else "")
    if status_label and status_label.winfo_exists(): status_label.config(text=status)
    window.update_idletasks() # Ensure UI elements are placed
    start_game_logic(mode, p_color) # Start the actual game logic AFTER UI shown

def show_settings():
    """Shows the settings screen."""
    hide_all_frames()
    if not settings_frame: create_settings_frame()
    if settings_frame and settings_frame.winfo_exists():
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        if status_label and status_label.winfo_exists(): status_label.config(text="Settings")

def show_credits():
    """Shows the credits screen."""
    hide_all_frames()
    if not credits_frame: create_credits_frame()
    if credits_frame and credits_frame.winfo_exists():
        credits_frame.pack(fill=tk.BOTH, expand=True)
        if status_label and status_label.winfo_exists(): status_label.config(text="Credits & Information")

def apply_settings():
    """Applies resolution setting and returns to main menu."""
    global ai_think_time, trash_talk_enabled, ai_skill_level_var, resolution_var, fullscreen_var, window

    print("\nApplying Settings...")
    print(f" - AI Think Time: {ai_think_time.get():.1f}s")
    print(f" - AI Skill Level: {ai_skill_level_var.get()}")
    print(f" - AI Banter Enabled: {trash_talk_enabled.get()}")
    print(f" - Fullscreen Active: {fullscreen_var.get()}")
    print(f" - Selected Resolution: {resolution_var.get()}")

    res = resolution_var.get()
    fs = fullscreen_var.get() # Check current fullscreen state

    if not fs and "Windowed" not in res: # Only apply geometry if NOT fullscreen and a specific size is selected
        try:
            # Make sure parsing is robust
            if 'x' in res:
                 width, height = map(int, res.split('x'))
                 # Add minimum size constraints maybe?
                 min_w, min_h = 800, 600 # Example minimums
                 if width >= min_w and height >= min_h:
                      window.geometry(f"{width}x{height}")
                      print(f" > Window geometry set to: {width}x{height}")
                 else:
                      print(f" > Warning: Selected resolution {res} is below minimum {min_w}x{min_h}. Not applied.")
                      messagebox.showwarning("Resolution Too Small", f"Selected resolution {res} is smaller than the minimum allowed ({min_w}x{min_h}).")
            else:
                 print(f" > Warning: Invalid resolution format selected: {res}")
        except ValueError:
            print(f" > Error parsing resolution string: {res}")
        except tk.TclError as e:
            print(f" > Error applying geometry (window might be gone): {e}")
        except Exception as e:
            print(f" > Unexpected error applying resolution: {e}")
    elif fs:
         print(" > Info: Fullscreen active, skipping window geometry change.")
    elif "Windowed" in res:
         print(" > Info: 'Windowed (Resizable)' selected, no fixed geometry applied.")
    if engine:
        print(" > Re-applying engine configuration based on settings...")
        apply_engine_configuration()
    else:
        print(" > Engine not running, configuration skipped.")


    show_main_menu()

# ======================================================
# SECTION 9: GUI FRAME CREATION FUNCTIONS
# ======================================================

def apply_ttk_styles(style):
    """Configure ttk styles for Checkmate Royale V2 theme."""
    # --- Base Styles ---
    style.configure(".", background=THEME_MAIN_BG, foreground=THEME_TEXT_LIGHT, font=FONT_UI_SANS_CLEAN) # Root style
    style.configure("TFrame", background=THEME_MAIN_BG)
    style.configure("TLabel", background=THEME_MAIN_BG, foreground=THEME_TEXT_LIGHT, font=FONT_UI_SANS_CLEAN)
    style.configure("Header.TLabel", font=FONT_UI_SANS_BOLD) # For section headers
    style.configure("Title.TLabel", foreground=THEME_ACCENT_PRIMARY, font=FONT_SUBTITLE) # Section titles
    style.configure("Category.TLabel", foreground=THEME_TEXT_MUTED) # Muted text for categories
    style.configure("FinalMessage.TLabel", foreground=THEME_ACCENT_PRIMARY, font=(FONT_UI_SANS_CLEAN[0], FONT_UI_SANS_CLEAN[1], 'bold'))

    # --- Button Style ---
    style.configure("TButton",
                    background=THEME_BUTTON_BG, foreground=THEME_BUTTON_FG,
                    font=FONT_BUTTON, padding=(20, 8), # Wider padding
                    relief=tk.FLAT, borderwidth=0, anchor='center')
    # style.layout("TButton", [('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})]) # Keep label centered maybe?
    style.map("TButton",
              # background=[('active', THEME_ACCENT_PRIMARY), ('!disabled', THEME_BUTTON_BG)], # Gold bg on hover
              # foreground=[('active', THEME_BUTTON_ACCENT_FG), ('!disabled', THEME_BUTTON_FG)], # Black text on hover
              relief=[('pressed', tk.FLAT), ('active', tk.FLAT)], # Keep flat look on hover/press
              borderwidth=[('active', 1)],
              bordercolor=[('active', THEME_ACCENT_PRIMARY)]) # Gold outline on hover

    # --- Accent Button Style (Gold Button) ---
    style.configure("Accent.TButton",
                    background=THEME_ACCENT_PRIMARY, foreground=THEME_BUTTON_ACCENT_FG,
                    font=FONT_BUTTON, padding=(20, 8),
                    relief=tk.FLAT, borderwidth=0)
    style.map("Accent.TButton",
              background=[('active', THEME_ACCENT_SECONDARY), ('!disabled', THEME_ACCENT_PRIMARY)], # Brighter gold on hover
              foreground=[('!disabled', THEME_BUTTON_ACCENT_FG)],
              relief=[('pressed', tk.FLAT), ('active', tk.FLAT)])

    # --- Other Widgets ---
    style.configure("TCheckbutton", background=THEME_MAIN_BG, foreground=THEME_TEXT_LIGHT, font=FONT_UI_SANS_CLEAN)
    style.map("TCheckbutton", indicatorcolor=[('selected', THEME_ACCENT_PRIMARY), ('!selected', THEME_TERTIARY)], foreground=[('active', THEME_ACCENT_SECONDARY)]) # Gold hover text

    style.configure("Horizontal.TScale", background=THEME_MAIN_BG, troughcolor=THEME_TERTIARY)
    # Slider styling is theme/OS dependent, basic color set attempt
    try: style.configure("Horizontal.TScale", sliderrelief=tk.FLAT, sliderlength=20)
    except: pass # Ignore if options not supported

    style.configure("TScrollbar", troughcolor=THEME_TERTIARY, background=THEME_ACCENT_SECONDARY, borderwidth=0, arrowcolor=THEME_TEXT_DARK, relief=tk.FLAT, arrowrelief=tk.FLAT)
    style.map("Vertical.TScrollbar", background=[('active',THEME_ACCENT_PRIMARY)])

    # Use highlight system for PanedWindow Sash if direct styling fails
    # style.configure("Sash", background=THEME_TERTIARY, borderwidth=0, relief=tk.FLAT, sashthickness=6) # Attempt direct first
    style.configure("TSeparator", background=THEME_TERTIARY)

def create_main_menu_frame():
    """Creates the Main Menu widgets."""
    global main_frame
    main_frame = ttk.Frame(window, style="TFrame", padding=(50, 30))

    if logo_photo_image: tk.Label(main_frame, image=logo_photo_image, bg=THEME_MAIN_BG).pack(pady=(0, 30))
    else: tk.Frame(main_frame, height=70, bg=THEME_MAIN_BG).pack()

    tk.Label(main_frame, text="Checkmate Royale", font=FONT_TITLE, fg=THEME_ACCENT_PRIMARY, bg=THEME_MAIN_BG).pack(pady=(0, 50))

    # Buttons - Just update text directly
    btn_width=26
    ttk.Button(main_frame, text="Play vs AI", command=lambda: show_game_screen("PvAI", chess.WHITE), style="Accent.TButton", width=btn_width).pack(pady=12) # Simpler text
    ttk.Button(main_frame, text="AI vs AI", command=lambda: show_game_screen("AIvAI"), style="TButton", width=btn_width).pack(pady=12) # Simpler text

    ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=25, padx=60)

    ttk.Button(main_frame, text="Settings", command=show_settings, style="TButton", width=btn_width).pack(pady=12)
    ttk.Button(main_frame, text="Credits", command=show_credits, style="TButton", width=btn_width).pack(pady=12)
    ttk.Button(main_frame, text="Exit", command=cleanup, style="TButton", width=btn_width).pack(pady=(12, 40))
    
def apply_chat_styles(text_widget):
    """Configures the appearance tags for the chat/log Text widget."""
    if not text_widget or not text_widget.winfo_exists(): return
    try:
        # Style for Player messages
        text_widget.tag_config("player",
                               foreground=THEME_ACCENT_SECONDARY, # Brighter gold/accent
                               font=(FONT_UI_SANS_CLEAN[0], FONT_UI_SANS_CLEAN[1], 'bold')) # Use base UI font, bold

        # Style for AI (Taskmaster) messages
        text_widget.tag_config("ai",
                               foreground=THEME_TEXT_LIGHT) # Standard light text

        # Style for System messages
        text_widget.tag_config("system",
                               foreground=THEME_TEXT_MUTED, # Muted grey
                               font=(FONT_UI_SANS_CLEAN[0], FONT_UI_SANS_CLEAN[1], 'italic')) # Italic for system

        # Optional: Configure selection colors if desired
        # text_widget.tag_config(tk.SEL, background=THEME_ACCENT_PRIMARY, foreground=THEME_TEXT_DARK)

    except tk.TclError as e:
        print(f"TclError configuring chat styles (likely closing): {e}")
    except Exception as e:
        print(f"Error applying chat styles: {e}\n{traceback.format_exc()}")

def create_game_frame():
    """Creates the main Game screen widgets (Board, Log, Controls)."""
    global game_frame, canvas, move_label, trash_talk_area, btn_start_game, btn_pause_resume # Correct global name

    game_frame = ttk.Frame(window, style="TFrame", padding=10) # Padding around game area
    paned_window = ttk.PanedWindow(game_frame, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Left Panel (Board & Status) - KEEP AS IS
    left_frame = ttk.Frame(paned_window, style="TFrame", padding=(5, 5, 5, 0))
    paned_window.add(left_frame, weight=3)
    canvas = tk.Canvas(left_frame, width=500, height=500,
                       highlightthickness=1, highlightbackground=THEME_TERTIARY, # Subtle border
                       bg=THEME_MAIN_BG) # BG *around* board
    canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
    canvas.bind("<Configure>", on_canvas_resize); canvas.bind("<Button-1>", on_canvas_click)
    move_label = ttk.Label(left_frame, text="Select game mode to begin", font=FONT_UI_SANS_BOLD, style="TLabel", padding=(5,3), anchor='w')
    move_label.pack(fill=tk.X)

    # Right Panel (Log & Controls) - MODIFY LOG AREA
    right_frame = ttk.Frame(paned_window, style="TFrame", padding=(10, 5))
    paned_window.add(right_frame, weight=1) # Adjust weight as needed
    ttk.Label(right_frame, text="Game Log / AI Banter", style="Header.TLabel", anchor='center').pack(pady=(0, 5), fill=tk.X) # Less top padding

    # --- Styled Log Area ---
    txt_cont = ttk.Frame(right_frame, style='TFrame') # Container frame for Text + Scrollbar
    txt_cont.pack(fill=tk.BOTH, expand=True, pady=(0, 10)) # Allow this container to expand

    # Configure tk.Text directly for better chat appearance
    trash_talk_area = tk.Text(
        txt_cont,
        height=15,               # Keep desired height
        width=35,                # Keep width or adjust
        wrap=tk.WORD,            # Wrap lines
        font=FONT_UI_SANS_CLEAN, # Use the clean UI font for readability
        state=tk.DISABLED,       # Start read-only
        bg=COLOR_TERTIARY,       # Use tertiary color for chat background
        fg=THEME_TEXT_LIGHT,     # Default text color
        padx=10,                 # Horizontal padding inside the text area
        pady=8,                  # Vertical padding inside the text area
        relief=tk.SOLID,         # Solid border looks better than default SUNKEN
        bd=1,                    # Border width
        selectbackground=THEME_ACCENT_PRIMARY, # Color when text is selected
        selectforeground=THEME_TEXT_DARK       # Text color when selected
    )

    # Attach Scrollbar
    scroll = ttk.Scrollbar(txt_cont, command=trash_talk_area.yview, style="Vertical.TScrollbar")
    trash_talk_area.config(yscrollcommand=scroll.set)

    # Pack Text and Scrollbar (Order matters for appearance)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    trash_talk_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Text fills remaining space

    # *** APPLY THE DEFINED CHAT STYLES ***
    apply_chat_styles(trash_talk_area)
    # --- End Styled Log Area ---


    # Buttons (Keep as is)
    btn_frame = ttk.Frame(right_frame, style="TFrame"); btn_frame.pack(fill=tk.X, pady=5, padx=5)
    btn_start_game = ttk.Button(btn_frame, text="Start New Game", state=tk.DISABLED, command=lambda: start_game_logic(game_mode or "AIvAI"), style="Accent.TButton")
    btn_start_game.pack(fill=tk.X, ipady=3, pady=4)
    btn_pause_resume = ttk.Button(btn_frame, text="Pause Game", command=pause_game, state=tk.DISABLED, style="TButton")
    btn_pause_resume.pack(fill=tk.X, ipady=3, pady=4)
    ttk.Separator(btn_frame).pack(fill=tk.X, pady=10)
    ttk.Button(btn_frame, text="Back to Main Menu", command=show_main_menu, style="TButton").pack(fill=tk.X, ipady=3, pady=4)

def create_settings_frame():
    """Creates the Settings screen widgets."""
    # Ensure globals are accessible
    global settings_frame, ai_think_time, trash_talk_enabled, ai_skill_level_var, fullscreen_var, resolution_var

    settings_frame = ttk.Frame(window, padding=35, style="TFrame")
    settings_frame.columnconfigure(1, weight=1) # Allow controls to expand if needed

    # --- Title ---
    title = ttk.Label(settings_frame, text="Settings", style="Title.TLabel", anchor='center')
    title.grid(row=0, column=0, columnspan=3, pady=(0, 30), sticky='ew')

    current_row = 1 # Start adding settings below the title

    # --- Helper for adding setting rows ---
    def add_setting_row(label_text, widget, row):
        ttk.Label(settings_frame, text=label_text, style="Header.TLabel").grid(row=row, column=0, sticky='w', padx=(0, 15))
        widget.grid(row=row, column=1, columnspan=2, sticky='ew', pady=4)
        return row + 1

    # --- Gameplay Settings Section ---
    ttk.Separator(settings_frame).grid(row=current_row, column=0, columnspan=3, sticky='ew', pady=(0, 10)); current_row += 1
    ttk.Label(settings_frame, text="Gameplay", style="TLabel", foreground=THEME_ACCENT_SECONDARY).grid(row=current_row, column=0, sticky='w', pady=(0,5)); current_row += 1

    # AI Think Time
    think_cont = ttk.Frame(settings_frame) # Container for Scale + Label
    think_cont.grid(row=current_row, column=1, columnspan=2, sticky='ew', pady=4)
    think_scale = ttk.Scale(think_cont, from_=0.1, to=5.0, variable=ai_think_time, orient=tk.HORIZONTAL, length=250)
    think_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
    think_lbl = ttk.Label(think_cont, font=FONT_UI_SANS_BOLD, width=5, style="TLabel", text=f"{ai_think_time.get():.1f}s") # Initial text
    think_lbl.pack(side=tk.LEFT)
    def _upd_think_lbl(*args): # Update label when scale moves
        if think_lbl.winfo_exists(): think_lbl.config(text=f"{ai_think_time.get():.1f}s")
    ai_think_time.trace_add('write', _upd_think_lbl) # Add trace AFTER think_lbl created
    ttk.Label(settings_frame, text="AI Think Time:", style="Header.TLabel").grid(row=current_row, column=0, sticky='w', padx=(0, 15)); current_row += 1

    # AI Skill Level
    skill_cont = ttk.Frame(settings_frame)
    skill_cont.grid(row=current_row, column=1, columnspan=2, sticky='ew', pady=4)
    skill_scale = ttk.Scale(skill_cont, from_=0, to=20, variable=ai_skill_level_var, orient=tk.HORIZONTAL, length=250)
    skill_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    skill_lbl = ttk.Label(skill_cont, font=FONT_UI_SANS_BOLD, width=5, style="TLabel", text=f"{ai_skill_level_var.get()}")
    skill_lbl.pack(side=tk.LEFT)
    def _upd_skill_lbl(*args):
        if skill_lbl.winfo_exists(): skill_lbl.config(text=f"{ai_skill_level_var.get()}")
    ai_skill_level_var.trace_add('write', _upd_skill_lbl)
    ttk.Label(settings_frame, text="AI Skill Level:", style="Header.TLabel").grid(row=current_row, column=0, sticky='w', padx=(0, 15)); current_row += 1

    # Trash Talk Toggle
    chk_banter = ttk.Checkbutton(settings_frame, text="Enable AI Banter", variable=trash_talk_enabled, style="TCheckbutton")
    current_row = add_setting_row("", chk_banter, current_row) # Label provided by Checkbutton text

    # --- Appearance Settings Section ---
    ttk.Separator(settings_frame).grid(row=current_row, column=0, columnspan=3, sticky='ew', pady=(15, 10)); current_row += 1
    ttk.Label(settings_frame, text="Appearance", style="TLabel", foreground=THEME_ACCENT_SECONDARY).grid(row=current_row, column=0, sticky='w', pady=(0,5)); current_row += 1

    # Fullscreen Toggle
    chk_fullscreen = ttk.Checkbutton(settings_frame, text="Fullscreen Mode", variable=fullscreen_var, style="TCheckbutton", command=toggle_fullscreen) # Command applies instantly
    # IMPORTANT: Save a reference to the resolution combobox for enable/disable
    settings_frame.resolution_combo = None # Initialize attribute
    current_row = add_setting_row("", chk_fullscreen, current_row)

    # Resolution Selection
    resolution_combo = ttk.Combobox(settings_frame, textvariable=resolution_var, values=available_resolutions, state="readonly", width=25)
    settings_frame.resolution_combo = resolution_combo # Store reference
    current_row = add_setting_row("Window Size:", resolution_combo, current_row)
    # Disable initially if starting fullscreen
    if fullscreen_var.get(): resolution_combo.config(state=tk.DISABLED)

    # --- Buttons ---
    btn_bar = ttk.Frame(settings_frame)
    btn_bar.grid(row=current_row + 1, column=0, columnspan=3, pady=(40, 10)) # Add spacer row via grid +1
    btn_bar.columnconfigure(0, weight=1); btn_bar.columnconfigure(1, weight=1) # Center buttons

    apply_btn = ttk.Button(btn_bar, text="Apply & Back", command=apply_settings, style="Accent.TButton", width=18)
    apply_btn.grid(row=0, column=0, padx=10, sticky='e')

    back_btn = ttk.Button(btn_bar, text="Back to Menu", command=show_main_menu, style="TButton", width=18)
    back_btn.grid(row=0, column=1, padx=10, sticky='w')

def create_credits_frame():
    """Creates the Credits screen with developer info and clickable links, centered content."""
    global credits_frame

    # Define link color if not already defined
    LINK_COLOR = "#66B2FF"

    credits_frame = ttk.Frame(window, padding=15, style="TFrame")
    credits_frame.columnconfigure(0, weight=1); credits_frame.rowconfigure(1, weight=1) # Grid for canvas+scrollbar

    # Title (Keep centered using grid's columnspan)
    ttk.Label(credits_frame, text="Credits & Information", style="Title.TLabel", anchor='center').grid(
        row=0, column=0, columnspan=2, pady=(5, 15), sticky='ew' # Reduce bottom padding slightly
    )

    # --- Scrollable Area Setup (Keep as is) ---
    canvas_outer = tk.Canvas(credits_frame, bg=THEME_FRAME_BG, highlightthickness=0, borderwidth=0)
    scrollbar = ttk.Scrollbar(credits_frame, orient="vertical", command=canvas_outer.yview, style="Vertical.TScrollbar")
    # Content frame NOW USES GRID for centering
    content_frame = ttk.Frame(canvas_outer, style="TFrame", padding=(20, 25)) # Add padding *inside*

    # *** KEY CHANGE FOR CENTERING: Configure grid inside content_frame ***
    content_frame.columnconfigure(0, weight=1) # Make the single column expandable

    content_frame.bind("<Configure>", lambda e: canvas_outer.configure(scrollregion=canvas_outer.bbox("all")))
    canvas_outer.create_window((0, 0), window=content_frame, anchor="nw", width=window.winfo_width()-50) # Approx width minus scrollbar/padding
    # ^ Optionally bind width to window/canvas size dynamically if needed
    canvas_outer.configure(yscrollcommand=scrollbar.set)
    canvas_outer.grid(row=1, column=0, sticky='nsew'); scrollbar.grid(row=1, column=1, sticky='ns')

    # --- Define Fonts for Links (Keep as is) ---
    try:
        link_font = (FONT_UI_SANS_CLEAN[0], FONT_UI_SANS_CLEAN[1], "underline")
    except:
        link_font = ("Segoe UI", 10, "underline")

    # --- Content Inside Scrollable Frame (Using grid row=N, column=0) ---
    current_row = 0 # Row counter for the grid

    # Helper function for adding centered rows
    def add_centered_row(widget, pady_config=(5, 5), columnspan=1, sticky='n'):
        nonlocal current_row
        widget.grid(row=current_row, column=0, columnspan=columnspan, pady=pady_config, sticky=sticky)
        current_row += 1

    # Helper function for creating section headers using grid
    def add_section_header(text):
        # Use a frame to hold label + separator for better spacing control maybe
        header_frame = ttk.Frame(content_frame, style="TFrame")
        lbl = ttk.Label(header_frame, text=text, style="Header.TLabel", anchor='center')
        lbl.pack(pady=(0, 5)) # Pad below label
        sep = ttk.Separator(header_frame)
        sep.pack(fill=tk.X, padx=20, pady=(0, 5)) # Pad separator
        add_centered_row(header_frame, pady_config=(15, 10), sticky='ew') # Grid the whole frame

    # -- Technology Section --
    add_section_header("Technology & Libraries")
    tech_frame = ttk.Frame(content_frame, style="TFrame") # Frame for the label-value grid
    tech_frame.columnconfigure(0, weight=0, pad=5); tech_frame.columnconfigure(1, weight=1) # Label: narrow, Value: expand
    tech_row_idx = 0
    def add_tech_item(label, value):
        nonlocal tech_row_idx
        ttk.Label(tech_frame, text=label, style="Category.TLabel").grid(row=tech_row_idx, column=0, sticky='ne', pady=1)
        ttk.Label(tech_frame, text=value, style="TLabel", wraplength=350, anchor='nw').grid(row=tech_row_idx, column=1, sticky='nw', pady=1)
        tech_row_idx += 1

    # (Fetch versions as before)
    try: py_ver = f"Python {'.'.join(map(str, os.sys.version_info[:3]))}"
    except: py_ver = "Python N/A"
    try: pychess_ver = f"python-chess (v{chess.__version__})"
    except: pychess_ver = "python-chess (vN/A)"
    try: pillow_ver = f"Pillow (v{Image.__version__})"
    except: pillow_ver = "Pillow (vN/A)"
    try: tk_ver = f"Tkinter/ttk (v{tk.TkVersion})"
    except: tk_ver = "Tkinter/ttk (vN/A)"

    add_tech_item("Language:", py_ver)
    add_tech_item("GUI:", tk_ver)
    add_tech_item("Chess Logic:", pychess_ver)
    # add_tech_item("Imaging:", pillow_ver) # Uncomment if needed

    add_centered_row(tech_frame, sticky='ew', pady_config=(0, 15)) # Grid the tech_frame itself

    # -- Development Section --
    add_section_header("Development")
    dev_label = ttk.Label(content_frame, text="Code by: Sid and Gemini", style="TLabel", anchor='center')
    add_centered_row(dev_label, pady_config=4)

    # GitHub Link
    github_url = "https://github.com/siddoit"
    github_link = tk.Label(content_frame, text="Sid's GitHub Profile", font=link_font, fg=LINK_COLOR, bg=THEME_FRAME_BG, cursor="hand2")
    github_link.bind("<Button-1>", lambda e, url=github_url: open_link(url))
    add_centered_row(github_link, pady_config=(2, 15))

    # -- Assets Section --
    add_section_header("Assets")
    piece_source_url = "https://greenchess.net/info.php?item=downloads"
    piece_source_link = tk.Label(content_frame, text="Chess Piece Graphics: Green Chess", font=link_font, fg=LINK_COLOR, bg=THEME_FRAME_BG, cursor="hand2")
    piece_source_link.bind("<Button-1>", lambda e, url=piece_source_url: open_link(url))
    add_centered_row(piece_source_link, pady_config=(4, 20))

    # -- Footer Message --
    sep_footer = ttk.Separator(content_frame)
    add_centered_row(sep_footer, sticky='ew', pady_config=(15, 15))
    footer_label = ttk.Label(content_frame, text="❣ Coded With Love by Sid & Gemini ❣", style="FinalMessage.TLabel", anchor='center')
    add_centered_row(footer_label, pady_config=10)


    # --- Back Button (Outside scroll area, Keep as is) ---
    back_btn = ttk.Button(credits_frame, text="Back to Main Menu", command=show_main_menu, style="Accent.TButton", width=20)
    back_btn.grid(row=2, column=0, columnspan=2, pady=(20, 10))

def open_link(url):
    """Opens the given URL in a new web browser tab."""
    try:
        webbrowser.open_new_tab(url)
        print(f"Opening link: {url}") # Log link opening attempt
    except Exception as e:
        messagebox.showerror("Link Error", f"Could not open link:\n{url}\n\nError: {e}")
        print(f"Error opening link {url}: {e}")
        
# ======================================================
# SECTION 10: Utility and Event Handlers
# ======================================================

def on_canvas_resize(event):
    """Debounced canvas resize handler."""
    # ... (Keep existing debounce logic) ...
    try: window.after_cancel(on_canvas_resize._after_id)
    except: pass
    try: on_canvas_resize._after_id = window.after_idle(perform_canvas_redraw, event) # Use after_idle
    except: pass

def perform_canvas_redraw(event):
    # ... (check args and size) ...
    try:
        create_photo_images_for_canvas_size(current_size)
        # Call background draw first
        draw_board_background(canvas)
        # Then draw pieces/highlights on top
        display_board(board if board else chess.Board(), canvas)
    except Exception as e: print(f"Err redraw: {e}")

def cleanup(confirm=True):
    """Gracefully stops, quits engine, closes window, confirms exit."""
    global engine, window, game_running, after_id

    # Confirmation Dialog
    if confirm and window and window.winfo_exists():
         if not messagebox.askyesno("Confirm Exit", "Depart the Royale?"):
             return # Abort if No

    print("\nCleanup requested...")
    stop_game(update_ui=False) # Stop game logic first

    # Quit Engine
    if engine:
        eng = engine       # Store ref before clearing global
        engine = None      # Clear global variable
        print("Quitting engine...")
        try:
            eng.quit()     # Attempt to quit using the stored reference
            print(" > Engine quit successful.")
        except Exception as e: # Catch potential errors during quit
            print(f"   > Warning: Exception during engine quit: {e}") # Log if quit fails

    # Destroy Window (AFTER engine quit attempt)
    if window:
        win = window       # Store ref before clearing global
        window = None      # Clear global variable immediately
        print("Destroying window...")
        try:
            # Ensure the window object itself is still valid before calling destroy
            if win.winfo_exists():
                 win.destroy()
            else:
                 print("   > Info: Window object was already gone.")
        except tk.TclError: # Catch specific Tkinter errors (like window already gone)
            print("   > Info: Window may have already been closed (TclError).") # More informative than pass
        except Exception as e: # Catch other unexpected errors
            print(f"   > Warning: Unexpected error destroying window: {e}")
        # Message indicates the sequence finished
        print(" > Window destroy sequence finished.")

    print("Cleanup finished.")

# ======================================================
# SECTION 11: Main Application Execution
# ======================================================

# --- Modify the __main__ block ---
# --- Corrected __main__ block ---
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Checkmate Royale - AI Chess")
    window.minsize(850, 650)
    window.config(bg=THEME_MAIN_BG)

    # --- Init Tk Vars (Corrected - Removed lines setting to None) ---
    ai_think_time = tk.DoubleVar(value=DEFAULT_AI_THINK_TIME)
    trash_talk_enabled = tk.BooleanVar(value=DEFAULT_TRASH_TALK_ENABLED)
    ai_skill_level_var = tk.IntVar(value=DEFAULT_AI_SKILL)       # KEEP this
    fullscreen_var = tk.BooleanVar(value=DEFAULT_FULLSCREEN)     # KEEP this
    resolution_var = tk.StringVar(value=DEFAULT_RESOLUTION)      # KEEP this
    # ai_skill_level_var = None  # REMOVE THIS LINE
    # fullscreen_var = None      # REMOVE THIS LINE
    # resolution_var = None      # REMOVE THIS LINE
    available_resolutions = ["1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "Windowed (Resizable)"]
    # --- End Corrected Init Tk Vars ---


    # --- Bind resolution changes ---
    # (This part is okay, but the trace might have failed before if resolution_var was None)
    def on_resolution_change(*args):
        pass # Application is handled by Apply button
    # Ensure resolution_var exists before adding trace
    if resolution_var:
        resolution_var.trace_add('write', on_resolution_change)
    else:
        print("CRITICAL ERROR: resolution_var is None, cannot add trace.")


    # --- Initial Fullscreen Apply ---
    def apply_initial_fullscreen():
        # Check if fullscreen_var exists AND is a BooleanVar before calling get()
        if fullscreen_var and isinstance(fullscreen_var, tk.BooleanVar) and fullscreen_var.get():
             try:
                 window.attributes('-fullscreen', True)
                 # Disable resolution combobox if starting fullscreen
                 # Need robust check if settings_frame and combo exist yet
                 # Consider doing this disable inside toggle_fullscreen or apply_settings
             except tk.TclError:
                 print("Warning: TclError during initial fullscreen apply (window might be gone).")
    window.after(100, apply_initial_fullscreen)


    # Apply Theming
    # Make sure errors here are visible for debugging
    print("Attempting to apply theme...")
    style = ttk.Style(window)
    try:
        style.theme_use('clam')
        print(f"Using theme: {style.theme_use()}")
        apply_ttk_styles(style);
        print("Theme styles applied.")
    except Exception as e:
        print(f"CRITICAL WARNING: Theme setup failed: {e}\n{traceback.format_exc()}")
        # Consider adding a messagebox warning here
        # messagebox.showwarning("Theme Error", f"Failed to apply custom theme:\n{e}")


    # Status Bar Setup (Assuming status_label is defined elsewhere correctly)
    status_label = tk.Label(window, text="Initializing...", relief=tk.SUNKEN, bd=1, anchor=tk.W,
                             font=FONT_STATUS, padx=8, pady=2, bg=THEME_TERTIARY, fg=THEME_TEXT_MUTED)
    status_label.pack(side=tk.BOTTOM, fill=tk.X)


    # Load Assets & Engine
    print("Loading assets...")
    assets_ok = load_assets()
    print("Setting up engine...")
    engine_ok = setup_engine() if assets_ok else False


    # Final Initial Status Update
    if status_label and status_label.winfo_exists(): # Check if status label was created
        if assets_ok and engine_ok:
            status_label.config(text="Ready. Select Mode.", fg="#AAFFAA")
        elif not assets_ok:
            status_label.config(text="CRITICAL Asset Error! Check 'assets' folder.", fg="#FF8888")
        else: # Engine error
            status_label.config(text="CRITICAL Engine Error! Check Stockfish path.", fg="#FF8888")


    # Start UI
    print("Showing main menu...")
    show_main_menu()
    window.protocol("WM_DELETE_WINDOW", lambda: cleanup(confirm=True))


    # Main Loop
    try:
        print("Starting Tkinter main loop...");
        window.mainloop()
    except KeyboardInterrupt:
        print("\nInterrupt received");
        cleanup(confirm=False)
    except Exception as main_loop_error: # Catch other potential errors during mainloop
        print(f"\nUNEXPECTED ERROR IN MAIN LOOP:\n{main_loop_error}\n{traceback.format_exc()}")
        cleanup(confirm=False)


    print("\nCheckmate Royale application has finished.")