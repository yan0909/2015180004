from pico2d import *
import random
import main_state

class Normal_Enemy:            # Normal_Enemy 로 바꾸기
    image = None
    die_image = None
    alive_image = None
    def __init__(self):
        self.x, self.y = 0,random.randint(146, 197)
        self.first_y = self.y
        self.last_y = None
        self.width = 50
        self.height = 75
        self.speed = random.randint(1,2) / 2
        if(Normal_Enemy.image == None):
            self.image = load_image('resource/enemy01_animation.png')
        if(Normal_Enemy.die_image == None):
            self.die_image = load_image('resource/enemy01_die.png')
        if(Normal_Enemy.alive_image == None):
            self.alive_image = load_image('resource/enemy01_alive.png')
        self.state = 0
        self.frame = 0
        self.die_frame = 0
        self.alive_frame = 0
        self.f_speed = 0
        self.isHit = False # 이 적이 성을 때렸는지 안때렸는지.
    def update(self):
        if(self.state == 0 or self.state == 1):
            self.x += self.speed
            if(self.y >= 146 and self.y < 160 and self.x >= 436):
                self.x = 436
                self.state = 1
            if(self.y >= 160 and self.y <= 178 and self.x >= 420):
                self.x = 420
                self.state = 1
            if(self.y > 178 and self.y <= 197 and self.x >= 404):
                self.x = 404
                self.state = 1
            if(self.state == 1 and self.frame == 0):
                self.isHit = True

        elif(self.state == 3):
            self.f_speed += 0.3
            self.y -= self.f_speed
            if(self.y <= self.first_y):
                self.y = self.first_y
                if(self.last_y >= 450):
                    self.state = 4
                else:
                    self.state = 5
                    self.alive_frame = 0
        elif(self.state == 4):
            if(self.die_frame < 6 * 12):
                self.die_frame += 1
        elif(self.state == 5):
            if(self.alive_frame >= 30):
                self.state = 0
            self.alive_frame += 1

        self.frame = (self.frame + 1) % (4 * 10)

    def draw(self):
        if(self.state == 0 or self.state == 2 or self.state == 3):
            self.image.clip_draw(math.floor(self.frame / 10) % 4 * 50, 75, 50, 75, self.x, self.y)
        elif(self.state == 1):
            self.image.clip_draw(math.floor(self.frame / 10) % 4 * 50, 0, 50, 75, self.x, self.y)
        elif(self.state == 4 and self.die_frame < 6 * 12):
            self.die_image.clip_draw(math.floor(self.die_frame / 12) * 70, 0 ,70, 100, self.x, self.y)
        elif(self.state == 5):
            self.alive_image.clip_draw(math.floor(self.alive_frame / 10) * 70, 0, 70, 60, self.x, self.y)
        #print(self.state, self.frame, self.frame % 4, self.frame % 5, self.x, self.y)
    pass

class Enemy02(Normal_Enemy):
    def __init__(self):
        Normal_Enemy.__init__()
        self.x, self.y = 0,random.randint(146, 197)
        self.first_y = self.y
        self.last_y = None
        self.width = 75
        self.height = 75
        self.speed = random.randint(1,2) / 2
        if(Normal_Enemy.image == None):
            self.image = load_image('resource/enemy02_animation.png')
        if(Normal_Enemy.die_image == None):
            self.die_image = load_image('resource/enemy01_die.png')
        if(Normal_Enemy.alive_image == None):
            self.alive_image = load_image('resource/enemy02_alive.png')
        self.state = 0
        self.frame = 0
        self.die_frame = 0
        self.alive_frame = 0
        self.f_speed = 0
        self.isHit = False
    def draw(self):
        if(self.state == 0 or self.state == 2 or self.state == 3):
            self.image.clip_draw(math.floor(self.frame / 10) % 4 * 80, 75, 80, 75, self.x, self.y)
        elif(self.state == 1):
            self.image.clip_draw(math.floor(self.frame / 10) % 4 * 80, 0, 80, 75, self.x, self.y)
        elif(self.state == 4 and self.die_frame < 6 * 12):
            self.die_image.clip_draw(math.floor(self.die_frame / 12) * 70, 0 ,70, 100, self.x, self.y)
        elif(self.state == 5):
            self.alive_image.clip_draw(math.floor(self.alive_frame / 10) * 70, 0, 70, 60, self.x, self.y)
        #print(self.state, self.frame, self.frame % 4, self.frame % 5, self.x, self.y)
    pass

class Giant_Enemy(Normal_Enemy):
    def __init__(self):
        self.x, self.y = 0, random.randint(146, 197)
        self.first_y = self.y
        self.last_y = None
        self.width = 75
        self.height = 75
        self.speed = random.randint(1, 2) / 2
        if (Normal_Enemy.image == None):
            self.image = load_image('resource/enemy03_animation.png')
        if (Normal_Enemy.die_image == None):
            self.die_image = load_image('resource/enemy01_die.png')
        if (Normal_Enemy.alive_image == None):
            self.alive_image = load_image('resource/enemy03_alive.png')
        self.state = 0
        self.frame = 0
        self.die_frame = 0
        self.alive_frame = 0
        self.f_speed = 0
        self.isHit = False

    def draw(self):
        if (self.state == 0 or self.state == 2 or self.state == 3):
            self.image.clip_draw(math.floor(self.frame / 10) % 4 * 80, 75, 80, 75, self.x, self.y)
        elif (self.state == 1):
            self.image.clip_draw(math.floor(self.frame / 10) % 4 * 80, 0, 80, 75, self.x, self.y)
        elif (self.state == 4 and self.die_frame < 6 * 12):
            self.die_image.clip_draw(math.floor(self.die_frame / 12) * 70, 0, 70, 100, self.x, self.y)
        elif (self.state == 5):
            self.alive_image.clip_draw(math.floor(self.alive_frame / 10) * 70, 0, 70, 60, self.x, self.y)
            # print(self.state, self.frame, self.frame % 4, self.frame % 5, self.x, self.y)

    pass