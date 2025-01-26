import pygame
import pyaudio
import numpy as np
import os
import time

pygame.init()

script_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(script_dir, 'empty.ico')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((500, 480))
pygame.display.set_caption("sprite")

sprite_dir = os.path.join(script_dir, 'sprite', 'pose', 'spider')

close_eyes_closed_mouth = pygame.image.load(os.path.join(sprite_dir, 'close_eyes_closed_mouse.png'))
close_eyes_open_mouth = pygame.image.load(os.path.join(sprite_dir, 'close_eyes_open_mouse.png'))
open_eyes_closed_mouth = pygame.image.load(os.path.join(sprite_dir, 'open_eyes_closed_mouse.png'))
open_eyes_open_mouth = pygame.image.load(os.path.join(sprite_dir, 'open_eyes_open_mouse.png'))

blink_interval = 5
last_blink_time = time.time()

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"{i}: {dev['name']}")

device_index = int(input("index: "))

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=chunk, input_device_index=device_index)

def detect_sound():
    data = np.frombuffer(stream.read(chunk), dtype=np.int16)
    peak = np.average(np.abs(data)) * 2
    return peak > 500  

running = True
eyes_open = True  
mouth_open = False  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()

    if current_time - last_blink_time >= blink_interval:
        eyes_open = False  
        screen.fill((255, 255, 255))  
        screen.blit(close_eyes_closed_mouth, (0, 0))  
        pygame.display.flip()  
        pygame.time.wait(200) 
        eyes_open = True 
        last_blink_time = current_time

    if detect_sound():
        mouth_open = True
    else:
        mouth_open = False

    if eyes_open and mouth_open:
        sprite = open_eyes_open_mouth
    elif eyes_open and not mouth_open:
        sprite = open_eyes_closed_mouth
    elif not eyes_open and mouth_open:
        sprite = close_eyes_open_mouth
    else:
        sprite = close_eyes_closed_mouth

    screen.fill((255, 255, 255)) 
    screen.blit(sprite, (0, 0)) 
    pygame.display.flip() 

    pygame.time.Clock().tick(30)

stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()