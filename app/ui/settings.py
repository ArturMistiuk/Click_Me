from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel, QComboBox, QApplication, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter

class Settings(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.background_image = QPixmap("resources/images/settings_background.png")
        self.init_ui()
        self.is_sound_muted = False  # Переменная для отслеживания состояния звука

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы по краям

        # Выпадающее меню для выбора разрешения экрана
        resolution_label = QLabel("Resolution:")
        resolution_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(resolution_label, alignment=Qt.AlignCenter)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItem("800x600")
        self.resolution_combo.addItem("1024x768")
        self.resolution_combo.addItem("1280x720")
        self.resolution_combo.addItem("1280x1024")
        self.resolution_combo.addItem("1366x768")
        self.resolution_combo.addItem("1440x900")
        self.resolution_combo.addItem("1600x900")
        self.resolution_combo.setCurrentText("1280x720")
        self.resolution_combo.setFont(QFont("Arial", 14))
        layout.addWidget(self.resolution_combo, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Флажок для выбора полноэкранного режима с надписью "OR F"
        fullscreen_layout = QHBoxLayout()
        fullscreen_label = QLabel("Fullscreen")
        fullscreen_label.setFont(QFont("Arial", 14))
        fullscreen_layout.addWidget(fullscreen_label)
        fullscreen_layout.setAlignment(Qt.AlignCenter)

        f_layout = QHBoxLayout()
        f_label = QLabel("or press 'F' in game")
        f_label.setFont(QFont("Arial", 14))
        f_layout.addWidget(f_label)
        f_layout.setAlignment(Qt.AlignCenter)

        self.fullscreen_checkbox = QCheckBox()
        self.fullscreen_checkbox.setFont(QFont("Arial", 14))
        fullscreen_layout.addWidget(self.fullscreen_checkbox)

        layout.addLayout(fullscreen_layout)
        layout.addLayout(f_layout)

        layout.addSpacing(20)

        # Надпись "Sound"
        sounds_label = QLabel("Sound:")
        sounds_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(sounds_label, alignment=Qt.AlignCenter)

        # Ползунок для регулировки громкости
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)  # Устанавливаем диапазон от 0 до 100
        self.volume_slider.setValue(15)  # Устанавливаем начальное значение громкости
        self.volume_slider.setFont(QFont("Arial", 14))
        self.volume_slider.setMinimumWidth(300)  # Устанавливаем минимальную ширину ползунка

        # Кнопка отключения всех звуков
        self.mute_button = QPushButton("Mute All Sounds")
        self.mute_button.setFont(QFont("Arial", 14))
        self.mute_button.clicked.connect(self.mute_all_sounds)  # Подключаем обработчик событий

        layout.addWidget(self.volume_slider, alignment=Qt.AlignCenter)
        layout.addWidget(self.mute_button, alignment=Qt.AlignCenter)

        layout.addSpacing(40)

        # Горизонтальный layout для кнопок
        button_layout = QVBoxLayout()

        # Кнопка сохранения настроек
        save_button = QPushButton("Save")
        save_button.setFont(QFont("Arial", 16))
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button, alignment=Qt.AlignHCenter)

        # Кнопка возврата в главное меню
        back_button = QPushButton("Back to Menu")
        back_button.setFont(QFont("Arial", 16))
        back_button.clicked.connect(self.back_to_menu)
        button_layout.addWidget(back_button, alignment=Qt.AlignHCenter)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

    def save_settings(self):
        fullscreen = self.fullscreen_checkbox.isChecked()

        if fullscreen:
            self.main_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.main_window.showFullScreen()
        else:
            self.main_window.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            resolution = self.resolution_combo.currentText()
            width, height = map(int, resolution.split('x'))
            self.main_window.setFixedSize(width, height)
            self.main_window.showNormal()
            self.main_window.center_on_screen()

        # Устанавливаем громкость на основе значения ползунка
        volume = self.volume_slider.value()
        if self.main_window.player is not None:
            self.main_window.player.setVolume(volume)

        # Обновляем окно для применения изменений флагов
        self.main_window.show()

    def back_to_menu(self):
        self.main_window.show_main_menu()

    def mute_all_sounds(self):
        if self.main_window.player is not None:
            if self.is_sound_muted:
                self.main_window.player.setVolume(15)  # Включаем звук
                self.is_sound_muted = False
                self.mute_button.setText("Mute All Sounds")  # Возвращаем текст кнопки
            else:
                self.main_window.player.setVolume(0)  # Выключаем звук
                self.is_sound_muted = True
                self.mute_button.setText("Unmute All Sounds")  # Изменяем текст кнопки
