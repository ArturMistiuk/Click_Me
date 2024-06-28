from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QPoint
from PyQt5.QtGui import QPixmap


class ChoosingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Установка фонового изображения
        self.background_label = QLabel(self)
        pixmap = QPixmap('resources/images/choosing_window_background.png')  # Путь к фоновому изображению
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
        hover_animation = QPropertyAnimation(button, b"pos")
        hover_animation.setDuration(200)
        hover_animation.setEasingCurve(QEasingCurve.OutCubic)

        def animate_down():
            start_pos = button.pos()
            end_pos = start_pos + QPoint(0, 10)  # Смещаем вниз на 10 пикселей
            hover_animation.setStartValue(start_pos)
            hover_animation.setEndValue(end_pos)
            hover_animation.start()

        def animate_up():
            start_pos = button.pos()
            end_pos = start_pos - QPoint(0, 10)  # Возвращаемся обратно на исходное место
            hover_animation.setStartValue(start_pos)
            hover_animation.setEndValue(end_pos)
            hover_animation.start()

        button.enterEvent = lambda event: animate_down()
        button.leaveEvent = lambda event: animate_up()


class ClickableImage(QLabel):
    """ QLabel, которая является кликабельным изображением """
    clicked = pyqtSignal()

    def __init__(self, image_path, size, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
