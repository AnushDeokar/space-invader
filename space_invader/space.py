import pygame
# import threading
# from timer import Timer
# t = Timer()
# t.start()
pygame.init()
BLACK_ENEMY = pygame.image.load("black.png")
RED_ENEMY = pygame.image.load("red.png")
BLACK_ENEMY = pygame.transform.scale(BLACK_ENEMY, (30, 30))
RED_ENEMY = pygame.transform.scale(RED_ENEMY, (30, 30))
SPACESHIP = pygame.image.load("spaceship.png")
SPACESHIP = pygame.transform.scale(SPACESHIP, (60, 60))
WIDTH = 700
HEIGHT = 550
class spaceship():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5
        self.life = 20

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        elif keys[pygame.K_DOWN] and self.y < HEIGHT - SPACESHIP.get_height():
            self.y += self.vel
        elif keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        elif keys[pygame.K_RIGHT] and self.x < WIDTH - SPACESHIP.get_width():
            self.x += self.vel

    def draw(self, win):
        win.blit(SPACESHIP, (self.x, self.y))
        pygame.display.update()
enemies = []
class bullets():

    def __init__(self, x, y, color, dirn):
        self.x = x
        self.y = y
        self.color = color
        self.dirn = dirn
        self.vel = 5
        self.acc = 1
    def draw(self, win):
        pygame.draw.line(win, self.color, (self.x, self.y), (self.x, self.y + 10))

    def move(self):
        self.y += self.vel*(self.dirn)

class enemy():

    def __init__(self, cornx,  corny):
        self.cornx = cornx
        self.corny = corny
        self.z = cornx
        self.vel = 5
        self.life = 10
        self.bullet = 0


    def draw(self, win):
        win.blit(RED_ENEMY, (self.cornx, self.corny))

    def move(self):
        self.cornx += self.vel
        if self.cornx == self.z + 170:
            self.vel = self.vel*(-1)
        elif self.cornx == self.z:
            self.vel = self.vel * (-1)

    def collision(self, b):
        if RED_ENEMY.get_width() + self.cornx >= b.x >= self.cornx and RED_ENEMY.get_height() + self.corny >= b.y >= self.corny:
            print("Hello")
            return True
        return False

def redraw_window(win):
    global ship, enemies, spaceship_bullet, score
    win.fill((0, 0, 0))
    ship.draw(win)
    font1 = pygame.font.SysFont("comicsans", 50)
    text = font1.render("Health:" + str(ship.life), 5, (0, 255, 0))
    scores = font1.render("Score:" + str(score), 5, (0, 255, 0))
    win.blit(text, (5, HEIGHT - text.get_height() -10))
    win.blit(scores, (WIDTH - text.get_width() - 10, HEIGHT - text.get_height() - 10))

    for enemy in enemies:
        enemy.draw(win)
    for b in spaceship_bullet:
        b.draw(win)
    for b in enemy_bullet:
        b.draw(win)
    pygame.display.update()

def main():
    global ship, enemies, spaceship_bullet, enemy_bullet, score
    score = 0
    clock = pygame.time.Clock()
    spaceship_bullet = []
    enemy_bullet =[]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invader")
    x, z = 20, 20
    for i in range(10):
        enemies.append(enemy(x, 30))
        x += 50
    for i in range(10):
        enemies.append(enemy(z, 90))
        z += 50
    ship = spaceship(650, 400)
    run = True
    while run:
        start_ticks = pygame.time.get_ticks()
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ship.life == 0 :
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spaceship_bullet.append(bullets(ship.x + SPACESHIP.get_width() / 2, ship.y, (255, 255, 255), -1))

        for b in spaceship_bullet:
            b.move()
        ship.move()
        for b in spaceship_bullet:
            for i, ene in enumerate(enemies):
                if ene.collision(b):
                    print("collision", i)
                    ene.life -= 1
                    spaceship_bullet.remove(b)
                if ene.life == 0:
                    enemies.pop(i)
                    score += 1
        for i, e in enumerate(enemies):
            e.move()
            if start_ticks%(10*(i + 1)) == 0:
                enemy_bullet.append(bullets(e.cornx + RED_ENEMY.get_width()/2, e.corny + RED_ENEMY.get_height(), (0, 0, 255), 1))
        for b in enemy_bullet:
            b.move()
            if ship.x + SPACESHIP.get_width()>= b.x >= ship.x and ship.y == b.y:
                ship.life -= 1
                enemy_bullet.remove(b)
        redraw_window(win)

main()