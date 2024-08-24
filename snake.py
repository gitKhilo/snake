import pygame
import random

pygame.init()

# Set up display (1.5x larger)
width, height = 900, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set up snake block size and other constants
snake_block = 30  # 3x bigger
snake_speed = 10
num_walls = 4  # Number of walls to appear

# Load and scale images
snake_head_img = pygame.image.load('snake_head.png')
snake_body_img = pygame.image.load('snake_body.png')
apple_img = pygame.image.load('apple.png')
background_img = pygame.image.load('background.png')
wall_img = pygame.image.load('wall.png')

snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))
wall_img = pygame.transform.scale(wall_img, (snake_block, snake_block))
background_img = pygame.transform.scale(background_img, (width, height))

# Set up clock and fonts
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_snake(snake_list):
    for i, pos in enumerate(snake_list):
        if i == 0:
            display.blit(snake_head_img, pos)
        else:
            display.blit(snake_body_img, pos)

def draw_walls(walls):
    for wall in walls:
        display.blit(wall_img, wall)

def draw_food(foodx, foody):
    display.blit(apple_img, (foodx, foody))

def show_score(score):
    value = score_font.render(f"Score: {score}", True, (255, 255, 255))
    display.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def generate_random_walls(num_walls):
    walls = []
    for _ in range(num_walls):
        wall_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
        wall_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
        walls.append([wall_x, wall_y])
    return walls

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

    walls = generate_random_walls(num_walls)

    while not game_over:

        while game_close:
            display.blit(background_img, (0, 0))
            message("You Lost! Press C-Play Again or Q-Quit", (213, 50, 80))
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

        # Wrap the snake around the screen
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        x1 += x1_change
        y1 += y1_change

        # Clear the screen by re-drawing the background
        display.blit(background_img, (0, 0))

        # Draw food, walls, and score
        draw_food(foodx, foody)
        draw_walls(walls)
        show_score(score)

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collision with walls or self
        if any([x == snake_head for x in snake_list[:-1]]) or any([wall[0] <= x1 < wall[0] + snake_block and wall[1] <= y1 < wall[1] + snake_block for wall in walls]):
            game_close = True

        draw_snake(snake_list)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
