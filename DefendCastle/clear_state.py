from pico2d import *
from sdl2.events import SDL_QUIT, SDL_KEYDOWN, SDL_MOUSEBUTTONDOWN
from sdl2.keycode import SDLK_ESCAPE

import game_framework
import main_state

name = 'Clear'
image = None
font = None
save_click = False
ok_click = False

stage_count = 1

stage_beginning_image = None
stage_beginning_image_time = 0

def enter():
    global image, font, now_stage ,save_click, ok_click, \
        stage_beginning_image, ok_click, stage_beginning_image_time, stage_beginning_sound

    image = load_image('resource/clear.png')
    stage_beginning_image = load_image('resource/stage_beginning.png')

    stage_beginning_image_time = 0
    ok_click = False
    stage_beginning_sound = load_wav('sound/stage_beginning.wav')
    stage_beginning_sound.set_volume(120)

    font = load_font('font/NANUMBARUNGOTHICBOLD.TTF', 60)
    f = open('now_stage','r')
    now_stage = f.read()
    f.close()

    save_click = False
    ok_click = False

def exit():
    global image, font
    del(image)
    del(font)
    pass

def update(frame_time):
    global ok_click, stage_beginning_image_time, stage_count
    if (ok_click == True):
        stage_beginning_image_time += frame_time
        if (stage_beginning_image_time > 3.0):
            ok_click = False
            game_framework.change_state(main_state)
    pass

def draw():
    global image, font, now_stage, save_click, ok_click, stage_count
    clear_canvas()
    image.draw(400, 300, 800,600)
    font.draw(325, 520, '%s' % now_stage, (0xff, 0xff, 0xff))

    if (save_click == True):
        font.draw(195, 290, 'GAME SAVED!', (0xff, 0xff, 0xff))
    if (ok_click == True):
        stage_beginning_image.draw(400, 300)
        font.draw(500, 310, '%d' % stage_count, (0xff, 0xff, 0xff))

    update_canvas()

    pass


def pause():
    print('pause')
    pass

def resume():
    print('resume')
    pass

def handle_events(frame_time):
    global save_click, ok_click, stage_beginning_sound, stage_count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                exit()
            elif (event.type == SDL_MOUSEBUTTONDOWN):
                if(485 < event.x and event.x < 565 and 512 < event.y and event.y < 554):
                    ok_click = True
                    stage_count += 1
                    stage_beginning_sound.play()
                if (261 < event.x and event.x < 392 and 512 < event.y and event.y < 554):
                    save_click = True
                print(event.x, 599 - event.y)