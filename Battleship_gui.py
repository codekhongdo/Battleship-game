from Battleship_class import *
import pygame
import sys
pygame.init()
#SET UP MÀN HÌNH
CELL_SIZE=50
MARGIN=50
SCREEN_SIZE = MARGIN + (10 * CELL_SIZE)
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("BATLLESHIP")
icon=pygame.image.load('image\icon.webp')
pygame.display.set_icon(icon)

# Set up màn hình input

game_state = "INPUT_NAME"
user_name = ""
active = False
Background_input=pygame.image.load('image\Background.PNG')
Background_input=pygame.transform.scale(Background_input,(SCREEN_SIZE,SCREEN_SIZE))
input_rect = pygame.Rect(150, 180, 250, 30)
COLOR_ACTIVE = (255, 255, 255)
COLOR_PASSIVE = (0, 0, 0)
current_color = COLOR_PASSIVE
# Set up Ocean

water_image = pygame.image.load('image\Water.png')
water_image = pygame.transform.scale(water_image, (CELL_SIZE, CELL_SIZE))
font = pygame.font.SysFont('Arial', 24, bold=True)
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
def draw_ocean():
    for y in range(10):          
        for x in range(10):      
            pixel_x = MARGIN + (x * CELL_SIZE)
            pixel_y = MARGIN + (y * CELL_SIZE)
            screen.blit(water_image, (pixel_x, pixel_y))
    for x in range(10):
        text_img = font.render(columns[x], True, (255, 255, 255))
        text_x = MARGIN + (x * CELL_SIZE) + (CELL_SIZE // 2) - (text_img.get_width() // 2)
        text_y = (MARGIN // 2) - (text_img.get_height() // 2)
        screen.blit(text_img, (text_x, text_y))
    for y in range(10):
        text_img = font.render(str(y), True, (255, 255, 255))
        text_x = (MARGIN // 2) - (text_img.get_width() // 2)
        text_y = MARGIN + (y * CELL_SIZE) + (CELL_SIZE // 2) - (text_img.get_height() // 2)
        screen.blit(text_img, (text_x, text_y))

# Vòng lặp game

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == "INPUT_NAME":
            screen.blit(Background_input,(0,0))
            pygame.draw.rect(screen, current_color, input_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                    current_color = COLOR_ACTIVE
                else:
                    active = False
                    current_color = COLOR_PASSIVE
        elif game_state == "PLACE_SHIPS":
             screen.fill((20, 30, 40))
             draw_ocean()
    pygame.display.update()