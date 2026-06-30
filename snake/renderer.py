"""
Renderer module for the Retro Snake Game.
Handles all drawing and display operations.
"""

import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    HEADER_HEIGHT,
    BLACK, WHITE, GREEN, DARK_GREEN, RED, YELLOW,
    BLUE, GRAY, LIGHT_GRAY,
    GRID_SIZE,
    TITLE_FONT_SIZE, SCORE_FONT_SIZE, GAME_OVER_FONT_SIZE, MENU_FONT_SIZE,
    SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, FOOD_COLOR, FOOD_GLOW_COLOR,
    SPECIAL_FOOD_COLOR, SPECIAL_FOOD_GLOW_COLOR, SPECIAL_FOOD_DURATION_MS
)


class Renderer:
    """Handles all rendering and display operations."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Snake")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("monospace", TITLE_FONT_SIZE, bold=True)
        self.score_font = pygame.font.SysFont("monospace", SCORE_FONT_SIZE)
        self.game_over_font = pygame.font.SysFont("monospace", GAME_OVER_FONT_SIZE, bold=True)
        self.menu_font = pygame.font.SysFont("monospace", MENU_FONT_SIZE)
        self.small_font = pygame.font.SysFont("monospace", 18)

    def render(self, game_state, game, input_handler):
        """Render the current game state."""
        self.screen.fill(BLACK)

        if game_state == "MENU":
            self._render_menu()
        elif game_state == "PLAYING":
            self._render_game(game, input_handler.game_paused)
        elif game_state == "GAME_OVER":
            self._render_game_over(game)

        pygame.display.flip()
        self.clock.tick(FPS)

    def _render_grid(self):
        """Draw a subtle grid background (excluding header area)."""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, HEADER_HEIGHT), (x, SCREEN_HEIGHT))
        for y in range(HEADER_HEIGHT, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def _render_header(self):
        """Draw the header bar background."""
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(self.screen, (20, 20, 20), header_rect)
        pygame.draw.line(self.screen, GRAY, (0, HEADER_HEIGHT), (SCREEN_WIDTH, HEADER_HEIGHT))

    def _render_header_stats(self, game):
        """Draw stats in the header bar."""
        score_text = self.score_font.render(f"Score: {game.get_score()}", True, WHITE)
        level_text = self.small_font.render(f"Level: {game.get_level()}", True, LIGHT_GRAY)
        high_text = self.small_font.render(f"High Score: {game.high_score}", True, YELLOW)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))
        self.screen.blit(high_text, (SCREEN_WIDTH - high_text.get_width() - 10, 10))

    def _render_snake(self, snake):
        """Draw the snake."""
        for i, segment in enumerate(snake.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE + HEADER_HEIGHT

            if i == 0:  # Head
                color = SNAKE_HEAD_COLOR
                size = GRID_SIZE - 2
                offset = 1
            else:  # Body
                color = SNAKE_BODY_COLOR
                size = GRID_SIZE - 4
                offset = 2

            rect = pygame.Rect(x + offset, y + offset, size, size)
            pygame.draw.rect(self.screen, color, rect)

            # Draw eyes on head
            if i == 0:
                head_x, head_y = segment
                dx, dy = snake.direction

                eye_size = 3
                if dx == 1:  # Moving right
                    eye1_pos = (x + GRID_SIZE - 6, y + 5)
                    eye2_pos = (x + GRID_SIZE - 6, y + GRID_SIZE - 8)
                elif dx == -1:  # Moving left
                    eye1_pos = (x + 3, y + 5)
                    eye2_pos = (x + 3, y + GRID_SIZE - 8)
                elif dy == -1:  # Moving up
                    eye1_pos = (x + 5, y + 3)
                    eye2_pos = (x + GRID_SIZE - 8, y + 3)
                else:  # Moving down
                    eye1_pos = (x + 5, y + GRID_SIZE - 6)
                    eye2_pos = (x + GRID_SIZE - 8, y + GRID_SIZE - 6)

                pygame.draw.circle(self.screen, WHITE, eye1_pos, eye_size)
                pygame.draw.circle(self.screen, WHITE, eye2_pos, eye_size)

    def _render_food(self, food):
        """Draw the food with a glow effect."""
        x = food.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = food.position[1] * GRID_SIZE + GRID_SIZE // 2 + HEADER_HEIGHT

        if food.is_special:
            # Special food - yellow with blinking effect
            remaining_ms = food.get_remaining_ms()
            
            # Blink faster as time runs out (last 2 seconds)
            if remaining_ms < 2000:
                # Blink every other frame when less than 2 seconds remain
                blink_interval = remaining_ms / 10  # Very fast blink
                if int(remaining_ms / blink_interval) % 2 == 0:
                    return  # Skip drawing (blink effect)
            
            # Glow effect for special food
            for radius in range(6, 0, -1):
                alpha_color = (*SPECIAL_FOOD_GLOW_COLOR, max(0, 60 - radius * 10))
                glow_surf = pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*SPECIAL_FOOD_GLOW_COLOR[:3], 40), (GRID_SIZE, GRID_SIZE), radius * 2)
                self.screen.blit(glow_surf, (x - GRID_SIZE, y - GRID_SIZE))

            # Special food circle (larger and yellow)
            pygame.draw.circle(self.screen, SPECIAL_FOOD_COLOR, (x, y), GRID_SIZE // 2)
            
            # Draw a star/asterisk in the center to indicate special
            star_size = 4
            pygame.draw.line(self.screen, BLACK, (x - star_size, y), (x + star_size, y), 2)
            pygame.draw.line(self.screen, BLACK, (x, y - star_size), (x, y + star_size), 2)
        else:
            # Normal food - red with glow effect
            for radius in range(5, 0, -1):
                alpha_color = (*FOOD_GLOW_COLOR, max(0, 50 - radius * 10))
                glow_surf = pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*FOOD_GLOW_COLOR[:3], 30), (GRID_SIZE, GRID_SIZE), radius * 2)
                self.screen.blit(glow_surf, (x - GRID_SIZE, y - GRID_SIZE))

            # Food circle
            pygame.draw.circle(self.screen, FOOD_COLOR, (x, y), GRID_SIZE // 2 - 2)

    def _render_score(self, game):
        """Draw the score display (deprecated - use _render_header_stats instead)."""
        pass

    def _render_sidebar_header(self):
        """Draw the sidebar header (deprecated)."""
        pass

    def _render_pause(self):
        """Draw pause overlay."""
        pause_text = self.game_over_font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)

    def _render_menu(self):
        """Draw the main menu."""
        # Title
        title = self.title_font.render("RETRO SNAKE", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)

        # Decorative snake
        snake_y = SCREEN_HEIGHT // 3
        for i in range(10):
            x = SCREEN_WIDTH // 2 - 100 + i * 20
            color = GREEN if i % 2 == 0 else DARK_GREEN
            rect = pygame.Rect(x, snake_y, 18, 18)
            pygame.draw.rect(self.screen, color, rect)

        # Instructions
        instructions = [
            "Use Arrow Keys or WASD to move",
            "Press P to pause",
            "Eat food to grow and score points",
            "Avoid walls and yourself!",
            "",
            "Press SPACE or R to Start",
            "Press ESC or Q to Quit"
        ]

        y_offset = SCREEN_HEIGHT // 2
        for instruction in instructions:
            if instruction.startswith("Press"):
                color = YELLOW
            else:
                color = LIGHT_GRAY
            text = self.menu_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

    def _render_game(self, game, paused=False):
        """Draw the gameplay screen."""
        self._render_header()
        self._render_grid()
        self._render_food(game.food)
        self._render_snake(game.snake)
        self._render_header_stats(game)

        if paused:
            self._render_pause()

    def _render_game_over(self, game):
        """Draw the game over screen."""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over = self.game_over_font.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over, game_over_rect)

        # Score display
        score_text = self.score_font.render(f"Score: {game.get_score()}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(score_text, score_rect)

        # High score
        if game.get_score() >= game.high_score and game.get_score() > 0:
            new_high = self.score_font.render("NEW HIGH SCORE!", True, YELLOW)
            new_high_rect = new_high.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(new_high, new_high_rect)

        # Level reached
        level_text = self.small_font.render(f"Level Reached: {game.get_level()}", True, LIGHT_GRAY)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(level_text, level_rect)

        # Restart prompt
        restart_text = self.menu_font.render("Press SPACE or R to Play Again", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(restart_text, restart_rect)

        # Menu prompt
        menu_text = self.menu_font.render("Press ESC or Q to Return to Menu", True, LIGHT_GRAY)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 40))
        self.screen.blit(menu_text, menu_rect)

    def quit(self):
        """Clean up pygame resources."""
        pygame.quit()
