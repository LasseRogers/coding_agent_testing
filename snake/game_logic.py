"""
Game logic module for the Retro Snake Game.
Handles snake movement, food spawning, collision detection, and scoring.
"""

import random
from config import (
    GRID_WIDTH, GRID_HEIGHT,
    SNAKE_START_LENGTH, SNAKE_INITIAL_POSITION,
    SCORE_PER_FOOD, LEVEL_UP_SCORE
)


class Food:
    """Represents food in the game."""

    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, snake_body=None):
        """Spawn food at a random position not occupied by the snake."""
        if snake_body is None:
            snake_body = []

        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                break


class Snake:
    """Represents the snake in the game."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset snake to initial state."""
        start_x, start_y = SNAKE_INITIAL_POSITION
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = (1, 0)  # Moving right initially
        self.grow_pending = 0

    def move(self, direction):
        """Move the snake in the given direction."""
        self.direction = direction

        # Calculate new head position
        head_x, head_y = self.body[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self):
        """Queue the snake to grow on next move."""
        self.grow_pending += 1

    def check_self_collision(self):
        """Check if the snake has collided with itself."""
        head = self.body[0]
        return head in self.body[1:]

    def get_head_position(self):
        """Get the current head position."""
        return self.body[0]


class Game:
    """Main game logic controller."""

    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.level = 1
        self.high_score = 0
        self.food.spawn(self.snake.body)

    def reset(self):
        """Reset the game to initial state."""
        self.snake.reset()
        self.score = 0
        self.level = 1
        self.food.spawn(self.snake.body)

    def update(self, direction):
        """Update game state by one frame."""
        # Move snake
        self.snake.move(direction)

        # Check food collision
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.score += SCORE_PER_FOOD * self.level

            # Level up every LEVEL_UP_SCORE points
            new_level = (self.score // LEVEL_UP_SCORE) + 1
            if new_level > self.level:
                self.level = new_level

            # Spawn new food
            self.food.spawn(self.snake.body)

        # Check collisions
        return self.check_collisions()

    def check_collisions(self):
        """Check all collision conditions. Returns True if collision occurred."""
        head = self.snake.get_head_position()

        # Wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True

        # Self collision
        if self.snake.check_self_collision():
            return True

        return False

    def get_score(self):
        """Get current score."""
        return self.score

    def get_level(self):
        """Get current level."""
        return self.level

    def update_high_score(self):
        """Update high score if current score is higher."""
        if self.score > self.high_score:
            self.high_score = self.score


