import settings

# Tetromino shapes (4x4 grids where 1 = filled block, 0 = empty)
TETROMINO_SHAPES = {
    'I': {
        'color': settings.COLORS['I'],
        'patterns': [
            [[1, 1, 1, 1]],
            [[1], [1], [1], [1]]
        ]
    },
    'O': {
        'color': settings.COLORS['O'],
        'patterns': [
            [[1, 1], [1, 1]]
        ]
    },
    'T': {
        'color': settings.COLORS['T'],
        'patterns': [
            [[0, 1, 0], [1, 1, 1]],
            [[1, 0], [1, 1], [1, 0]],
            [[1, 1, 1], [0, 1, 0]],
            [[0, 1], [1, 1], [0, 1]]
        ]
    },
    'S': {
        'color': settings.COLORS['S'],
        'patterns': [
            [[0, 1, 1], [1, 1, 0]],
            [[1, 0], [1, 1], [0, 1]]
        ]
    },
    'Z': {
        'color': settings.COLORS['Z'],
        'patterns': [
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1], [1, 1], [1, 0]]
        ]
    },
    'J': {
        'color': settings.COLORS['J'],
        'patterns': [
            [[1, 0, 0], [1, 1, 1]],
            [[1, 1], [1, 0], [1, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[0, 1], [0, 1], [1, 1]]
        ]
    },
    'L': {
        'color': settings.COLORS['L'],
        'patterns': [
            [[0, 0, 1], [1, 1, 1]],
            [[1, 0], [1, 0], [1, 1]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1], [0, 1], [0, 1]]
        ]
    }
}


class Tetromino:
    """Represents a falling tetromino piece."""
    
    def __init__(self, shape, grid_width):
        self.shape = shape
        self.color = TETROMINO_SHAPES[shape]['color']
        self.rotation_index = 0
        self.patterns = TETROMINO_SHAPES[shape]['patterns']
        self.grid_width = grid_width
        
        # Spawn at top center
        self.pattern = self.patterns[self.rotation_index]
        self.x = (grid_width - len(self.pattern[0])) // 2
        self.y = 0
    
    def get_blocks(self):
        """Return list of (x, y) coordinates for this tetromino's blocks."""
        blocks = []
        pattern = self.patterns[self.rotation_index]
        for row_idx, row in enumerate(pattern):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    blocks.append((self.x + col_idx, self.y + row_idx))
        return blocks
    
    def rotate(self):
        """Rotate the tetromino 90 degrees clockwise."""
        old_rotation = self.rotation_index
        self.rotation_index = (self.rotation_index + 1) % len(self.patterns)
        
        # Check if rotation is valid
        pattern = self.patterns[self.rotation_index]
        width = len(pattern[0])
        
        # Adjust x position if piece goes out of bounds
        if self.x + width > self.grid_width:
            self.x = self.grid_width - width
        if self.x < 0:
            self.x = 0
    
    def move_left(self):
        """Move tetromino left."""
        self.x -= 1
        self._clamp_x()
    
    def move_right(self):
        """Move tetromino right."""
        self.x += 1
        self._clamp_x()
    
    def move_down(self):
        """Move tetromino down."""
        self.y += 1
    
    def _clamp_x(self):
        """Ensure x position stays within bounds."""
        pattern = self.patterns[self.rotation_index]
        width = len(pattern[0])
        if self.x < 0:
            self.x = 0
        if self.x + width > self.grid_width:
            self.x = self.grid_width - width
