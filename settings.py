import pygame
import math

# ======================================================================
# Editable settings

FPS = 60
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors (RGB)
COLORS = {
    'background': (20, 25, 30),
    'grid': (50, 60, 70),
    'text': (255, 255, 255),
    'I': (0, 240, 240),      # Cyan
    'O': (255, 240, 0),      # Yellow
    'T': (160, 0, 240),      # Purple
    'S': (0, 240, 0),        # Green
    'Z': (240, 0, 0),        # Red
    'J': (0, 0, 240),        # Blue
    'L': (240, 160, 0),      # Orange
}

# Game mechanics
INITIAL_FALL_SPEED = 800  # milliseconds
MIN_FALL_SPEED = 100      # milliseconds
FALL_SPEED_DECREASE = 50  # per level
LINES_PER_LEVEL = 10

# ======================================================================
# Game constants - do not edit

pygame.init()

WINDOW_WIDTH = GRID_WIDTH * BLOCK_SIZE + 200
WINDOW_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Game states
class GameState:
    PLAYING = 'playing'
    PAUSED = 'paused'
    GAME_OVER = 'game_over'

# Events
TETROMINO_FALL_EVENT = pygame.USEREVENT + 1
GAME_UPDATE_EVENT = pygame.USEREVENT + 2
