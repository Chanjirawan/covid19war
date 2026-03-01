# ==========================================
# COVID19 WAR - SNAKE GAME
# Python + Pygame
# ==========================================

# import pygame library สำหรับสร้างเกม
import pygame

# import random สำหรับสุ่มตำแหน่ง virus
import random

# ==========================================
# GAME SETTINGS
# ==========================================

# กำหนดความกว้างหน้าจอเกม
WIDTH = 600

# กำหนดความสูงหน้าจอเกม
HEIGHT = 600

# กำหนดขนาด grid ของ snake
GRID_SIZE = 20

# กำหนด FPS ของเกม
FPS = 10


# ==========================================
# INITIALIZE PYGAME
# ==========================================

# เริ่มต้น pygame
pygame.init()

# เริ่มต้นระบบเสียง
pygame.mixer.init()

# สร้างหน้าจอเกม
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ตั้งชื่อหน้าต่างเกม
pygame.display.set_caption("Covid19War Snake")

# ใช้ควบคุมความเร็วเกม
clock = pygame.time.Clock()

# สร้าง font สำหรับแสดงข้อความ
font = pygame.font.SysFont("arial", 28)


# ==========================================
# LOAD FILES (IMAGES + SOUND)
# ==========================================

# โหลดภาพ background
background = pygame.image.load("bg.png")

# โหลดภาพ immune cell (snake)
snake_img = pygame.image.load("immune.png")

# โหลดภาพ virus
virus_img = pygame.image.load("covid19.png")

# โหลดเสียงตอนกิน virus
eat_sound = pygame.mixer.Sound("boom.wav")


# ==========================================
# SNAKE CLASS
# ==========================================


class Snake:

    # constructor ของ snake
    def __init__(self):

        # list เก็บตำแหน่ง body ของ snake
        self.body = [(300, 300)]

        # ความเร็วแกน x
        self.dx = GRID_SIZE

        # ความเร็วแกน y
        self.dy = 0

        # ตัวแปรสำหรับ grow
        self.grow = False

    # function สำหรับขยับ snake
    def move(self):

        # ดึงตำแหน่งหัว snake
        head_x, head_y = self.body[0]

        # คำนวณตำแหน่งหัวใหม่
        new_head = (head_x + self.dx, head_y + self.dy)

        # เพิ่มหัวใหม่เข้า list
        self.body.insert(0, new_head)

        # ถ้าไม่ได้ grow ให้ลบหาง
        if not self.grow:

            # ลบ segment สุดท้าย
            self.body.pop()

        else:

            # reset grow
            self.grow = False

    # function วาด snake
    def draw(self):

        # loop ทุก segment
        for segment in self.body:

            # วาดภาพ snake
            screen.blit(snake_img, segment)

    # function ตรวจสอบชน
    def collision(self):

        # หาตำแหน่งหัว
        head = self.body[0]

        # ถ้าชนกำแพงซ้าย
        if head[0] < 0:
            return True

        # ถ้าชนกำแพงขวา
        if head[0] >= WIDTH:
            return True

        # ถ้าชนกำแพงบน
        if head[1] < 0:
            return True

        # ถ้าชนกำแพงล่าง
        if head[1] >= HEIGHT:
            return True

        # ถ้าชนตัวเอง
        if head in self.body[1:]:
            return True

        # ถ้าไม่ชนอะไร
        return False


# ==========================================
# VIRUS CLASS
# ==========================================


class Virus:

    # constructor
    def __init__(self):

        # เรียก spawn
        self.spawn()

    # สุ่มตำแหน่ง virus
    def spawn(self):

        # สุ่มตำแหน่ง x
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

        # สุ่มตำแหน่ง y
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

        # เก็บตำแหน่ง
        self.pos = (x, y)

    # วาด virus
    def draw(self):

        # วาดภาพ virus
        screen.blit(virus_img, self.pos)


# ==========================================
# CREATE GAME OBJECTS
# ==========================================

# สร้าง snake
snake = Snake()

# สร้าง virus
virus = Virus()

# คะแนนผู้เล่น
score = 0

# ตัวแปร game over
game_over = False


# ==========================================
# GAME LOOP
# ==========================================

# ตัวแปรควบคุม loop
running = True

# loop หลักของเกม
while running:

    # จำกัด FPS
    clock.tick(FPS)

    # ======================================
    # INPUT
    # ======================================

    # ตรวจสอบ event ต่างๆ
    for event in pygame.event.get():

        # ถ้ากดปิดหน้าต่าง
        if event.type == pygame.QUIT:

            # ออกจากเกม
            running = False

        # ถ้ากด keyboard
        if event.type == pygame.KEYDOWN:

            # ถ้ากดปุ่มซ้าย
            if event.key == pygame.K_LEFT:

                # เปลี่ยนทิศ
                snake.dx = -GRID_SIZE
                snake.dy = 0

            # ถ้ากดปุ่มขวา
            if event.key == pygame.K_RIGHT:

                # เปลี่ยนทิศ
                snake.dx = GRID_SIZE
                snake.dy = 0

            # ถ้ากดปุ่มขึ้น
            if event.key == pygame.K_UP:

                # เปลี่ยนทิศ
                snake.dx = 0
                snake.dy = -GRID_SIZE

            # ถ้ากดปุ่มลง
            if event.key == pygame.K_DOWN:

                # เปลี่ยนทิศ
                snake.dx = 0
                snake.dy = GRID_SIZE

    # ======================================
    # UPDATE GAME
    # ======================================

    # ถ้ายังไม่ game over
    if not game_over:

        # ขยับ snake
        snake.move()

        # ถ้าหัว snake ชน virus
        if snake.body[0] == virus.pos:

            # เล่นเสียง
            eat_sound.play()

            # เพิ่มคะแนน
            score += 1

            # snake โต
            snake.grow = True

            # spawn virus ใหม่
            virus.spawn()

        # ตรวจสอบชน
        if snake.collision():

            # game over
            game_over = True

    # ======================================
    # DRAW
    # ======================================

    # วาด background
    screen.blit(background, (0, 0))

    # วาด virus
    virus.draw()

    # วาด snake
    snake.draw()

    # สร้าง text คะแนน
    score_text = font.render("Virus Eliminated: " + str(score), True, (0, 255, 255))

    # แสดงคะแนน
    screen.blit(score_text, (10, 10))

    # ถ้า game over
    if game_over:

        # สร้างข้อความ
        over_text = font.render("SYSTEM INFECTED", True, (255, 0, 0))

        # แสดงข้อความ
        screen.blit(over_text, (180, 300))

    # update หน้าจอ
    pygame.display.flip()


# ==========================================
# QUIT GAME
# ==========================================

# ปิด pygame
pygame.quit()
