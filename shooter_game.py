from pygame import *
from random import randint

score = 0
lost = 0

font.init()
velkost_fontu = 36
velkost_fontu_vacsia = 142
our_font = font.SysFont('Arial', velkost_fontu)
bigger_font = font.SysFont('Arial', velkost_fontu_vacsia)

lose = bigger_font.render("YOU LOSE" , 1, (230, 150, 150))
win = bigger_font.render("YOU WIN" , 1, (150, 230, 150))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Space invaders z temu")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))


mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__() # naimportuje premenne z triedy Sprite
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -25)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            lost += 1
            self.rect.x = randint(5, win_width - 100)
            self.rect.y = 5


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

enemies = sprite.Group()
for i in range(5):
    a = randint(5, win_width - 100)
    b = 5
    enemy = Enemy("ufo.png", a, b, 80, 50, randint(2, 6))
    enemies.add(enemy)


game = True
finish = False
clock = time.Clock()
fps = 24

ship = Player("rocket.png", win_width/2 - 40, 350, 80, 100, 15)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False


        elif e.type == MOUSEBUTTONDOWN:
            ship.fire()
                


    if not finish:
        window.blit(background,(0, 0))

        if score >= 25:
            finish = True
            window.blit(win, (win_width/(velkost_fontu_vacsia / 20), win_height/(velkost_fontu_vacsia / 45)))
        
        score_text = our_font.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(score_text, (10, 10))


        lost_text = our_font.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(lost_text, (10, 50))

        collides = sprite.groupcollide(enemies, bullets, True, True)

        for alien in collides:
            score += 1
            enemy = Enemy("ufo.png", randint(5, win_width - 100), 5, 80, 50, randint(2, 6))
            enemies.add(enemy)
            
        if sprite.spritecollide(ship, enemies, True) or lost >= 3:
            window.blit(lose, (win_width/(velkost_fontu_vacsia / 13), win_height/(velkost_fontu_vacsia / 45)))
            finish = True


        ship.update()
        enemies.update()
        bullets.update()


        ship.reset()
        enemies.draw(window)
        bullets.draw(window)

        

        display.update()

    else:
        #reset
        for enemy in enemies:
            enemy.kill()

        for bullet in bullets:
            bullet.kill()
        
        


        time.delay(1000)
        score = 0
        lost = 0
        

        for i in range(5):
            a = randint(5, win_width - 100)
            b = 5
            enemy = Enemy("ufo.png", a, b, 80, 50, randint(2, 6))
            enemies.add(enemy)
        ship = Player("rocket.png", win_width/2 - 40, 350, 80, 100, 15)
        ship.reset()

        finish = False
        

    clock.tick(fps)

