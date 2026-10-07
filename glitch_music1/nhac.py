import sys
import os
import time
import random
import math
import pygame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt6.QtGui import QFont, QMovie, QCursor
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMessageBox

try:
    pygame.mixer.init()
except Exception as e:
    print("Pygame mixer init error:", e)

current_dir = os.path.dirname(os.path.abspath(__file__))
music_path = os.path.join(current_dir, "music.mp3")
eyelid_path = os.path.join(current_dir, "eyelid.gif")
random_gif_path = os.path.join(current_dir, "random.gif")

app = QApplication(sys.argv)

if not os.path.exists(music_path):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText("Music file music.mp3 not found!")
    msg.setInformativeText(f"Please place 'music.mp3' in:\n{current_dir}")
    msg.exec()
    sys.exit()

bai_hat = [
    (14.0, 20.0, "If I told you you know how to go and break my heart in two"),
    (20.0, 27.0, "'Cause I would anyway, and end up like always"),
    (27.0, 33.0, "You know me, you better show me that you could say it to my face"),
    (33.0, 40.0, "'Cause you know we're the same, there's worse things I can take"),
    (42.0, 66.0, "♪ ------------------------------------ ♪"),
    (66.0, 73.0, "If I told you you know how to go and break my heart in two"),
    (73.0, 79.0, "'Cause I would anyway, and end up like always"),
    (79.0, 86.0, "You know me, you better show me that you could say it to my face"),
    (86.0, 93.0, "'Cause you know we're the same, there's worse things I can take")
]

class ImagePopupCard(QWidget):
    def __init__(self, start_time, end_time):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.card_size = 350  # Kích thước khung hình ở giữa
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self.card_size, self.card_size)
        
        # Đặt vị trí ở CHÍNH GIỮA màn hình
        screen = QApplication.primaryScreen().geometry()
        self.pos_x = (screen.width() - self.card_size) // 2
        self.pos_y = (screen.height() - self.card_size) // 2
        self.move(self.pos_x, self.pos_y)
        
        container = QWidget(self)
        container.setFixedSize(self.card_size, self.card_size)
        
        self.eyelid_label = QLabel(container)
        self.extra_space = 50
        self.eyelid_label.setGeometry(
            -self.extra_space // 2, 
            -self.extra_space // 2, 
            self.card_size + self.extra_space, 
            self.card_size + self.extra_space
        )
        self.eyelid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if os.path.exists(eyelid_path) and eyelid_path.endswith('.gif'):
            self.movie = QMovie(eyelid_path)
            self.movie.setScaledSize(self.eyelid_label.size())
            self.movie.setCacheMode(QMovie.CacheMode.CacheAll)
            self.movie.frameChanged.connect(self.update_gaze_direction)
            self.movie.start()
        else:
            self.eyelid_label.setText("Missing eyelid.gif!")
            self.eyelid_label.setStyleSheet("color: white; background-color: rgba(0,0,0,200); font-weight: bold;")

        self.setWindowOpacity(0.0)
        self.hide()

    def update_gaze_direction(self):
        if not hasattr(self, 'movie'):
            return
        pixmap = self.movie.currentPixmap()
        if pixmap.isNull():
            return
            
        abs_center_x = self.pos_x + self.card_size // 2
        abs_center_y = self.pos_y + self.card_size // 2
        cursor_pos = QCursor.pos()
        
        dx = cursor_pos.x() - abs_center_x
        dy = cursor_pos.y() - abs_center_y
        distance = math.hypot(dx, dy)
        
        max_offset = 25
        if distance > 0:
            offset_x = (dx / distance) * min(distance * 0.15, max_offset)
            offset_y = (dy / distance) * min(distance * 0.15, max_offset)
        else:
            offset_x, offset_y = 0, 0
            
        self.eyelid_label.move(
            int(-self.extra_space // 2 + offset_x), 
            int(-self.extra_space // 2 + offset_y)
        )
        self.eyelid_label.setPixmap(pixmap)

    def update_state(self, current_time):
        if current_time < self.start_time or current_time > self.end_time:
            if self.isVisible():
                self.hide()
            return
            
        if not self.isVisible():
            self.show()
            
        total_duration = self.end_time - self.start_time
        elapsed = current_time - self.start_time
        
        if elapsed < 1.0:
            opacity = elapsed / 1.0
        elif current_time > self.end_time - 1.5:
            opacity = (self.end_time - current_time) / 1.5
        else:
            opacity = 1.0
            
        self.setWindowOpacity(max(0.0, min(1.0, opacity)))

class RandomPopupGif(QWidget):
    def __init__(self):
        super().__init__()
        self.size_w = 280
        self.size_h = 280
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self.size_w, self.size_h)
        
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.size_w, self.size_h)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if os.path.exists(random_gif_path) and random_gif_path.endswith('.gif'):
            self.movie = QMovie(random_gif_path)
            self.movie.setScaledSize(self.label.size())
            self.movie.setCacheMode(QMovie.CacheMode.CacheAll)
            self.label.setMovie(self.movie)
            self.movie.start()
        else:
            self.label.setText("Extra GIF")
            self.label.setStyleSheet("color: white; background-color: black; border: none;")
            
        self.hide()
        self.active_until = 0

    def trigger_random_appear(self, current_time, duration=3.0):
        self.active_until = current_time + duration
        self.show()

    def update_state(self, current_time):
        if self.isVisible():
            if current_time >= self.active_until:
                self.hide()
                return
            cursor_pos = QCursor.pos()
            self.move(cursor_pos.x() - self.size_w // 2, cursor_pos.y() - self.size_h // 2)

class SmoothLyricCard(QWidget):
    def __init__(self, start_time, end_time, text, index):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
        self.index = index
        self.has_started = False
        self.offset_x = 0
        self.offset_y = 0
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.card_size = 250
        self.resize(self.card_size, self.card_size)
        
        screen = QApplication.primaryScreen().geometry()
        min_x = 50
        max_x = screen.width() - self.card_size - 50
        self.base_x = random.randint(min_x, max(min_x, max_x))
        self.start_y = screen.height() - 100
        self.target_y = screen.height() - 300
        self.move(self.base_x, self.start_y)
        
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.card_size, self.card_size)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Impact", 13, QFont.Weight.Bold))
        
        duration_ms = int((self.end_time - self.start_time) * 1000)
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(max(1500, duration_ms))
        self.anim.setStartValue(QPoint(self.base_x, self.start_y))
        self.anim.setEndValue(QPoint(self.base_x, self.target_y))
        
        self.setWindowOpacity(0.0)
        self.hide()

    def update_label_style(self, is_inverted, is_glitching):
        if is_glitching:
            is_inverted = random.choice([True, False])
        bg_color = "rgba(255, 255, 255, 250)" if is_inverted else "rgba(10, 10, 10, 250)"
        text_color = "#000000" if is_inverted else "#FFFFFF"
        self.label.setStyleSheet(f"background-color: {bg_color}; color: {text_color}; padding: 12px;")

    def update_state(self, current_time):
        if current_time < self.start_time or current_time > self.end_time:
            if self.isVisible():
                self.hide()
            return
        if not self.isVisible():
            self.show()
        if not self.has_started:
            self.has_started = True
            self.anim.start()
            
        total_duration = self.end_time - self.start_time
        elapsed = current_time - self.start_time
        progress = elapsed / total_duration if total_duration > 0 else 1.0
        
        opacity = progress / 0.15 if progress < 0.15 else ((1.0 - progress) / 0.20 if progress > 0.80 else 1.0)
        self.setWindowOpacity(max(0.0, min(1.0, opacity)))
            
        current_pos = self.anim.currentValue()
        is_glitching = False
        if current_pos:
            target_x, target_y = current_pos.x(), current_pos.y()
            mouse_pos = QCursor.pos()
            dist_x = mouse_pos.x() - (target_x + self.card_size // 2)
            dist_y = mouse_pos.y() - (target_y + self.card_size // 2)
            distance = math.hypot(dist_x, dist_y)
            
            if distance < 180 and distance > 0:
                is_glitching = True
                push = (180 - distance) * 1.2
                self.offset_x -= (dist_x / distance) * push
                self.offset_y -= (dist_y / distance) * push
            else:
                self.offset_x *= 0.85
                self.offset_y *= 0.85
                
            glitch_range = 25 if is_glitching else 4
            gx = random.randint(-glitch_range, glitch_range) if (is_glitching or random.random() < 0.2) else 0
            gy = random.randint(-glitch_range, glitch_range) if (is_glitching or random.random() < 0.2) else 0
            super().move(int(target_x + self.offset_x + gx), int(target_y + self.offset_y + gy))
            
        self.update_label_style(int(current_time * 2.5) % 2 == 0, is_glitching)
        
        typing_progress = min(1.0, progress / 0.2)
        char_count = int(len(self.text) * typing_progress)
        current_substr = self.text[:char_count]
        cursor = "_" if int(current_time * 6) % 2 == 0 else " "
        self.label.setText(current_substr + cursor)

def main():
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
    except Exception as e:
        print("Playback error:", e)
        sys.exit()

    bat_dau_phat = time.time()
    image_card = ImagePopupCard(bai_hat[0][0], bai_hat[-1][1])
    lyric_cards = [SmoothLyricCard(start, end, text, i) for i, (start, end, text) in enumerate(bai_hat)]
    random_gif_popup = RandomPopupGif()
    next_random_trigger = time.time() + 1.0

    def update_lyrics():
        nonlocal next_random_trigger
        try:
            current_time = pygame.mixer.music.get_pos() / 1000.0
            if current_time < 0:
                current_time = time.time() - bat_dau_phat
        except Exception:
            current_time = time.time() - bat_dau_phat

        image_card.update_state(current_time)
        random_gif_popup.update_state(current_time)
        for card in lyric_cards:
            card.update_state(current_time)

        if current_time >= next_random_trigger:
            random_gif_popup.trigger_random_appear(current_time, duration=random.uniform(3.0, 6.0))
            next_random_trigger = current_time + random.uniform(4.0, 6.0)

        music_busy = True
        try:
            music_busy = pygame.mixer.music.get_busy()
        except Exception:
            pass

        if (not music_busy and current_time > bai_hat[-1][1]) or current_time > bai_hat[-1][1] + 5.0:
            timer.stop()
            try:
                import ctypes
                hwnd = ctypes.windll.user32.FindWindowW(None, "DDLC")
                if not hwnd:
                    hwnd = ctypes.windll.user32.FindWindowW(None, "Monika After Story")
                if hwnd:
                    ctypes.windll.user32.ShowWindow(hwnd, 9)
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
            except Exception:
                pass
            app.quit()

    timer = QTimer()
    timer.timeout.connect(update_lyrics)
    timer.start(25)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()