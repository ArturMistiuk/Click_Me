from PyQt5.QtCore import QTimer, QObject, pyqtSignal


class ClickHandler(QObject):
    click_updated = pyqtSignal(int)

    DECREMENT_PERCENT = 0.07  # Значение уменьшения счетчика

    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_count = 60000
        self.click_multiplier = 1  # Коэффициент удвоения очков за клик

    def on_click(self):
        """Обрабатывает событие клика."""
        self.click_updated.emit(self.click_count)

    def reset_clicks(self):
        self.click_count = 0

    def apply_multiplier_upgrade(self):
        self.click_multiplier = self.click_multiplier * 2
        print(f"Click multiplier updated to {self.click_multiplier}")
