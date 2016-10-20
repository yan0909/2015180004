from pico2d import *
import enemy
import random
import game_framework
import math

EnemyCount, background, castle, CloudTeam, EnemyTeam, TargetEnemyIndex, isMouseDown = None, None, None, None, None, -1, False

class Cloud:
    def __init__(self,name):
        self.x, self.y = random.randint(900,1500),random.randint(430,500)
        self.speed = random.randint(5,10)/10
        self.image = load_image(name)
    def update(self):
        self.x -= self.speed
        if(self.x <= -100):
            self.x = random.randint(900,1500)
            self.y = random.randint(430,500)
            self.speed = random.randint(5,10)/10
    def draw(self):
        self.image.draw(self.x,self.y)
    pass

def handle_events():
    global mx, my, EnemyTeam, TargetEnemyIndex, isMouseDown
    events = get_events()
    for event in events:
        if(event.type == SDL_QUIT):
            game_framework.quit()
        elif(event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
        elif(event.type == SDL_MOUSEMOTION):
            mx = event.x
            my = 599 - event.y
            print(mx, my)
            if(isMouseDown and TargetEnemyIndex != -1):
                EnemyTeam[TargetEnemyIndex].x = mx
                EnemyTeam[TargetEnemyIndex].y = my
        elif(event.type == SDL_MOUSEBUTTONDOWN):
            isMouseDown = True
            mx = event.x
            my = 599 - event.y
            TargetEnemyIndex = -1
            for i in range(EnemyCount):
                if(EnemyTeam[i].state == 0 or EnemyTeam[i].state == 1):
                   if(EnemyTeam[i].x - EnemyTeam[i].width / 2 <= mx and mx <= EnemyTeam[i].x + EnemyTeam[i].width / 2
                   and EnemyTeam[i].y - EnemyTeam[i].height / 2 <= my and my <= EnemyTeam[i].y + EnemyTeam[i].height / 2):
                        TargetEnemyIndex = i
                        EnemyTeam[i].state = 2
                        EnemyTeam[i].f_speed = 0
                        break

        if(event.type == SDL_MOUSEBUTTONUP or (isMouseDown == True and mx == 0 or mx == 799 or my == 0 or my == 599)):
            isMouseDown = False
            if(TargetEnemyIndex != -1):
                EnemyTeam[TargetEnemyIndex].state = 3
                EnemyTeam[TargetEnemyIndex].last_y = my
            TargetEnemyIndex = -1



def enter():
    global EnemyCount, background, castle, CloudTeam, EnemyTeam
    EnemyCount = random.randint(5,10)

    print(background)
    background = load_image('background.png')
    print(background)
    castle = load_image('castle.png')
    CloudTeam = [Cloud('cloud01.png'), Cloud('cloud01.png'),Cloud('cloud02.png'),Cloud('cloud02.png')]
    EnemyTeam = [enemy.Enemy() for i in range(EnemyCount)]

    for i in range(EnemyCount):
        EnemyTeam[i].x = -((((80-5) / (EnemyCount - 1)) * i + 5) * 100 * EnemyTeam[i].speed)
        print(i, ";", EnemyTeam[i].x)

def update():
    global CloudTeam, EnemyTeam
    for c in CloudTeam:
        c.update()
    for e in EnemyTeam:
        e.update()

def draw():
    global background, castle, CloudTeam, EnemyTeam
    clear_canvas()

    background.draw(400, 300)
    castle.draw(433, 300)
    for c in CloudTeam:
        c.draw()
    for e in EnemyTeam:
        e.draw()

    update_canvas()

    delay(0.01)

def pause():
    pass

def resume():
    pass

def exit():
    global background, castle, CloudTeam, EnemyTeam
    del(background)
    del(castle)
    for c in CloudTeam:
        del(c)
    for e in EnemyTeam:
        del(e)
    pass