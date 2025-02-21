import pygame
import pytmx
from pytmx.util_pygame import load_pygame

# Khởi tạo pygame
pygame.init()

# ⚠️ Tạo cửa sổ game trước khi load bản đồ (tránh lỗi No video mode)
screen = pygame.display.set_mode((800, 600))  # Tạo cửa sổ tạm

# Load bản đồ từ file .tmx
tmx_map = load_pygame("assets/maps/level1.tmx")

# Lấy kích thước bản đồ
WIDTH = tmx_map.width * tmx_map.tilewidth
HEIGHT = tmx_map.height * tmx_map.tileheight

# Tạo cửa sổ game với kích thước vừa bản đồ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Chúc Mừng 8/3")

# Hàm vẽ bản đồ
def draw_map():
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_map.tilewidth, y * tmx_map.tileheight))

# Tải hình ảnh nhân vật
character_stand = pygame.image.load("assets/images/goku.png")
character_run_right = [pygame.image.load(f"assets/images/goku_run{i}.png") for i in range(1, 7)]
character_run_left = [pygame.image.load(f"assets/images/goku_runcopy{i}.png") for i in range(1, 7)]
character_jump_right = [pygame.image.load(f"assets/images/goku_jump{i}.png") for i in range(1, 4)]
character_jump_left = [pygame.image.load(f"assets/images/goku_jumpcopy{i}.png") for i in range(1, 4)]

# Đọc file lời chúc
def load_messages():
    with open("messages.txt", "r", encoding="utf-8") as file:
        return [msg.strip() for msg in file.readlines()]

messages = load_messages()

# Biến lưu trạng thái nhân vật
x =100
y= HEIGHT -140
vel = 3
is_jumping = False
jump_count = 13
left, right = False, False
walk_count = 0
level = 1
score = 0
max_score = 700  # Giả sử mỗi cấp độ tối đa 100 điểm

# Giới hạn chiều cao mặt đất
ground_y = HEIGHT -140

# Hàm vẽ nhân vật
def draw_character():
    global walk_count
    if is_jumping:
        if right:
            screen.blit(character_jump_right[walk_count % len(character_jump_right)], (x, y))
        elif left:
            screen.blit(character_jump_left[walk_count % len(character_jump_left)], (x, y))
        else:
            screen.blit(character_jump_right[0], (x, y))
    elif left:
        screen.blit(character_run_left[walk_count % len(character_run_left)], (x, y))
    elif right:
        screen.blit(character_run_right[walk_count % len(character_run_right)], (x, y))
    else:
        screen.blit(character_stand, (x, y))
    
    walk_count += 1

# Hàm hiển thị lời chúc
def show_message():
    font = pygame.font.Font(None, 36)
    if level == 7 and score >= max_score:
        text = font.render(messages[-1], True, (255, 0, 0))
    else:
        text = font.render(messages[level - 1], True, (0, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(2000)

# Vòng lặp game
running = True
while running:
    pygame.time.delay(50)
    screen.fill((255, 255, 255))

    # Vẽ bản đồ
    draw_map()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= vel
        left, right = True, False
    elif keys[pygame.K_RIGHT]:
        x += vel
        left, right = False, True
    else:
        left, right = False, False
        walk_count = 0

    # Kiểm soát nhảy
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if jump_count >= -13:
            y -= (jump_count * abs(jump_count)) // 3  # Làm mượt nhảy
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 13

    # Giữ nhân vật không rơi khỏi màn hình
    if y > ground_y:
        y = ground_y

    draw_character()
    pygame.display.update()
    
    # Giả lập hoàn thành cấp độ
    if x > WIDTH - 50:
        x = 100
        level += 1
        score += 100
        if level > 7:
            running = False
        else:
            show_message()

pygame.quit()
