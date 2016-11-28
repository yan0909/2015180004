from pico2d import *
import game_framework
import start_menu
import main_state

name = 'Lose'
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('resource/lose.png')

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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                exit()
            elif (event.type == SDL_MOUSEBUTTONDOWN):
                if (event.x >= 365 and event.x <= 439 and 599 - event.y >= 59 and 599 - event.y <= 97):
                    game_framework.change_state(start_menu)


                #print(event.x)
                #print(599 - event.y)
