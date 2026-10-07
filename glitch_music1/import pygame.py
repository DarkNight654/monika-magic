import pygame
import time

try:
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play()
    print("Đang phát thử nhạc, bạn có nghe thấy gì không?")
    time.sleep(10) # Chờ 10 giây để nghe thử
except Exception as e:
    print("Có lỗi xảy ra:", e)