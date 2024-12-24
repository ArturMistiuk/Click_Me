import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from ui.game_window import GameWindow  # Импортируем окно игры

BUTTON_SIZE_PERCENT = 0.5
BACKGROUND_IMAGE_PATH = 'resources/images/choosing_window_background.png'
EXIT_ICON_PATH = 'resources/images/exit_icon.png'
CHARACTER_IMAGES = [
    'resources/images/character_1/choice_button.png',
    'resources/images/character_2/choice_button.png',
    'resources/images/character_3/choice_button.png'
]
EXIT_BUTTON_SIZE = 55

class ChoosingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setup_background()
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.create_buttons(button_layout)

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.create_exit_button(layout)

    def setup_background(self):
        self.background_label = QLabel(self)
        pixmap = QPixmap(BACKGROUND_IMAGE_PATH)
        if pixmap.isNull():
            print("Failed to load background image.")
        else:
            self.background_label.setPixmap(pixmap)

    def create_buttons(self, button_layout):
        button_size = int(self.main_window.width() * BUTTON_SIZE_PERCENT)

        self.buttons = []
        for image_path in CHARACTER_IMAGES:
            button = ClickableImage(image_path, button_size, self)
            self.setup_animation(button)
            button_layout.addWidget(button, alignment=Qt.AlignCenter)
            self.buttons.append(button)

        self.buttons[0].clicked.connect(lambda: self.start_game("character_1"))
        self.buttons[1].clicked.connect(self.show_coming_soon_message)
        self.buttons[2].clicked.connect(lambda: self.start_game("character_3"))

    def create_exit_button(self, layout):
        exit_button = QPushButton()
        exit_button.setIcon(QIcon(EXIT_ICON_PATH))
        exit_button.setFixedSize(EXIT_BUTTON_SIZE, EXIT_BUTTON_SIZE)
        exit_button.clicked.connect(self.back_to_menu)

        exit_button_layout = QHBoxLayout()
        exit_button_layout.addStretch()
        exit_button_layout.addWidget(exit_button)
        layout.addLayout(exit_button_layout)

    def back_to_menu(self):
        self.main_window.show_main_menu()

    def start_game(self, character_name):
        self.main_window.show_game_window(character_name)

    def show_coming_soon_message(self):
        QMessageBox.information(self, "Coming Soon", "Still in the works, darling!")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.update_button_sizes()

    def update_button_sizes(self):
        button_size = int(self.main_window.width() * BUTTON_SIZE_PERCENT)
        for button in self.buttons:
            button.setFixedSize(button_size, button_size)

    def setup_animation(self, button):
        button.animation = QPropertyAnimation(button, b"pos")
        button.animation.setDuration(20)
        button.animation.setEasingCurve(QEasingCurve.OutCubic)

        def animate_button():
            if button.animation.state() == QPropertyAnimation.Running:
                button.animation.stop()
            start_pos = button.pos()
            end_pos = start_pos - QPoint(0, 5) if button.hovered else start_pos + QPoint(0, 5)
            button.animation.setStartValue(start_pos)
            button.animation.setEndValue(end_pos)
            button.animation.start()

        button.hovered = False

        button.enterEvent = lambda event: self.on_button_hover(button, animate_button, True)
        button.leaveEvent = lambda event: self.on_button_hover(button, animate_button, False)
        button.animation.finished.connect(lambda: button.setGeometry(button.pos().x(), button.pos().y(), button.width(), button.height()))

    def on_button_hover(self, button, animate_button, is_hovered):
        button.hovered = is_hovered
        animate_button()

class ClickableImage(QLabel):
    clicked = pyqtSignal()

    def __init__(self, image_path, size, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        self.setPixmap(pixmap)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)