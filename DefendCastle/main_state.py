from pico2d import *
from sdl2.events import SDL_QUIT, SDL_KEYDOWN, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP
from sdl2.keycode import SDLK_ESCAPE, SDLK_1, SDLK_2

import enemy
import random
import game_framework
import clear_state
import lose_state
import math

JSON_FILENAME = "game_data.json"
JSON_DATA = None

json_file = open(JSON_FILENAME, "r")
JSON_DATA = json.load(json_file)
json_file.close()

PIXEL_PER_METER = JSON_DATA["PIXEL_PER_METER"] #(75.0 / 1.0)

enemy_count, background, castle, cloud_team, enemy_team, target_enemy_index, isMouseDown = None, None, None, None, None, -1, False
stage_play_time = 0.0
mouse_x, mouse_y = 0, 0
now_stage = 0

class Castle:
    def __init__(self):
        self.x = JSON_DATA['Castle']['x']
        self.y = JSON_DATA['Castle']['y']

        self.castle = load_image('resource/castle.png')
        self.castle_HP_bar = load_image('resource/castle_HP.png')
        self.castle_HP = JSON_DATA['Castle']['castle_HP']

        self.bgm = load_music('sound/background.mp3')
        self.bgm.set_volume(JSON_DATA['Castle']['bgm_volume'])
        #self.bgm.repeat_play()

    def draw(self):
        self.castle.draw(self.x, self.y)
        self.castle_HP_bar.draw(JSON_DATA['Castle']['castle_HP_bar_x'] + JSON_DATA['Castle']['castle_HP_bar_w'] / 2 / 100 * int(self.castle_HP), JSON_DATA['Castle']['castle_HP_bar_y'], JSON_DATA['Castle']['castle_HP_bar_w'] / 100 * int(self.castle_HP), JSON_DATA['Castle']['castle_HP_bar_h'])
    pass


class Cloud:
    MOVE_SPEED_KMPH = JSON_DATA['Cloud']['MOVE_SPEED_KMPH']
    MOVE_SPEED_MPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
    MOVE_SPEED_MPS = MOVE_SPEED_MPM / 60.0
    MOVE_SPEED_PPS = MOVE_SPEED_MPS * PIXEL_PER_METER

    def __init__(self, name):
        self.name = name
        self.x, self.y = random.randint(JSON_DATA['Cloud']['x_rand_min'], JSON_DATA['Cloud']['x_rand_max']), random.randint(JSON_DATA['Cloud']['y_rand_min'], JSON_DATA['Cloud']['y_rand_max'])
        self.speed = Cloud.MOVE_SPEED_PPS * random.randint(JSON_DATA['Cloud']['move_speed_rand_min'], JSON_DATA['Cloud']['move_speed_rand_max']) / 10.0
        self.image = load_image(self.name)
    def update(self, frame_time):
        self.x -= self.speed * frame_time
        if(self.x <= JSON_DATA['Cloud']['die_limit_x']):
            self.__init__(self.name)
    def draw(self):
        self.image.draw(self.x, self.y)
    pass

def handle_events(frame_time):
    global mouse_x, mouse_y, enemy_team, enemy_count, target_enemy_index, isMouseDown, now_stage, stage_play_time
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT):
            game_framework.quit()
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_1):  # 치트키
            #game_framework.change_state(clear_state)
            stage_play_time = 9999999
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_2):  # 치트키
            game_framework.change_state(lose_state)
        elif (event.type == SDL_MOUSEMOTION):
            mouse_x = event.x
            mouse_y = 599 - event.y
            # print(mouse_x, mouse_y)
            if (isMouseDown and target_enemy_index != -1):
                enemy_team[target_enemy_index].x = mouse_x
                enemy_team[target_enemy_index].y = mouse_y
        elif (event.type == SDL_MOUSEBUTTONDOWN):
            isMouseDown = True
            mouse_x = event.x
            mouse_y = 599 - event.y
            target_enemy_index = -1
            if(now_stage < JSON_DATA['stage_difficult_change_level_1']):
                for i in range(enemy_count * 1):
                    if(enemy_team[i].state == 'running' or enemy_team[i].state == 'attacking'):
                        if(enemy_team[i].x - enemy_team[i].running_width / 2 <= mouse_x and mouse_x <= enemy_team[i].x + enemy_team[i].running_width / 2   # running_width 와 attacking_width 는 같음
                        and enemy_team[i].y - enemy_team[i].running_height / 2 <= mouse_y and mouse_y <= enemy_team[i].y + enemy_team[i].running_height / 2):
                            target_enemy_index = i
                            enemy_team[i].state = 'dragging'
                            enemy_team[i].falling_speed = 0
                            break
            elif(now_stage < JSON_DATA['stage_difficult_change_level_2']):
                for i in range(enemy_count * 2):
                    if(enemy_team[i].state == 'running' or enemy_team[i].state == 'attacking'):
                        if(enemy_team[i].x - enemy_team[i].running_width / 2 <= mouse_x and mouse_x <= enemy_team[i].x + enemy_team[i].running_width / 2   # running_width 와 attacking_width 는 같음
                        and enemy_team[i].y - enemy_team[i].running_height / 2 <= mouse_y and mouse_y <= enemy_team[i].y + enemy_team[i].running_height / 2):
                            target_enemy_index = i
                            enemy_team[i].state = 'dragging'
                            enemy_team[i].falling_speed = 0
                            break
            else:
                for i in range(enemy_count * 3):
                    if(enemy_team[i].state == 'running' or enemy_team[i].state == 'attacking'):
                        if(enemy_team[i].x - enemy_team[i].running_width / 2 <= mouse_x and mouse_x <= enemy_team[i].x + enemy_team[i].running_width / 2   # running_width 와 attacking_width 는 같음
                        and enemy_team[i].y - enemy_team[i].running_height / 2 <= mouse_y and mouse_y <= enemy_team[i].y + enemy_team[i].running_height / 2):
                            target_enemy_index = i
                            enemy_team[i].state = 'dragging'
                            enemy_team[i].falling_speed = 0
                            break
        if(event.type == SDL_MOUSEBUTTONUP or (isMouseDown == True and mouse_x == 0 or mouse_x == 799 or mouse_y == 0 or mouse_y == 599)):
            isMouseDown = False
            if(target_enemy_index != -1):
                enemy_team[target_enemy_index].state = 'falling'
                mouse_y = 599 - event.y
                enemy_team[target_enemy_index].falling_started_y = mouse_y
            target_enemy_index = -1



def enter():
    global enemy_count, background, castle, cloud_team, enemy_team, castle, stage_play_time, now_stage

    castle = Castle()
    castle.bgm.repeat_play()
    background = load_image('resource/background.png')
    cloud_team = [Cloud('resource/big_cloud.png'), Cloud('resource/big_cloud.png'),Cloud('resource/small_cloud.png'),Cloud('resource/small_cloud.png')]
    enemy_team = []
    if(now_stage == 0):
        enemy_count = random.randint(JSON_DATA['enemy_count_at_stage0_rand_min'], JSON_DATA['enemy_count_at_stage0_rand_max'])
    else: #if(now_stage > 5):
        enemy_count = int(enemy_count * JSON_DATA['enemy_count_multi_per_stage'])
    print(now_stage, enemy_count)

    for i in range(enemy_count):
        e = enemy.Enemy_Normal()
        #e.x = -((((80 - 5) / (enemy_count - 1)) * i + 5) * 100 * e.RUN_SPEED_PPS * 0.016) + 500
        e.x = -((JSON_DATA['stage_clear_time'] - JSON_DATA['enemy_spawn_last_time_sec']) / (enemy_count - 1) * i * e.running_speed)
        #print(e.x)
        enemy_team.append(e)

    if (now_stage >= JSON_DATA['stage_difficult_change_level_1']):
        for i in range(enemy_count):
            e = enemy.Enemy_Crush()
            e.x = -((JSON_DATA['stage_clear_time'] - JSON_DATA['enemy_spawn_last_time_sec']) / (enemy_count - 1) * i * e.running_speed)
            enemy_team.append(e)
        if (now_stage >= JSON_DATA['stage_difficult_change_level_2']):
            for i in range(enemy_count):
                e = enemy.Enemy_Giant()
                e.x = -((JSON_DATA['stage_clear_time'] - JSON_DATA['enemy_spawn_last_time_sec']) / (enemy_count - 1) * i * e.running_speed)
                enemy_team.append(e)

    stage_play_time = 0.0

def update(frame_time):
    global cloud_team, enemy_team, castle, stage_play_time, castle_HP, now_stage
    for c in cloud_team:
        c.update(frame_time)
    for e in enemy_team:
        e.update(frame_time)
        if(e.state == 'attacking'): #and e.attacking_frame == 0):
            castle.castle_HP -= frame_time
    if (castle.castle_HP <= 0):
        game_framework.change_state(lose_state)

    if (stage_play_time >= JSON_DATA['stage_clear_time']):
        now_stage += 1
        game_framework.change_state(clear_state)

    stage_play_time += frame_time

def draw():
    global background, castle, cloud_team, enemy_team, castle_HP_bar, castle_HP, stage_play_time
    clear_canvas()

    background.draw(400, 300)
    castle.draw()

    for c in cloud_team:
        c.draw()
    for e in enemy_team:
        e.draw()


    update_canvas()

    #stage_play_time += 0.01
    #delay(0.01)

def pause():
    pass

def resume():
    pass

def exit():
    pass