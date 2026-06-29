"""
Input handler module for the Retro Snake Game.
Manages keyboard input and direction changes.
"""

import pygame

# Key aliases for convenience
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_w = pygame.K_w
K_a = pygame.K_a
K_s = pygame.K_s
K_d = pygame.K_d
K_SPACE = pygame.K_SPACE
K_RETURN = pygame.K_RETURN
K_r = pygame.K_r
K_ESCAPE = pygame.K_ESCAPE
K_q = pygame.K_q

class InputHandler:
    """Handles all keyboard input for the game."""

    def __init__(self):
        self.current_direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.game_paused = False

    def handle_events(self, events, game_state):
        """Process pygame events and update game state."""
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                # Game controls
                if game_state == "PLAYING":
                    self._handle_playing_controls(event.key)
                elif game_state == "GAME_OVER":
                    result = self._handle_game_over_controls(event.key)
                    if result:
                        return result
                elif game_state == "MENU":
                    result = self._handle_menu_controls(event.key)
                    if result:
                        return result

        return game_state

    def _handle_playing_controls(self, key):
        """Handle keyboard input during gameplay."""
        # Direction controls (WASD or Arrow keys)
        if key in (K_LEFT, K_a):
            if self.current_direction != "RIGHT":
                self.next_direction = "LEFT"
        elif key in (K_RIGHT, K_d):
            if self.current_direction != "LEFT":
                self.next_direction = "RIGHT"
        elif key in (K_UP, K_w):
            if self.current_direction != "DOWN":
                self.next_direction = "UP"
        elif key in (K_DOWN, K_s):
            if self.current_direction != "UP":
                self.next_direction = "DOWN"

        # Pause toggle
        if key == pygame.K_p:
            self.game_paused = not self.game_paused

    def _handle_game_over_controls(self, key):
        """Handle keyboard input on game over screen."""
        if key in (K_SPACE, K_r):
            return "RESTART"
        elif key in (K_ESCAPE, K_q):
            return "MENU"

    def _handle_menu_controls(self, key):
        """Handle keyboard input on menu screen."""
        if key in (K_SPACE, K_RETURN, K_r):
            return "START"
        elif key in (K_ESCAPE, K_q):
            return "QUIT"

    def update_direction(self):
        """Apply the next direction to current direction."""
        self.current_direction = self.next_direction

    def get_direction(self):
        """Get the current direction as a vector."""
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        return directions[self.current_direction]


