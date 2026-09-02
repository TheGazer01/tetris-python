#!/usr/bin/env python3
"""
Tetris Game - Run this file to start playing!
Controls:
  - LEFT/RIGHT arrows: Move piece
  - UP arrow: Rotate piece
  - DOWN arrow: Soft drop (faster fall)
  - SPACE: Pause/Unpause
  - ESC: Quit
"""

import pygame
from game import Game


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
