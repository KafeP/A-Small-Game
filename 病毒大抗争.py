import sys, random, pygame
from pygame.locals import *
import os

def print_text(font, x, y, text, color=(0, 0, 255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()  # req'd when function moved into MyLibrary
    screen.blit(imgText, (x, y))


class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0, 0.0)

    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)

    def load(self, filename):
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getx(self): return self.__x

    def setx(self, x): self.__x = x

    x = property(getx, setx)

    def gety(self): return self.__y

    def sety(self, y): self.__y = y

    y = property(gety, sety)
    
def calc_velocity(direction, vel=3):
    velocity = Point(0, 0)
    if direction == 0:
        velocity.y = -vel
    elif direction == 2:
        velocity.x = vel
    elif direction == 4:
        velocity.y = vel
    elif direction == 6:
        velocity.x = -vel
    return velocity


def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2


pygame.init()
# 添加背景音乐
pygame.mixer.init()
Cricket = pygame.mixer.Sound("fight_looped.wav")
Cricket.play(loops=0)

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((1300, 777))
pygame.display.set_caption("躲避新冠病毒")
font = pygame.font.Font(None, 57)
timer = pygame.time.Clock()

# 封面
fengmian = pygame.image.load("游戏封面.png")
fengmian = pygame.transform.scale(fengmian, (1300, 777))
screen.blit(fengmian, (0, 0))
pygame.display.update()
status = True
while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            status = False
            break
        elif event.type == pygame.KEYDOWN:
            status = False
            break

virus = ['病毒1.png', '病毒2.png', '病毒3.png', '病毒4.png', '病毒5.png', '病毒6.png', '病毒7.png', '病毒8.png']
virus_defense = ['洗手.png', '通风.png', '口罩.png']
max_x = 1300 - 500
max_y = 777 - 500

player_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

player = MySprite()
player.load("玩家.png")
player.position = 77, 77
player.direction = 4
player_group.add(player)

for n in range(len(virus)):
    zombie = MySprite()
    zombie.load(virus[n])
    zombie.position = random.randint(0, max_x + 300), random.randint(0, max_y + 300)
    zombie.direction = random.randint(0, 3) * 2
    zombie_group.add(zombie)

for n in range(len(virus_defense)):
    health = MySprite()
    health.load(virus_defense[n])
    health.position = random.randint(0, max_x + 300), random.randint(0, max_y + 300)
    health_group.add(health)

game_over = False
player_moving = False
player_health = 100
background = pygame.image.load("背景.png")
background = pygame.transform.scale(background, (1300, 777))
# repeating loop
while True:

    timer.tick(30)
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_UP] or keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False

    if not game_over:
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns - 1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        if not player_moving:
            player.frame = player.first_frame = player.last_frame
        else:
            player.velocity = calc_velocity(player.direction, 6)
            player.velocity.x *= 4
            player.velocity.y *= 4

        player_group.update(ticks, 50)

        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0:
                player.X = 0
            elif player.X > max_x + 500 - 200:
                player.X = max_x + 500 - 200
            if player.Y < 0:
                player.Y = 0
            elif player.Y > max_y + 500 - 160:
                player.Y = max_y + 500 - 160

        zombie_group.update(ticks, 50)

        for z in zombie_group:
            z.first_frame = z.direction * z.columns
            z.last_frame = z.first_frame + z.columns - 1
            if z.frame < z.first_frame:
                z.frame = z.first_frame
            z.velocity = calc_velocity(z.direction, 6)

            z.X += z.velocity.x
            z.Y += z.velocity.y
            if z.X < 0 or z.X > max_x + 300 or z.Y < 0 or z.Y > max_y + 300:
                reverse_direction(z)

        attacker = pygame.sprite.spritecollideany(player, zombie_group)
        if attacker is not None:
            if pygame.sprite.collide_rect_ratio(0.5)(player, attacker):
                # 减血撞击的声音
                Cricket = pygame.mixer.Sound("Boss Battle.wav")
                Cricket.play(loops=1, maxtime=5)
                if player_health < 0:
                    player_health = 0
                player_health -= 10
                if attacker.X < player.X:
                    attacker.X -= 10
                elif attacker.X > player.X:
                    attacker.X += 10
            else:
                attacker = None

        health_group.update(ticks, 50)
        for h in health_group:
            if pygame.sprite.collide_rect_ratio(0.5)(player, h):
                # 加血撞击的声音
                Cricket = pygame.mixer.Sound("Boss Battle.wav")
                Cricket.play(loops=1, maxtime=5)
                player_health += 30
                if player_health > 100:
                    player_health = 100
                h.X = random.randint(0, max_x)
                h.Y = random.randint(0, max_y)

    if player_health <= 0:
        game_over = True

    screen.fill((255, 255, 255))
    # 背景
    screen.blit(background, (0, 0))

    health_group.draw(screen)
    zombie_group.draw(screen)
    player_group.draw(screen)
    pygame.draw.rect(screen, (50, 150, 50, 180), Rect(550, 657, player_health * 2, 25))
    pygame.draw.rect(screen, (100, 200, 100, 180), Rect(550, 657, 200, 25), 2)

    if game_over:
        print_text(font, 500, 100, "G A M E   O V E R")
    pygame.display.update()
