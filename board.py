import settings


class Board:
    """Represents the game board/grid."""
    
    def __init__(self, width=settings.GRID_WIDTH, height=settings.GRID_HEIGHT):
        self.width = width
        self.height = height
        # Grid: 0 = empty, color tuple = filled with that color
        self.grid = [[None for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, tetromino):
        """Check if tetromino can be placed at its current position."""
        blocks = tetromino.get_blocks()
        for x, y in blocks:
            # Check boundaries
            if x < 0 or x >= self.width or y >= self.height:
                return False
            # Check collision with placed blocks
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    
    def place_tetromino(self, tetromino):
        """Place tetromino blocks on the board."""
        blocks = tetromino.get_blocks()
        for x, y in blocks:
            if 0 <= y < self.height:
                self.grid[y][x] = tetromino.color
    
    def clear_rows(self):
        """Clear complete rows and return count."""
        rows_cleared = 0
        
        # Check each row from bottom to top
        rows_to_remove = []
        for row_idx in range(self.height - 1, -1, -1):
            if all(cell is not None for cell in self.grid[row_idx]):
                rows_to_remove.append(row_idx)
        
        # Remove complete rows
        for row_idx in sorted(rows_to_remove, reverse=True):
            self.grid.pop(row_idx)
            # Insert empty row at top
            self.grid.insert(0, [None for _ in range(self.width)])
        
        return len(rows_to_remove)
    
    def get_next_y_position(self, tetromino):
        """Get the y position where tetromino will land."""
        tetromino.y += 1
        while self.is_valid_position(tetromino):
            tetromino.y += 1
        tetromino.y -= 1
        landing_y = tetromino.y
        tetromino.y -= 1  # Move back to original position
        return landing_y
    
    def is_game_over(self, tetromino):
        """Check if tetromino collides at spawn position."""
        return not self.is_valid_position(tetromino)
