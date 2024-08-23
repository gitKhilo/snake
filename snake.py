import pygame
import random

pygame.init()

# Set up display (1.5x larger)
width, height = 900, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)
white = (255, 255, 255)

# Set up clock and speed
clock = pygame.time.Clock()
snake_speed = 10
snake_block = 30  # 3x bigger

# Set up fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        pygame.draw.rect(display, green, [x[0], x[1], snake_block, snake_block])
        pygame.draw.circle(display, black, (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 4)

def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(display, red, [wall[0], wall[1], wall[2], wall[3]])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 30.0) * 30.0
    foody = round(random.randrange(0, height - snake_block) / 30.0) * 30.0

    # Define walls (3 or 4 small walls)
    walls = [
        (150, 150, 300, 30),  # Horizontal wall
        (450, 450, 30, 300),  # Vertical wall
        (600, 100, 200, 30),  # Horizontal wall
    ]

    while not game_over:

        while game_close:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        display.fill(blue)

        # Draw food and walls
        pygame.draw.rect(display, white, [foodx, foody, snake_block, snake_block])
        draw_walls(walls)

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collision with walls or self
        if any([x == snake_head for x in snake_list[:-1]]) or any([wall[0] <= x1 < wall[0] + wall[2] and wall[1] <= y1 < wall[1] + wall[3] for wall in walls]):
            game_close = True

        draw_snake(snake_block, snake_list)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 30.0) * 30.0
            foody = round(random.randrange(0, height - snake_block) / 30.0) * 30.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
