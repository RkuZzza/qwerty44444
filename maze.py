#создай игру "Лабиринт"!
from pygame import *
font.init()
font = font.Font(None, 70)

win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")
background = image.load("background.jpg")
background = transform.scale(background, (win_width, win_height))
window.blit(background, (0,0))

clock = time.Clock()
FPS = 50

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
	
    # Метод перерисовки персонажа
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x < win_width - 350:
            self.direction = "right"
        if self.rect.x > win_width - 85:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1,color_2, color_3, wall_x, wall_y, wall_width,wall_height):
        super().__init__()
        self.color_1 = color_1 #color_2 и color_3 аналогично   
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Player("hero.png", 50, 50, 10)
enemy = Enemy("cyborg.png", 800, 400, 8)
goal = GameSprite("treasure.png", 780, 620, 0)
wall_1 = Wall(255,255,0, 150, 5, 10, 520)
wall_2 = Wall(255,255,0, 300, 180, 10, 510)
wall_3 = Wall(255,255,0, 500, 5, 10, 340)
wall_4 = Wall(255,255,0, 450, 340, 100, 10)
wall_5 = Wall(255,255,0, 450, 500, 100, 10)
wall_6 = Wall(255,255,0, 500, 500, 10, 190)

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0,0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        wall_6.draw_wall()
        
        player.update()
        enemy.update()
        player.reset()
        enemy.reset()
        goal.reset()

        if sprite.collide_rect(player, goal):
            
            win = font.render("ПОБЕДА", True, (255,215,0))
            window.blit(win, (250,250))
            finish = True
            # Можго запустить звук монет

        if sprite.collide_rect(player, enemy):
            lose = font.render("ПОРАЖЕНИЕ", True, (255,215,0))
            window.blit(lose, (250,250))
            finish = True

        if sprite.collide_rect(player, wall_1) or sprite.collide_rect(player, wall_2) or sprite.collide_rect(player, wall_3) or sprite.collide_rect(player, wall_4) or sprite.collide_rect(player, wall_5) or sprite.collide_rect(player, wall_6):
            player.rect.x = 50
            player.rect.y = 50


    display.update()
    clock.tick(FPS)
