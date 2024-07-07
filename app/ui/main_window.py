import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication, QMessageBox
from ui.main_menu import MainMenu
from ui.settings import Settings
from ui.choosing_window import ChoosingWindow
from ui.game_window import GameWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click Me")
        self.setFixedSize(1280, 720)
        self.center_on_screen()

        self.setCursor(Qt.PointingHandCursor)  # Устанавливаем курсор руки по умолчанию
        grabbing_pixmap = QPixmap("resources/images/grab.png").scaled(16, 16, Qt.KeepAspectRatio)
        self.grabbing_cursor = QCursor(grabbing_pixmap)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self)
        self.settings = Settings(self)
        self.choosing_window = ChoosingWindow(self)  # Инициализируем окно выбора персонажа

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings)
        self.stacked_widget.addWidget(self.choosing_window)  # Добавляем окно выбора персонажа в stacked widget

        self.init_music()
        self.show_main_menu()

    def init_music(self):
        self.playlist = QMediaPlaylist()
        current_directory = os.getcwd()
        media_path = os.path.join(current_directory, "resources", "sounds", "County_Lines_-_Telecasted.mp3")
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(media_path)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(15)
        self.player.play()


    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings)

    def show_choosing_window(self):
        self.stacked_widget.setCurrentWidget(self.choosing_window)

    def show_game_window(self, selected_character):
        # Создаем окно игры с выбранным персонажем и переходим к нему
        game_window = GameWindow(self, selected_character)
        self.stacked_widget.addWidget(game_window)
        self.stacked_widget.setCurrentWidget(game_window)

    def center_on_screen(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape:
            if self.stacked_widget.currentWidget() == self.main_menu:
                self.close_application()
            else:
                self.show_main_menu()

    def close_application(self):
        reply = QMessageBox.question(self, 'Exit Game',
                                     "Are you sure you want to exit the game?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
