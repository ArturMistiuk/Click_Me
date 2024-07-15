import os.path
import random
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QCursor, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer

from ui.QProgressBar import ProgressBar
from ui.click_handler import ClickHandler
from ui.character import Character
from ui.character_data import character_data
from ui.shop import ShopWidget
from ui.settings import Settings


MOAN_CHANCE_PERCENT = 0.08


class GameWindow(QWidget):
    def __init__(self, main_window, selected_character):
        super().__init__()
        self.main_window = main_window
        self.selected_character = selected_character
        self.character = self.load_character(selected_character)
        self.current_threshold = self.character.get_current_threshold() if self.character else 0
        self.first_click_count = 0

        self.passive_income = 5  # Сколько очков даёт пассивный доход
        self.passive_income_timer = QTimer(self)
        self.passive_income_timer.timeout.connect(self.give_passive_income)

        self.decrement_chance = 34

        self.progress_bar = ProgressBar(self)
        self.click_handler = ClickHandler()
        self.click_handler.click_updated.connect(self.handle_click)

        self.shop_button = QPushButton(self)
        shop_icon = QIcon('resources/images/shop.ico')
        self.shop_button.setIcon(shop_icon)
        self.shop_button.setIconSize(shop_icon.actualSize(self.shop_button.size()))
        self.shop_button.clicked.connect(self.open_shop)

        self.shop_menu = ShopWidget(self)
        self.shop_menu.hide()
        self.shop_menu.upgrade_purchased.connect(self.purchase_upgrade)  # Правильный метод

        settings_icon = QIcon('resources/images/settings_icon.png')
        self.settings_button = QPushButton(self)  # Добавляем кнопку настроек
        self.settings_button.setIcon(settings_icon)
        self.settings_button.clicked.connect(self.open_settings)  # Подключаем слот

        self.init_cursors()
        self.init_ui()

        self.temp_label = QLabel(self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        self.temp_label.hide()

        self.score_label = QLabel(self)
        self.score_label.setAlignment(Qt.AlignTop)
        self.score_label.setStyleSheet("font-weight: bold; font-size: 28px; color: yellow;")
        self.update_score_label(0)
        self.score_label.hide()

        self.variant_timer = QTimer(self)
        self.variant_timer.timeout.connect(self.update_variant_image)


    def init_cursors(self):
        try:
            path_to_cursor_image = "resources/images/cursor.png"
            path_to_grabbing_cursor_image = "resources/images/cursor_grab.png"

            hand_pixmap = QPixmap(path_to_cursor_image).scaled(26, 26, Qt.KeepAspectRatio)
            self.hand_cursor = QCursor(hand_pixmap)

            grabbing_pixmap = QPixmap(path_to_grabbing_cursor_image).scaled(26, 26, Qt.KeepAspectRatio)
            self.grabbing_cursor = QCursor(grabbing_pixmap)

            self.setCursor(self.hand_cursor)
        except Exception as e:
            print(f"Error initializing cursors: {e}")

    def init_ui(self):
        try:
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(self.progress_bar, 0)

            self.character_label = QLabel(self)
            self.character_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.character_label, 1)
            self.setLayout(layout)
            self.update_character_image()

            self.character_label.mousePressEvent = self.handle_character_mouse_press
            self.character_label.mouseReleaseEvent = self.handle_character_mouse_release

            self.shop_button.raise_()
            self.shop_menu.raise_()
            self.settings_button.raise_()

        except Exception as e:
            print(f"Error initializing UI: {e}")

    def load_character(self, character_name):
        try:
            character_info = character_data.get(character_name)
            if character_info:
                return Character(**character_info)
            else:
                raise ValueError(f"Character '{character_name}' not found in character_data.py")
        except Exception as e:
            print(f"Error loading character '{character_name}' from character_data.py: {e}")

    def resizeEvent(self, event):
        try:
            progress_width_percent = 0.05
            progress_width = int(self.width() * progress_width_percent)
            progress_height = self.height()
            self.progress_bar.setFixedSize(progress_width, progress_height)

            self.shop_button.setFixedSize(100, 50)
            self.shop_button.move(self.width() - self.shop_button.width() - 10, 10)

            self.shop_menu.setFixedSize(self.width() // 4, self.height())

            self.settings_button.setFixedSize(100, 50)  # Настраиваем размеры кнопки настроек
            self.settings_button.move(self.width() - self.settings_button.width() - 10, self.height() - self.settings_button.height() - 10)  # Размещаем кнопку в правом нижнем углу

            super().resizeEvent(event)

            self.update_character_image()
        except Exception as e:
            print(f"Error resizing window: {e}")

    def open_shop(self):
        try:
            self.shop_menu.move(self.width() - self.shop_menu.width(), 0)
            self.shop_menu.show()
        except Exception as e:
            print(f"Error opening shop: {e}")

    def open_settings(self):
        try:
            self.settings_window = Settings(self.main_window)  # Создаем окно настроек
            self.settings_window.show()  # Показываем окно настроек
        except Exception as e:
            print(f"Error opening settings: {e}")

    def update_character_image(self):
        try:
            if self.character:
                image_path = self.character.get_image_path()
                print(f"Updating image to: {image_path}")
                image_name = os.path.basename(image_path)
                self.main_window.on_image_change(image_name)
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio)
                self.character_label.setPixmap(pixmap)
                if self.character.current_stage in self.character.variant_images:
                    self.start_variant_timer()
                else:
                    self.stop_variant_timer()
        except Exception as e:
            print(f"Error updating character image: {e}")

    def handle_character_mouse_press(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.setCursor(self.grabbing_cursor)
                self.main_window.play_effect_sound("click")
                self.handle_character_click(event)
                if random.random() < MOAN_CHANCE_PERCENT:
                    self.main_window.play_effect_sound(f"{self.selected_character}_moan_{random.randint(1, 5)}.wav")
        except Exception as e:
            print(f"Error handling character mouse press: {e}")

    def handle_character_mouse_release(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.setCursor(self.hand_cursor)
        except Exception as e:
            print(f"Error handling character mouse release: {e}")

    def handle_character_click(self, event):
        try:
            if self.first_click_count < 2:
                self.first_click_count += 1
                self.character.advance_stage()
                print(f"Character advanced to stage {self.character.current_stage}")
                self.update_character_image()
            else:
                self.click_handler.on_click()
        except Exception as e:
            print(f"Error handling character click: {e}")

    def handle_click(self, clicks):
        try:
            progress = min(clicks / self.current_threshold * 100, 100)
            self.progress_bar.setValue(int(progress))

            if random.random() < self.decrement_chance / 100:
                decrement_amount = int(self.progress_bar.value() * self.click_handler.DECREMENT_PERCENT)
                self.progress_bar.setValue(max(0, self.progress_bar.value() - decrement_amount))
                self.show_temp_label(f"-{decrement_amount}", QColor("red"))
            else:
                points_per_click = 1 * self.click_handler.click_multiplier
                self.update_score(points_per_click)
                self.show_temp_label(f"+{points_per_click}", QColor("green"))

            if clicks >= self.current_threshold:
                self.character.advance_stage()
                print(f"Progress bar filled, advancing character to stage {self.character.current_stage}")
                self.update_character_image()
                self.current_threshold = self.character.get_current_threshold()
                self.click_handler.reset_clicks()  # Сбрасываем количество кликов
                self.progress_bar.setValue(0)  # Сбрасываем прогресс-бар

            self.update_score_label(self.click_handler.click_count)

        except Exception as e:
            print(f"Error handling click: {e}")

    def update_score(self, amount):
        self.click_handler.click_count += amount
        self.update_score_label(self.click_handler.click_count)

    def purchase_upgrade(self, index):
        try:
            # Учитываем уровень текущего апгрейда для правильного расчета стоимости
            upgrade_cost = self.shop_menu.prices[index]

            if self.click_handler.click_count >= upgrade_cost:
                # Отнимаем стоимость апгрейда от количества кликов
                self.click_handler.click_count -= upgrade_cost

                # Увеличиваем уровень апгрейда
                self.shop_menu.levels[index] += 1

                # Обновляем текст метки уровня
                self.shop_menu.level_labels[index].setText(f'Level: {self.shop_menu.levels[index]}')


                # Обновляем текст метки цены
                new_price = self.shop_menu.prices[index] * 2
                self.shop_menu.prices[index] = new_price
                self.shop_menu.price_labels[index].setText(f'Price: {new_price}')

                print(f'Upgrade {index + 1} to level {self.shop_menu.levels[index]}!')
                self.main_window.play_effect_sound("purchase")
                # Применяем апгрейд
                self.apply_upgrade(index)

                # Обновляем метку счета после покупки апгрейда
                self.update_score_label(self.click_handler.click_count)
            else:
                print("Not enough points!")
        except Exception as e:
            print(f'Error upgrading item: {e}')

    def start_variant_timer(self):
        try:
            self.variant_timer.start(450)
        except Exception as e:
            print(f"Error starting variant timer: {e}")

    def stop_variant_timer(self):
        try:
            self.variant_timer.stop()
        except Exception as e:
            print(f"Error stopping variant timer: {e}")

    def update_variant_image(self):
        try:
            if self.character.current_stage in self.character.variant_images and len(
                    self.character.variant_images[self.character.current_stage]) > 1:
                self.update_character_image()
        except Exception as e:
            print(f"Error updating variant image: {e}")

    def show_temp_label(self, text, color):
        try:
            self.temp_label.setText(text)
            self.temp_label.setStyleSheet(f"color: {color.name()}; font-size: 24px;")
            self.temp_label.adjustSize()

            cursor_pos = QCursor.pos()
            window_pos = self.mapFromGlobal(cursor_pos)

            label_x = window_pos.x() + 20
            label_y = window_pos.y() + 20
            self.temp_label.move(label_x, label_y)
            self.temp_label.show()

            QTimer.singleShot(1000, self.temp_label.hide)
        except Exception as e:
            print(f"Error showing temp label: {e}")

    def show_upgrade_label(self, text, color):
        try:
            self.temp_label.setText(text)
            self.temp_label.setStyleSheet(f"color: {color.name()}; font-size: 30px;")
            self.temp_label.adjustSize()

            # Центрируем метку на экране
            center_x = (self.width() - self.temp_label.width()) // 2
            center_y = (self.height() - self.temp_label.height()) // 2
            self.temp_label.move(center_x, center_y)
            self.temp_label.show()

            QTimer.singleShot(3000, self.temp_label.hide)
        except Exception as e:
            print(f"Error showing upgrade label: {e}")

    def update_score_label(self, score):
        try:
            self.score_label.setText(f"¥: {score}")
            self.score_label.adjustSize()
            label_x = (self.width() - self.score_label.width()) // 2
            self.score_label.move(label_x, 0)
            self.score_label.show()
        except Exception as e:
            print(f"Error updating score label: {e}")

    def apply_upgrade(self, idx):
        if idx == 0:  # Первый апгрейд - удвоение очков за клик
            self.click_handler.apply_multiplier_upgrade()
            print(self.shop_menu.levels[0])
            self.show_upgrade_label(f"Click points upgraded!", QColor("green"))
        elif idx == 1:  # Второй апгрейд - увеличение пассивного дохода
            self.passive_income = self.passive_income * 2
            self.passive_income_timer.start(5000)
            self.show_upgrade_label(f"Passive income upgraded!", QColor("green"))
        elif idx == 2:  # Третий апгрейд - уменьшение шанса на потерю очков
            self.decrement_chance = max(0, self.decrement_chance - 2)
            self.show_upgrade_label(f"Decrement chance reduced to: {self.decrement_chance}%", QColor("green"))
        elif idx == 3:  # Четвертый апгрейд - уменьшение количества теряемых очков на 0,3% за уровень
            self.click_handler.DECREMENT_PERCENT = max(0, self.click_handler.DECREMENT_PERCENT - 0.004)
            self.show_upgrade_label(f"Decrement amount reduced to: {round(self.click_handler.DECREMENT_PERCENT * 100, 2)}%", QColor("green"))

    def give_passive_income(self):
        self.update_score(self.passive_income)
        self.update_progress_bar()
        self.show_temp_label(f"+{self.passive_income}", QColor("green"))

    def update_progress_bar(self):
        clicks = self.click_handler.click_count
        progress = min(clicks / self.current_threshold * 100, 100)
        self.progress_bar.setValue(int(progress))

        if clicks >= self.current_threshold:
            self.character.advance_stage()
            print(f"Progress bar filled, advancing character to stage {self.character.current_stage}")
            self.update_character_image()
            self.current_threshold = self.character.get_current_threshold()
            self.click_handler.reset_clicks()  # Сбрасываем количество кликов
            self.progress_bar.setValue(0)  # Сбрасываем прогресс-бар

    def keyPressEvent(self, event):
        """Обработчик нажатия клавиш."""
        if event.key() == Qt.Key_Escape:
            self.handle_escape_key()
        elif event.key() == Qt.Key_F:
            self.main_window.toggle_fullscreen()

    def handle_escape_key(self):
        """Обработка нажатия клавиши Escape."""
        self.close_application()

    def close_application(self):
        """Закрытие приложения с подтверждением."""
        reply = QMessageBox.question(self, 'Exit to Main Menu', "Are you sure you want to exit to the main menu?\nAll game progress will be reset.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.main_window.show_main_menu()

