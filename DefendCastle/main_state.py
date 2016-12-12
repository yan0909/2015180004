from pico2d import *
import enemy
import random
import game_framework
import clear_state
import lose_state
import math

enemy_count, background, castle, cloud_team, enemy_team, target_enemy_index, isMouseDown = None, None, None, None, None, -1, False
stage_play_time = 0.0
mouse_x, mouse_y = 0, 0
now_stage = 0
class Castle:
    def __init__(self):
        self.castle = load_image('resource/castle.png')
        self.castle_HP_bar = load_image('resource/castle_HP.png')
        self.castle_HP = 100.0

        self.bgm = load_music('sound/background.mp3')
        self.bgm.set_volume(90)
        self.bgm.repeat_play()

    def draw(self):
        self.castle.draw(433, 300)
        self.castle_HP_bar.draw(507 + 282 / 2 / 100 * self.castle_HP, 562, 282 / 100 * self.castle_HP, 17)

    pass


class Cloud:
    def __init__(self, name):
        self.x, self.y = random.randint(900, 1500), random.randint(430, 500)
        self.speed = random.randint(5, 10)/10
        self.image = load_image(name)
    def update(self):
        self.x -= self.speed
        if(self.x <= -100):
            self.x = random.randint(900, 1500)
            self.y = random.randint(430, 500)
            self.speed = random.randint(5, 10)/10
    def draw(self):
        self.image.draw(self.x, self.y)
    pass

def handle_events():
    global mouse_x, mouse_y, enemy_team, enemy_count, target_enemy_index, isMouseDown, now_stage, stage_play_time
    events = get_events()
    for event in events:
        if(event.type == SDL_QUIT):
            game_framework.quit()
        elif(event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_1):   # 치트키
            #game_framework.change_state(clear_state)
            stage_play_time = 9999999
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_2):   # 치트키
            game_framework.change_state(lose_state)
        elif(event.type == SDL_MOUSEMOTION):
            mouse_x = event.x
            mouse_y = 599 - event.y
            #print(mouse_x, mouse_y)
            if(isMouseDown and target_enemy_index != -1):
                enemy_team[target_enemy_index].x = mouse_x
                enemy_team[target_enemy_index].y = mouse_y
        elif(event.type == SDL_MOUSEBUTTONDOWN):
            isMouseDown = True
            mouse_x = event.x
            mouse_y = 599 - event.y
            target_enemy_index = -1
            if(now_stage < 3):
                for i in range(enemy_count * 1):
                    if(enemy_team[i].state == 'running' or enemy_team[i].state == 'attacking'):
                        if(enemy_team[i].x - enemy_team[i].running_width / 2 <= mouse_x and mouse_x <= enemy_team[i].x + enemy_team[i].running_width / 2   # running_width 와 attacking_width 는 같음
                        and enemy_team[i].y - enemy_team[i].running_height / 2 <= mouse_y and mouse_y <= enemy_team[i].y + enemy_team[i].running_height / 2):
                            target_enemy_index = i
                            enemy_team[i].state = 'dragging'
                            enemy_team[i].falling_speed = 0
                            break
            elif(now_stage < 5):
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
    background = load_image('resource/background.png')
    cloud_team = [Cloud('resource/big_cloud.png'), Cloud('resource/big_cloud.png'),Cloud('resource/small_cloud.png'),Cloud('resource/small_cloud.png')]
    enemy_team = []
    if(now_stage == 0):
        enemy_count = random.randint(5, 10)
    elif(now_stage >= 6):
        enemy_count = math.floor(1.5)
    print(now_stage, enemy_count)

    for i in range(enemy_count):
        e = enemy.Enemy_Normal()
        e.x = -((((80 - 5) / (enemy_count - 1)) * i + 5) * 100 * e.running_speed) + 500 #######
        enemy_team.append(e)

    if (now_stage >= 3):
        for i in range(enemy_count):
            e = enemy.Enemy_Crush()
            e.x = -((((80 - 5) / (enemy_count - 1)) * i + 5) * 100 * e.running_speed)
            enemy_team.append(e)
        if (now_stage >= 5):
            for i in range(enemy_count):
                e = enemy.Enemy_Giant()
                e.x = -((((80 - 5) / (enemy_count - 1)) * i + 5) * 100 * e.running_speed)
                enemy_team.append(e)

    stage_play_time = 0.0

def update():
    global cloud_team, enemy_team, castle, stage_play_time, castle_HP, now_stage
    for c in cloud_team:
        c.update()
    for e in enemy_team:
        e.update()
        if(e.state == 'attacking' and e.attacking_frame == 0):
            castle.castle_HP -= 0.1
    if (castle.castle_HP == 0):
        game_framework.change_state(lose_state)

    if (stage_play_time >= 50.0):
        now_stage += 1
        game_framework.change_state(clear_state)


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

    stage_play_time += 0.01
    delay(0.01)

def pause():
    pass

def resume():
    pass

def exit():
    pass