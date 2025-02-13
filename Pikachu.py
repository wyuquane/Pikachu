# INSTRUCTION: Just need to change this path and can run game
PATH = r'C:\Users\HOANG\Desktop\upload code\Pikachu-Classic'

import pygame, sys, json, random, copy, time, collections, os
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 1000
WINDOWHEIGHT = 570
BOXSIZE = 55
BOARDWIDTH = 4
BOARDHEIGHT = 4
NUMSAMEHEROES = 4
NUMHEROES_ONBOARD = (BOARDHEIGHT - 2) * (BOARDWIDTH - 2) // NUMSAMEHEROES
TIMEBAR_LENGTH = 300
TIMEBAR_WIDTH = 30
LEVELMAX = 5
LIVES = 10
GAMETIME = 240
GETHINTTIME = 1

XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

# set up the colors
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BOLDGREEN = (0, 175, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = NAVYBLUE
HIGHLIGHTCOLOR = BLUE
BORDERCOLOR = RED

# TIMEBAR setup
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, YMARGIN // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN

# Make a dict to store scaled images
LISTHEROES = os.listdir(PATH + '/hero_icon')
NUMHEROES = len(LISTHEROES)
HEROES_DICT = {}

for i in range(len(LISTHEROES)):
    HEROES_DICT[i + 1] = pygame.transform.scale(pygame.image.load('hero_icon/' + LISTHEROES[i]), (BOXSIZE, BOXSIZE))

# Load pictures
aegis = pygame.image.load('aegis_2.jpg')
aegis = pygame.transform.scale(aegis, (45, 45))

# Load background
startBG = pygame.image.load('dota_background/nen_game_start.jpg')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))

listBG = [pygame.image.load('dota_background/{}.jpg'.format(i)) for i in range(15)]
for i in range(len(listBG)):
    listBG[i] = pygame.transform.scale(listBG[i], (WINDOWWIDTH, WINDOWHEIGHT))

# Load sound and music
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('beep4.ogg')
getPointSound = pygame.mixer.Sound('beep1.ogg')
startScreenSound = pygame.mixer.Sound('warriors-of-the-night-assemble.wav')
listMusicBG = ['musicBG1.mp3', 'musicBG2.mp3', 'musicBG3.mp3', 'musicBG4.mp3', 'musicBG5.mp3']

# Load sound effects
LIST_SOUNDEFFECT = os.listdir(PATH + '/sound_effect')

for i in range(len(LIST_SOUNDEFFECT)):
    LIST_SOUNDEFFECT[i] = pygame.mixer.Sound('sound_effect/' + LIST_SOUNDEFFECT[i])


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    while True:
        random.shuffle(listBG)
        random.shuffle(listMusicBG)
        LEVEL = 1
        showStartScreen()

def showStartScreen():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    startScreenSound.play()
    while True:
        DISPLAYSURF.blit(startBG, (0, 0))

        login_surf = BASICFONT.render('LOGIN', True, WHITE, BLACK)
        login_rect = login_surf.get_rect()
        login_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 4)

        register_surf = BASICFONT.render('REGISTER', True, WHITE, BLACK)
        register_rect = register_surf.get_rect()
        register_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)

        leaderboard_surf = BASICFONT.render('LEADERBOARD', True, WHITE, BLACK)
        leaderboard_rect = leaderboard_surf.get_rect()
        leaderboard_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT * 3 // 4)

        DISPLAYSURF.blit(login_surf, login_rect)
        DISPLAYSURF.blit(register_surf, register_rect)
        DISPLAYSURF.blit(leaderboard_surf, leaderboard_rect)

        pygame.draw.rect(DISPLAYSURF, WHITE, login_rect, 4)
        pygame.draw.rect(DISPLAYSURF, WHITE, register_rect, 4)
        pygame.draw.rect(DISPLAYSURF, WHITE, leaderboard_rect, 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if login_rect.collidepoint((mousex, mousey)):
                    pygame.quit()
                    login()
                    return
                elif register_rect.collidepoint((mousex, mousey)):
                    pygame.quit()
                    register()
                    return
                elif leaderboard_rect.collidepoint((mousex, mousey)):
                    pygame.quit()
                    leaderboard()
                    return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def register(screen_width=800, screen_height=600):
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Register")
    font = pygame.font.SysFont(None, 48)

    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    username = ""
    password = ""
    confirm_password = ""
    message = ""

    input_active_username = False
    input_active_password = False
    input_active_confirm_password = False

    input_box_username = pygame.Rect(screen_width // 3, screen_height // 4, 300, 50)
    input_box_password = pygame.Rect(screen_width // 3, screen_height // 3, 300, 50)
    input_box_confirm_password = pygame.Rect(screen_width // 3, screen_height * 5 // 12, 300, 50)
    button_rect = pygame.Rect(screen_width // 2.5, screen_height // 1.7, 200, 50)  # Định nghĩa khung nút Đăng ký

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    color_confirm_password = color_inactive

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_username.collidepoint(event.pos):
                    input_active_username = not input_active_username
                else:
                    input_active_username = False

                if input_box_password.collidepoint(event.pos):
                    input_active_password = not input_active_password
                else:
                    input_active_password = False

                if input_box_confirm_password.collidepoint(event.pos):
                    input_active_confirm_password = not input_active_confirm_password
                else:
                    input_active_confirm_password = False

                if button_rect.collidepoint(event.pos):
                    if username in user_data:
                        message = 'username have already exist'
                    elif password != confirm_password:  # Xác nhận mật khẩu khớp
                        message = 'password do not match'
                    else:
                        user_data[username] = {'password': password,
                                               'level': None,
                                               'time': None,
                                               'board': None}
                        database = open('user_data.json', 'w')
                        json.dump(user_data, database, indent=4)
                        database.close()
                        message = 'register successfully, login to start'
                        pygame.quit()
                        main()

                color_username = color_active if input_active_username else color_inactive
                color_password = color_active if input_active_password else color_inactive
                color_confirm_password = color_active if input_active_confirm_password else color_inactive

            if event.type == pygame.KEYDOWN:
                if input_active_username:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                if input_active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

                if input_active_confirm_password:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password = confirm_password[:-1]
                    else:
                        confirm_password += event.unicode

        screen.fill((30, 30, 30))
        txt_surface_username = font.render("Username: " + username, True, color_username)
        txt_surface_password = font.render("Password: " + '*' * len(password), True, color_password)
        txt_surface_confirm_password = font.render("Confirm: " + '*' * len(confirm_password), True,
                                                   color_confirm_password)
        txt_surface_message = font.render(message, True, pygame.Color('red')) # hiển thị thông báo
        txt_surface_button = font.render("Sign Up", True, (255, 255, 255))

        width_username = max(300, txt_surface_username.get_width() + 10)
        width_password = max(300, txt_surface_password.get_width() + 10)
        width_confirm_password = max(300, txt_surface_confirm_password.get_width() + 10)
        input_box_username.w = width_username
        input_box_password.w = width_password
        input_box_confirm_password.w = width_confirm_password

        screen.blit(txt_surface_username, (input_box_username.x + 5, input_box_username.y + 5))
        screen.blit(txt_surface_password, (input_box_password.x + 5, input_box_password.y + 5))
        screen.blit(txt_surface_confirm_password, (input_box_confirm_password.x + 5, input_box_confirm_password.y + 5))
        screen.blit(txt_surface_message, (screen_width // 3, screen_height * 3 // 4))  # vị trí thông báo

        pygame.draw.rect(screen, color_username, input_box_username, 2)
        pygame.draw.rect(screen, color_password, input_box_password, 2)
        pygame.draw.rect(screen, color_confirm_password, input_box_confirm_password, 2)

        pygame.draw.rect(screen, (0, 128, 0), button_rect)  # Vẽ khung nút Đăng ký
        screen.blit(txt_surface_button, (button_rect.x + 35, button_rect.y + 10))  # Hiển thị chữ "Sign Up" trên nút

        pygame.display.flip()

    pygame.quit()

def login(screen_width=800, screen_height=600):
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Login")
    font = pygame.font.SysFont(None, 48)

    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    username = ""
    password = ""
    message = ""

    input_active_username = False
    input_active_password = False

    input_box_username = pygame.Rect(screen_width // 3, screen_height // 4, 300, 50)
    input_box_password = pygame.Rect(screen_width // 3, screen_height // 3, 300, 50)
    button_rect = pygame.Rect(screen_width // 2.5, screen_height // 1.7, 200, 50)  # Định nghĩa khung nút Đăng ký

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_username.collidepoint(event.pos):
                    input_active_username = not input_active_username
                else:
                    input_active_username = False

                if input_box_password.collidepoint(event.pos):
                    input_active_password = not input_active_password
                else:
                    input_active_password = False


                if button_rect.collidepoint(event.pos):
                    if username not in user_data or user_data[username]['password'] != password:
                        message = 'username or password is incorrect'
                    else:
                        level = user_data[username]['level']
                        time_left = user_data[username]['time']
                        board = user_data[username]['board']
                        pygame.quit()

                        if level is None:
                            global BOARDHEIGHT, BOARDWIDTH, NUMHEROES_ONBOARD, XMARGIN, YMARGIN
                            BOARDHEIGHT, BOARDWIDTH = menu_setting()
                            BOARDHEIGHT += 2
                            BOARDWIDTH += 2
                            NUMHEROES_ONBOARD = (BOARDHEIGHT - 2) * (BOARDWIDTH - 2) // NUMSAMEHEROES
                            XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
                            YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

                        runGame(username,level, time_left, board)


                color_username = color_active if input_active_username else color_inactive
                color_password = color_active if input_active_password else color_inactive

            if event.type == pygame.KEYDOWN:
                if input_active_username:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                if input_active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        screen.fill((30, 30, 30))
        txt_surface_username = font.render("Username: " + username, True, color_username)
        txt_surface_password = font.render("Password: " + '*' * len(password), True, color_password)

        txt_surface_message = font.render(message, True, pygame.Color('red')) # hiển thị thông báo
        txt_surface_button = font.render("Login", True, (255, 255, 255))

        width_username = max(300, txt_surface_username.get_width() + 10)
        width_password = max(300, txt_surface_password.get_width() + 10)

        input_box_username.w = width_username
        input_box_password.w = width_password


        screen.blit(txt_surface_username, (input_box_username.x + 5, input_box_username.y + 5))
        screen.blit(txt_surface_password, (input_box_password.x + 5, input_box_password.y + 5))
        screen.blit(txt_surface_message, (screen_width // 3, screen_height * 3 // 4))  # vị trí thông báo

        pygame.draw.rect(screen, color_username, input_box_username, 2)
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        pygame.draw.rect(screen, (0, 128, 0), button_rect)  # Vẽ khung nút Đăng ký
        screen.blit(txt_surface_button, (button_rect.x + 35, button_rect.y + 10))  # Hiển thị chữ "Sign Up" trên nút

        pygame.display.flip()

    pygame.quit()

def menu_setting():
    pygame.init()
    man_hinh = pygame.display.set_mode((800, 500))
    pygame.display.set_caption('Setting menu')

    # Tải hình nền
    hinh_nen = pygame.image.load('dota_background/0.jpg')
    hinh_nen = pygame.transform.scale(hinh_nen, (800, 500))

    # Sử dụng font chữ tùy chỉnh
    font = pygame.font.Font(None, 32)
    font_thong_bao = pygame.font.Font(None, 28)

    # Màu sắc
    mau_trang = (255, 255, 255)
    mau_do = (255, 0, 0)
    mau_xanh = (0, 255, 0)
    mau_vang = (255, 255, 0)
    mau_den = (0, 0, 0)

    # Danh sách các lựa chọn cho từng thông số
    thong_so_1 = ['4', '6', '8', '10']
    thong_so_2 = ['8', '10', '12', '14']

    # Tạo các nút cho từng thông số
    nut_thong_so_1 = []
    nut_thong_so_2 = []

    # Tính toán vị trí cho các nút
    so_luong_nut = len(thong_so_1)
    khoang_cach = man_hinh.get_width() // (so_luong_nut + 1)

    for i, ts in enumerate(thong_so_1):
        rect = pygame.Rect(0, 0, 150, 50)
        rect.center = (khoang_cach * (i + 1), 150)
        nut_thong_so_1.append({'text': ts, 'rect': rect})

    for i, ts in enumerate(thong_so_2):
        rect = pygame.Rect(0, 0, 150, 50)
        rect.center = (khoang_cach * (i + 1), 250)
        nut_thong_so_2.append({'text': ts, 'rect': rect})

    # Nút "Bắt Đầu Game"
    rect_start = pygame.Rect(0, 0, 200, 60)
    rect_start.center = (man_hinh.get_width() // 2, 400)
    nut_bat_dau = {'text': 'Start playing', 'rect': rect_start}

    thong_so_da_chon = {'Thông Số 1': None, 'Thông Số 2': None}
    thong_bao = ''
    chay = True
    while chay:
        for su_kien in pygame.event.get():
            if su_kien.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif su_kien.type == pygame.MOUSEBUTTONDOWN:
                vi_tri_chuot = su_kien.pos
                # Kiểm tra các nút Thông Số 1
                for nut in nut_thong_so_1:
                    if nut['rect'].collidepoint(vi_tri_chuot):
                        thong_so_da_chon['Thông Số 1'] = nut['text']
                # Kiểm tra các nút Thông Số 2
                for nut in nut_thong_so_2:
                    if nut['rect'].collidepoint(vi_tri_chuot):
                        thong_so_da_chon['Thông Số 2'] = nut['text']
                # Kiểm tra nút "Bắt Đầu Game"
                if nut_bat_dau['rect'].collidepoint(vi_tri_chuot):
                    if thong_so_da_chon['Thông Số 1'] and thong_so_da_chon['Thông Số 2']:
                        chay = False  # Thoát vòng lặp để bắt đầu game
                    else:
                        thong_bao = "Table's height or width haven't been chosen"

        vi_tri_chuot = pygame.mouse.get_pos()

        # Vẽ hình nền
        man_hinh.blit(hinh_nen, (0, 0))

        # Vẽ tiêu đề
        tieu_de = font.render("Choose table's height and width", True, mau_vang)
        rect_tieu_de = tieu_de.get_rect(center=(man_hinh.get_width() // 2, 50))
        man_hinh.blit(tieu_de, rect_tieu_de)

        # Vẽ thông báo nếu có
        if thong_bao:
            text_thong_bao = font_thong_bao.render(thong_bao, True, mau_do)
            rect_thong_bao = text_thong_bao.get_rect(center=(man_hinh.get_width() // 2, 350))
            man_hinh.blit(text_thong_bao, rect_thong_bao)

        # Vẽ các nút Thông Số 1
        for nut in nut_thong_so_1:
            mau = mau_trang
            if nut['rect'].collidepoint(vi_tri_chuot):
                mau = mau_do
            if thong_so_da_chon['Thông Số 1'] == nut['text']:
                mau = mau_xanh
            pygame.draw.rect(man_hinh, mau, nut['rect'])
            pygame.draw.rect(man_hinh, mau_den, nut['rect'], 2)  # Viền đen
            text_surf = font.render(nut['text'], True, mau_den)
            text_rect = text_surf.get_rect(center=nut['rect'].center)
            man_hinh.blit(text_surf, text_rect)

        # Vẽ các nút Thông Số 2
        for nut in nut_thong_so_2:
            mau = mau_trang
            if nut['rect'].collidepoint(vi_tri_chuot):
                mau = mau_do
            if thong_so_da_chon['Thông Số 2'] == nut['text']:
                mau = mau_xanh
            pygame.draw.rect(man_hinh, mau, nut['rect'])
            pygame.draw.rect(man_hinh, mau_den, nut['rect'], 2)
            text_surf = font.render(nut['text'], True, mau_den)
            text_rect = text_surf.get_rect(center=nut['rect'].center)
            man_hinh.blit(text_surf, text_rect)

        # Vẽ nút "Bắt Đầu Game"
        mau = mau_trang
        if nut_bat_dau['rect'].collidepoint(vi_tri_chuot):
            mau = mau_do
        pygame.draw.rect(man_hinh, mau, nut_bat_dau['rect'])
        pygame.draw.rect(man_hinh, mau_den, nut_bat_dau['rect'], 2)
        text_surf = font.render(nut_bat_dau['text'], True, mau_den)
        text_rect = text_surf.get_rect(center=nut_bat_dau['rect'].center)
        man_hinh.blit(text_surf, text_rect)

        pygame.display.flip()

    pygame.quit()
    return int(thong_so_da_chon['Thông Số 1']), int(thong_so_da_chon['Thông Số 2'])


def score(username):
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    level = user_data[username]['level']
    board = user_data[username]['board']
    if level is None:
        return 0
    height = len(board) - 2
    width = len(board[0]) - 2
    paired_item = 0
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            if board[i][j] == 0:
                paired_item += 1
    paired_item //= 2
    result = ((level - 1) * height * width // 2 + paired_item) * 5
    return result

def update_leaderboard():
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    leaderboard = dict()
    for username in user_data:
        leaderboard[username] = score(username)

    get_score = lambda x: x[1]
    leaderboard = dict(sorted(leaderboard.items(), key=get_score, reverse=True))

    update = open('leaderboard.json', 'w')
    json.dump(leaderboard, update, indent=4)
    update.close()

def display_leaderboard(screen, scores):
    title_font = pygame.font.SysFont(None, 48)
    content_font = pygame.font.SysFont(None, 36)
    screen.fill(WHITE)

    # Title
    title_text = title_font.render("Leaderboard", True, BLACK)
    screen.blit(title_text, (800 // 2 - title_text.get_width() // 2, 50))

    # Table Headers
    header_font = pygame.font.SysFont(None, 40)
    headers = ["Rank", "Name", "Score"]
    header_y = 150
    column_widths = [100, 400, 200]

    for idx, header in enumerate(headers):
        header_text = header_font.render(header, True, WHITE)
        header_x = sum(column_widths[:idx]) + 50
        pygame.draw.rect(screen, GRAY, (header_x, header_y - 10, column_widths[idx], 50))
        screen.blit(header_text, (header_x + (column_widths[idx] - header_text.get_width()) // 2, header_y))

    # Table Content
    y_offset = 200
    for index, score in enumerate(scores.items()):
        rank_text = content_font.render(f"{index + 1}", True, BLACK)
        name_text = content_font.render(f"{score[0]}", True, BLACK)
        score_text = content_font.render(f"{score[1]}", True, BLACK)

        screen.blit(rank_text, (50 + (column_widths[0] - rank_text.get_width()) // 2, y_offset))
        screen.blit(name_text,
                    (sum(column_widths[:1]) + 50 + (column_widths[1] - name_text.get_width()) // 2, y_offset))
        screen.blit(score_text,
                    (sum(column_widths[:2]) + 50 + (column_widths[2] - score_text.get_width()) // 2, y_offset))

        y_offset += 50

    pygame.display.update()

def leaderboard():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Leaderboard')
    font = pygame.font.Font(None, 36)

    update_leaderboard()

    file_in = open('leaderboard.json', 'r')
    leaderboard = json.load(file_in)
    file_in.close()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Hiển thị bảng xếp hạng
        display_leaderboard(screen, leaderboard)

        pygame.display.flip()

    pygame.quit()

def save_game(username, level, time_left, board):
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    user_data[username]['level'] = level
    user_data[username]['time'] = time_left
    user_data[username]['board'] = board

    database = open('user_data.json', 'w')
    json.dump(user_data, database, indent=4)
    database.close()

def runGame(username, level, time_left, board):
    pygame.init()
    global GAMETIME, LEVEL, LIVES, TIMEBONUS, STARTTIME, LIVESFONT, BASICFONT
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)


    if level is None: level = LEVEL = 1
    elif level > 5: leaderboard()
    else:
        LEVEL = level

    if board is None:
        mainBoard = getRandomizedBoard()
    else:
        mainBoard = board
        global BOARDHEIGHT, BOARDWIDTH, NUMHEROES_ONBOARD, XMARGIN, YMARGIN
        BOARDHEIGHT, BOARDWIDTH = len(board), len(board[0])
        NUMHEROES_ONBOARD = (BOARDHEIGHT - 2) * (BOARDWIDTH - 2) // NUMSAMEHEROES
        XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
        YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

    if time_left is not None:
        GAMETIME = time_left


    clickedBoxes = [] # stores the (x, y) of clicked boxes
    firstSelection = None # stores the (x, y) of the first box clicked
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)

    STARTTIME = time.time()
    TIMEBONUS = 0

    randomBG = listBG[LEVEL - 1]
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1, 0.0)

    while True:
        mouseClicked = False

        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard, DISPLAYSURF)
        drawClickedBox(mainBoard, clickedBoxes, DISPLAYSURF)
        drawTimeBar(DISPLAYSURF)
        drawLives(DISPLAYSURF)

        if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
            LEVEL = LEVELMAX + 1
            break
        if time.time() - lastTimeGetPoint >= GETHINTTIME:
            drawHint(hint, DISPLAYSURF)

        for event in pygame.event.get():

            if event.type == QUIT:
                # if user quit the game, save it
                save_game(username, level, GAMETIME + TIMEBONUS - time.time() + STARTTIME, mainBoard)
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if event.type == KEYUP:
                if event.key == K_n:
                    boxy1, boxx1 = hint[0][0], hint[0][1]
                    boxy2, boxx2 = hint[1][0], hint[1][1]
                    mainBoard[boxy1][boxx1] = 0
                    mainBoard[boxy2][boxx2] = 0
                    TIMEBONUS += 1
                    alterBoardWithLevel(mainBoard, boxy1, boxx1, boxy2, boxx2, LEVEL)

                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard, DISPLAYSURF)
                        save_game(username, level, GAMETIME + TIMEBONUS - time.time() + STARTTIME, mainBoard)
                        runGame(username, LEVEL + 1, None, None)

                    if not(mainBoard[boxy1][boxx1] != 0 and bfs(mainBoard, boxy1, boxx1, boxy2, boxx2)):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(100)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                leaderboard()
                            hint = getHint(mainBoard)

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0:
            # The mouse is currently over a box
            drawHighlightBox(mainBoard, boxx, boxy, DISPLAYSURF)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0 and mouseClicked == True:
            # The mouse is clicking on a box
            clickedBoxes.append((boxx, boxy))
            drawClickedBox(mainBoard, clickedBoxes, DISPLAYSURF)
            mouseClicked = False

            if firstSelection == None:
                firstSelection = (boxx, boxy)
                clickSound.play()
            else:
                path = bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx)
                if path:
                    if random.randint(0, 100) < 20:
                        soundObject = random.choice(LIST_SOUNDEFFECT)
                        soundObject.play()
                    getPointSound.play()
                    mainBoard[firstSelection[1]][firstSelection[0]] = 0
                    mainBoard[boxy][boxx] = 0
                    drawPath(mainBoard, path, DISPLAYSURF)
                    TIMEBONUS += 1
                    lastTimeGetPoint = time.time()
                    alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, LEVEL)

                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard, DISPLAYSURF)
                        runGame(username, LEVEL + 1, None, None)
                    if not(mainBoard[hint[0][0]][hint[0][1]] != 0 and bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(500)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                leaderboard()
                            hint = getHint(mainBoard)
                else:
                    clickSound.play()

                clickedBoxes = []
                firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    GAMETIME = 240
    runGame(username, level + 1, None, None)

def getRandomizedBoard():
    list_pokemons = list(range(1, len(HEROES_DICT) + 1))
    random.shuffle(list_pokemons)
    list_pokemons = list_pokemons[:NUMHEROES_ONBOARD] * NUMSAMEHEROES
    random.shuffle(list_pokemons)
    board = [[0 for _ in range(BOARDWIDTH)] for _ in range(BOARDHEIGHT)]

    # We create a board of images surrounded by 4 arrays of zeroes
    k = 0
    for i in range(1, BOARDHEIGHT - 1):
        for j in range(1, BOARDWIDTH - 1):
            board[i][j] = list_pokemons[k]
            k += 1
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + XMARGIN
    top = boxy * BOXSIZE + YMARGIN
    return left, top

def getBoxAtPixel(x, y):
    if x <= XMARGIN or x >= WINDOWWIDTH - XMARGIN or y <= YMARGIN or y >= WINDOWHEIGHT - YMARGIN:
        return None, None
    return (x - XMARGIN) // BOXSIZE, (y - YMARGIN) // BOXSIZE

def drawBoard(board, DISPLAYSURF):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if board[boxy][boxx] != 0:
                left, top = leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                DISPLAYSURF.blit(HEROES_DICT[board[boxy][boxx]], boxRect)

def drawHighlightBox(board, boxx, boxy, DISPLAYSURF):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 2, top - 2,
                                                   BOXSIZE + 4, BOXSIZE + 4), 2)

def drawClickedBox(board, clickedBoxes, DISPLAYSURF):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = HEROES_DICT[board[boxy][boxx]].copy()

        # Darken the clicked image
        image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
        DISPLAYSURF.blit(image, boxRect)

def bfs(board, boxy1, boxx1, boxy2, boxx2):
    def backtrace(parent, boxy1, boxx1, boxy2, boxx2):
        start = (boxy1, boxx1, 0, 'no_direction')
        end = 0
        for node in parent:
            if node[:2] == (boxy2, boxx2):
                end = node

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()

        for i in range(len(path)):
            path[i] = path[i][:2]
        return path

    if board[boxy1][boxx1] != board[boxy2][boxx2]:
        return []

    n = len(board)
    m = len(board[0])

    import collections
    q = collections.deque()
    q.append((boxy1, boxx1, 0, 'no_direction'))
    visited = set()
    visited.add((boxy1, boxx1, 0, 'no_direction'))
    parent = {}

    while len(q) > 0:
        r, c, num_turns, direction = q.popleft()
        if (r, c) != (boxy1, boxx1) and (r, c) == (boxy2, boxx2):
            return backtrace(parent, boxy1, boxx1, boxy2, boxx2)

        dict_directions = {(r + 1, c): 'down', (r - 1, c): 'up', (r, c - 1): 'left',
                           (r, c + 1): 'right'}
        for neiborX, neiborY in dict_directions:
            next_direction = dict_directions[(neiborX, neiborY)]
            if 0 <= neiborX <= n - 1 and 0 <= neiborY <= m - 1 and (
                    board[neiborX][neiborY] == 0 or (neiborX, neiborY) == (boxy2, boxx2)):
                if direction == 'no_direction':
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction == next_direction and (
                        neiborX, neiborY, num_turns, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction != next_direction and num_turns < 2 and (
                        neiborX, neiborY, num_turns + 1, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns + 1, next_direction))
                    visited.add((neiborX, neiborY, num_turns + 1, next_direction))
                    parent[
                        (neiborX, neiborY, num_turns + 1, next_direction)] = (
                    r, c, num_turns, direction)
    return []

def getCenterPos(pos): # pos is coordinate of a box in mainBoard
    left, top = leftTopCoordsOfBox(pos[1], pos[0])
    return tuple([left + BOXSIZE // 2, top + BOXSIZE // 2])

def drawPath(board, path, DISPLAYSURF):
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i + 1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos, 4)
    pygame.display.update()
    pygame.time.wait(300)

def drawTimeBar(DISPLAYSURF):
    progress = 1 - ((time.time() - STARTTIME - TIMEBONUS) / GAMETIME)

    pygame.draw.rect(DISPLAYSURF, borderColor, (barPos, barSize), 1)
    innerPos = (barPos[0] + 2, barPos[1] + 2)
    innerSize = ((barSize[0] - 4) * progress, barSize[1] - 4)
    pygame.draw.rect(DISPLAYSURF, barColor, (innerPos, innerSize))

def showGameOverScreen(DISPLAYSURF):
    playAgainFont = pygame.font.Font('freesansbold.ttf', 50)
    playAgainSurf = playAgainFont.render('Play Again?', True, PURPLE)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(playAgainSurf, playAgainRect)
    pygame.draw.rect(DISPLAYSURF, PURPLE, playAgainRect, 4)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if playAgainRect.collidepoint((mousex, mousey)):
                    return

def getHint(board):
    boxPokesLocated = collections.defaultdict(list)
    hint = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                boxPokesLocated[board[boxy][boxx]].append((boxy, boxx))
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                for otherBox in boxPokesLocated[board[boxy][boxx]]:
                    if otherBox != (boxy, boxx) and bfs(board, boxy, boxx, otherBox[0], otherBox[1]):
                        hint.append((boxy, boxx))
                        hint.append(otherBox)
                        return hint
    return []

def drawHint(hint, DISPLAYSURF):
    for boxy, boxx in hint:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top,
                                                       BOXSIZE, BOXSIZE), 2)

def resetBoard(board):
    pokesOnBoard = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                pokesOnBoard.append(board[boxy][boxx])
    referencedList = pokesOnBoard[:]
    while referencedList == pokesOnBoard:
        random.shuffle(pokesOnBoard)

    i = 0
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                board[boxy][boxx] = pokesOnBoard[i]
                i += 1
    return board

def isGameComplete(board):
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                return False
    return True

def alterBoardWithLevel(board, boxy1, boxx1, boxy2, boxx2, level):

    # Level 2: All the pokemons move up to the top boundary
    if level == 2:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            while len(cur_list) < BOARDHEIGHT:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 3: All the pokemons move down to the bottom boundary
    if level == 3:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            cur_list.append(0)
            cur_list = [0] * (BOARDHEIGHT - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 4: All the pokemons move left to the left boundary
    if level == 4:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            while len(cur_list) < BOARDWIDTH:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    # Level 5: All the pokemons move right to the right boundary
    if level == 5:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            cur_list.append(0)
            cur_list = [0] * (BOARDWIDTH - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    return board

def drawLives(DISPLAYSURF):
    aegisRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
    DISPLAYSURF.blit(aegis, aegisRect)
    livesSurf = LIVESFONT.render(str(LIVES), True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)

if __name__ == '__main__':
    showStartScreen()


