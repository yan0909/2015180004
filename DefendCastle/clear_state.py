from pico2d import *
from sdl2.events import SDL_QUIT, SDL_KEYDOWN, SDL_MOUSEBUTTONDOWN
from sdl2.keycode import SDLK_ESCAPE

import game_framework
import main_state

name = 'Clear'
image = None

def enter():
    global image
    image = load_image('resource/clear.png')

def exit():
    global image
    del(image)
    pass

def update(frame_time):
    #print(game_framework.getStage())
    pass

def draw():
    global image
    clear_canvas()
    image.draw(400, 300, 800,600)
    update_canvas()
    pass


def pause():
    print('pause')
    pass

def resume():
    print('resume')
    pass

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                exit()
            elif (event.type == SDL_MOUSEBUTTONDOWN):
                if(485 < event.x and event.x < 565 and 45 < 599 - event.y and 599 - event.y < 87):
                    game_framework.change_state(main_state)
                print(event.x, 599 - event.y)