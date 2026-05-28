from Battleship_class import *
import pygame
import datetime
import os
import sys
pygame.init()
pygame.mixer.init()
#SET UP MÀN HÌNH
os.environ['SDL_VIDEO_WINDOW_POS'] = "150,120"
CELL_SIZE=50
MARGIN=50
HEADER_Y = 100
MARGIN_BOTTOM=80
SCREEN_SIZE = MARGIN + (10 * CELL_SIZE)
WINDOW_WIDTH_PLAYING = SCREEN_SIZE * 2
WINDOW_HEIGHT_PLAYING = HEADER_Y + SCREEN_SIZE + MARGIN_BOTTOM
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE+MARGIN_BOTTOM))
pygame.display.set_caption("BATLLESHIP")
icon=pygame.image.load('image\icon.webp')
pygame.display.set_icon(icon)

# music
sound_on=True
btn_sound_menu = pygame.Rect(150, 450, 250, 40)
pygame.mixer.music.load('music\music_game.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
sound_explosion = pygame.mixer.Sound("music\shot_music.flac")
sound_explosion.set_volume(0.7)


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
Background_input=pygame.transform.scale(Background_input,(SCREEN_SIZE,SCREEN_SIZE+MARGIN_BOTTOM))
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
def draw_ocean(offset_x=0,offset_y=0):
    for y in range(10):          
        for x in range(10):      
            pixel_x =offset_x+ MARGIN + (x * CELL_SIZE)
            pixel_y =offset_y+MARGIN + (y * CELL_SIZE)
            screen.blit(water_image, (pixel_x, pixel_y))
    for x in range(10):
        text_img = font.render(columns[x], True, (255, 255, 255))
        text_x = offset_x+ MARGIN + (x * CELL_SIZE) + (CELL_SIZE // 2) - (text_img.get_width() // 2)
        text_y = offset_y+ (MARGIN // 2) - (text_img.get_height() // 2)
        screen.blit(text_img, (text_x, text_y))
    for y in range(10):
        text_img = font.render(str(y), True, (255, 255, 255))
        text_x = offset_x+(MARGIN // 2) - (text_img.get_width() // 2)
        text_y = offset_y+MARGIN + (y * CELL_SIZE) + (CELL_SIZE // 2) - (text_img.get_height() // 2)
        screen.blit(text_img, (text_x, text_y))
def Draw_player_ship(offset_x=0,offset_y=0):
    if Player1 is not None:
        for y in range (10):
            for x in range(10):
                if Player1.board.grid[y][x]==1:
                    pixel_x = offset_x+ MARGIN + (x * CELL_SIZE)
                    pixel_y = offset_y+MARGIN + (y * CELL_SIZE)
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
avatar_player=pygame.image.load('image/Player 1.png')
avatar_player = pygame.transform.scale(avatar_player, (70, 70))
avatar_ai = pygame.image.load('image\AI.jpg')
avatar_ai = pygame.transform.scale(avatar_ai, (70, 70))
def Draw_Hits_Misses(offset_x,offset_y, board):
    if board is not None:
        for y in range(10):
            for x in range(10):
                pixel_x = offset_x + MARGIN + (x * CELL_SIZE)
                pixel_y =offset_y+ MARGIN + (y * CELL_SIZE)
                if board.grid[y][x] == 2:
                    screen.blit(miss_image, (pixel_x, pixel_y))
                elif board.grid[y][x] == 3:
                    screen.blit(hit_image, (pixel_x, pixel_y))
#Victory và Game_over set up
font_title = pygame.font.SysFont("arial", 80, bold=True)
btn_play_again = pygame.Rect(WINDOW_WIDTH_PLAYING // 2 - 220, WINDOW_HEIGHT_PLAYING // 2 + 50, 200, 60)
btn_exit = pygame.Rect(WINDOW_WIDTH_PLAYING // 2 + 20, WINDOW_HEIGHT_PLAYING // 2 + 50, 200, 60)

# history set up

def save_history(player_name, ai_level, result):
    ai_name = "Hard AI" if ai_level == 2 else "Easy AI"
    time_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    record = f"[{time_str}] {player_name} vs {ai_name} - Kết quả: {result}\n"
    try:
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(record)
    except Exception as e:
        print("Lỗi lưu lịch sử:", e)
def read_history():
    try:
        if not os.path.exists("history.txt"):
            return []
        with open("history.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines[-10:]] 
    except Exception as e:
        print("Lỗi đọc lịch sử:", e)
        return []
history_data = []
btn_clear_history = pygame.Rect(150, 430, 250, 40)
btn_back = pygame.Rect(150, 480, 250, 40)

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
                    history_data = read_history()
                    game_state = "HISTORY"
                if btn_sound_menu.collidepoint(event.pos):
                    sound_on = not sound_on 
                    if sound_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
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
                        elif current_direction=='V':
                            current_direction='H'
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
                            screen = pygame.display.set_mode((WINDOW_WIDTH_PLAYING, WINDOW_HEIGHT_PLAYING))
                            game_state="PLAYING"
        # chơi
        elif game_state=="PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                grid_x = (mouse_x - MARGIN - SCREEN_SIZE) // CELL_SIZE
                grid_y = (mouse_y - MARGIN-HEADER_Y) // CELL_SIZE
                if (0 <= grid_x <= 9) and (0 <= grid_y <= 9):
                    if sound_on:
                        sound_explosion.play()
                    if Player2.board.grid[grid_y][grid_x] < 2:
                        player_shot_result = Player2.board.receive_shot(grid_x, grid_y)
                        Draw_Hits_Misses(offset_x=SCREEN_SIZE,offset_y=HEADER_Y, board=Player2.board)
                        pygame.display.update()
                        if Player2.board.check_lose():
                            pygame.time.delay(1000)
                            game_state="VICTORY"
                            save_history(user_name, level, "THẮNG")
                            continue
                        ai_shot=Player2.takeShot()
                        if sound_on:
                            sound_explosion.play()
                        if ai_shot is not None:
                            ax, ay = ai_shot
                            ai_shot_result = Player1.board.receive_shot(ax, ay)
                            Draw_Hits_Misses(offset_x=0,offset_y=HEADER_Y, board=Player1.board)
                            pygame.display.update()
                            if level == 2:
                                Player2.afterShot(ai_shot_result)
                                while len(Player2.targets) >0:
                                    ax, ay=Player2.takeShot()
                                    if sound_on:
                                        sound_explosion.play()
                                    ai_shot_result=Player1.board.receive_shot(ax,ay)
                                    Player2.afterShot(ai_shot_result)
                                    Draw_Hits_Misses(offset_x=0,offset_y=HEADER_Y, board=Player1.board)
                                    player_hits = np.sum(Player2.board.grid == 3)
                                    score_p = font_texts.render(f"Phát bắn trúng: {player_hits}/18", True, (0, 255, 0))
                                    screen.blit(score_p, (MARGIN + 85, 55))
                                    ai_hits = np.sum(Player1.board.grid == 3)
                                    score_ai = font_texts.render(f"Phát bắn trúng: {ai_hits}/18", True, (255, 50, 50))
                                    screen.blit(score_ai, (ai_x_pos + 85, 55))
                                    pygame.display.update()
                                    pygame.time.delay(300)
                                    if Player1.board.check_lose():
                                        game_state="GAME_OVER"
                                        save_history(user_name, level, "THUA")
                                        break
                            if Player1.board.check_lose() and game_state != "GAME_OVER":
                                pygame.time.delay(1000)
                                game_state = "GAME_OVER"
                                save_history(user_name, level, "THUA")
        elif game_state in ["VICTORY", "GAME_OVER"]:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play_again.collidepoint(event.pos):
                    Player1 = None
                    Player2 = None
                    current_ship_idx = 0
                    current_direction = 'H'
                    user_name = ""
                    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
                    game_state="INPUT_NAME"
                elif btn_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    # lịch sử
        elif game_state == "HISTORY":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.collidepoint(event.pos):
                    game_state = "INPUT_NAME"
                elif btn_clear_history.collidepoint(event.pos):
                    open("history.txt", "w", encoding="utf-8").close()
                    history_data = []
# VẼ NÊN MÀN HÌNH GAME

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
        color_sound = (50, 150, 50) if sound_on else (150, 50, 50)
        text_sound_str = "ÂM THANH: BẬT" if sound_on else "ÂM THANH: TẮT"
        pygame.draw.rect(screen, color_sound, btn_sound_menu, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), btn_sound_menu, width=2, border_radius=10)
        txt_sound = font_lable.render(text_sound_str, True, (0, 0, 0))
        screen.blit(txt_sound, (btn_sound_menu.x + 20, btn_sound_menu.y + 7))

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
        screen.fill((15, 25, 35))
        
        # 1. Vẽ bàn cờ CỦA MÌNH (Bên trái) - Bị đẩy xuống HEADER_Y
        draw_ocean(offset_x=0, offset_y=HEADER_Y) 
        Draw_player_ship(offset_x=0, offset_y=HEADER_Y)
        Draw_Hits_Misses(offset_x=0, offset_y=HEADER_Y, board=Player1.board)
        
        # 2. Vẽ bàn cờ RADAR AI (Bên phải) - Bị đẩy xuống HEADER_Y
        draw_ocean(offset_x=SCREEN_SIZE, offset_y=HEADER_Y)
        Draw_Hits_Misses(offset_x=SCREEN_SIZE, offset_y=HEADER_Y, board=Player2.board)
        # =================================================================
        # VẼ HEADER (MARGIN TOP)
        # =================================================================
        pygame.draw.rect(screen, (30, 45, 60), (0, 0, WINDOW_WIDTH_PLAYING, HEADER_Y))
        pygame.draw.line(screen, (100, 100, 100), (0, HEADER_Y), (WINDOW_WIDTH_PLAYING, HEADER_Y), 2)
        
        # Thông tin Người chơi
        screen.blit(avatar_player, (MARGIN, 15))
        name_text = font_lable.render(f"PLAYER: {user_name.upper()}", True, (255, 255, 255))
        screen.blit(name_text, (MARGIN + 85, 25))
        player_hits = np.sum(Player2.board.grid == 3)
        score_p = font_texts.render(f"Phát bắn trúng: {player_hits}/18", True, (0, 255, 0))
        screen.blit(score_p, (MARGIN + 85, 55))
        
        # Thông tin AI
        ai_x_pos = SCREEN_SIZE + MARGIN
        screen.blit(avatar_ai, (ai_x_pos, 15))
        ai_name = "HARD AI" if level == 2 else "EASY AI"
        ai_text = font_lable.render(f"ENEMY: {ai_name}", True, (255, 100, 100))
        screen.blit(ai_text, (ai_x_pos + 85, 25))
        ai_hits = np.sum(Player1.board.grid == 3)
        score_ai = font_texts.render(f"Phát bắn trúng: {ai_hits}/18", True, (255, 50, 50))
        screen.blit(score_ai, (ai_x_pos + 85, 55))
        
        pygame.draw.line(screen, (80, 80, 80), (SCREEN_SIZE, 0), (SCREEN_SIZE, HEADER_Y), 2)

        # =================================================================
        # VẼ THỐNG KÊ (MARGIN BOTTOM)
        # =================================================================
        y_bottom_start = HEADER_Y + SCREEN_SIZE + 15
        pygame.draw.line(screen, (100, 100, 100), (0, HEADER_Y + SCREEN_SIZE), (WINDOW_WIDTH_PLAYING, HEADER_Y + SCREEN_SIZE), 2)
        
        # Thống kê tổng quan
        status_player_msg = f"Tàu mình bị trúng: {ai_hits} ô"
        status_enemy_msg = f"Tàu địch bị trúng: {player_hits} ô"
        txt_p_status = font_lable.render(status_player_msg, True, (255, 255, 100) if ai_hits > 0 else (255, 255, 255))
        txt_e_status = font_lable.render(status_enemy_msg, True, (255, 100, 100) if player_hits > 0 else (255, 255, 255))
        screen.blit(txt_p_status, (MARGIN, y_bottom_start + 10))
        screen.blit(txt_e_status, (SCREEN_SIZE + MARGIN, y_bottom_start + 10))
    #vẽ victory và game over
    elif game_state in ["VICTORY", "GAME_OVER"]:
        overlay = pygame.Surface((WINDOW_WIDTH_PLAYING, WINDOW_HEIGHT_PLAYING), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0, 0))
        if game_state == "VICTORY":
            title_text = font_title.render("VICTORY!", True, (0, 255, 0)) 
            msg_text = font_texts.render("Chúc mừng! Bạn đã tiêu diệt toàn bộ hạm đội địch.", True, (255, 255, 255))
        else:
            title_text = font_title.render("GAME OVER", True, (255, 50, 50))
            msg_text = font_texts.render("Hạm đội của bạn đã bị tiêu diệt. Hãy thử lại!", True, (255, 255, 255))
        screen.blit(title_text, (WINDOW_WIDTH_PLAYING // 2 - title_text.get_width() // 2, WINDOW_HEIGHT_PLAYING // 2 - 120))
        screen.blit(msg_text, (WINDOW_WIDTH_PLAYING // 2 - msg_text.get_width() // 2, WINDOW_HEIGHT_PLAYING // 2 - 30))
        pygame.draw.rect(screen, (0, 150, 255), btn_play_again, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_play_again, width=2, border_radius=10)
        txt_play = font_lable.render("PLAY AGAIN", True, (255, 255, 255))
        screen.blit(txt_play, (btn_play_again.x + 25, btn_play_again.y + 15))
        pygame.draw.rect(screen, (200, 50, 50), btn_exit, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_exit, width=2, border_radius=10)
        txt_exit = font_lable.render("EXIT", True, (255, 255, 255))
        screen.blit(txt_exit, (btn_exit.x + 70, btn_exit.y + 15))
    # VẼ MÀN HÌNH LỊCH SỬ
    elif game_state == "HISTORY":
        screen.fill((20, 30, 40))
        title_surf = font_lable.render("LỊCH SỬ TRẬN ĐẤU", True, (255, 215, 0))
        screen.blit(title_surf, (SCREEN_SIZE // 2 - title_surf.get_width() // 2, 40))
        
        # Danh sách lịch sử
        y_pos = 120
        if len(history_data) == 0:
            no_data_surf = font_texts.render("Chưa có trận đấu nào được lưu.", True, (150, 150, 150))
            screen.blit(no_data_surf, (SCREEN_SIZE // 2 - no_data_surf.get_width() // 2, y_pos))
        else:
            # Đảo ngược danh sách để hiện trận mới nhất lên trên
            for record in reversed(history_data):
                color = (100, 255, 100) if "THẮNG" in record else (255, 100, 100)
                record_surf = font_texts.render(record, True, color)
                screen.blit(record_surf, (SCREEN_SIZE // 2 - record_surf.get_width() // 2, y_pos))
                y_pos+=35
        pygame.draw.rect(screen, (200, 100, 50), btn_clear_history, border_radius=10) # Màu cam gạch
        pygame.draw.rect(screen, (255, 255, 255), btn_clear_history, width=2, border_radius=10)
        txt_clear = font_lable.render("XÓA LỊCH SỬ", True, (255, 255, 255))
        screen.blit(txt_clear, (btn_clear_history.x + 40, btn_clear_history.y + 5))
        pygame.draw.rect(screen, (200, 50, 50), btn_back, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_back, width=2, border_radius=10)
        txt_back = font_lable.render("QUAY LẠI", True, (255, 255, 255))
        screen.blit(txt_back, (btn_back.x + 65, btn_back.y + 5))
    pygame.display.update()
