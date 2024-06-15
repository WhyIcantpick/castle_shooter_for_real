from operator import truediv
from turtle import update
from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі


mixer.init()
mixer.music.load('Precipice.mp3')
mixer.music.play()
fire_sound = mixer.Sound('bow.mp3')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
font3 = font.SysFont("Arial", 50)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "bg.png"
img_hero = "archer.png"
img_enemy = "orc.png"
img_superEnemy = "orcX.png"
img_non_killable_enemy = "cannonball.png"
img_health = "heart.png"
img_rangeEnemy = "orc_arch.png"
img_arrowEnemy = "arrow_evil.png"
img_super = "super_arrow.png"

score = 0
lost = 0
goal = 75
max_lost = 20
life = 5

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 450:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("arrow.png", self.rect.centerx - 5, self.rect.centery, 25, 10, -15)
        bullets.add(bullet)
    def fireX(self):
        bulletX = BulletX("super_arrow.png", self.rect.centerx - 5, self.rect.centery, 25, 10, -20)
        bulletsX.add(bulletX)

class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x == 0:
            self.rect.x = 600
            self.rect.y = randint (50, 450)
            lost +=1

class Cannonball(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (5, win_width - 80)
            self.rect.y = 0

class SuperEnemy(Enemy):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, max_hits):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.max_hits = max_hits
    def gotHit(self):
        self.max_hits -= 1
    def isKilled(self):
        if(self.max_hits <= 0):
            self.kill()
            return True
        else: return False

class Archer(Enemy):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, max_hits):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.max_hits = max_hits
        self.isReload  = False
        self.shoot_time = timer()
    def gotHit(self):
        self.max_hits -= 1
    def isKilled(self):
        if(self.max_hits <= 0):
            self.kill()
            return True
        else: return False
    def stand(self):
        self.speed = 0
    def shoot(self):
        arrow = Arrow("arrow_evil.png", self.rect.centerx - 5, self.rect.centery, 25, 10, 15)
        arrows.add(arrow)

class HealthPack(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 50)
            self.rect.y = 0 
    def apply(self):
        global life
        life += 2
        self.kill()

class Bullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # self.image = transform.rotate(self.image, 90)
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x >= 700:
            self.kill()

class BulletX(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # self.image = transform.rotate(self.image, 90)
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x >= 700:
            self.kill()

class Arrow(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # self.image = transform.rotate(self.image, 90)
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x <= 10:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 5, win_height - 100, 50, 60, 5)
hp1 = GameSprite(img_health, 650, 10, 30, 30, 0)
hp2 = GameSprite(img_health, 625, 10, 30, 30, 0)
hp3 = GameSprite(img_health, 600, 10, 30, 30, 0)
hp4 = GameSprite(img_health, 575, 10, 30, 30, 0)
hp5 = GameSprite(img_health, 550, 10, 30, 30, 0)



health_packs = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
cannonballs = sprite.Group()
superMonsters = sprite.Group()
archers = sprite.Group()
arrows = sprite.Group()
bulletsX = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, 600, randint(50, 450), 70, 70, randint(3, 5))
    monsters.add(monster)
for i in range(1, 6):
    cannonball = Cannonball(img_non_killable_enemy, randint(5, win_width - 50), -40, 50, 50, randint(3, 7))
    cannonballs.add(cannonball)
for i in range(1, 3):
    superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 80, randint(1, 3), 5)
    superMonsters.add(superMonster)
for i in range(1, 3):
    archer = Archer(img_rangeEnemy, 600, randint(50, 450), 70, 70, randint(1, 5), 2)
    archers.add(archer)

run = True
finish = False
clock = time.Clock()
FPS = 30
rel_time = False  # прапор, що відповідає за перезаряджання
num_fire = 0  # змінна для підрахунку пострілів    
rel_timex = False
num_firex = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire < 20 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                   
                if num_fire >= 20 and rel_time == False : #якщо гравець зробив 20 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки

            if e.key == K_LSHIFT:
                if num_firex < 20 and rel_timex == False:
                    num_firex += 1
                    fire_sound.play()
                    player.fireX()
                   
                if num_firex >= 2 and rel_timex == False : #якщо гравець зробив 20 пострілів
                    last_timex = timer() #засікаємо час, коли це сталося
                    rel_timex = True #ставимо прапор перезарядки


    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monsters.update()
        bullets.update()
        cannonballs.update()
        health_packs.update()
        superMonsters.update()
        archers.update()
        arrows.update()
        bulletsX.update()
        # hp1.update()
        # hp2.update()
        # hp3.update()
        # hp4.update()
        # hp5.update()
        
        
        health_packs.draw(window)
        player.reset()
        monsters.draw(window)
        superMonsters.draw(window)
        bullets.draw(window)
        cannonballs.draw(window)
        archers.draw(window)
        arrows.draw(window)
        bulletsX.draw(window)

        
        

        if life == 2 and len(health_packs) == 0:
            health_pack = HealthPack(img_health, randint(30, win_width - 450), -40, 30, 30, 3)
            health_packs.add(health_pack)

        if rel_time == True:
            now_time = timer() # зчитуємо час
            if now_time - last_time < 2: #поки не минуло 2 секунди виводимо інформацію про перезарядку
                reload = font3.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (win_width/2-100, win_height-150))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки

        if rel_timex == True:
            now_timeX = timer() # зчитуємо час
            if now_timeX - last_timex < 5: #поки не минуло 2 секунди  виводимо інформацію про перезарядку
                reload = font3.render('Wait, reload...', 1, (250, 250, 0))
                window.blit(reload, (win_width/2-100, win_height-100))
            else:
                num_firex = 0     #обнулюємо лічильник куль
                rel_timex = False #скидаємо прапор перезарядки


        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        collidesx = sprite.groupcollide(monsters, bulletsX, True, False)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, 600, randint(50, 450), 70, 70, randint(1, 3))
            monsters.add(monster)

        for collidex in collidesx:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, 600, randint(50, 450), 70, 70, randint(1, 3))
            monsters.add(monster)

        for superMonster in superMonsters:
            if sprite.spritecollide(superMonster, bullets, True):
                superMonster.gotHit()
                if superMonster.isKilled():
                    score = score + 1
                    superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 80, randint(1, 3), 5)
                    superMonsters.add(superMonster)
            if sprite.spritecollide(superMonster, bulletsX, False):
                superMonster.kill()
                score = score + 1
                superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 80, randint(1, 3), 5)
                superMonsters.add(superMonster)


        for archer in archers:
            if sprite.spritecollide(archer, bullets, True):
                archer.gotHit()
                if archer.isKilled():
                    score = score + 1
                    archer = Archer(img_rangeEnemy, 600, randint(50, 450), 70, 70, randint(1, 5), 2)
                    archers.add(archer)
            if sprite.spritecollide(archer, bulletsX, False):
                archer.kill()
                score = score + 1
                archer = Archer(img_rangeEnemy, 600, randint(50, 450), 70, 70, randint(1, 5), 2)
                archers.add(archer)
            if archer.rect.x <= 500:
                archer.stand()
                tg = timer()
                if archer.isReload == False:
                    archer.shoot()
                    archer.shoot_time = timer()
                    archer.isReload = True
                if archer.shoot_time + 1 < tg:
                    archer.isReload = False
                    



        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, cannonballs, False) or sprite.spritecollide(player, superMonsters, False) or sprite.spritecollide(player, archers, False) or sprite.spritecollide(player, arrows, False):
            life = life - 1
            if sprite.spritecollide(player, monsters, True):
                monster = Enemy(img_enemy, 600, randint(50, 450), 70, 70, randint(1, 3))
                monsters.add(monster)
            if sprite.spritecollide(player, cannonballs, True):  
                cannonball = Cannonball(img_non_killable_enemy, randint(5, win_width - 50), -40, 50, 50, randint(1, 7))
                cannonballs.add(cannonball)
            if sprite.spritecollide(player, superMonsters, True):
                superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 80, randint(1, 3), 5)
                superMonsters.add(superMonster)
            if sprite.spritecollide(player, archers, True):
                archer = Archer(img_rangeEnemy, 600, randint(50, 450), 70, 70, randint(1, 5), 2)
                archers.add(archer)
            if sprite.spritecollide(player, arrows, True):
                arrow = Arrow(img_arrowEnemy, archer.rect.centerx - 5, archer.rect.centery, 25, 10, 15)
                arrows.add(arrow)
            

        if sprite.spritecollide(player, health_packs, True):
            health_pack.apply()


        #програш
        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))
        if life > 0:
            hp1.reset()
        if life > 1:
            hp2.reset()
        if life > 2:
            hp3.reset()
        if life > 3:
            hp4.reset()
        if life > 4:
            hp5.reset()

        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font1.render("Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        # text_life = font1.render(str(life), 1, (250, 250, 250))
        #window.blit(text_life, (650, 10))
        display.update()

    clock.tick(FPS)