import os
import random

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, QSoundEffect
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication, QMessageBox
from ui.main_menu import MainMenu
from ui.settings import Settings
from ui.choosing_window import ChoosingWindow
from ui.game_window import GameWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click Me")
        main_icon = QIcon("resources/images/logo_icon.png")
        self.setWindowIcon(main_icon)
        self.setFixedSize(1280, 720)
        self.center_on_screen()
        self.setup_cursors()
        self.setup_ui()
        self.init_music()
        self.init_sounds()
        self.show_main_menu()

    def setup_cursors(self):
        """Настройка курсоров."""
        self.setCursor(Qt.PointingHandCursor)
        grabbing_pixmap = QPixmap("resources/images/grab.png").scaled(16, 16, Qt.KeepAspectRatio)
        self.grabbing_cursor = QCursor(grabbing_pixmap)

    def setup_ui(self):
        """Настройка пользовательского интерфейса."""
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self)
        self.settings = Settings(self)
        self.choosing_window = ChoosingWindow(self)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings)
        self.stacked_widget.addWidget(self.choosing_window)

    def init_music(self):
        """Инициализация музыкального плеера."""
        self.playlist = QMediaPlaylist()
        media_path = os.path.join(os.getcwd(), "resources", "sounds", "County_Lines_-_Telecasted.mp3")
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(media_path)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(15)
        self.player.play()

    def init_sounds(self):
        """Инициализация звуковых эффектов."""
        self.effects_volume = 80
        self.effect_sounds = {}

        self.image_to_sound_map = {
            "1.png": "text_sound.wav",
            "2.png": "text_sound.wav",
            "3.png": "text_sound.wav",
            "4_1.png": "text_sound.wav",
            "8_1.png": "text_sound.wav",
            "10_3.png": "text_sound.wav",
            "11_1.png": "text_sound.wav",
        }
        self.load_effect_sound("click", "click_sound.wav")
        self.load_effect_sound("purchase", "shop_purchase.wav")

        characters = [f"character_{number}" for number in range(1, 3 + 1)]
        moan_files = [f"moan_{number}.wav" for number in range(1, 8 + 1)]

        for char in characters:
            for moan in moan_files:
                self.load_effect_sound(f"{char}_{moan}", f"voice/{char}/{moan}")


    def load_effect_sound(self, sound_name, sound_file):
        """Загрузка звукового эффекта."""
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(os.path.join("resources", "sounds", sound_file)))
        effect.setVolume(self.effects_volume / 100.0)
        self.effect_sounds[sound_name] = effect

    def set_effects_volume(self, volume):
        """Установка громкости звуковых эффектов."""
        self.effects_volume = volume
        for sound in self.effect_sounds.values():
            sound.setVolume(self.effects_volume / 100.0)

    def play_effect_sound(self, sound_file):
        """Воспроизведение звукового эффекта."""
        if sound_file not in self.effect_sounds:
            self.load_effect_sound(sound_file, sound_file)
        self.effect_sounds[sound_file].play()

    def on_image_change(self, image):
        """Обработчик смены изображения."""
        if image in self.image_to_sound_map:
            self.play_effect_sound(self.image_to_sound_map[image])

    def show_main_menu(self):
        """Показ главного меню."""
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_settings(self):
        """Показ настроек."""
        self.stacked_widget.setCurrentWidget(self.settings)

    def show_game_window(self, selected_character):
        """Показ окна игры с выбранным персонажем."""
        game_window = GameWindow(self, selected_character)
        self.stacked_widget.addWidget(game_window)
        self.stacked_widget.setCurrentWidget(game_window)

    def center_on_screen(self):
        """Центрирование окна на экране."""
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        """Обработчик нажатия клавиш."""
        if event.key() == Qt.Key_F:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_Escape:
            self.handle_escape_key()

    def toggle_fullscreen(self):
        """Переключение полноэкранного режима."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def handle_escape_key(self):
        """Обработка нажатия клавиши Escape."""
        if self.stacked_widget.currentWidget() == self.main_menu:
            self.close_application()
        else:
            self.show_main_menu()

    def close_application(self):
        """Закрытие приложения с подтверждением."""
        reply = QMessageBox.question(self, 'Exit Game', "Are you sure you want to exit the game?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
