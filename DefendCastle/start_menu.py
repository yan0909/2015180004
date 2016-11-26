from pico2d import *
import game_framework
import main_state

name = 'StartMenu'
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('resource/title.png')

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
            game_framework.quit()
            #exit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                #game_framework.quit()
                exit()
            elif (event.type == SDL_MOUSEBUTTONDOWN):
                if(354 < event.x and event.x < 535 and 370 < event.y and event.y < 400):
                    game_framework.change_state(main_state)
                if(event.x >= 409 and event.x <= 476 and 599 - event.y >= 127 and 599 - event.y <= 154):
                    game_framework.quit()
                #mx = event.x
                #my = 599 - event.y
                #print(mx, my)