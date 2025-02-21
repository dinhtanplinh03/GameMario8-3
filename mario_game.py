import pygame
import pytmx
from pytmx.util_pygame import load_pygame

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ hiển thị theo chiều cao 12 tiles
TILE_SIZE = 64  # Kích thước mỗi tile
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 12 * TILE_SIZE  # 12 tiles chiều cao
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Chúc Mừng 8/3")

# Load bản đồ từ file .tmx
tmx_map = load_pygame("assets/maps/level1.tmx")

# Lấy kích thước bản đồ
MAP_WIDTH = tmx_map.width * tmx_map.tilewidth
MAP_HEIGHT = tmx_map.height * tmx_map.tileheight

# Camera theo dõi nhân vật
camera_x = 0

# Hàm vẽ bản đồ
def draw_map():
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_map.tilewidth - camera_x, y * tmx_map.tileheight))

# Tải hình ảnh nhân vật
character_stand = pygame.image.load("assets/images/goku.png")
character_run_right = [pygame.image.load(f"assets/images/goku_run{i}.png") for i in range(1, 7)]
character_run_left = [pygame.image.load(f"assets/images/goku_runcopy{i}.png") for i in range(1, 7)]
character_jump_right = [pygame.image.load(f"assets/images/goku_jump{i}.png") for i in range(1, 4)]
character_jump_left = [pygame.image.load(f"assets/images/goku_jumpcopy{i}.png") for i in range(1, 4)]

# Nhân vật
x = 100
y = MAP_HEIGHT - 140
vel = 5
is_jumping = False
jump_count = 13
left, right = False, False
walk_count = 0

# Giới hạn mặt đất
ground_y = MAP_HEIGHT - 140

# Hàm cập nhật camera
def update_camera():
    global camera_x
    camera_x = x - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, MAP_WIDTH - SCREEN_WIDTH))

# Hàm vẽ nhân vật
def draw_character():
    global walk_count
    if is_jumping:
        if right:
            screen.blit(character_jump_right[walk_count % len(character_jump_right)], (x - camera_x, y))
        elif left:
            screen.blit(character_jump_left[walk_count % len(character_jump_left)], (x - camera_x, y))
        else:
            screen.blit(character_jump_right[0], (x - camera_x, y))
    elif left:
        screen.blit(character_run_left[walk_count % len(character_run_left)], (x - camera_x, y))
    elif right:
        screen.blit(character_run_right[walk_count % len(character_run_right)], (x - camera_x, y))
    else:
        screen.blit(character_stand, (x - camera_x, y))
    
    walk_count += 1

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
    
    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
        left, right = True, False
    elif keys[pygame.K_RIGHT] and x < MAP_WIDTH - 50:
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
            y -= (jump_count * abs(jump_count)) // 3
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 13

    # Giữ nhân vật không rơi khỏi màn hình
    if y > ground_y:
        y = ground_y

    # Cập nhật camera
    update_camera()

    # Vẽ nhân vật
    draw_character()
    pygame.display.update()

pygame.quit()
