from pico2d import *
from sdl2.events import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDL_QUIT
from sdl2.keycode import SDLK_ESCAPE

import game_framework
import main_state

name = 'StartMenu'
image = None
logo_time = 0.0
button_sound = None

new_button_mouse_over = False
load_button_mouse_over = False
exit_button_mouse_over = False

new_button_rect = None
load_button_rect = None
exit_button_rect = None

new_button_image = None
load_button_image = None
exit_button_image = None

buttons_over = []
buttons_rect = []
buttons_image = []

def enter():
    global image, button_sound, \
        new_button_mouse_over, load_button_mouse_over, exit_button_mouse_over, buttons_over, \
        new_button_rect, load_button_rect, exit_button_rect, buttons_rect, \
        new_button_image, load_button_image, exit_button_image, buttons_image

    image = load_image('resource/title.png')
    button_sound = load_wav('sound/menu.wav')
    button_sound.set_volume(90)

    new_button_mouse_over = False
    load_button_mouse_over = False
    exit_button_mouse_over = False

    new_button_rect = [354, 369, 535, 403]
    load_button_rect = [342, 411, 535, 436]
    exit_button_rect = [409, 441, 476, 471]

    new_button_image = load_image('resource/new_game.png')
    load_button_image = load_image('resource/load_game.png')
    exit_button_image = load_image('resource/exit.png')

    buttons_rect = [new_button_rect, load_button_rect, exit_button_rect]
    buttons_over = [new_button_mouse_over, load_button_mouse_over, exit_button_mouse_over]
    buttons_image = [new_button_image, load_button_image, exit_button_image]


def exit():
    global image
    del(image)
    pass

def update():
    pass

def draw():
    global image, buttons_over, buttons_rect, buttons_image
    clear_canvas()
    image.draw(400, 300)
    for index in range(len(buttons_image)):
        if(buttons_over[index]):
            buttons_image[index].draw((buttons_rect[index][0] + buttons_rect[index][2]) / 2, (599 - buttons_rect[index][1] + 599 - buttons_rect[index][3]) / 2)
    update_canvas()
    pass


def pause():
    print('pause')
    pass

def resume():
    print('resume')
    pass


def ptInRect(pt, rect):
    if (pt.x < rect[0]): return False
    if (pt.y < rect[1]): return False
    if (pt.x > rect[2]): return False
    if (pt.y > rect[3]): return False
    return True
    pass

def handle_events():
    global button_sound, buttons_rect, buttons_over, \
        new_button_rect, load_button_rect, exit_button_rect


    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                exit()
            elif (event.type == SDL_MOUSEBUTTONDOWN):
                mouse_x = event.x
                mouse_y =  event.y
                print(mouse_x, mouse_y)

                if(ptInRect(event, new_button_rect)):
                    game_framework.change_state(main_state)
                if (ptInRect(event, load_button_rect)):
                    game_framework.change_state(main_state)
                if (ptInRect(event, exit_button_rect)):
                    game_framework.quit()


            elif(event.type == SDL_MOUSEMOTION):
                for index in range(len(buttons_rect)):
                    if (buttons_over[index] == False and ptInRect(event, buttons_rect[index])):
                        buttons_over[index] = True
                        button_sound.play()
                        print(index)
                    elif (buttons_over[index] and not ptInRect(event, buttons_rect[index])):
                        buttons_over[index] = False



