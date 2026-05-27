from Battleship_class import *
import pygame
import os
import sys
pygame.init()
#SET UP MÀN HÌNH
os.environ['SDL_VIDEO_WINDOW_POS'] = "150,150"
CELL_SIZE=50
MARGIN=50
MARGIN_BOTTOM=40
SCREEN_SIZE = MARGIN + (10 * CELL_SIZE)
WINDOW_WIDTH_PLAYING = SCREEN_SIZE * 2
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE+MARGIN_BOTTOM))
pygame.display.set_caption("BATLLESHIP")
icon=pygame.image.load('image\icon.webp')
pygame.display.set_icon(icon)

# set up place ship
Player1=None
Player2=None
ship_sizes = [2, 3, 4, 5, 4]
current_ship_idx = 0       
current_direction = 'H'


# Set up màn hình input

game_state = "INPUT_NAME"
user_name = ""
active = False
Background_input=pygame.image.load('image\Background.PNG')
Background_input=pygame.transform.scale(Background_input,(SCREEN_SIZE,SCREEN_SIZE))
input_rect = pygame.Rect(150, 180, 250, 30)
btn_easyAI=pygame.Rect(150,250,250,30)
btn_hardAI=pygame.Rect(150,320,250,30)
btn_history=pygame.Rect(150,390,250,30)
# màu ô input
COLOR_ACTIVE = (255, 255, 255)
COLOR_PASSIVE = (0, 0, 0)
current_color = COLOR_PASSIVE
# màu btn
COLOR_EASY = (46, 204, 113)    
COLOR_HARD = (231, 76, 60)     
COLOR_HISTORY = (52, 152, 219)
font_text=pygame.font.SysFont('Arial',15,bold=True)
font_lable=pygame.font.SysFont('Arial',26,bold=True)
font_texts=pygame.font.SysFont('Arial',12,bold=True)

# Set up Place ship
water_image = pygame.image.load('image\Water.png')
water_image = pygame.transform.scale(water_image, (CELL_SIZE, CELL_SIZE))
font = pygame.font.SysFont('Arial', 24, bold=True)
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
def draw_ocean(offset_x=0):
    for y in range(10):          
        for x in range(10):      
            pixel_x =offset_x+ MARGIN + (x * CELL_SIZE)
            pixel_y = MARGIN + (y * CELL_SIZE)
            screen.blit(water_image, (pixel_x, pixel_y))
    for x in range(10):
        text_img = font.render(columns[x], True, (255, 255, 255))
        text_x = offset_x+ MARGIN + (x * CELL_SIZE) + (CELL_SIZE // 2) - (text_img.get_width() // 2)
        text_y = (MARGIN // 2) - (text_img.get_height() // 2)
        screen.blit(text_img, (text_x, text_y))
    for y in range(10):
        text_img = font.render(str(y), True, (255, 255, 255))
        text_x = offset_x+(MARGIN // 2) - (text_img.get_width() // 2)
        text_y = MARGIN + (y * CELL_SIZE) + (CELL_SIZE // 2) - (text_img.get_height() // 2)
        screen.blit(text_img, (text_x, text_y))
def Draw_player_ship(offset_x=0):
    if Player1 is not None:
        for y in range (10):
            for x in range(10):
                if Player1.board.grid[y][x]==1:
                    pixel_x = offset_x+ MARGIN + (x * CELL_SIZE)
                    pixel_y = MARGIN + (y * CELL_SIZE)
                    pygame.draw.rect(screen, (140, 140, 140), (pixel_x + 4, pixel_y + 4, CELL_SIZE - 8, CELL_SIZE - 8), border_radius=4)
                    pygame.draw.rect(screen, (255, 255, 255), (pixel_x + 4, pixel_y + 4, CELL_SIZE - 8, CELL_SIZE - 8), width=1, border_radius=4)
# playing set up

def Draw_AI_ship():
    ai_sizes = [2, 3, 4, 5, 4]
    ai_directions = ['H', 'V', 'S']
    for idx, size in enumerate(ai_sizes):
        placed = False
        ship = Ship(size)
        while not placed:
            rx = random.randint(0, 9)
            ry = random.randint(0, 9)
            rd = 'S' if idx == 4 else random.choice(['H', 'V']) 
            if Player2.board.place_ship(ship, rx, ry, rd):
                placed = True
hit_image=pygame.image.load('image\Fire.png')
hit_image=pygame.transform.scale(hit_image,(CELL_SIZE,CELL_SIZE))
miss_image=pygame.image.load('image\miss.png')
miss_image=pygame.transform.scale(miss_image,(CELL_SIZE,CELL_SIZE))
def Draw_Hits_Misses(offset_x, board):
    if board is not None:
        for y in range(10):
            for x in range(10):
                pixel_x = offset_x + MARGIN + (x * CELL_SIZE)
                pixel_y = MARGIN + (y * CELL_SIZE)
                if board.grid[y][x] == 2:
                    screen.blit(miss_image, (pixel_x, pixel_y))
                elif board.grid[y][x] == 3:
                    screen.blit(hit_image, (pixel_x, pixel_y))
# Vòng lặp game

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Màn Hình Home
        if game_state=="INPUT_NAME":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                    current_color = COLOR_ACTIVE
                else:
                    active = False
                    current_color = COLOR_PASSIVE
                if btn_easyAI.collidepoint(event.pos):
                    game_state="PLACE_SHIPS"
                    level=1
                    Player1=Human(user_name)
                    Player2=EasyAI("Máy")
                if btn_hardAI.collidepoint(event.pos):
                    game_state="PLACE_SHIPS"
                    level=2
                    Player1=Human(user_name)
                    Player2=HardAI("Máy")
                if btn_history.collidepoint(event.pos):
                    pass
            if event.type==pygame.KEYDOWN:
                if active:
                    if event.key==pygame.K_BACKSPACE:
                        user_name = user_name[:-1]
                    else:
                        if (len(user_name))<20:
                            user_name += event.unicode

    # Đặt tàu
        elif game_state == "PLACE_SHIPS":
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_r:
                        if current_direction=='H':
                            current_direction='V'
                            print(current_direction)
                        elif current_direction=='V':
                            current_direction='H'
                            print(current_direction)
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        mouse_x=event.pos[0]
                        mouse_y=event.pos[1]
                        grid_x=(mouse_x-MARGIN)//CELL_SIZE
                        grid_y=(mouse_y-MARGIN)//CELL_SIZE
                        if (0<=grid_x<=9) and (0<=grid_y<=9) and (current_ship_idx<=3):
                            size=ship_sizes[current_ship_idx]
                            new_ship=Ship(size)
                            if Player1.board.place_ship(new_ship,grid_x,grid_y,current_direction):
                                current_ship_idx+=1       
                        elif (0<=grid_x<=9) and (0<=grid_y<=9) and (current_ship_idx==4):
                            size=ship_sizes[current_ship_idx]
                            new_ship=Ship(size)
                            if Player1.board.place_ship(new_ship,grid_x,grid_y,'S'):
                                current_ship_idx+=1
                        if current_ship_idx==5:
                            Draw_AI_ship()
                            screen = pygame.display.set_mode((WINDOW_WIDTH_PLAYING, SCREEN_SIZE + MARGIN_BOTTOM))
                            game_state="PLAYING"
        # chơi
        elif game_state=="PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                grid_x = (mouse_x - MARGIN - SCREEN_SIZE) // CELL_SIZE
                grid_y = (mouse_y - MARGIN) // CELL_SIZE
                if (0 <= grid_x <= 9) and (0 <= grid_y <= 9):
                    if Player2.board.grid[grid_y][grid_x] < 2:
                        player_shot_result = Player2.board.receive_shot(grid_x, grid_y)
                        Draw_Hits_Misses(offset_x=SCREEN_SIZE, board=Player2.board)
                        pygame.display.update()
                        if Player2.board.check_lose():
                            pygame.time.delay(1000)
                            game_state="VICTORY"
                            continue
                        ai_shot=Player2.takeShot()
                        if ai_shot is not None:
                            ax, ay = ai_shot
                            ai_shot_result = Player1.board.receive_shot(ax, ay)
                            Draw_Hits_Misses(offset_x=0, board=Player1.board)
                            pygame.display.update()
                            if level == 2:
                                Player2.afterShot(ai_shot_result)
                                while len(Player2.targets) >0:
                                    ax, ay=Player2.takeShot()
                                    ai_shot_result=Player1.board.receive_shot(ax,ay)
                                    Player2.afterShot(ai_shot_result)
                                    Draw_Hits_Misses(offset_x=0, board=Player1.board)
                                    pygame.display.update()
                                    pygame.time.delay(300)
                                    if Player1.board.check_lose():
                                        game_state="GAME_OVER"
                                        break
                            if Player1.board.check_lose() and game_state != "GAME_OVER":
                                pygame.time.delay(1000)
                                game_state = "GAME_OVER"
    # vẽ home
    if game_state =="INPUT_NAME":
        screen.blit(Background_input,(0,0))
        pygame.draw.rect(screen, current_color, input_rect)
        text_surface = font_text.render("Tên: " + user_name, True, (231, 84, 128))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 7))
        pygame.draw.rect(screen,COLOR_EASY,btn_easyAI,border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_easyAI, width=2, border_radius=10)
        text_ezAI=font_lable.render("EASY AI",True,(0,0,0))
        screen.blit(text_ezAI,(215,250))
        pygame.draw.rect(screen,COLOR_HARD,btn_hardAI,border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_hardAI, width=2, border_radius=10)
        text_hardAI=font_lable.render("HARD AI",True,(0,0,0))
        screen.blit(text_hardAI,(215,320))
        pygame.draw.rect(screen,COLOR_HISTORY,btn_history,border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_history, width=2, border_radius=10)
        text_history=font_lable.render("HISTORY",True,(0,0,0))
        screen.blit(text_history,(215,390))

    #vẽ màn hình đặt tàu

    elif game_state == "PLACE_SHIPS":
            screen.fill((20, 30, 40))
            if current_ship_idx==4:
                text_hdsd = f"Đang đặt tàu cỡ: {ship_sizes[current_ship_idx]} ô | Hướng ( H:Ngang/V:dọc/S:4 ô xung quoanh ): S"
                instruct_place_ship = font_texts.render(text_hdsd, True, (0, 255, 0))
                screen.blit(instruct_place_ship, (MARGIN, SCREEN_SIZE + 10))
            if current_ship_idx<4:
                text_hdsd = f"Đang đặt tàu cỡ: {ship_sizes[current_ship_idx]} ô | Hướng (H:Ngang/V:dọc/S:4 ô xung quoanh) : {current_direction} | Nhấn 'R' để xoay"
                instruct_place_ship = font_texts.render(text_hdsd, True, (0, 255, 0))
                screen.blit(instruct_place_ship, (MARGIN, SCREEN_SIZE + 10))
            draw_ocean()
            Draw_player_ship()

    #vẽ màn hình chơi 

    elif game_state == "PLAYING":
        screen.fill((20, 30, 40))
        draw_ocean(offset_x=0) 
        Draw_player_ship(offset_x=0)
        Draw_Hits_Misses(offset_x=0, board=Player1.board)
        draw_ocean(offset_x=SCREEN_SIZE)
        Draw_Hits_Misses(offset_x=SCREEN_SIZE, board=Player2.board)
    pygame.display.update()