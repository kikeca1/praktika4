import pygame
import time
import random
import os

pygame.init()

# Размер на екрана
dis_width = 800
dis_height = 600

# Настройка на дисплея
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Зареждане на задния план (background)
background_img = pygame.image.load('C:/Users/User/Desktop/Snake Game/praktika4/background.png')
background_img = pygame.transform.scale(background_img, (dis_width, dis_height))

clock = pygame.time.Clock()
snake_block = 30  # Размер на блока на змията
normal_speed = 10  # Скорост за нормалното ниво
hard_speed = 15  # Скорост за трудното ниво

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Зареждане на изображения за главата на змията в различни посоки
snake_head_up = pygame.image.load('C:/Users/User/Desktop/Snake Game/praktika4/snake_head_up.png')
snake_head_down = pygame.image.load('C:/Users/User/Desktop/Snake Game/praktika4/snake_head_down.png')
snake_head_left = pygame.image.load('C:/Users/User/Desktop/Snake Game/praktika4/snake_head_left.png')
snake_head_right = pygame.image.load('C:/Users/User/Desktop/Snake Game/praktika4/snake_head_right.png')

# Преоразмеряване на изображенията на главата на змията
snake_head_up = pygame.transform.scale(snake_head_up, (snake_block, snake_block))
snake_head_down = pygame.transform.scale(snake_head_down, (snake_block, snake_block))
snake_head_left = pygame.transform.scale(snake_head_left, (snake_block, snake_block))
snake_head_right = pygame.transform.scale(snake_head_right, (snake_block, snake_block))

# Зареждане на изображението на ябълката
apple_img = pygame.image.load('C:/Users/User/Desktop/Snake Game/praktika4/apple.png')
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

# Зареждане на фоновата музика
pygame.mixer.music.load('C:/Users/User/Desktop/Snake Game/praktika4/music.mp3')
pygame.mixer.music.play(-1)  # Пускане на музиката на повторение

# Проверка и създаване на файл за най-добрите резултати
high_score_file = 'high_score.txt'
if not os.path.exists(high_score_file):
    with open(high_score_file, 'w') as f:
        f.write('0')

def get_high_score():
    with open(high_score_file, 'r') as f:
        return int(f.read().strip())

def save_high_score(score):
    with open(high_score_file, 'w') as f:
        f.write(str(score))

def score_display(score, high_score):
    value = score_font.render("Вашият резултат: " + str(score), True, (255, 255, 102))
    high_score_value = score_font.render("Най-добър резултат: " + str(high_score), True, (255, 255, 102))
    dis.blit(value, [10, 10])
    dis.blit(high_score_value, [10, 50])

def our_snake(snake_block, snake_list, direction):
    for i, (x, y) in enumerate(snake_list):
        if i == 0:
            if direction == 'up':
                dis.blit(snake_head_up, (x, y))
            elif direction == 'down':
                dis.blit(snake_head_down, (x, y))
            elif direction == 'left':
                dis.blit(snake_head_left, (x, y))
            elif direction == 'right':
                dis.blit(snake_head_right, (x, y))
        else:
            pygame.draw.rect(dis, (0, 255, 0), [x, y, snake_block, snake_block])  # Тялото на змията е зелено

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 3))
    dis.blit(mesg, mesg_rect)

def is_collision(apple_x, apple_y, snake_x, snake_y):
    if (apple_x <= snake_x < apple_x + snake_block) or (snake_x <= apple_x < snake_x + snake_block):
        if (apple_y <= snake_y < apple_y + snake_block) or (snake_y <= apple_y < snake_y + snake_block):
            return True
    return False

def gameLoop(snake_speed):  # Приема се скоростта като параметър
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    direction = 'up'  # Първоначална посока на движение

    foodx = round(random.randrange(0, dis_width - snake_block) / 30.0) * 30.0
    foody = round(random.randrange(0, dis_height - snake_block) / 30.0) * 30.0

    high_score = get_high_score()

    while not game_over:

        while game_close == True:
            dis.blit(background_img, (0, 0))  # Показване на background
            message("Загубихте! Натиснете Q за изход или C за нова игра", (213, 50, 80))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(snake_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and direction != 'down':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'down'

        # Промяна на позицията при преминаване през стените
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block
        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        x1 += x1_change
        y1 += y1_change
        
        # Показване на background
        dis.blit(background_img, (0, 0))
        
        # Показване на ябълката
        dis.blit(apple_img, (foodx, foody))
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        
        # Проверка за колизия с ябълката
        if is_collision(foodx, foody, x1, y1):
            foodx = round(random.randrange(0, dis_width - snake_block) / 30.0) * 30.0
            foody = round(random.randrange(0, dis_height - snake_block) / 30.0) * 30.0
            Length_of_snake += 1
            if Length_of_snake > high_score:
                high_score = Length_of_snake  # Актуализиране на най-добър резултат
                save_high_score(high_score)
        
        # Добавяне на главата на змията към началото на списъка с позиции
        snake_List.insert(0, snake_Head)
        if len(snake_List) > Length_of_snake:
            snake_List.pop()

        # Проверка за колизия със собственото тяло
        for segment in snake_List[1:]:
            if segment == snake_Head:
                game_close = True

        # Показване на змията
        our_snake(snake_block, snake_List, direction)
        
        # Показване на текущ резултат и най-добър резултат
        score_display(Length_of_snake - 1, high_score)
        
        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def show_difficulty_selection():
    difficulty_selected = False

    while not difficulty_selected:
        dis.blit(background_img, (0, 0))
        message("Натиснете 1 за нормално ниво, 2 за трудно ниво", (255, 255, 255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameLoop(normal_speed)  # Започва играта с нормална скорост
                    difficulty_selected = True
                elif event.key == pygame.K_2:
                    gameLoop(hard_speed)  # Започва играта с по-висока скорост
                    difficulty_selected = True

show_difficulty_selection()
