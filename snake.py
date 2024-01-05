import pygame
import time
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)
        self.food = self.spawn_food()
        self.running = False
        self.food_counter = 0

    def spawn_food(self):
        while True:
            food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
            if food not in self.snake:
                return food

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def draw_food(self):
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], GRID_SIZE, GRID_SIZE))

    def draw_start_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Snake Game", True, WHITE)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        instruction_text1 = font.render("Use arrow keys to control the snake", True, WHITE)
        instruction_text2 = font.render("Press Enter to start", True, GREEN)
        instruction_text3 = font.render("Credits: Tejas, Vishu, Roshan", True, YELLOW)

        self.screen.blit(instruction_text1, (WIDTH // 2 - instruction_text1.get_width() // 2, HEIGHT // 2))
        self.screen.blit(instruction_text2, (WIDTH // 2 - instruction_text2.get_width() // 2, HEIGHT // 2 + 50))
        self.screen.blit(instruction_text3, (WIDTH // 2 - instruction_text3.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

    def draw_game_over_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {self.food_counter}", True, WHITE)
        restart_text = font.render("Press Enter to play again", True, WHITE)

        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

    def add_score(self):
        self.food_counter += 1

    def move_snake(self):
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        self.snake.insert(0, head)
        if head == self.food:
            self.food = self.spawn_food()
            self.add_score()  # Increment the score
            # Increase FPS every 5 foods eaten
            if self.food_counter % 5 == 0:
                self.increase_fps()
        else:
            self.snake.pop()

    def increase_fps(self):
        global FPS
        FPS += 1
        self.clock.tick(FPS)  # Adjust the clock with the new FPS

    def check_collision(self):
        head = self.snake[0]
        return (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in self.snake[1:]
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if not self.running and event.key == pygame.K_RETURN:
                        self.running = True
                    elif self.running:
                        if event.key == pygame.K_UP and self.direction != (0, GRID_SIZE):
                            self.direction = (0, -GRID_SIZE)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -GRID_SIZE):
                            self.direction = (0, GRID_SIZE)
                        elif event.key == pygame.K_LEFT and self.direction != (GRID_SIZE, 0):
                            self.direction = (-GRID_SIZE, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-GRID_SIZE, 0):
                            self.direction = (GRID_SIZE, 0)

            if not self.running:
                self.draw_start_screen()
            else:
                self.move_snake()
                if self.check_collision():
                    self.running = False
                    self.snake = [(WIDTH // 2, HEIGHT // 2)]
                    self.direction = (GRID_SIZE, 0)
                    self.screen.fill(BLACK)  # Clear the screen before drawing the game over screen
                    self.draw_game_over_screen()
                    pygame.display.flip()
                    pygame.time.delay(1000)  # Delay after drawing game over screen
                    self.food_counter = 0  # Reset the food counter
                else:
                    self.screen.fill(BLACK)
                    self.draw_snake()
                    self.draw_food()
                    pygame.display.flip()
                    self.clock.tick(FPS)

                    # Check if snake eats food
                    head = self.snake[0]
                    if head == self.food:
                        self.add_score()  # Increment the score
                        self.food = self.spawn_food()
                        # Increase FPS every 5 foods eaten
                        if self.food_counter % 5 == 0:
                            self.increase_fps()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
