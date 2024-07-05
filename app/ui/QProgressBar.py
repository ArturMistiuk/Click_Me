# progressbar.py
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Qt


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Vertical)

        # Настройка стилей для кастомизации ProgressBar
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid red; /* Красная граница */
                border-radius: 5px; /* Скругленные углы */
                background-color: white; /* Цвет фона внутренней части */
                text-align: center; /* Выравнивание текста (если требуется) */
            }
            QProgressBar::chunk {
                background-color: pink; /* Розовая полоса заполнения */
                border-radius: 5px; /* Скругленные углы для заполненной части */
            }
        """)

        self.setMaximum(100)
