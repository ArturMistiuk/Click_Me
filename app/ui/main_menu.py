from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from ui.choosing_window import ChoosingWindow


class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Установка фонового изображения
        self.background_label = QLabel(self)
        pixmap = QPixmap('resources/images/main_menu_background.png')
        if pixmap.isNull():
            print("Failed to load background image.")
        else:
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)

        # Основной layout для всех элементов интерфейса
        main_layout = QVBoxLayout(self)

        # Добавляем пустое пространство сверху
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Добавляем логотип как кнопку с анимацией при наведении
        self.logo_button = ClickableImage('resources/images/logo.png', self)
        self.logo_button.clicked.connect(self.logo_clicked)

        # Создаем анимацию для логотипа при наведении и уходе
        self.hover_animation = QPropertyAnimation(self.logo_button, b"pos")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)

        def animate_logo_down():
            start_pos = self.logo_button.pos()
            end_pos = QPoint(start_pos.x(), start_pos.y() + 10)  # Смещаем вниз на 10 пикселей
            self.hover_animation.setStartValue(start_pos)
            self.hover_animation.setEndValue(end_pos)
            self.hover_animation.start()

        def animate_logo_up():
            start_pos = self.logo_button.pos()
            end_pos = QPoint(start_pos.x(), start_pos.y() - 10)  # Возвращаемся обратно на исходное место
            self.hover_animation.setStartValue(start_pos)
            self.hover_animation.setEndValue(end_pos)
            self.hover_animation.start()

        self.logo_button.enterEvent = lambda event: animate_logo_down()
        self.logo_button.leaveEvent = lambda event: animate_logo_up()

        main_layout.addWidget(self.logo_button, alignment=Qt.AlignCenter)

        # Добавляем пустое пространство между логотипом и кнопками
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Добавляем пустое пространство снизу
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка настроек в нижнем правом углу
        settings_button = QPushButton()
        settings_button.setIcon(QIcon('resources/images/settings_icon.png'))
        settings_button.setFixedSize(55, 55)  # Устанавливаем фиксированный размер кнопки
        settings_button.clicked.connect(self.open_settings)

        # Создаем горизонтальный layout для кнопки настроек и выравнивания внизу справа
        settings_button_layout = QHBoxLayout()
        settings_button_layout.addStretch()
        settings_button_layout.addWidget(settings_button)

        # Добавляем кнопку настроек в основной layout
        main_layout.addLayout(settings_button_layout)

        exit_button = QPushButton()
        exit_button.setIcon(QIcon('resources/images/exit_icon.png'))
        exit_button.setFixedSize(55, 55)  # Устанавливаем фиксированный размер кнопки
        exit_button.clicked.connect(QApplication.instance().quit)

        exit_button_layout = QHBoxLayout()
        exit_button_layout.addStretch()
        exit_button_layout.addWidget(exit_button)

        main_layout.addLayout(exit_button_layout)

        # Установка основного layout
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Растягиваем фоновое изображение на весь виджет
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def open_settings(self):
        self.main_window.show_settings()


    def logo_clicked(self):
        choosing_window = ChoosingWindow(self.main_window)

        # Добавляем новое окно в QStackedWidget главного окна
        self.main_window.stacked_widget.addWidget(choosing_window)
        self.main_window.stacked_widget.setCurrentWidget(choosing_window)

        # Закрываем текущее окно (главное меню)
        self.close()


class ClickableImage(QLabel):
    """ QLabel, которая является кликабельным изображением """
    clicked = pyqtSignal()

    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

