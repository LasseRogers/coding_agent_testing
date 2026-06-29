#!/usr/bin/env python3
"""
Retro Snake Game - Main Entry Point

A classic snake game built with Pygame, organized into modular components:
- config.py: Game constants and settings
- input_handler.py: Keyboard input management
- game_logic.py: Snake, Food, and game state logic
- renderer.py: All drawing and display operations
"""

import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from input_handler import InputHandler
from game_logic import Game
from renderer import Renderer


def main():
    """Main game loop."""
    # Initialize components
    renderer = Renderer()
    input_handler = InputHandler()
    game = Game()

    # Game states: "MENU", "PLAYING", "GAME_OVER"
    game_state = "MENU"

    print("=" * 50)
    print("  RETRO SNAKE GAME")
    print("=" * 50)
    print("  Controls:")
    print("    Arrow Keys / WASD - Move")
    print("    P - Pause/Resume")
    print("    SPACE / R - Start/Restart")
    print("    ESC / Q - Quit")
    print("=" * 50)

    running = True

    while running:
        # Handle pygame events
        events = pygame.event.get()
        game_state = input_handler.handle_events(events, game_state)

        # State transitions
        if game_state == "QUIT":
            running = False
            break
        elif game_state == "START":
            game.reset()
            input_handler.game_paused = False
            game_state = "PLAYING"
        elif game_state == "RESTART":
            game.reset()
            input_handler.game_paused = False
            game_state = "PLAYING"

        # Update game logic during gameplay
        if game_state == "PLAYING":
            if not input_handler.game_paused:
                direction = input_handler.get_direction()
                collision = game.update(direction)
                input_handler.update_direction()

                if collision:
                    game.update_high_score()
                    game_state = "GAME_OVER"

        # Render current state
        renderer.render(game_state, game, input_handler)

    # Cleanup
    game.update_high_score()
    renderer.quit()
    print(f"\nThanks for playing! Final Score: {game.get_score()}")
    print(f"High Score: {game.high_score}")
    sys.exit(0)


if __name__ == "__main__":
    main()


