import pygame
import os
import math
from button import Button
import csv


pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HIGHT = int(SCREEN_WIDTH * 0.8)
RIGHT_MARGIN = 300
BOTTOM_MARGIN = 100
BG_COLOR = (9, 18, 56)
FPS = 60
GRID_ROWS = 16
GRID_COLUMS = 150
GRID_COLOR = (255, 255, 255)
TILE_SIZE = SCREEN_HIGHT // GRID_ROWS
ACTIVE_TILE_COLOR = (163, 2, 2)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH + RIGHT_MARGIN, SCREEN_HIGHT + BOTTOM_MARGIN))
pygame.display.set_caption('level Editor')
clock = pygame.time.Clock()

background_layers = []
for filename in sorted(os.listdir('images/background'), reverse=True):
    image = pygame.image.load(f'images/background/{filename}').convert_alpha()
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HIGHT))
    background_layers.append(image)


is_scrolling_left = False
is_scroling_right = False
scroll = 0
scroll_speed = 5
background_width =background_layers[0].get_width()
current_tile = 0
tile_images = []
buttons = []
side_panel_height = SCREEN_HIGHT +1
side_panel_csroll = 0
world_data = []
level = 0
main_font = pygame.font.SysFont('Futura', 30)
is_empty_level = True

save_image = pygame.image.load('images/buttons/save.png').convert_alpha()
save_button = Button(save_image)

for row in range(GRID_ROWS):
    world_data.append([-1] * GRID_COLUMS)

for filename in sorted(os.listdir('images/tiles')):
    image = pygame.image.load(f'images/tiles/{filename}').convert_alpha()
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    tile_images.append(image)
    button = Button(image)
    buttons.append(button)

if len (buttons) > 36:
    side_panel_height = 75 * math.ceil(len(buttons) / 3) + 75

def draw_dackground():
    bg_layer_counter = len(background_layers)
    for x in range(4):
        for i, background_image in enumerate(background_layers):
            layer_scroll_speed = (x * background_width) - (scroll * ((i + 1) / bg_layer_counter))
            screen.blit(background_image, (layer_scroll_speed, 0))

def draw_grid():
    for column in range(GRID_COLUMS + 1):
        pygame.draw.line(screen, GRID_COLOR, (column * TILE_SIZE - scroll, 0), (column * TILE_SIZE - scroll, SCREEN_HIGHT))
    for row in range (GRID_ROWS + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, TILE_SIZE * row), (SCREEN_WIDTH, TILE_SIZE * row))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile > -1:
                screen.blit(tile_images[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

def draw_text(text, xy, font = None, color = TEXT_COLOR):
    if font == None:
        font = main_font

    image = font.render(text, True, color)
    screen.blit(image, xy)


def save_world():
    if os.path.exists('levels') == False:
        os.mkdir('levels')

    if is_empty_level == False:
        with open(f'levels/level_{level}.csv', 'w', newline ='') as file_content:
            writer = csv.writer(file_content, delimiter=',')
            for row in world_data:
                writer.writerow(row)

def load_world():
    global is_empty_level, scroll

    scroll = 0

    if os.path.exists(f'levels/level_{level}.csv'):
        is_empty_level = False
        with open(f'levels/level_{level}.csv', newline='') as file_content:
            reader = csv.reader(file_content, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    else:
        is_empty_level = True
        for x, row in enumerate(world_data):
            for y, tile in enumerate(row):
                world_data[x][y] = -1
        for cell_index in range(0, GRID_COLUMS):
            world_data[GRID_ROWS - 1][cell_index] = 0

load_world()

run = True
while run:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    draw_dackground()
    draw_grid()
    draw_world()

    save_button.draw(screen, (SCREEN_WIDTH // 2, SCREEN_HIGHT + BOTTOM_MARGIN - 70))
    if save_button.clicked():
        save_world()

    draw_text(f'Level: {level}', (10, SCREEN_HIGHT + BOTTOM_MARGIN - 90))
    draw_text('Press UP or Down to change level', (10, SCREEN_HIGHT + BOTTOM_MARGIN - 60))


    pygame.draw.rect(screen, BG_COLOR, (SCREEN_WIDTH, 0 + side_panel_csroll, RIGHT_MARGIN, side_panel_height))

    button_column = 0
    button_row = 0
    for tile_button_index, tile_button in enumerate(buttons):
        xy = (SCREEN_WIDTH + (75 * button_column) + 50, 75 * button_row + 50 + side_panel_csroll)
        tile_button.draw(screen, xy)

        button_column += 1
        if button_column == 3:
            button_row += 1
            button_column = 0

        if tile_button.clicked():
            current_tile = tile_button_index

    # print(current_tile)
    pygame.draw.rect(screen, ACTIVE_TILE_COLOR, buttons[current_tile].rectangle, 5)

    cursor_position = pygame.mouse.get_pos()
    x = (cursor_position[0] + scroll) // TILE_SIZE
    y = cursor_position[1] // TILE_SIZE

    if cursor_position[0] < SCREEN_WIDTH and cursor_position[1] < SCREEN_HIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                is_empty_level = False
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            if world_data[y][x] != -1:
                is_empty_level = False
                world_data[y][x] = -1



    if is_scrolling_left and scroll > 0:
            scroll -= scroll_speed
    if is_scroling_right and scroll < (background_width * 3):
            scroll += scroll_speed



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                save_world()
                level += 1
                load_world()

            if event.key == pygame.K_DOWN and level > 0:
                save_world()
                level -= 1
                load_world()

            if event.key == pygame.K_LEFT:
                is_scrolling_left = True

            if event.key == pygame.K_RIGHT:
                is_scroling_right = True

            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                scroll_speed = 20

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                is_scrolling_left = False

            if event.key == pygame.K_RIGHT:
                is_scroling_right = False

            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                scroll_speed = 5

        if event.type == pygame.MOUSEWHEEL:
            side_panel_csroll += event.y * 40
            if side_panel_csroll >= 0:
                side_panel_csroll = 0
            elif abs(side_panel_csroll) >= (side_panel_height - SCREEN_HIGHT):
                side_panel_csroll = -abs(side_panel_height - SCREEN_HIGHT) + 1



        
    pygame.display.update()



pygame.quit()