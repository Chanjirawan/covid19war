# import pygame library สำหรับสร้างเกม
import pygame

# import random สำหรับสุ่มตำแหน่งศัตรู
import random


# =============================
# GAME SETUP
# =============================

# กำหนดความกว้างของหน้าจอเกม
WIDTH = 600

# กำหนดความสูงของหน้าจอเกม
HEIGHT = 800

# กำหนดจำนวน frame ต่อวินาที
FPS = 60

# คะแนนที่ต้องได้เพื่อชนะเกม
WIN_SCORE = 30


# เริ่มต้น pygame
pygame.init()

# เริ่มต้นระบบเสียง
pygame.mixer.init()


# สร้างหน้าจอเกม
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ตั้งชื่อหน้าต่างเกม
pygame.display.set_caption("Covid19War")


# ใช้ควบคุมความเร็วของเกม
clock = pygame.time.Clock()

# สร้าง font สำหรับแสดงข้อความ
font = pygame.font.SysFont("roboto", 40, bold=True)


# =============================
# LOAD GAME FILES
# =============================

# โหลดภาพ background
bg = pygame.image.load("bg.png").convert()

# ใช้เลื่อน background
bg_offset = bg.get_height() - HEIGHT


# โหลดภาพ player
player_img = pygame.image.load("JiJiSR1.png").convert_alpha()

# โหลดภาพ player ตอนเลี้ยวซ้าย
player_left = pygame.image.load("JiJiSR1L.png").convert_alpha()

# โหลดภาพ player ตอนเลี้ยวขวา
player_right = pygame.image.load("JiJiSR1R.png").convert_alpha()


# โหลดภาพไวรัส
covid_img = pygame.image.load("covid19.png").convert_alpha()

# โหลดภาพกระสุนยา
cure_img = pygame.image.load("cure.png").convert_alpha()


# โหลดเสียงระเบิด
boom_sound = pygame.mixer.Sound("boom.wav")


# =============================
# GAME VARIABLES
# =============================

# สถานะเกมว่าเริ่มหรือยัง
game_started = False

# สถานะเกม over
game_over = False

# สถานะชนะเกม
game_win = False


# เวลาตั้งต้นของเกม
game_time = 5

# เวลาเริ่มเกม
start_ticks = pygame.time.get_ticks()


# ตัวแปรสำหรับ animation ของ time bar
bar_flash = True
last_flash = 0
bar_boost = 0


# list เก็บตำแหน่ง explosion
explosions = []


# =============================
# PLAYER CLASS
# =============================


# class player สร้างตัวละครผู้เล่น
class Player(pygame.sprite.Sprite):

    def __init__(self):

        # เรียก constructor ของ pygame sprite
        pygame.sprite.Sprite.__init__(self)

        # เก็บภาพ player ทั้งหมด
        self.images = [player_img, player_left, player_right]

        # กำหนดภาพเริ่มต้น
        self.image = self.images[0]

        # สร้าง rectangle ของ player
        self.rect = self.image.get_rect()

        # ตั้งตำแหน่งเริ่มต้น player
        self.rect.midbottom = (WIDTH / 2, HEIGHT - 50)

        # กำหนด radius สำหรับ collision
        self.radius = 40

        # ความเร็วแนวนอน
        self.speedx = 0

        # เก็บค่าความเร็วก่อนหน้า
        self.lastSpeedx = 0

        # คะแนนของผู้เล่น
        self.score = 0

    def update(self):

        # อัพเดทตำแหน่ง player ตามความเร็ว
        self.rect.x += self.speedx

        # ไม่ให้ player ออกนอกจอด้านซ้าย
        if self.rect.left < 0:
            self.rect.left = 0

        # ไม่ให้ player ออกนอกจอด้านขวา
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # เปลี่ยนภาพตอนเลี้ยวซ้าย
        if self.speedx < 0 and self.lastSpeedx != self.speedx:
            self.image = self.images[1]

        # เปลี่ยนภาพตอนเลี้ยวขวา
        elif self.speedx > 0 and self.lastSpeedx != self.speedx:
            self.image = self.images[2]

        # เปลี่ยนภาพตอนหยุด
        elif self.speedx == 0 and self.lastSpeedx != self.speedx:
            self.image = self.images[0]

        # บันทึกความเร็วล่าสุด
        self.lastSpeedx = self.speedx

    def shoot(self):

        # สร้างกระสุน
        cure = Cure(self.rect.centerx, self.rect.top)

        # เพิ่มใน sprite group
        allsprites.add(cure)

        cures.add(cure)


# =============================
# COVID ENEMY CLASS
# =============================


# class ศัตรูไวรัส
class Covid(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        # ตั้งภาพไวรัส
        self.image = covid_img

        # สร้าง rectangle
        self.rect = self.image.get_rect()

        # radius สำหรับ collision
        self.radius = int(self.rect.width * 0.7 / 2)

        # spawn ไวรัส
        self.respawn()

    def respawn(self):

        # สุ่มตำแหน่ง x
        self.rect.x = random.randrange(WIDTH - self.rect.width)

        # spawn จากด้านบนจอ
        self.rect.y = random.randrange(-100, -40)

        # ความเร็วแนวนอน
        self.speedx = random.randrange(-2, 2)

        # ความเร็วแนวตั้ง
        self.speedy = random.randrange(2, 8)

    def update(self):

        # ขยับไวรัส
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # ถ้าออกนอกจอให้ spawn ใหม่
        if self.rect.top > HEIGHT:
            self.respawn()


# =============================
# CURE BULLET CLASS
# =============================


class Cure(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        # ตั้งภาพกระสุน
        self.image = cure_img

        # สร้าง rectangle
        self.rect = self.image.get_rect()

        # ตั้งตำแหน่ง x
        self.rect.centerx = x

        # ตั้งตำแหน่ง y
        self.rect.bottom = y

        # ความเร็วกระสุน
        self.speedy = -8

    def update(self):

        # กระสุนเคลื่อนขึ้น
        self.rect.y += self.speedy

        # ถ้ากระสุนออกจอให้ลบ
        if self.rect.bottom < 0:
            self.kill()


# =============================
# SPRITE GROUPS
# =============================

# group สำหรับ sprite ทั้งหมด
allsprites = pygame.sprite.Group()

# group ศัตรู
covids = pygame.sprite.Group()

# group กระสุน
cures = pygame.sprite.Group()


# สร้าง player
player = Player()

# เพิ่ม player ลง group
allsprites.add(player)


# สร้างไวรัส 10 ตัว
for i in range(10):

    c = Covid()

    allsprites.add(c)

    covids.add(c)


# =============================
# GAME LOOP
# =============================

running = True

while running:

    # ควบคุม FPS
    clock.tick(FPS)

    # =============================
    # INPUT
    # =============================

    for event in pygame.event.get():

        # ปิดเกม
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # เริ่มเกม
            if not game_started:

                if event.key == pygame.K_SPACE:
                    game_started = True
                    start_ticks = pygame.time.get_ticks()

            # เดินซ้าย
            elif event.key == pygame.K_LEFT:
                player.speedx = -6

            # เดินขวา
            elif event.key == pygame.K_RIGHT:
                player.speedx = 6

            # ยิงกระสุน
            elif event.key == pygame.K_SPACE and not game_over:
                player.shoot()

        if event.type == pygame.KEYUP:

            # หยุดเดินซ้าย
            if event.key == pygame.K_LEFT:
                player.speedx = 0

            # หยุดเดินขวา
            if event.key == pygame.K_RIGHT:
                player.speedx = 0

            # restart เกม
            if event.key == pygame.K_RETURN and game_over:

                player.score = 0

                game_time = 5

                start_ticks = pygame.time.get_ticks()

                game_over = False

                game_win = False

    # =============================
    # START SCREEN
    # =============================

    if not game_started:

        screen.blit(bg, (0, -bg_offset))

        title = font.render("COVID19 WAR", True, (0, 255, 255))

        screen.blit(title, ((WIDTH - title.get_width()) / 2, HEIGHT / 2 - 100))

        start = font.render("PRESS SPACE TO START", True, (255, 255, 0))

        screen.blit(start, ((WIDTH - start.get_width()) / 2, HEIGHT / 2))

        pygame.display.flip()

        continue

    # =============================
    # TIMER
    # =============================

    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000

    seconds = game_time - elapsed

    if seconds <= 0:

        seconds = 0

        game_over = True

    # =============================
    # UPDATE GAME
    # =============================

    if not game_over and not game_win:

        allsprites.update()

    # =============================
    # COLLISION
    # =============================

    if not game_over:

        hits = pygame.sprite.groupcollide(covids, cures, True, True)

        for hit in hits:

            explosions.append(hit.rect.center)

            boom_sound.play()

            player.score += 1

            game_time += 2

            c = Covid()

            allsprites.add(c)

            covids.add(c)

            if player.score >= WIN_SCORE:

                game_win = True

                game_over = True

    # =============================
    # DRAW GAME
    # =============================

    screen.blit(bg, (0, -bg_offset))

    allsprites.draw(screen)

    # explosion effect

    for pos in explosions:

        pygame.draw.circle(screen, (255, 200, 0), pos, 40)

        pygame.draw.circle(screen, (255, 255, 255), pos, 20)

    if explosions:
        explosions.pop(0)

    # =============================
    # TIME BAR
    # =============================

    bar_width = 200

    time_ratio = seconds / game_time if game_time else 0

    current_width = bar_width * time_ratio

    if time_ratio > 0.6:
        bar_color = (0, 255, 255)

    elif time_ratio > 0.3:
        bar_color = (255, 255, 0)

    else:
        bar_color = (255, 0, 0)

    pygame.draw.rect(screen, (50, 50, 50), (10, 10, bar_width, 15))

    pygame.draw.rect(screen, bar_color, (10, 10, current_width, 15))

    # =============================
    # TEXT DISPLAY
    # =============================

    score_text = font.render("Score " + str(player.score), True, (0, 255, 255))

    screen.blit(score_text, ((WIDTH - score_text.get_width()) / 2, 10))

    timer_text = font.render("Time " + str(seconds), True, (255, 255, 0))

    screen.blit(timer_text, (WIDTH - 150, 10))

    # =============================
    # GAME OVER / WIN SCREEN
    # =============================

    if game_over and not game_win:

        text = font.render("GAME OVER", True, (255, 0, 0))

        screen.blit(text, ((WIDTH - text.get_width()) / 2, HEIGHT / 2))

    if game_win:

        text = font.render("YOU WIN!", True, (0, 255, 0))

        screen.blit(text, ((WIDTH - text.get_width()) / 2, HEIGHT / 2))

    pygame.display.flip()


pygame.quit()
