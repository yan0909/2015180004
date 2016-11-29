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
        self.falling_started_y = 0

        self.running_speed = random.randint(1, 2) / 2

        self.running_width, self.running_height, self.attacking_width, self.attacking_height, self.dying_width,\
        self.dying_height, self.getting_up_width, self.getting_up_height = 0, 0, 0, 0, 0, 0, 0, 0

        self.state = 'running'  # [running, attacking, dragging, falling, dying, getting_up]
        self.running_frame = 0
        self.attacking_frame = 0
        self.dying_frame = 0
        self.getting_up_frame = 0
        self.falling_speed = 0

    def update(self):
        if (self.state == 'running'):
            self.x += self.running_speed
            if (self.y >= 146 and self.y < 160 and self.x >= 436):
                self.x = 436
                self.state = 'attacking'
            if (self.y >= 160 and self.y <= 178 and self.x >= 420):
                self.x = 420
                self.state = 'attacking'
            if (self.y > 178 and self.y <= 197 and self.x >= 404):
                self.x = 404
                self.state = 'attacking'

        elif (self.state == 'attacking'):
            self.attacking_frame = (self.attacking_frame + 1) % (4 * 10)

        elif (self.state == 'falling'):
            self.falling_speed += 0.3
            self.y -= self.falling_speed
            if (self.y <= self.starting_y): # 땅에 부딪혔을 때
                self.y = self.starting_y # 위치보정
                if (self.falling_started_y >= 450): # 죽을 높이였으면
                    self.state = 'dying'
                    self.dying_frame = 0
                else:
                    self.state = 'getting_up'
                    self.getting_up_frame = 0

        elif (self.state == 'dying'):
            if (self.dying_frame < 6 * 12):
                self.dying_frame += 1

        elif (self.state == 'getting_up'):
            if (self.getting_up_frame >= 30):
                self.state = 'running'
            self.getting_up_frame += 1

        if(self.state == 'running' or self.state == 'dragging' or self.state == 'falling'):
            self.running_frame = (self.running_frame + 1) % (4 * 10)

    def draw(self):
        if(self.state == 'running' or self.state == 'dragging' or self.state == 'falling'):
            self.running_image.clip_draw(math.floor(self.running_frame / 10) % 4 * self.running_width, 0, self.running_width, self.running_height, self.x, self.y)
        elif(self.state == 'attacking'):
            self.attacking_image.clip_draw(math.floor(self.attacking_frame / 10) % 4 * self.attacking_width, 0, self.attacking_width, self.attacking_height, self.x, self.y)
        elif(self.state == 'dying' and self.dying_frame < 6 * 12):
            self.dying_image.clip_draw(math.floor(self.dying_frame / 12) * self.dying_width, 0, self.dying_width, self.dying_height, self.x, self.y)
        elif(self.state == 'getting_up'):
            self.getting_up_image.clip_draw(math.floor(self.getting_up_frame / 10) *  self.getting_up_width, 0, self.getting_up_width, self.getting_up_height, self.x, self.y)

    def get_bb(self):
        return self.x - self.running_width / 2, self.y - self.running_height / 2, self.x + self.running_width / 2, self.y + self.running_height / 2

    pass

class Enemy_Normal(Enemy_Base):
    def __init__(self):
        Enemy_Base.__init__(self)

        self.running_width = 50
        self.running_height = 75

        self.attacking_width = 50
        self.attacking_height = 75

        self.dying_width = 70
        self.dying_height = 100

        self.getting_up_width = 70
        self.getting_up_height = 60

        if(Enemy_Normal.running_image == None):
            self.running_image = load_image('resource/enemy_normal_running.png')
        if (Enemy_Normal.attacking_image == None):
            self.attacking_image = load_image('resource/enemy_normal_attacking.png')
        if(Enemy_Normal.dying_image == None):
            self.dying_image = load_image('resource/enemy_normal_dying.png')
        if(Enemy_Normal.getting_up_image == None):
            self.getting_up_image = load_image('resource/enemy_normal_getting_up.png')

    pass

class Enemy_Crush(Enemy_Base):
    def __init__(self):
        Enemy_Base.__init__(self)

        self.running_width = 80
        self.running_height = 75

        self.attacking_width = 80
        self.attacking_height = 75

        self.dying_width = 70
        self.dying_height = 100

        self.getting_up_width = 70
        self.getting_up_height = 60

        if(Enemy_Crush.running_image == None):
            self.running_image = load_image('resource/enemy_crush_running.png')
        if (Enemy_Crush.attacking_image == None):
            self.attacking_image = load_image('resource/enemy_crush_attacking.png')
        if(Enemy_Crush.dying_image == None):
            self.dying_image = load_image('resource/enemy_normal_dying.png')
        if(Enemy_Crush.getting_up_image == None):
            self.getting_up_image = load_image('resource/enemy_crush_getting_up.png')

    pass


class Enemy_Giant(Enemy_Base):
    def __init__(self):
        Enemy_Base.__init__(self)

        self.running_width = 60
        self.running_height = 120

        self.attacking_width = 60
        self.attacking_height = 120

        self.dying_width = 75
        self.dying_height = 100

        self.getting_up_width = 130
        self.getting_up_height = 120

        if (Enemy_Giant.running_image == None):
            self.running_image = load_image('resource/enemy_giant_running.png')
        if (Enemy_Giant.attacking_image == None):
            self.attacking_image = load_image('resource/enemy_giant_attacking.png')
        if (Enemy_Giant.dying_image == None):
            self.dying_image = load_image('resource/enemy_giant_dying.png')
        if (Enemy_Giant.getting_up_image == None):
            self.getting_up_image = load_image('resource/enemy_giant_getting_up.png')

    pass