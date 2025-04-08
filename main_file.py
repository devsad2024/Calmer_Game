from sun import Sun
import pygame
import random
import threading
import time

import os

os.chdir(r"C:\Users\Sadovnik\.vscode\.venv\Python-files\Calmer_Game")
"""
GAME VARS HERE
"""
window_width, window_height = 800, 600
global_score = 0
global_suns_counter = 0
MIN_TIME_BETWEEN_SUNS = 0.4
MAX_TIME_BETWEEN_SUNS = 1.4  # in seconds

pygame.init()
pygame.display.set_caption("Calmer Game")

screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()

original_background = pygame.image.load(r"SunBackGround.jpg")

# Global suns array
suns_arr = []
scores_text_dict = {}



def fade_in_play(filename, custom_volume=100):
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(custom_volume / 100)  # Pygame expects 0.0 to 1.0
    sound.play()


def add_score_text_and_pos(sun_pos, score_to_write):
    text_obj = pygame.font.Font(None, 50).render(f"+{int(score_to_write)}", True, (255, 215, 0))
    text_obj.set_alpha(100)
    global scores_text_dict
    scores_text_dict[sun_pos] = text_obj
    sound_name = random.choice(["coin1.mp3"])
    fade_in_play(sound_name, 10)
    threading.Thread(target=fade_out_text, args=(text_obj,)).start()


def fade_out_text(text_obj):
    seconds_left = 2.0
    while seconds_left > 0:
        text_obj.set_alpha(int(255 * (seconds_left / 1.0)))  # Fade out over 1 second
        seconds_left -= 0.01
        time.sleep(0.01)

def represent_score_text():
    global scores_text_dict, screen
    for pos, text_obj in scores_text_dict.items():
        screen.blit(text_obj, pos)



"""If any sun was clicked then implementing add global_score and etc"""
def check_sun_click(mouse_pos):
    global global_suns_counter, global_score, suns_arr
    for sun in suns_arr:
        if sun.sun_rect.collidepoint(mouse_pos):
            global_score += sun.score
            global_suns_counter += 1
            add_score_text_and_pos(sun.sun_rect.bottomleft, sun.score)
            suns_arr.remove(sun)


"""Displaying and moving down the suns"""
def display_suns_and_move_them(screen_to_display: pygame.Surface):
    global suns_arr
    for sun in suns_arr:
        sun.move_sun_down()
        screen_to_display.blit(sun.image, sun.sun_rect.topleft)


# helper function for proper screen resize
def scale_to_fit(image, max_width, max_height):
    """Scale image to fill the screen while maintaining aspect ratio (may crop edges)"""
    original_width, original_height = image.get_size()
    ratio = max(max_width/original_width, max_height/original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    scaled = pygame.transform.smoothscale(image, (new_width, new_height))
    
    x = (new_width - max_width) // 2
    y = (new_height - max_height) // 2
    return scaled.subsurface((x, y, max_width, max_height))


def add_sun(screen_ref: pygame.Surface):
    global suns_arr
    suns_arr.append(Sun(screen_ref))
    threading.Timer(random.uniform(MIN_TIME_BETWEEN_SUNS, MAX_TIME_BETWEEN_SUNS), add_sun, args=(screen_ref,)).start()




background_image = scale_to_fit(original_background, window_width, window_height)
# start adding suns
add_sun(screen)
fade_in_play("Classic_cut.mp3", 100)


running = True
while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                check_sun_click(mouse_pos)

            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
            # resize the background image when the window is resized
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                background_image = scale_to_fit(original_background, window_width, window_height)
        

        screen.blit(background_image, (0, 0))
        screen.blit(pygame.font.Font(None, 50).render(f"Global score: {int(global_score)}", True, (255, 215, 0)), (10, 10))
        screen.blit(pygame.font.Font(None, 40).render(f"Suns Collected: {global_suns_counter}", True, (255, 215, 0)), (10, 70))
        represent_score_text()
        display_suns_and_move_them(screen)
        pygame.display.flip()

        clock.tick(60)
    except Exception as e:
        print(e)
