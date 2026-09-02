# Tetris Python (NOTE THIS IS CREATED BY AN AI I WILL REDO IN MY FREE TIME)

A classic Tetris game implementation in Python using Pygame, compatible with Python 3.14+

## Features

- ✨ Classic Tetris gameplay
- 🎮 Smooth controls and responsive input
- 📊 Score tracking and level progression
- 👻 Ghost piece preview showing where pieces will land
- 🎨 Colorful, modern interface
- ⏸️ Pause/Resume functionality
- 🔄 Game restart on game over

## Requirements

- Python 3.14+
- Pygame 2.5.2+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TheGazer01/tetris-python.git
cd tetris-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python run.py
```

### Controls

| Key | Action |
|-----|--------|
| **LEFT** / **RIGHT** | Move piece left/right |
| **UP** | Rotate piece clockwise |
| **DOWN** | Soft drop (faster fall) |
| **SPACE** | Pause/Unpause game |
| **ESC** | Quit game |

### Gameplay

1. Tetromino pieces fall from the top
2. Move and rotate pieces to complete horizontal lines
3. Complete lines clear and award points
4. Game ends when pieces stack to the top
5. Level increases every 10 lines cleared
6. Difficulty increases with each level (pieces fall faster)

## Game Mechanics

### Scoring
- **1 Line**: 40 × Level points
- **2 Lines**: 100 × Level points
- **3 Lines**: 300 × Level points
- **4 Lines (Tetris)**: 1200 × Level points

### Difficulty
- Initial fall speed: 800ms
- Speed increases by 50ms per level
- Minimum speed: 100ms

## Project Structure

```
tetris-python/
├── run.py              # Entry point
├── game.py             # Main game controller
├── board.py            # Game board/grid logic
├── tetriminos.py       # Tetromino piece definitions
├── settings.py         # Game configuration
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## Python 3.14 Compatibility

This game is fully compatible with Python 3.14. No external platform-specific dependencies are required beyond Pygame.

## Future Enhancements

- [ ] Sound effects and music
- [ ] High score persistence
- [ ] Difficulty selection
- [ ] Different game modes
- [ ] AI player
- [ ] Network multiplayer

## License

MIT License - Feel free to use this code for learning and personal projects!

## Contributing

Contributions are welcome! Feel free to fork, modify, and submit pull requests.

## Author

TheGazer01
