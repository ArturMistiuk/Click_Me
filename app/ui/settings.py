from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel, QComboBox, QHBoxLayout, QSlider, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QIcon
from PyQt5.QtCore import QSettings


class Settings(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.background_image = QPixmap("resources/images/settings_background.png")
        self.setWindowTitle("Settings")
        settings_icon = QIcon("resources/images/logo_icon.png")
        self.setWindowIcon(settings_icon)
        self.is_sound_muted = False
        self.is_effects_muted = False
        self.fullscreen = False
        self.settings = QSettings('MistiukCreations', 'ClickMe')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.add_header(layout, "Resolution:")
        self.resolution_combo = self.create_resolution_combo()
        layout.addWidget(self.resolution_combo, alignment=Qt.AlignCenter)
        layout.addSpacing(20)

        self.add_fullscreen_checkbox(layout)
        layout.addSpacing(20)

        self.add_header(layout, "Music:")
        self.volume_slider = self.create_slider(15)
        self.mute_button = self.create_button("Mute Music", self.mute_all_sounds)
        layout.addWidget(self.volume_slider, alignment=Qt.AlignCenter)
        layout.addWidget(self.mute_button, alignment=Qt.AlignCenter)
        layout.addSpacing(20)

        self.add_header(layout, "Effects Sound:")
        self.effects_volume_slider = self.create_slider(80)
        self.mute_effects_button = self.create_button("Mute Effects Sounds", self.mute_effects_sounds)
        layout.addWidget(self.effects_volume_slider, alignment=Qt.AlignCenter)
        layout.addWidget(self.mute_effects_button, alignment=Qt.AlignCenter)
        layout.addSpacing(40)

        self.add_control_buttons(layout)
        self.setLayout(layout)
        self.load_settings()

    def add_header(self, layout, text):
        label = QLabel(text)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(label, alignment=Qt.AlignCenter)

    def create_resolution_combo(self):
        combo = QComboBox()
        resolutions = ["800x600", "1024x768", "1280x720", "1280x1024", "1366x768", "1440x900", "1600x900"]
        combo.addItems(resolutions)
        combo.setCurrentText("1280x720")
        combo.setFont(QFont("Arial", 14))
        return combo

    def add_fullscreen_checkbox(self, layout):
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

    def create_slider(self, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(initial_value)
        slider.setFont(QFont("Arial", 14))
        slider.setMinimumWidth(300)
        return slider

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 14))
        button.clicked.connect(callback)
        return button

    def add_control_buttons(self, layout):
        button_layout = QVBoxLayout()
        save_button = self.create_button("Save", self.save_settings)
        back_button = self.create_button("Back to Menu", self.back_to_menu)
        button_layout.addWidget(save_button, alignment=Qt.AlignHCenter)
        button_layout.addWidget(back_button, alignment=Qt.AlignHCenter)
        layout.addLayout(button_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

    def save_settings(self):
        self.fullscreen = self.fullscreen_checkbox.isChecked()
        self.settings.setValue('fullscreen', self.fullscreen)
        self.settings.setValue('resolution', self.resolution_combo.currentText())
        self.settings.setValue('volume', self.volume_slider.value())
        self.settings.setValue('effects_volume', self.effects_volume_slider.value())
        self.settings.setValue('sound_muted', self.is_sound_muted)
        self.settings.setValue('effects_muted', self.is_effects_muted)

        if self.fullscreen:
            self.main_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.main_window.showFullScreen()
        else:
            self.main_window.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            resolution = self.resolution_combo.currentText()
            width, height = map(int, resolution.split('x'))
            self.main_window.setFixedSize(width, height)
            self.main_window.showNormal()
            self.main_window.center_on_screen()

        if not self.is_sound_muted:
            volume = self.volume_slider.value()
            if self.main_window.player is not None:
                self.main_window.player.setVolume(volume)

        if not self.is_effects_muted:
            effects_volume = self.effects_volume_slider.value()
            self.main_window.set_effects_volume(effects_volume)

        self.main_window.show()

    def load_settings(self):
        self.fullscreen_checkbox.setChecked(self.settings.value('fullscreen', False, type=bool))
        self.resolution_combo.setCurrentText(self.settings.value('resolution', "1280x720", type=str))
        self.volume_slider.setValue(self.settings.value('volume', 15, type=int))
        self.effects_volume_slider.setValue(self.settings.value('effects_volume', 80, type=int))
        self.mute_button.setText("Unmute Music" if self.is_sound_muted else "Mute Music")
        self.mute_effects_button.setText("Unmute Effects Sounds" if self.is_effects_muted else "Mute Effects Sounds")

    def back_to_menu(self):
        self.main_window.show_main_menu()

    def mute_all_sounds(self):
        if self.main_window.player is not None:
            if self.is_sound_muted:
                self.main_window.player.setVolume(self.volume_slider.value())
                self.is_sound_muted = False
                self.mute_button.setText("Mute Music")
            else:
                self.main_window.player.setVolume(0)
                self.is_sound_muted = True
                self.mute_button.setText("Unmute Music")

    def mute_effects_sounds(self):
        if self.is_effects_muted:
            self.main_window.set_effects_volume(self.effects_volume_slider.value())
            self.is_effects_muted = False
            self.mute_effects_button.setText("Mute Effects Sounds")
        else:
            self.main_window.set_effects_volume(0)
            self.is_effects_muted = True
            self.mute_effects_button.setText("Unmute Effects Sounds")
