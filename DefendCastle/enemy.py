from pico2d import *
import random
import main_state
import json
import os

JSON_FILENAME = 'game_data.json'
JSON_DATA = None

class Enemy_Base:
    global JSON_DATA, JSON_FILENAME

    json_file = open(JSON_FILENAME, 'r')
    JSON_DATA = json.load(json_file)
    json_file.close()

    PIXEL_PER_METER = JSON_DATA["PIXEL_PER_METER"] #(75.0 / 1.0)
    
    RUN_SPEED_KMPH = JSON_DATA['Enemy']['RUN_SPEED_KMPH']
    RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
    RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
    RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

    FALL_SPEED_KMPH = JSON_DATA['Enemy']['FALL_SPEED_KMPH']
    FALL_SPEED_MPM = FALL_SPEED_KMPH * 1000.0 / 60.0
    FALL_SPEED_MPS = FALL_SPEED_MPM / 60.0
    FALL_SPEED_PPS = FALL_SPEED_MPS * PIXEL_PER_METER

    RUN_TIME_PER_ACTION = JSON_DATA['Enemy']['RUN_TIME_PER_ACTION']
    RUN_ACTION_PER_TIME = 1.0 / RUN_TIME_PER_ACTION
    RUN_FRAMES_PER_ACTION = JSON_DATA['Enemy']['RUN_FRAMES_PER_ACTION']

    ATTACK_TIME_PER_ACTION = JSON_DATA['Enemy']['ATTACK_TIME_PER_ACTION']
    ATTACK_ACTION_PER_TIME = 1.0 / ATTACK_TIME_PER_ACTION
    ATTACK_FRAMES_PER_ACTION = JSON_DATA['Enemy']['ATTACK_FRAMES_PER_ACTION']

    DIE_TIME_PER_ACTION = JSON_DATA['Enemy']['DIE_TIME_PER_ACTION']
    DIE_ACTION_PER_TIME = 1.0 / DIE_TIME_PER_ACTION
    DIE_FRAMES_PER_ACTION = JSON_DATA['Enemy']['DIE_FRAMES_PER_ACTION']

    GET_UP_TIME_PER_ACTION = JSON_DATA['Enemy']['GET_UP_TIME_PER_ACTION']
    GET_UP_ACTION_PER_TIME = 1.0 / GET_UP_TIME_PER_ACTION
    GET_UP_FRAMES_PER_ACTION = JSON_DATA['Enemy']['GET_UP_FRAMES_PER_ACTION']

    running_image = None
    attacking_image = None
    dying_image = None
    getting_up_image = None

    dying_sound = None
    getting_up_sound = None

    def __init__(self):
        self.x = JSON_DATA['Enemy']['x']
        self.y = random.randint(JSON_DATA['Enemy']['y_rand_min'], JSON_DATA['Enemy']['y_rand_max'])
        self.starting_y = self.y
        self.falling_started_y = 0

        self.running_speed = Enemy_Base.RUN_SPEED_PPS / float(random.randint(1, 2))

        if (Enemy_Base.dying_sound == None):
            Enemy_Base.dying_sound = []
            Enemy_Base.dying_sound.append(load_wav('sound/dying1.wav'))
            Enemy_Base.dying_sound.append(load_wav('sound/dying2.wav'))
            Enemy_Base.dying_sound.append(load_wav('sound/dying3.wav'))
            for e in Enemy_Base.dying_sound:
                e.set_volume(JSON_DATA['Enemy']['dying_sound_volume'])

        if (Enemy_Base.getting_up_sound == None):
            Enemy_Base.getting_up_sound = load_wav('sound/getting_up.wav')
            Enemy_Base.getting_up_sound.set_volume(JSON_DATA['Enemy']['getting_up_sound_volume'])

        #self.running_speed = random.randint(1, 2) / 2

        self.running_width, self.running_height, self.attacking_width, self.attacking_height, self.dying_width,\
        self.dying_height, self.getting_up_width, self.getting_up_height = 0, 0, 0, 0, 0, 0, 0, 0

        self.state = 'running'  # [running, attacking, dragging, falling, dying, getting_up]

        self.running_frame = 0
        self.running_total_frame = 0.0

        self.attacking_frame = 0
        self.attacking_total_frame = 0.0

        self.dying_frame = 0
        self.dying_total_frame = 0.0

        self.getting_up_frame = 0
        self.getting_up_total_frame = 0.0

        self.falling_speed = 0.0

    def update(self, frame_time):
        if (self.state == 'running'):
            #self.x += self.running_speed
            self.x += self.running_speed * frame_time
            if (self.y >= JSON_DATA['Enemy']['castle_door_level1_y'] and self.y < JSON_DATA['Enemy']['castle_door_level2_y'] and self.x >= JSON_DATA['Enemy']['castle_door_level1_x']):
                self.x = JSON_DATA['Enemy']['castle_door_level1_x']
                self.state = 'attacking'
            if (self.y >= JSON_DATA['Enemy']['castle_door_level2_y'] and self.y <= JSON_DATA['Enemy']['castle_door_level3_y'] and self.x >= JSON_DATA['Enemy']['castle_door_level2_x']):
                self.x = JSON_DATA['Enemy']['castle_door_level2_x']
                self.state = 'attacking'
            if (self.y > JSON_DATA['Enemy']['castle_door_level3_y'] and self.y <= JSON_DATA['Enemy']['castle_door_level4_y'] and self.x >= JSON_DATA['Enemy']['castle_door_level3_x']):
                self.x = JSON_DATA['Enemy']['castle_door_level3_x']
                self.state = 'attacking'

        elif (self.state == 'attacking'):
            self.attacking_total_frame += Enemy_Base.ATTACK_FRAMES_PER_ACTION * Enemy_Base.ATTACK_ACTION_PER_TIME * frame_time
            self.attacking_frame = int(self.attacking_total_frame) % Enemy_Base.ATTACK_FRAMES_PER_ACTION

        elif (self.state == 'falling'):
            #self.falling_speed += 0.3
            self.falling_speed += Enemy_Base.FALL_SPEED_PPS * frame_time
            self.y -= self.falling_speed
            if (self.y <= self.starting_y): # 땅에 부딪혔을 때
                self.y = self.starting_y # 위치보정
                if (self.falling_started_y >= JSON_DATA['Enemy']['height_to_die']): # 죽을 높이였으면
                    self.state = 'dying'
                    r = random.randint(0,2)
                    Enemy_Base.dying_sound[r].play()
                    self.dying_frame = 0
                    self.dying_total_frame = 0.0
                else:
                    self.state = 'getting_up'
                    Enemy_Base.getting_up_sound.play()
                    self.getting_up_frame = 0
                    self.getting_up_total_frame = 0.0

        elif (self.state == 'dying'):
            if (self.dying_total_frame < float(Enemy_Base.DIE_FRAMES_PER_ACTION)):
                self.dying_total_frame += Enemy_Base.DIE_FRAMES_PER_ACTION * Enemy_Base.DIE_ACTION_PER_TIME * frame_time
                self.dying_frame = int(self.dying_total_frame)

        elif (self.state == 'getting_up'):
            self.getting_up_total_frame += Enemy_Base.GET_UP_FRAMES_PER_ACTION * Enemy_Base.GET_UP_ACTION_PER_TIME * frame_time
            self.getting_up_frame = int(self.getting_up_total_frame)
            #print(self.getting_up_total_frame)
            if (self.getting_up_total_frame >= float(Enemy_Base.GET_UP_FRAMES_PER_ACTION - 1)):
                self.state = 'running'


        if(self.state == 'running' or self.state == 'dragging' or self.state == 'falling'):
            self.running_total_frame += Enemy_Base.RUN_FRAMES_PER_ACTION * Enemy_Base.RUN_ACTION_PER_TIME * frame_time
            self.running_frame = int(self.running_total_frame) % Enemy_Base.RUN_FRAMES_PER_ACTION

    def draw(self):
        if(self.state == 'running' or self.state == 'dragging' or self.state == 'falling'):
            self.running_image.clip_draw(self.running_frame* self.running_width, 0, self.running_width, self.running_height, self.x, self.y)
        elif(self.state == 'attacking'):
            self.attacking_image.clip_draw(self.attacking_frame * self.attacking_width, 0, self.attacking_width, self.attacking_height, self.x, self.y)
        elif(self.state == 'dying' and self.dying_total_frame < float(Enemy_Base.DIE_FRAMES_PER_ACTION)):
            self.dying_image.clip_draw(self.dying_frame * self.dying_width, 0, self.dying_width, self.dying_height, self.x, self.y)
        elif(self.state == 'getting_up'):
            self.getting_up_image.clip_draw(self.getting_up_frame *  self.getting_up_width, 0, self.getting_up_width, self.getting_up_height, self.x, self.y)


    def get_bb(self):
        return self.x - self.running_width / 2, self.y - self.running_height / 2, self.x + self.running_width / 2, self.y + self.running_height / 2

    pass

class Enemy_Normal(Enemy_Base):
    def __init__(self):
        global JSON_DATA
        Enemy_Base.__init__(self)

        self.running_width = JSON_DATA['Enemy']['Enemy_Normal']['running_width']
        self.running_height = JSON_DATA['Enemy']['Enemy_Normal']['running_height']

        self.attacking_width = JSON_DATA['Enemy']['Enemy_Normal']['attacking_width']
        self.attacking_height = JSON_DATA['Enemy']['Enemy_Normal']['attacking_height']

        self.dying_width = JSON_DATA['Enemy']['Enemy_Normal']['dying_width']
        self.dying_height = JSON_DATA['Enemy']['Enemy_Normal']['dying_height']

        self.getting_up_width = JSON_DATA['Enemy']['Enemy_Normal']['getting_up_width']
        self.getting_up_height = JSON_DATA['Enemy']['Enemy_Normal']['getting_up_height']

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
        global JSON_DATA
        Enemy_Base.__init__(self)

        self.running_width = JSON_DATA['Enemy']['Enemy_Crush']['running_width']
        self.running_height = JSON_DATA['Enemy']['Enemy_Crush']['running_height']

        self.attacking_width = JSON_DATA['Enemy']['Enemy_Crush']['attacking_width']
        self.attacking_height = JSON_DATA['Enemy']['Enemy_Crush']['attacking_height']

        self.dying_width = JSON_DATA['Enemy']['Enemy_Crush']['dying_width']
        self.dying_height = JSON_DATA['Enemy']['Enemy_Crush']['dying_height']

        self.getting_up_width = JSON_DATA['Enemy']['Enemy_Crush']['getting_up_width']
        self.getting_up_height = JSON_DATA['Enemy']['Enemy_Crush']['getting_up_height']

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
        global JSON_DATA
        Enemy_Base.__init__(self)

        self.running_width = JSON_DATA['Enemy']['Enemy_Giant']['running_width']
        self.running_height = JSON_DATA['Enemy']['Enemy_Giant']['running_height']

        self.attacking_width = JSON_DATA['Enemy']['Enemy_Giant']['attacking_width']
        self.attacking_height = JSON_DATA['Enemy']['Enemy_Giant']['attacking_height']

        self.dying_width = JSON_DATA['Enemy']['Enemy_Giant']['dying_width']
        self.dying_height = JSON_DATA['Enemy']['Enemy_Giant']['dying_height']

        self.getting_up_width = JSON_DATA['Enemy']['Enemy_Giant']['getting_up_width']
        self.getting_up_height = JSON_DATA['Enemy']['Enemy_Giant']['getting_up_height']

        if (Enemy_Giant.running_image == None):
            self.running_image = load_image('resource/enemy_giant_running.png')
        if (Enemy_Giant.attacking_image == None):
            self.attacking_image = load_image('resource/enemy_giant_attacking.png')
        if (Enemy_Giant.dying_image == None):
            self.dying_image = load_image('resource/enemy_giant_dying.png')
        if (Enemy_Giant.getting_up_image == None):
            self.getting_up_image = load_image('resource/enemy_giant_getting_up.png')

    pass