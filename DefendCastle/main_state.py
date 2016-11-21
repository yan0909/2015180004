from pico2d import *
import enemy
import random
import game_framework
import clear_state
import math

EnemyCount, background, castle, CloudTeam, EnemyTeam, TargetEnemyIndex, isMouseDown = None, None, None, None, None, -1, False
playTime = 0.0
class Castle:
    def __init__(self):
        self.castle = load_image('castle.png')
        self.castleHPBar = load_image('Red.png')
        self.castleHP = 100.0

    def draw(self):
        self.castle.draw(433, 300)
        self.castleHPBar.draw(507 + 282 / 2 / 100 * self.castleHP, 562, 282 / 100 * self.castleHP, 17)

    pass


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
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_1):
            game_framework.change_state(clear_state)
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
            for i in range(EnemyCount * 2):
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
    global EnemyCount, background, castle, CloudTeam, EnemyTeam, castle
    EnemyCount = random.randint(5,10)

    castle = Castle()
    #print(background)
    background = load_image('background.png')
    print(background)
    CloudTeam = [Cloud('cloud01.png'), Cloud('cloud01.png'),Cloud('cloud02.png'),Cloud('cloud02.png')]
    EnemyTeam = []

    for i in range(EnemyCount):
        e = enemy.Enemy()
        e.x = -((((80 - 5) / (EnemyCount - 1)) * i + 5) * 100 * e.speed)
        EnemyTeam.append(e)
    for i in range(EnemyCount):
        e = enemy.Enemy02()
        e.x = -((((80 - 5) / (EnemyCount - 1)) * i + 5) * 100 * e.speed)
        EnemyTeam.append(e)

        print(i, ";", EnemyTeam[i].x)

def update():
    global CloudTeam, EnemyTeam, castle, playTime
    for c in CloudTeam:
        c.update()
    for e in EnemyTeam:
        e.update()
        if e.isHit:
            castle.castleHP -= 1
            e.isHit = False
    print(game_framework.getStage())
    if playTime >= 50.0:
        game_framework.upStage()
        game_framework.change_state(clear_state)


def draw():
    global background, castle, CloudTeam, EnemyTeam, castleHPBar, castleHP, playTime
    clear_canvas()

    background.draw(400, 300)

    castle.draw()

    for c in CloudTeam:
        c.draw()
    for e in EnemyTeam:
        e.draw()


    update_canvas()

    playTime += 0.01
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
        del(c.image)
    for e in EnemyTeam:
        del(e.image)
    pass