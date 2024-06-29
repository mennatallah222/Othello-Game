import sys
import pygame
import copy

# Define constants for representing the board state
EMPTY, BLACK, WHITE, OUTER = '.', '1', '0', '?'
# Define directions for checking valid moves
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Function to initialize the game board
def initial_board():
    # Create the initial board configuration with outer boundary and initial pieces
    board = [[OUTER] * 10] + [[OUTER] + [EMPTY] * 8 + [OUTER] for _ in range(8)] + [[OUTER] * 10]
    board[4][4], board[5][5] = WHITE, WHITE
    board[4][5], board[5][4] = BLACK, BLACK
    return board

# Function to check if a move is valid
def isValidMove(board, player, move):
    # Extract the coordinates of the move
    (x, y) = move
    # Check if the selected cell is empty
    if board[x][y] != EMPTY:
        return False
    # Check each direction for valid moves
    for (dx, dy) in DIRECTIONS:
        nx, ny = x + dx, y + dy
        # Continue in this direction until reaching a piece of the opposite color
        if board[nx][ny] == (WHITE if player == BLACK else BLACK):
            while board[nx][ny] == (WHITE if player == BLACK else BLACK):
                nx += dx
                ny += dy
            # If the next piece is of the player's color, the move is valid
            if board[nx][ny] == player:
                return True
    return False

# Function to make a move on the board
def make_move(board, player, move):
    (x, y) = move
    board[x][y] = player
    # Flip pieces in all valid directions
    for (dx, dy) in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if board[nx][ny] == (WHITE if player == BLACK else BLACK):
            tilesToFlip=[]
            while board[nx][ny] == (WHITE if player == BLACK else BLACK):
                tilesToFlip.append((nx, ny))
                nx += dx
                ny += dy
            if board[nx][ny] == player:
                for fx, fy in tilesToFlip:
                    board[fx][fy]=player
    return board

# Function for the alpha-beta pruning algorithm
def alpha_beta_pruning(board, player, alpha, beta, depth):
    if depth == 0 or is_terminal(board):
        return evaluate(board, player)
    if player == BLACK:
        value = float('-inf')
        # Iterate over all possible moves for the player
        for move in get_all_moves(board, player):
            if isValidMove(board, player, move):
                # Make a move and recursively evaluate the resulting board state
                new_board = make_move(copy.deepcopy(board), player, move)
                value = max(value, alpha_beta_pruning(new_board, WHITE, alpha, beta, depth - 1))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return value
    else:
        value = float('inf')
        # Iterate over all possible moves for the opponent
        for move in get_all_moves(board, player):
            if isValidMove(board, player, move):
                # Make a move and recursively evaluate the resulting board state
                new_board = make_move(copy.deepcopy(board), player, move)
                value = min(value, alpha_beta_pruning(new_board, BLACK, alpha, beta, depth - 1))
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value

# Function to evaluate the board state for a player
def evaluate(board, player):
    opponent = WHITE if player == BLACK else BLACK
    # Calculate the difference in scores between the player and the opponent
    player_score = sum(row.count(player) for row in board)
    opponentScore = sum(row.count(opponent) for row in board)
    return player_score - opponentScore

# Function to check if the game is in a terminal state
def is_terminal(board):
    for x in range(1, 9):
        for y in range(1, 9):
            if board[x][y] == EMPTY:
                if any(isValidMove(board, BLACK, (x, y)) for (dx, dy) in DIRECTIONS):
                    return False
                if any(isValidMove(board, WHITE, (x, y)) for (dx, dy) in DIRECTIONS):
                    return False
    return True

# Function to get all possible moves for a player
def get_all_moves(board, player):
    return [(x, y) for x in range(1, 9) for y in range(1, 9) if isValidMove(board, player, (x, y))]

# Function to get the best move for a player using alpha-beta pruning
def get_best_move(board, player, level):
    moves = get_all_moves(board, player)
    if not moves:
        return None
    best_move = moves[0]
    best_score = float('-inf')
    # Iterate over all possible moves and select the one with the highest score
    for move in moves:
        new_board = make_move(copy.deepcopy(board), player, move)
        score = alpha_beta_pruning(new_board, WHITE if player == BLACK else BLACK, float('-inf'), float('inf'), level)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

# Function to calculate the score for each player
def calculate_score(board):
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    return black_score, white_score

# Function to display the scores on the screen
def display_score(black_score, white_score):
    font = pygame.font.Font(None, 36)
    black_text = font.render(f"Black Score: {black_score}", True, BLACK)
    white_text = font.render(f"White Score: {white_score}", True, WHITE)
    screen.blit(black_text, (10, 10))
    screen.blit(white_text, (10, 50))

# Initialize pygame and set up the screen
pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GREEN = (10, 130, 0)
LIGHT_GREEN = (0, 120, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED=(225, 26, 60)

board_size = 8
cell_size = SCREEN_WIDTH // board_size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))# Initialize the screen
pygame.display.set_caption("Othello Board")
rectangles = []# List to store rectangles

# Function to initialize the game board and draw the initial state
def initialize_board():
    screen.fill(GREEN)
    board = initial_board()
    for row in range(board_size):
        for col in range(board_size):
            x = col * cell_size
            y = row * cell_size
            if (row + col) % 2 == 0:
                color = GREEN
            else:
                color = LIGHT_GREEN
            rect_dict = {
                "rect": pygame.Rect(x, y, cell_size, cell_size),
                "color": color,
                "clicked": False,
                "disk_color": None
            }
            rectangles.append(rect_dict)
    rectangles[27]["clicked"] = True
    rectangles[27]["disk_color"] = WHITE
    rectangles[36]["clicked"] = True
    rectangles[36]["disk_color"] = WHITE
    rectangles[28]["clicked"] = True
    rectangles[28]["disk_color"] = BLACK
    rectangles[35]["clicked"] = True
    rectangles[35]["disk_color"] = BLACK

# Function to display the level selection screen
def display_level_selection():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text_easy = font.render("Easy", True, BLACK)
    text_medium = font.render("Medium", True, BLACK)
    text_hard = font.render("Hard", True, BLACK)
    screen.blit(text_easy, (250, 100))
    screen.blit(text_medium, (250, 200))
    screen.blit(text_hard, (250, 300))
    pygame.display.update()

# Function to display the "Game Over" message
def display_game_over_message():
    font = pygame.font.Font(None, 100)
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()

# Function to clear the screen
def clear_screen():
    screen.fill(BLACK)
    pygame.display.update()

# Main function to run the game
def main():
    initialize_board()
    selected_level = None
    # Loop until a level is selected
    while not selected_level:
        display_level_selection()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 250 < x < 450:
                    if 100 < y < 150:
                        selected_level = 2#easy
                    elif 200 < y < 250:
                        selected_level = 3 #medium
                    elif 300 < y < 350:
                        selected_level = 5 #hard
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    board = initial_board()
    while True:
        screen.fill((0, 0, 0))
        # Update the board state and display
        for x in range(1, 9):
            for y in range(1, 9):
                if board[x][y] == BLACK:
                    rectangles[(x - 1) * board_size + y - 1]["clicked"] = True
                    rectangles[(x - 1) * board_size + y - 1]["disk_color"] = BLACK
                elif board[x][y] == WHITE:
                    rectangles[(x - 1) * board_size + y - 1]["clicked"] = True
                    rectangles[(x - 1) * board_size + y - 1]["disk_color"] = WHITE
        for r in rectangles:  # Draw rectangles
            pygame.draw.rect(screen, r["color"], r["rect"])
            if r["clicked"]:
                pygame.draw.circle(screen, r["disk_color"], (r["rect"].centerx, r["rect"].centery),
                                   min(cell_size // 2 - 2, 20))
        for x in range(1, 9):# Highlight valid moves with black circles
            for y in range(1, 9):
                if isValidMove(board, BLACK, (x, y)):
                    pygame.draw.circle(screen, BLACK, (y * cell_size - cell_size // 2, x * cell_size - cell_size // 2),
                                       min(cell_size // 4, 10), 3)  # Draw a black circle with a radius of cell_size/4

        pygame.display.update()
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()  # Get click position
                for r in rectangles:  # Check each rectangle
                    if r["rect"].collidepoint(x, y):  # Check if click is within rectangle
                        # Calculate the move
                        move = (r["rect"].y // cell_size + 1, r["rect"].x // cell_size + 1)
                        if isValidMove(board, BLACK, move):# Check if the move is valid
                            # Make the move
                            board = make_move(board, BLACK, move)
                            # Let the computer make a move
                            move = get_best_move(board, WHITE, selected_level)
                            if move:
                                # Update the board
                                board = make_move(board, WHITE, move)
                            else:
                                game_over=True
                                clear_screen()
                                display_game_over_message()
                                pygame.time.wait(5000)
                                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Check if the game is in a terminal state
        if is_terminal(board):
            game_over = True
            black_score, white_score = calculate_score(board)
            display_score(black_score, white_score)
            pygame.display.update()
            pygame.time.wait(8000)
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level Selection")
    main()
