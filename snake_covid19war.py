# นำเข้า pygame สำหรับสร้างเกม
import pygame

# นำเข้า random สำหรับสุ่มตำแหน่ง virus
import random

# นำเข้า time สำหรับระบบเวลา
import time

# เริ่มต้นระบบ pygame
pygame.init()

# กำหนดความกว้างหน้าจอ
WIDTH = 900

# กำหนดความสูงหน้าจอ
HEIGHT = 600

# สร้างหน้าต่างเกม
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ตั้งชื่อหน้าต่างเกม
pygame.display.set_caption("Covid19War Snake A+")

# สร้าง clock สำหรับควบคุม FPS
clock = pygame.time.Clock()

# โหลดภาพ background
bg = pygame.image.load("bg.png")

# ปรับขนาด background ให้เต็มหน้าจอ
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# โหลดภาพ immune (งู)
immune_img = pygame.image.load("immune.png")

# โหลดภาพ virus
virus_img = pygame.image.load("virus.png")

# กำหนดขนาด grid สำหรับการเดินของ snake
GRID = 40

# สร้าง font สำหรับข้อความ
font = pygame.font.SysFont("arial", 28)

# สร้าง font สำหรับข้อความใหญ่
big_font = pygame.font.SysFont("arial", 50)


# ฟังก์ชันสุ่มตำแหน่ง virus
def random_pos():

    # สุ่มค่า x
    x = random.randint(0, (WIDTH - GRID) // GRID) * GRID

    # สุ่มค่า y
    y = random.randint(0, (HEIGHT - GRID) // GRID) * GRID

    # คืนค่าตำแหน่ง
    return (x, y)


# ฟังก์ชันเริ่มเกมใหม่
def reset_game():

    # snake เริ่มต้น 1 ช่อง
    snake = [(200, 200)]

    # ทิศทางเริ่มต้น
    direction = "RIGHT"

    # สร้าง virus 3 ตัว
    viruses = [random_pos() for _ in range(3)]

    # จำนวน virus ที่กิน
    eaten = 0

    # เวลาเริ่มต้น
    start_time = time.time()

    # เวลาในเกม
    time_limit = 15

    # คืนค่าทั้งหมด
    return snake, direction, viruses, eaten, start_time, time_limit


# เริ่มเกมครั้งแรก
snake, direction, viruses, eaten, start_time, time_limit = reset_game()

# ตัวแปรควบคุม loop
running = True

# ตัวแปรสถานะเกม
game_over = False

# ตัวแปรชนะ
win = False

# game loop
while running:

    # อ่าน event ต่างๆ
    for event in pygame.event.get():

        # ถ้าปิดหน้าต่าง
        if event.type == pygame.QUIT:

            # ปิดเกม
            running = False

        # ถ้ามีการกดปุ่ม
        if event.type == pygame.KEYDOWN:

            # ถ้าเกมจบแล้วและกด R
            if (game_over or win) and event.key == pygame.K_r:

                # reset เกมใหม่
                snake, direction, viruses, eaten, start_time, time_limit = reset_game()

                # รีเซ็ตสถานะ
                game_over = False
                win = False

            # เปลี่ยนทิศทาง
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"

            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"

            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"

            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # ถ้าเกมยังไม่จบ
    if not game_over and not win:

        # หัวงู
        head_x, head_y = snake[0]

        # คำนวณตำแหน่งใหม่
        if direction == "UP":
            head_y -= GRID

        if direction == "DOWN":
            head_y += GRID

        if direction == "LEFT":
            head_x -= GRID

        if direction == "RIGHT":
            head_x += GRID

        # สร้างหัวใหม่
        new_head = (head_x, head_y)

        # เพิ่มหัวเข้า snake
        snake.insert(0, new_head)

        # ตรวจชน virus
        for v in viruses:

            # ถ้าหัวชน virus
            if new_head == v:

                # เพิ่มจำนวนที่กิน
                eaten += 1

                # เพิ่มเวลา 1 วินาที
                time_limit += 1

                # ลบ virus ที่กิน
                viruses.remove(v)

                # เพิ่ม virus ใหม่หลายตัว
                for i in range(2):
                    viruses.append(random_pos())

                # ออกจาก loop
                break

        else:

            # ถ้าไม่ได้กิน virus
            snake.pop()

        # ตรวจชนขอบจอ
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        # ตรวจชนตัวเอง
        if new_head in snake[1:]:
            game_over = True

        # ตรวจว่ากินครบ 10
        if eaten >= 10:
            win = True

    # วาด background
    screen.blit(bg, (0, 0))

    # คำนวณขนาด immune ตามจำนวนที่กิน
    size = 32 + eaten * 3

    # ปรับขนาด immune
    immune_scaled = pygame.transform.scale(immune_img, (size, size))

    # วาด snake
    for part in snake:
        screen.blit(immune_scaled, part)

    # ปรับขนาด virus
    virus_scaled = pygame.transform.scale(virus_img, (32, 32))

    # วาด virus ทุกตัว
    for v in viruses:
        screen.blit(virus_scaled, v)

    # คำนวณเวลาที่ผ่านไป
    elapsed = int(time.time() - start_time)

    # เวลาที่เหลือ
    remaining = time_limit - elapsed

    # ถ้าเวลาหมด
    if remaining <= 0 and not win:
        game_over = True
        remaining = 0

    # แสดงข้อความเวลา
    time_text = font.render("Time: " + str(remaining), True, (255, 255, 255))

    # วาดเวลา
    screen.blit(time_text, (20, 20))

    # แสดงจำนวน virus ที่กิน
    eat_text = font.render("Virus eaten: " + str(eaten) + "/10", True, (255, 255, 255))

    # วาดจำนวนที่กิน
    screen.blit(eat_text, (20, 60))

    # ถ้า game over
    if game_over:

        # สร้างข้อความแพ้
        text = big_font.render("GAME OVER", True, (255, 50, 50))

        # วาดข้อความ
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 40))

        # ข้อความ restart
        r = font.render("Press R to Restart", True, (255, 255, 255))

        # วาดข้อความ restart
        screen.blit(r, (WIDTH // 2 - 120, HEIGHT // 2 + 20))

    # ถ้าชนะ
    if win:

        # สร้างข้อความชนะ
        text = big_font.render("YOU WIN!", True, (50, 255, 50))

        # วาดข้อความ
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))

        # ข้อความ restart
        r = font.render("Press R to Play Again", True, (255, 255, 255))

        # วาดข้อความ restart
        screen.blit(r, (WIDTH // 2 - 120, HEIGHT // 2 + 20))

    # อัปเดตหน้าจอ
    pygame.display.update()

    # จำกัด FPS
    clock.tick(6)

# ปิด pygame
pygame.quit()
