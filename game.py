import pygame
import random
import settings
from tetriminos import Tetromino
from board import Board


class Game:
    """Main game controller."""
    
    def __init__(self):
        self.board = Board()
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        pygame.display.set_caption('Tetris')
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game state
        self.state = settings.GameState.PLAYING
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = settings.INITIAL_FALL_SPEED
        
        # Tetromino management
        self.current_tetromino = self._spawn_tetromino()
        self.next_tetromino = self._spawn_tetromino()
        self.ghost_tetromino = None
        
        # Set up fall timer
        pygame.time.set_timer(settings.TETROMINO_FALL_EVENT, self.fall_speed)
    
    def _spawn_tetromino(self):
        """Spawn a new random tetromino."""
        shapes = list(settings.TETROMINO_SHAPES.keys())
        shape = random.choice(shapes)
        return Tetromino(shape, self.board.width)
    
    def _get_ghost_tetromino(self):
        """Get a ghost tetromino showing where current piece will land."""
        ghost = Tetromino(self.current_tetromino.shape, self.board.width)
        ghost.x = self.current_tetromino.x
        ghost.y = self.current_tetromino.y
        ghost.rotation_index = self.current_tetromino.rotation_index
        
        # Move ghost down until collision
        while self.board.is_valid_position(ghost):
            ghost.y += 1
        ghost.y -= 1
        
        return ghost
    
    def _update_fall_speed(self):
        """Update fall speed based on level."""
        new_speed = max(
            settings.MIN_FALL_SPEED,
            settings.INITIAL_FALL_SPEED - (self.level - 1) * settings.FALL_SPEED_DECREASE
        )
        pygame.time.set_timer(settings.TETROMINO_FALL_EVENT, new_speed)
        self.fall_speed = new_speed
    
    def _add_score(self, lines):
        """Add score based on lines cleared."""
        multipliers = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        score = multipliers.get(lines, 0) * self.level
        self.score += score
    
    def handle_input(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.state == settings.GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.__init__()  # Restart game
                    continue
                
                if event.key == pygame.K_SPACE:
                    self.state = settings.GameState.PAUSED if self.state == settings.GameState.PLAYING else settings.GameState.PLAYING
                
                if self.state == settings.GameState.PLAYING:
                    if event.key == pygame.K_LEFT:
                        self.current_tetromino.move_left()
                        if not self.board.is_valid_position(self.current_tetromino):
                            self.current_tetromino.move_right()
                    
                    elif event.key == pygame.K_RIGHT:
                        self.current_tetromino.move_right()
                        if not self.board.is_valid_position(self.current_tetromino):
                            self.current_tetromino.move_left()
                    
                    elif event.key == pygame.K_DOWN:
                        self.current_tetromino.move_down()
                        if not self.board.is_valid_position(self.current_tetromino):
                            self.current_tetromino.y -= 1
                    
                    elif event.key == pygame.K_UP:
                        old_rotation = self.current_tetromino.rotation_index
                        self.current_tetromino.rotate()
                        if not self.board.is_valid_position(self.current_tetromino):
                            self.current_tetromino.rotation_index = old_rotation
        
        return True
    
    def update(self):
        """Update game logic."""
        if self.state != settings.GameState.PLAYING:
            return
        
        # Check for tetromino fall event
        for event in pygame.event.get():
            if event.type == settings.TETROMINO_FALL_EVENT:
                self.current_tetromino.move_down()
                
                if not self.board.is_valid_position(self.current_tetromino):
                    # Place tetromino
                    self.current_tetromino.y -= 1
                    self.board.place_tetromino(self.current_tetromino)
                    
                    # Check for game over
                    if self.board.is_game_over(self.current_tetromino):
                        self.state = settings.GameState.GAME_OVER
                        return
                    
                    # Clear rows and update score
                    rows_cleared = self.board.clear_rows()
                    if rows_cleared > 0:
                        self._add_score(rows_cleared)
                        self.lines_cleared += rows_cleared
                        
                        # Update level
                        new_level = (self.lines_cleared // settings.LINES_PER_LEVEL) + 1
                        if new_level > self.level:
                            self.level = new_level
                            self._update_fall_speed()
                    
                    # Spawn new tetromino
                    self.current_tetromino = self.next_tetromino
                    self.next_tetromino = self._spawn_tetromino()
    
    def draw(self):
        """Draw game to screen."""
        self.screen.fill(settings.COLORS['background'])
        
        # Draw grid
        self._draw_board()
        
        # Draw ghost tetromino
        if self.state == settings.GameState.PLAYING:
            self._draw_ghost()
        
        # Draw current tetromino
        if self.state != settings.GameState.GAME_OVER:
            self._draw_tetromino(self.current_tetromino, settings.COLORS['text'])
        
        # Draw info panel
        self._draw_info_panel()
        
        # Draw pause overlay
        if self.state == settings.GameState.PAUSED:
            self._draw_pause_overlay()
        
        # Draw game over overlay
        if self.state == settings.GameState.GAME_OVER:
            self._draw_game_over_overlay()
        
        pygame.display.flip()
    
    def _draw_board(self):
        """Draw the game board."""
        board_left = 10
        board_top = 10
        
        # Draw background grid
        for y in range(self.board.height):
            for x in range(self.board.width):
                rect = pygame.Rect(
                    board_left + x * settings.BLOCK_SIZE,
                    board_top + y * settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, settings.COLORS['grid'], rect, 1)
                
                # Draw placed blocks
                if self.board.grid[y][x] is not None:
                    pygame.draw.rect(self.screen, self.board.grid[y][x], rect)
    
    def _draw_tetromino(self, tetromino, color, alpha=255):
        """Draw a tetromino."""
        board_left = 10
        board_top = 10
        
        for x, y in tetromino.get_blocks():
            if y >= 0:  # Don't draw above screen
                rect = pygame.Rect(
                    board_left + x * settings.BLOCK_SIZE,
                    board_top + y * settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
    
    def _draw_ghost(self):
        """Draw ghost tetromino."""
        self.ghost_tetromino = self._get_ghost_tetromino()
        board_left = 10
        board_top = 10
        
        ghost_color = tuple(int(c * 0.3) for c in self.current_tetromino.color)
        
        for x, y in self.ghost_tetromino.get_blocks():
            if y >= 0:
                rect = pygame.Rect(
                    board_left + x * settings.BLOCK_SIZE,
                    board_top + y * settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, ghost_color, rect, 1)
    
    def _draw_info_panel(self):
        """Draw the info panel on the right."""
        panel_x = self.board.width * settings.BLOCK_SIZE + 30
        
        # Title
        title = self.font_large.render('TETRIS', True, settings.COLORS['text'])
        self.screen.blit(title, (panel_x, 20))
        
        # Score
        score_label = self.font_medium.render('Score', True, settings.COLORS['text'])
        self.screen.blit(score_label, (panel_x, 100))
        score_value = self.font_small.render(str(self.score), True, settings.COLORS['text'])
        self.screen.blit(score_value, (panel_x, 140))
        
        # Level
        level_label = self.font_medium.render('Level', True, settings.COLORS['text'])
        self.screen.blit(level_label, (panel_x, 200))
        level_value = self.font_small.render(str(self.level), True, settings.COLORS['text'])
        self.screen.blit(level_value, (panel_x, 240))
        
        # Lines
        lines_label = self.font_medium.render('Lines', True, settings.COLORS['text'])
        self.screen.blit(lines_label, (panel_x, 300))
        lines_value = self.font_small.render(str(self.lines_cleared), True, settings.COLORS['text'])
        self.screen.blit(lines_value, (panel_x, 340))
        
        # Next tetromino
        next_label = self.font_medium.render('Next', True, settings.COLORS['text'])
        self.screen.blit(next_label, (panel_x, 400))
        
        # Draw next tetromino preview
        preview_x = panel_x
        preview_y = 450
        for x, y in self.next_tetromino.get_blocks():
            rect = pygame.Rect(
                preview_x + x * settings.BLOCK_SIZE // 2,
                preview_y + y * settings.BLOCK_SIZE // 2,
                settings.BLOCK_SIZE // 2,
                settings.BLOCK_SIZE // 2
            )
            pygame.draw.rect(self.screen, self.next_tetromino.color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
    
    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        overlay = pygame.Surface(settings.WINDOW_SIZE)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render('PAUSED', True, settings.COLORS['text'])
        pause_rect = pause_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font_small.render('Press SPACE to continue', True, settings.COLORS['text'])
        continue_rect = continue_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)
    
    def _draw_game_over_overlay(self):
        """Draw game over overlay."""
        overlay = pygame.Surface(settings.WINDOW_SIZE)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render('GAME OVER', True, settings.COLORS['text'])
        game_over_rect = game_over_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f'Score: {self.score}', True, settings.COLORS['text'])
        score_rect = score_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font_small.render('Press SPACE to restart', True, settings.COLORS['text'])
        restart_rect = restart_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        
        pygame.quit()
