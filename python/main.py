import pygame
import random
pygame.font.init()

W,H=750,750
window=pygame.display.set_mode((W,H))
pygame.display.set_caption('OWASP Stops Aliens')

Enemy1=pygame.transform.scale(pygame.image.load("python/characters/PngItem_490764.png"),(90,90))
Enemy2=pygame.transform.scale(pygame.image.load("python/characters/PngItem_851324.png"),(45,90))
Enemy3=pygame.transform.scale(pygame.image.load("python/characters/pngwing.com.png"),(90,90))


Player=pygame.image.load("python/characters/Player.png")

#Lasers
red = pygame.image.load("python/characters/pixel_laser_red.png")
green = pygame.image.load("python/characters/pixel_laser_green.png")
blue = pygame.image.load("python/characters/pixel_laser_blue.png")
yellow = pygame.image.load("python/characters/pixel_laser_yellow.png")

bg=pygame.transform.scale(pygame.image.load("python/characters/background.jpeg"),(W,H))

class Laser:
    def __init__(self, x, y, img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y+=vel

    def off_screen(self,height):
        return self.y<=height and self.y>=0
    
    #def collision(self, obj):
        #return collide(self, obj)
    
class Ship:
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.shipImg=Enemy1
        self.laserImg=None
        self.lasers = []
        self.stopShooting = 0
    def draw(self,window):
        window.blit(self.shipImg,(self.x,self.y))
        # pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50))

    def width(self):
        return self.shipImg.get_width()
    def height(self):
        return self.shipImg.get_height()
class owaspTiet(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.shipImg = Player
        self.laserImg = yellow
        self.mask = pygame.mask.from_surface(self.shipImg)
        self.maxHealth=health

class Enemy(Ship):
    shipMap={
            "red": (Enemy1,red),
            "green": (Enemy2,green),
            "blue": (Enemy3,blue)
            }
    def _init_(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.shipImg,self.laserImg=self.shipMap[color]
        self.mask=pygame.mask.from_surface(self.shipImg)

    def move(self,velocity):
        self.y+=velocity

def main():
    run=True
    FPS=60
    level = 0
    lives=5
    velocity=4
    fonti=pygame.font.SysFont('stencil',40)
    lost_font = pygame.font.SysFont("stencil", 60)
    enemies=[]
    wave_length=5
    enemyVel=1
    player=owaspTiet(300,650)
    clk=pygame.time.Clock()
    lost=False
    lost_count=0

    def window_update():
            window.blit(bg, (0, 0))
            livesCount=fonti.render(f"Lives: {lives}",1,(255,255,255))
            levelCount=fonti.render(f"Levels: {level}",1,(255,255,255))
            window.blit(livesCount,(10,10))
            window.blit(levelCount,(W-levelCount.get_width()-10,10))
            for enemy in enemies:
                enemy.draw(window)
            player.draw(window)
            if lost:
                lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
                window.blit(lost_label, (W/2 - lost_label.get_width()/2, 350))
            pygame.display.update()

    while run:
        clk.tick(FPS)
        window_update()
        if lives<= 0 or player.health <= 0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count>FPS*3:
                run = False
            else:
                continue
        if len(enemies)==0:
            level+=1
            wave_length+=1
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,W-100),random.randrange(-400,-100),random.choice(["red","blue","green"]))

                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x-velocity>0:
            player.x-=velocity #Left-a
        if keys[pygame.K_LEFT] and player.x-velocity>0:
            player.x-=velocity #Left-left arrow
        if keys[pygame.K_d] and player.x +velocity<W-player.width():
            player.x+=velocity #Right-d
        if keys[pygame.K_RIGHT] and player.x +velocity<W-player.width():
            player.x+=velocity #Right-right arrow
        if keys[pygame.K_w] and player.y-velocity>0:
            player.y-=velocity #Up-w
        if keys[pygame.K_UP] and player.y-velocity>0:
            player.y-=velocity #Up-up arrow
        if keys[pygame.K_s] and player.y+velocity<H-player.height():
            player.y+=velocity #Down-s
        if keys[pygame.K_DOWN] and player.y+velocity<H-player.height():
            player.y+=velocity #Down-down arrow

        for enemy in enemies[:]:
            enemy.move(enemyVel)
            if enemy.y + enemy.height()>H:
                lives-=1
                enemies.remove(enemy)

        window_update()

main()