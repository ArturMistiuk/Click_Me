from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer
from ui.QProgressBar import ProgressBar
from ui.click_handler import ClickHandler
from ui.character import Character


class GameWindow(QWidget):
    def __init__(self, main_window, selected_character):
        super().__init__()
        self.main_window = main_window
        self.selected_character = selected_character
        self.character = self.load_character(selected_character)
        self.current_threshold = self.character.get_current_threshold()
        self.first_click_count = 0

        self.progress_bar = ProgressBar(self)
        self.click_handler = ClickHandler()
        self.click_handler.click_updated.connect(self.handle_click)

        # Устанавливаем курсоры
        self.init_cursors()

        self.init_ui()
        self.variant_timer = QTimer(self)
        self.variant_timer.timeout.connect(self.update_variant_image)

    def init_cursors(self):
        # Загрузите пути к изображениям курсоров
        path_to_cursor_image = "resources/images/cursor.png"
        path_to_grabbing_cursor_image = "resources/images/cursor_grab.png"

        # Создаем курсоры
        hand_pixmap = QPixmap(path_to_cursor_image).scaled(26, 26, Qt.KeepAspectRatio)
        self.hand_cursor = QCursor(hand_pixmap)

        grabbing_pixmap = QPixmap(path_to_grabbing_cursor_image).scaled(26, 26, Qt.KeepAspectRatio)
        self.grabbing_cursor = QCursor(grabbing_pixmap)

        # Устанавливаем курсор руки по умолчанию
        self.setCursor(self.hand_cursor)

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.progress_bar, 1)
        self.character_label = QLabel(self)
        self.character_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.character_label, 3)
        self.setLayout(layout)
        self.update_character_image()

        # Привязываем обработчики событий к character_label
        self.character_label.mousePressEvent = self.handle_character_mouse_press
        self.character_label.mouseReleaseEvent = self.handle_character_mouse_release



    def load_character(self, character_name):
        character_data = {
            "character_1": Character("character_1", [
                "resources/images/character_1/2.png",
                "resources/images/character_1/3.png",
                "resources/images/character_1/4.png",
                "resources/images/character_1/5.png",
                "resources/images/character_1/6.png",
                "resources/images/character_1/7.png",
                "resources/images/character_1/8.png",
                "resources/images/character_1/9.png",
                "resources/images/character_1/10.png",
                "resources/images/character_1/11.png",
                "resources/images/character_1/12.png",
            ], [70, 80, 90, 100, 110, 120, 150, 200, 230, 260, 50000], {
                3: [
                    "resources/images/character_1/5.png",
                    "resources/images/character_1/5(1).png",
                    "resources/images/character_1/5(2).png",
                    "resources/images/character_1/5(3).png",
                    "resources/images/character_1/5(4).png",
                    "resources/images/character_1/5(5).png",
                    "resources/images/character_1/5(6).png",
                ],
                4: [
                    "resources/images/character_1/6.png",
                    "resources/images/character_1/6(1).png",
                    "resources/images/character_1/6(2).png",
                    "resources/images/character_1/6(3).png",
                    "resources/images/character_1/6(4).png",
                    "resources/images/character_1/6(5).png",
                    "resources/images/character_1/6(6).png",
                    "resources/images/character_1/6(7).png",
                    "resources/images/character_1/6(8).png",
                    "resources/images/character_1/6(9).png",
                ],
                5: [
                    "resources/images/character_1/7.png",
                    "resources/images/character_1/7(1).png",
                    "resources/images/character_1/7(2).png",
                    "resources/images/character_1/7(3).png",
                    "resources/images/character_1/7(4).png",
                    "resources/images/character_1/7(5).png",
                    "resources/images/character_1/7(6).png",
                    "resources/images/character_1/7(7).png",
                    "resources/images/character_1/7(8).png",
                    "resources/images/character_1/7(9).png",
                    "resources/images/character_1/7(10).png",
                    "resources/images/character_1/7(11).png",
                ],
                6: [
                    "resources/images/character_1/8.png",
                ],
                7: [
                    "resources/images/character_1/9.png",
                    "resources/images/character_1/9(1).png",
                ],
                8: [
                    "resources/images/character_1/10.png",
                    "resources/images/character_1/10(1).png",
                    "resources/images/character_1/10(2).png",
                ],
                9: [
                    "resources/images/character_1/11.png",
                ],
                10: [
                    "resources/images/character_1/12.png",
                ]
            }),
            "character_2": Character("character_2", [
                "resources/images/character_2/1.png",
                "resources/images/character_2/2.png",
                "resources/images/character_2/3.png",
                "resources/images/character_2/4.png"
            ], [15, 25, 35]),
            "character_3": Character("character_3", [
                "resources/images/character_3/1.png",
                "resources/images/character_3/2.png",
                "resources/images/character_3/3.png",
                "resources/images/character_3/4.png"
            ], [20, 30, 40])
        }
        return character_data.get(character_name, None)

    def resizeEvent(self, event):
        progress_width_percent = 0.05
        progress_width = int(self.width() * progress_width_percent)
        progress_height = self.height()
        self.progress_bar.setFixedSize(progress_width, progress_height)
        self.update_character_image()
        super().resizeEvent(event)

    def update_character_image(self):
        try:
            if self.character:
                image_path = self.character.get_image_path()
                print(f"Updating image to: {image_path}")  # Для отладки
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio)
                self.character_label.setPixmap(pixmap)
            if self.character.current_stage in self.character.variant_images:
                self.start_variant_timer()
            else:
                self.stop_variant_timer()
        except Exception as e:
            print(f"Error updating character image: {e}")

    def handle_character_click(self, event):
        try:
            if self.first_click_count < 2:
                self.first_click_count += 1
                self.character.advance_stage()
                print(f"Character advanced to stage {self.character.current_stage}")  # Для отладки
                self.update_character_image()
            else:
                self.click_handler.on_click()
        except Exception as e:
            print(f"Error handling character click: {e}")

    def handle_click(self, clicks):
        try:
            progress = min(clicks / self.current_threshold * 100, 100)
            self.progress_bar.setValue(int(progress))

            if clicks >= self.current_threshold:
                self.character.advance_stage()
                print(
                    f"Progress bar filled, advancing character to stage {self.character.current_stage}")  # Для отладки
                self.update_character_image()
                self.click_handler.click_count = 0
                self.current_threshold = self.character.get_current_threshold()
                self.progress_bar.setValue(0)
        except Exception as e:
            print(f"Error handling click: {e}")

    def start_variant_timer(self):
        try:
            self.variant_timer.start(1000)
        except Exception as e:
            print(f"Error starting variant timer: {e}")

    def stop_variant_timer(self):
        try:
            self.variant_timer.stop()
        except Exception as e:
            print(f"Error stopping variant timer: {e}")

    def update_variant_image(self):
        try:
            if self.character.current_stage in self.character.variant_images:
                self.update_character_image()
        except Exception as e:
            print(f"Error updating variant image: {e}")

    def handle_character_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(self.grabbing_cursor)
        self.handle_character_click(event)

    def handle_character_mouse_release(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(self.hand_cursor)