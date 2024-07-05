from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from ui.game_window import GameWindow  # Импортируем окно игры

class ChoosingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Установка фонового изображения
        self.background_label = QLabel(self)
        pixmap = QPixmap('resources/images/choosing_window_background.png')
        if pixmap.isNull():
            print("Failed to load background image.")
        else:
            self.background_label.setPixmap(pixmap)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Добавляем пространство сверху
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Добавляем пространство слева
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Размер кнопок в процентах от текущего размера окна
        button_size_percent = 0.5  # Процент от ширины окна
        button_size = int(self.main_window.width() * button_size_percent)

        # Создаем три кнопки-изображения
        self.button1 = ClickableImage('resources/images/character_1/choice_button.png', button_size, self)
        self.button2 = ClickableImage('resources/images/character_2/choice_button.png', button_size, self)
        self.button3 = ClickableImage('resources/images/character_3/choice_button.png', button_size, self)

        button_layout.addWidget(self.button1, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.button2, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.button3, alignment=Qt.AlignCenter)

        # Добавляем пространство справа
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Добавляем пространство снизу
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Устанавливаем анимацию при наведении для всех кнопок
        self.setup_animation(self.button1)
        self.setup_animation(self.button2)
        self.setup_animation(self.button3)

        # Добавляем кнопку выхода
        exit_button = QPushButton()
        exit_button.setIcon(QIcon('resources/images/exit_icon.png'))
        exit_button.setFixedSize(55, 55)  # Устанавливаем фиксированный размер кнопки
        exit_button.clicked.connect(self.back_to_menu)

        exit_button_layout = QHBoxLayout()
        exit_button_layout.addStretch()
        exit_button_layout.addWidget(exit_button)

        layout.addLayout(exit_button_layout)

        # Соединяем сигналы клика на кнопках с обработчиком перехода к игре
        self.button1.clicked.connect(lambda: self.start_game("character_1"))
        self.button2.clicked.connect(lambda: self.start_game("character_2"))
        self.button3.clicked.connect(lambda: self.start_game("character_3"))

    def back_to_menu(self):
        self.main_window.show_main_menu()

    def start_game(self, character_name):
        # Создаем окно игры с выбранным персонажем и переходим к нему
        self.main_window.show_game_window(character_name)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Растягиваем фоновое изображение на весь виджет
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Обновляем размеры кнопок при изменении размеров окна
        button_size_percent = 0.5  # Процент от ширины окна
        button_size = int(self.main_window.width() * button_size_percent)
        self.button1.setFixedSize(button_size, button_size)
        self.button2.setFixedSize(button_size, button_size)
        self.button3.setFixedSize(button_size, button_size)

    def setup_animation(self, button):
        button.animation = QPropertyAnimation(button, b"pos")
        button.animation.setDuration(20)
        button.animation.setEasingCurve(QEasingCurve.OutCubic)

        def animate_button():
            if button.animation.state() == QPropertyAnimation.Running:
                button.animation.stop()
            start_pos = button.pos()
            if button.hovered:
                end_pos = start_pos - QPoint(0, 5)  # Смещаем вверх на 5 пикселей при наведении
            else:
                end_pos = start_pos + QPoint(0, 5)  # Возвращаемся обратно на 5 пикселей при уходе
            button.animation.setStartValue(start_pos)
            button.animation.setEndValue(end_pos)
            button.animation.start()

        button.hovered = False

        def on_enter(event):
            button.hovered = True
            animate_button()

        def on_leave(event):
            button.hovered = False
            animate_button()

        button.enterEvent = on_enter
        button.leaveEvent = on_leave

        button.animation.finished.connect(lambda: button.setGeometry(button.pos().x(), button.pos().y(), button.width(), button.height()))


class ClickableImage(QLabel):
    clicked = pyqtSignal()  # Определение собственного сигнала clicked

    def __init__(self, image_path, size, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Вызываем сигнал clicked при клике на изображение
        super().mousePressEvent(event)
