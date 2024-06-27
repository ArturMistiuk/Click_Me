from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

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

        # Добавляем логотип вместо названия игры
        logo_label = QLabel(self)
        logo_pixmap = QPixmap('resources/images/logo.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(logo_label)
        else:
            # Если изображение логотипа не удалось загрузить
            title = QLabel("Hentai Clicker")
            title.setStyleSheet("font-size: 24px; font-weight: bold;")
            title.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(title)

        # Добавляем пустое пространство между логотипом и кнопками
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка старта игры
        start_button = QPushButton("Start Game")
        start_button.setFixedSize(200, 50)  # Устанавливаем фиксированный размер кнопки
        start_button.clicked.connect(self.start_game)

        # Создаем горизонтальный layout для кнопки старта игры и выравнивания по центру
        start_button_layout = QHBoxLayout()
        start_button_layout.addStretch()
        start_button_layout.addWidget(start_button)
        start_button_layout.addStretch()
        main_layout.addLayout(start_button_layout)

        # Добавляем пустое пространство между кнопками
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

        # Установка основного layout
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Растягиваем фоновое изображение на весь виджет
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def start_game(self):
        # Здесь будет код для начала игры
        pass

    def open_settings(self):
        self.main_window.show_settings()
