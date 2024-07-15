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
        """Инициализация пользовательского интерфейса."""
        self.setup_background()
        main_layout = QVBoxLayout(self)

        # Добавляем пустое пространство сверху
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Добавляем логотип как кнопку с анимацией при наведении
        self.setup_logo(main_layout)

        # Добавляем пустое пространство между логотипом и кнопками
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Добавляем пустое пространство снизу
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки настроек и выхода внизу справа
        self.add_icon_button(main_layout, 'resources/images/settings_icon.png', self.open_settings)
        self.add_icon_button(main_layout, 'resources/images/exit_icon.png', QApplication.instance().quit)

        self.setLayout(main_layout)

    def setup_background(self):
        """Настройка фонового изображения."""
        self.background_label = QLabel(self)
        pixmap = QPixmap('resources/images/main_menu_background.png')
        if pixmap.isNull():
            print("Failed to load background image.")
        else:
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)

    def setup_logo(self, layout):
        """Настройка логотипа с анимацией."""
        self.logo_button = ClickableImage('resources/images/logo.png', self)
        self.logo_button.clicked.connect(self.logo_clicked)

        self.hover_animation = QPropertyAnimation(self.logo_button, b"pos")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)

        self.logo_button.enterEvent = lambda event: self.animate_logo(10)
        self.logo_button.leaveEvent = lambda event: self.animate_logo(-10)

        layout.addWidget(self.logo_button, alignment=Qt.AlignCenter)

    def animate_logo(self, offset):
        """Анимация логотипа при наведении и уходе."""
        start_pos = self.logo_button.pos()
        end_pos = QPoint(start_pos.x(), start_pos.y() + offset)
        self.hover_animation.setStartValue(start_pos)
        self.hover_animation.setEndValue(end_pos)
        self.hover_animation.start()

    def add_icon_button(self, layout, icon_path, callback):
        """Добавление кнопки с иконкой и обратным вызовом."""
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setFixedSize(55, 55)
        button.clicked.connect(callback)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)

        layout.addLayout(button_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Растягиваем фоновое изображение на весь виджет
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def open_settings(self):
        """Открытие окна настроек."""
        self.main_window.show_settings()

    def logo_clicked(self):
        """Обработчик клика по логотипу."""
        choosing_window = ChoosingWindow(self.main_window)
        self.main_window.stacked_widget.addWidget(choosing_window)
        self.main_window.stacked_widget.setCurrentWidget(choosing_window)
        self.close()

class ClickableImage(QLabel):
    """QLabel, которая является кликабельным изображением."""
    clicked = pyqtSignal()

    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
