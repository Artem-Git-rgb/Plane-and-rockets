import pygame
import random
import time
from pygame.locals import (  # назначаю клавиши
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)


def draw_text(text, font, color, x, y):
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('jet.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.up_image = pygame.transform.rotate(self.image, 20)
        self.down_image = pygame.transform.rotate(self.image, -20)
        self.standard_image = pygame.image.load('jet.png').convert()
        self.standard_image.set_colorkey((255, 255, 255))
        self.vertical = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 200

    def attack(self):  # атака пулями
        now = pygame.time.get_ticks()
        cord_x = 35
        cord_y = 10
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            new_bullet = Bullet(self.rect.x + cord_x, self.rect.y + cord_y)  # (!!!)
            all_sprites.add(new_bullet)
            bullets.add(new_bullet)

    def update(self):  # движение
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.vertical = 1
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.vertical = -1
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            self.attack()
        if not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
            self.vertical = 0
        match self.vertical:
            case 1:
                self.image = self.up_image
            case -1:
                self.image = self.down_image
            case 0:
                self.image = self.standard_image
            case _:
                self.image = self.standard_image
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.vertical == 1:
            if self.rect.top < -10:
                self.rect.top = -10
        else:
            if self.rect.top < 0:
                self.rect.top = 0

        if self.vertical == -1:
            if self.rect.bottom > SCREEN_HEIGHT - 10:
                self.rect.bottom = SCREEN_HEIGHT - 10
        else:
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):  # класс пули
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('big_bullet.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (21, 7))  # (!!!)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5  # скорость пули

    def update(self):  # исчезновение
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):  # класс врага
    velocity = 1

    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('missile.png').convert()
        self.image = pygame.transform.scale(self.image, (38, 15))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        if Enemy.velocity > 2:
            Enemy.velocity = 2
        self.speed = random.randint(3, 6) * Enemy.velocity  # (!!!)

    def update(self):  # исчезновение
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            Enemy.velocity += 0.02  # ускорение спавна врагов (!!!)
            self.kill()


class Cloud(pygame.sprite.Sprite):  # класс облаков
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('cloud.png').convert()
        self.image = pygame.transform.scale(self.image, (170, 120))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(90, 130)

    def update(self):  # исчезновение
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):  # класс взрыва
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = arr_images[size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center  # ?
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.size = size

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(arr_images[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = arr_images[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800  # ширина
SCREEN_HEIGHT = 600  # высота
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 600)  # таймер для спавна врага (!!!)
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1500)  # таймер для спавна облака (!)
ADD_BULLET = pygame.USEREVENT + 2
player = Player()
# группы
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# музыка
pygame.mixer.music.load('Apoxode_-_Electric.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(loops=-1)
collision_sound = pygame.mixer.Sound('Collision.ogg')
move_up_sound = pygame.mixer.Sound('Rising_putter.ogg')
move_up_sound.set_volume(0.01)  # громкость звука вверх
move_down_sound = pygame.mixer.Sound('Falling_putter.ogg')
move_down_sound.set_volume(0.01)  # громкость звука вниз
# анимация
arr_images = {}  # цикл загрузки картинок взрыва
arr_images['large'] = []
arr_images['small'] = []
for img in range(1, 6):
    img = pygame.image.load(str(img) + '.png').convert()
    img.set_colorkey((255, 255, 255))
    img_large = pygame.transform.scale(img, (90, 90))
    arr_images['large'].append(img_large)
    img_small = pygame.transform.scale(img, (50, 50))
    arr_images['small'].append(img_small)
# счётчик
timer = pygame.font.Font(None, 36)
time_score = 1
enemy_score = 0
is_game_over = False
# цикл игры
running = True
while running:  # цикл игры
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADD_ENEMY:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()
            all_sprites.add(new_cloud)
            clouds.add(new_cloud)

    # удаление
    all_sprites.update()
    # экран
    screen_image = pygame.image.load('skyLD.png').convert()
    screen_image = pygame.transform.scale(screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(screen_image, (0, 0))
    # screen.fill((0, 127, 255))
    # остальное
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:  # сбитие ракеты
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
        enemy_score += 1
        expl = Explosion(hit.rect.center, 'small')  # взрыв
        all_sprites.add(expl)
    if is_game_over:
        draw_text('GAME OVER', timer, (255, 0, 0), SCREEN_WIDTH / 2 - 85, SCREEN_HEIGHT / 2 - 55)
        draw_text('время: ' + str(time_score // 90) + ' сек.', timer, (0, 0, 0), SCREEN_WIDTH - 485,
                  SCREEN_HEIGHT - 325)
        draw_text('сбито врагов: ' + str(enemy_score), timer, (0, 0, 0), SCREEN_WIDTH - 495, SCREEN_HEIGHT - 295)
    # счётчики
    else:
        if pygame.sprite.spritecollideany(player, enemies):  # столкновение игрока с врагом
            is_game_over = True
            player.kill()  # убираем игрока
            move_down_sound.stop()
            move_up_sound.stop()
            expl = Explosion(player.rect.center, 'large')  # взрыв
            all_sprites.add(expl)
            collision_sound.set_volume(0.5)  # громкость звука взрыва
            collision_sound.play()
        time_score += 1  # счёт времени
        text_time = timer.render('время: ' + str(time_score // 90) + ' сек.', True, (255, 255, 255))  #
        text_enemy = timer.render('сбито врагов: ' + str(enemy_score), True, (255, 255, 255))  #
        screen.blit(text_time, (SCREEN_WIDTH - 165, SCREEN_HEIGHT - 40))
        screen.blit(text_enemy, (SCREEN_WIDTH - 780, SCREEN_HEIGHT - 40))
    pygame.display.flip()
    clock.tick(90)  # кадры в секунду
# за циклом
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
