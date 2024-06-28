from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication, QDesktopWidget
from ui.main_menu import MainMenu
from ui.settings import Settings
from ui.choosing_window import ChoosingWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click Me")
        self.setFixedSize(1280, 720)
        self.center_on_screen()  # Центрируем окно на экране

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self)
        self.settings = Settings(self)
        self.choosing_window = ChoosingWindow(self)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings)
        self.stacked_widget.addWidget(self.choosing_window)

        self.show_main_menu()

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings)

    def center_on_screen(self):
        # Получаем геометрию основного экрана
        screen_geometry = QApplication.desktop().screenGeometry()

        # Центрируем окно относительно основного экрана
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)
