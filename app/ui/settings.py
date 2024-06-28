from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel, QComboBox, QApplication
from PyQt5.QtCore import Qt


class Settings(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок настроек
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Оконный или полный экран
        self.fullscreen_checkbox = QCheckBox("Fullscreen")
        layout.addWidget(self.fullscreen_checkbox)

        # Добавляем выпадающее меню для выбора разрешения экрана
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItem("800x600")
        self.resolution_combo.addItem("1024x768")
        self.resolution_combo.addItem("1280x720")
        self.resolution_combo.addItem("1280x1024")
        self.resolution_combo.addItem("1366x768")
        self.resolution_combo.addItem("1440x900")
        self.resolution_combo.addItem("1600x900")
        self.resolution_combo.setCurrentText("1280x720")
        layout.addWidget(self.resolution_combo)

        # Кнопка сохранения настроек
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Кнопка возврата в главное меню
        back_button = QPushButton("Back to Menu")
        back_button.clicked.connect(self.back_to_menu)
        layout.addWidget(back_button)

        self.setLayout(layout)

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

        # Обновляем окно для применения изменений флагов
        self.main_window.show()

    def back_to_menu(self):
        self.main_window.show_main_menu()

