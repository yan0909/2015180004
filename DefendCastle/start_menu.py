from pico2d import *
from sdl2.events import SDL_MOUSEMOTION

import game_framework
import main_state

name = 'StartMenu'
image = None
logo_time = 0.0
menu_mouse_over_sound = None
start_button_mouse_over = False

def enter():
    global image, start_button_mouse_over, menu_mouse_over_sound
    image = load_image('resource/title.png')
    menu_mouse_over_sound = load_music('sound/menu.mp3')
    menu_mouse_over_sound.set_volume(90)
    start_button_mouse_over = False

def exit():
    global image
    del(image)
    pass

def update():
    pass

def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass


def pause():
    print('pause')
    pass

def resume():
    print('resume')
    pass

def handle_events():
    global start_button_mouse_over, menu_mouse_over_sound
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                exit()
            elif (event.type == SDL_MOUSEBUTTONDOWN):
                if(354 < event.x and event.x < 535 and 370 < event.y and event.y < 400):
                    menu_mouse_over_sound.play()
                    game_framework.change_state(main_state)

                if (342 < event.x and event.x < 535 and 163 < event.y and event.y < 188):
                    game_framework.change_state(main_state)
                if(event.x >= 409 and event.x <= 476 and 599 - event.y >= 127 and 599 - event.y <= 154):
                    game_framework.quit()
            elif(event.type == SDL_MOUSEMOTION):
                if (start_button_mouse_over == False and 354 < event.x and event.x < 535 and 370 < event.y and event.y < 400):
                    start_button_mouse_over = True
                    menu_mouse_over_sound.play()
                elif(start_button_mouse_over and not (354 < event.x and event.x < 535 and 370 < event.y and event.y < 400)):
                    start_button_mouse_over = False
                #mouse_x = event.x
                #mouse_y = 599 - event.y
                #print(mouse_x, mouse_y)