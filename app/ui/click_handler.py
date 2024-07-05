from PyQt5.QtCore import QTimer, QObject, pyqtSignal


class ClickHandler(QObject):
    click_updated = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_count = 0
        self.decrement_value = 5
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)  # Интервал таймера в миллисекундах

    def on_click(self):
        self.click_count += 1
        self.click_updated.emit(self.click_count)

    def update_progress(self):
        self.click_count = max(0, self.click_count - self.decrement_value)
        self.click_updated.emit(self.click_count)
