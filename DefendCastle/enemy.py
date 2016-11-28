from pico2d import *
import random
import main_state

class Enemy_Base:
    running_image = None
    attacking_image = None
    dying_image = None
    getting_up_image = None

    def __init__(self):
        self.x, self.y = 0, random.randint(146, 197)
        self.starting_y = self.y
        self.falling_started_y = None

        self.running_speed = random.randint(1, 2) / 2

        self.state = 'running'  # [running, attacking, dragging, falling, dying, getting_up]
        self.running_frame = 0
        self.attacking_frame = 0
        self.dying_frame = 0
        self.getting_up_frame = 0
        self.falling_speed = 0

class Normal_Enemy(Enemy_Base):            # Normal_Enemy 로 바꾸기
    def __init__(self):
        self.running_width = 50
        self.running_height = 75

        self.attacking_width = 50
        self.attacking_height = 75

        self.dying_width = 70
        self.dying_height = 100

        self.getting_up_width = 70
        self.getting_up_height = 60

        if(Normal_Enemy.running_image == None):
            self.running_image = load_image('resource/normal_enemy_running.png')
        if (Normal_Enemy.attacking_image == None):
            self.attacking_image = load_image('resource/normal_enemy_attacking.png')
        if(Normal_Enemy.dying_image == None):
            self.dying_image = load_image('resource/normal_enemy_dying.png')
        if(Normal_Enemy.getting_up_image == None):
            self.getting_up_image = load_image('resource/normal_enemy_getting_up.png')

    def update(self):
        if(self.state == 'running'):
            self.x += self.running_speed
            # self.frame = (self.frame + 1) % (4 * 10)
            if(self.y >= 146 and self.y < 160 and self.x >= 436):
                self.x = 436
                self.state = 'attacking'
            if(self.y >= 160 and self.y <= 178 and self.x >= 420):
                self.x = 420
                self.state = 'attacking'
            if(self.y > 178 and self.y <= 197 and self.x >= 404):
                self.x = 404
                self.state = 'attacking'


        elif(self.state == 'dragging'):
            self.falling_speed += 0.3
            self.y -= self.falling_speed
            if(self.y <= self.starting_y):
                self.y = self.starting_y
                if(self.falling_started_y >= 450):
                    self.state = 'falling'
                else:
                    self.state = 'getting_up'
                    self.getting_up_frame = 0
        elif(self.state == 'dying'):
            if(self.dying_frame < 6 * 12):
                self.dying_frame += 1
        elif(self.state == 'getting_up'):
            if(self.getting_up_frame >= 30):
                self.state = 0
            self.getting_up_frame += 1



    def draw(self):
        if(self.state == 'running' or self.state == 'dragging' or self.state == 'falling'):
            self.running_image.clip_draw(math.floor(self.running_frame / 10) % 4 * 50, 75, self.running_width, self.running_height, self.x, self.y)
        elif(self.state == 'attacking'):
            self.attacking_image.clip_draw(math.floor(self.attacking_frame / 10) % 4 * 50, 0, self.attacking_width, self.attacking_height, self.x, self.y)
        elif(self.state == 'dying' and self.dying_frame < 6 * 12):
            self.dying_image.clip_draw(math.floor(self.dying_frame / 12) * 70, 0, self.dying_width, self.dying_height, self.x, self.y)
        elif(self.state == 'getting_up'):
            self.getting_up_image.clip_draw(math.floor(self.getting_up_frame / 10) * 70, 0, self.getting_up_width, self.getting_up_height, self.x, self.y)
        #print(self.state, self.frame, self.frame % 4, self.frame % 5, self.x, self.y)

    def get_bb(self):
        return self.x - self.running_width / 2, self.y - self.running_height / 2, self.x + self.running_width / 2, self.y + self.running_height / 2

    pass

class Crush_Enemy(Enemy_Base):
    def __init__(self):
        Normal_Enemy.__init__()
        self.x, self.y = 0,random.randint(146, 197)
        self.first_y = self.y
        self.last_y = None
        self.width = 75
        self.height = 75
        self.speed = random.randint(1,2) / 2
        if(Normal_Enemy.image == None):
            self.image = load_image('resource/crush_enemy_running.png')
        if (Normal_Enemy.attacking_image == None):
            self.attacking_image = load_image('resource/crush_enemy_attacking.png')
        if(Normal_Enemy.die_image == None):
            self.die_image = load_image('resource/normal_enemy_dying.png')
        if(Normal_Enemy.alive_image == None):
            self.alive_image = load_image('resource/crush_enemy_getting_up.png')
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
    def get_bb(self):
        return self.x - self.running_width / 2, self.y - self.running_height / 2, self.x + self.running_width / 2, self.y + self.running_height / 2
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

    def get_bb(self):
        return self.x - self.running_width / 2, self.y - self.running_height / 2, self.x + self.running_width / 2, self.y + self.running_height / 2

    pass