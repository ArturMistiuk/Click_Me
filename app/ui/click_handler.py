from PyQt5.QtCore import QTimer


class ClickHandler:
    def __init__(self, click_label, progress_bar):
        self.click_label = click_label
        self.progress_bar = progress_bar
        self.click_count = 0
        self.progress_value = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def on_click(self):
        self.click_count += 1
        self.click_label.setText(f"Clicks: {self.click_count}")
        self.progress_value += 3  # Увеличиваем значение прогресса за клик
        self.progress_bar.setValue(self.progress_value)

    def update_progress(self):
        if self.progress_value > 0:
            self.progress_value -= 1  # Уменьшаем значение прогресса со временем
        self.progress_bar.setValue(self.progress_value)

    def get_timer(self):
        return self.timer
