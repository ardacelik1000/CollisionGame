import pygame

pygame.init()
Screen = pygame.display.set_mode((720, 850))
running = True
clock = pygame.time.Clock()
dt = 0
EnemyVisible = True 
font = pygame.font.Font(None, 36)


class Enemy(): 
    def __init__(self): 
        self.EnemyPos = pygame.Vector2(Screen.get_width() / 2, Screen.get_height() / 2 -200)
        self.EnemyVelocity = 6
        
    def EnemyMove(self):
        self.EnemyPos.x += self.EnemyVelocity
        if self.EnemyPos.x <= 0 or  self.EnemyPos.x >= 720 - 35:
            self.EnemyVelocity *= -1 
        
        if EnemyVisible: 
            self.rect2 = pygame.draw.rect(Screen,"blue",(self.EnemyPos.x,self.EnemyPos.y,35,35))
        
     

class HealthBar(): 
    def __init__(self,x,y,w,h,max_hp):
        self.HeartImage =  pygame.image.load("C:\\Users\\Arda\\Desktop\\PlaneGameIFiles\\heart.png")
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h 
        self.hp = max_hp #initial hp - full hp 
        self.max_hp = max_hp

    def Calculation(self): 
        ratio = self.hp / self.max_hp 
        Screen.blit(self.HeartImage,(self.x-55,self.y-6))
        pygame.draw.rect(Screen,"red",(self.x,self.y+0,self.w,self.h))
        pygame.draw.rect(Screen,"green",(self.x,self.y,self.w*ratio,self.h))

class Player(): 
    def __init__(self):
        self.PlayerPos = pygame.Vector2(Screen.get_width() / 2, Screen.get_height() / 2 + 350)

    def Move(self): 
        MoveKeys = pygame.key.get_pressed()
        if MoveKeys[pygame.K_LEFT] and self.PlayerPos.x > 35 :
            self.PlayerPos.x -= 350 * dt
        if MoveKeys[pygame.K_RIGHT] and self.PlayerPos.x < 720 -35: 
            self.PlayerPos.x += 350 * dt
        if MoveKeys[pygame.K_DOWN] and self.PlayerPos.y < 850-36:
            self.PlayerPos.y += 350 * dt
        if MoveKeys[pygame.K_UP] and self.PlayerPos.y > 35: 
            self.PlayerPos.y -= 350 * dt


        pygame.draw.circle(Screen, "red", self.PlayerPos,30,30)

class Bullet(): 
    def __init__(self): 
        self.BulletX = player.PlayerPos.x
        self.BulletY = player.PlayerPos.y
        self.BulletY_change = 10  

    def BulletMove(self,x,y): 
        self.BulletY -= self.BulletY_change  
        self.rect1 = pygame.draw.circle(Screen,"green",(x,y),10,10)


player = Player()
healthbar = HealthBar(100,20,100,20,100)
enemy =Enemy()
bullets = []
bullet = Bullet()

RestartGame = False
GameStarted = False 

def restart_game():
    global healthbar, enemy, bullets, EnemyVisible
    healthbar.hp = healthbar.max_hp
    enemy = Enemy()
    bullets = []
    EnemyVisible = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Bullet()) 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            RestartGame = True
        if not GameStarted and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            GameStarted = True
                
    Screen.fill("black")
    if not GameStarted:
        start_text = font.render("Press Enter to Start", True, 'white')
        start_text_rect = start_text.get_rect(center=(Screen.get_width() // 2, Screen.get_height() // 2))
        Screen.blit(start_text, start_text_rect)
        
    if RestartGame:
        restart_game()
        RestartGame = False
    
    if GameStarted: 
        for bullet in bullets: 
            bullet.BulletMove(bullet.BulletX,bullet.BulletY)
            if bullet.rect1.colliderect(enemy.rect2):
                healthbar.hp -= 20
                bullets.remove(bullet)
            if bullet.BulletY < 40: 
                bullets.remove(bullet)


        if healthbar.hp == 0: 
            EnemyVisible = False    
            text = font.render("You Win!", True, 'white')
            text_rect = text.get_rect(center=(Screen.get_width() // 2, Screen.get_height() // 2))
            Screen.blit(text, text_rect)
            restart_text = font.render("Press ESC to Play Again", True,'white')
            restart_text_rect = restart_text.get_rect(center=(Screen.get_width() // 2, Screen.get_height()// 2 + 50))
            Screen.blit(restart_text, restart_text_rect)


        healthbar.Calculation()
        player.Move()
        enemy.EnemyMove()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()