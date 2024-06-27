from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel
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

        # Example: Applying fullscreen settings
        if fullscreen:
            self.main_window.showFullScreen()
        else:
            self.main_window.showNormal()  # Show in normal mode

    def back_to_menu(self):
        self.main_window.show_main_menu()

# Example usage in a main application window
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QLabel

    app = QApplication(sys.argv)
    main_window = QWidget()
    settings_window = Settings(main_window)
    main_window.setFixedSize(400, 300)  # Example size for the main window
    main_window.show()
    sys.exit(app.exec_())
