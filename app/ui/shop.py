from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QApplication, QGridLayout
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal


class ShopWidget(QWidget):
    upgrade_purchased = pyqtSignal(int)  # Signal for upgrade purchase

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle('Shop')
        self.setMinimumSize(400, 600)  # Minimum size of the shop window
        self.levels = [1, 1, 1, 1]  # Upgrade levels
        self.level_labels = []  # List to store level QLabels
        self.price_labels = []  # List to store price QLabels
        self.prices = [100, 100, 400, 400]  # Prices for upgrades

        # Allow for a transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add some padding

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent;")
        scroll_content = QWidget(scroll_area)
        scroll_content.setStyleSheet("background: rgba(30, 0, 30, 127);")  # Semi-transparent background
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area)

        # Close button
        btn_close = QPushButton(self)
        btn_close.setFixedSize(QSize(60, 60))
        close_icon = QPixmap('resources/images/shop_close.ico').scaled(35, 35, Qt.KeepAspectRatio)
        icon = QIcon(close_icon)
        btn_close.setIcon(icon)
        btn_close.setIconSize(QSize(60, 60))
        btn_close.setStyleSheet("background: transparent;")
        btn_close.clicked.connect(self.close)
        scroll_layout.addWidget(btn_close, alignment=Qt.AlignRight | Qt.AlignTop)

        # Title label
        label_title = QLabel('Shop', self)
        label_title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        label_title.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(label_title)

        # Upgrade section
        upgrades_layout = QVBoxLayout()

        for i in range(4):
            upgrade_layout = QVBoxLayout()

            # Horizontal layout for icon and upgrade level
            top_row_layout = QHBoxLayout()

            # Upgrade icon
            pixmap = QPixmap(f'resources/images/shop_upgrade_icon_{i + 1}.png').scaled(65, 65, Qt.KeepAspectRatio)
            icon_label = QLabel(self)
            icon_label.setPixmap(pixmap)
            top_row_layout.addWidget(icon_label)

            # QLabel for displaying the level
            level_label = QLabel(f'Level: {self.levels[i]}', self)
            level_label.setStyleSheet("color: white; font-size: 22px;")
            level_label.setAlignment(Qt.AlignCenter)
            top_row_layout.addWidget(level_label)
            self.level_labels.append(level_label)

            upgrade_layout.addLayout(top_row_layout)

            # Buy button for the upgrade
            btn_upgrade = QPushButton(self)
            btn_upgrade.setStyleSheet(
                "QPushButton { border-image: url(resources/images/shop_upgrade.png); background: transparent; }"
            )
            btn_upgrade.setFixedSize(50, 50)
            btn_upgrade.clicked.connect(lambda _, idx=i: self.upgrade_item(idx))
            upgrade_layout.addWidget(btn_upgrade, alignment=Qt.AlignCenter)

            # QLabel for displaying the price
            price_label = QLabel(f'Price: {self.prices[i]}', self)
            price_label.setStyleSheet("color: white; font-size: 20px;")
            price_label.setAlignment(Qt.AlignCenter)
            upgrade_layout.addWidget(price_label)
            self.price_labels.append(price_label)

            upgrades_layout.addLayout(upgrade_layout)
            upgrades_layout.addSpacing(10)  # Add spacing between upgrades

        scroll_layout.addLayout(upgrades_layout)

        # Spacing between sections
        # Spacing between sections
        scroll_layout.addSpacing(40)

        # Descriptions of upgrades
        descriptions_layout = QGridLayout()
        descriptions_text = [
            "Increases the number of points per click",
            "Increases passive income of points",
            "Reduces the chance of failed click (money is not added, points are deducted from progress) when clicking\nInitially 34% chance and -2% for each level",
            "Reduces the number of points lost on a failed click\nInitially 7% and -0.4% for each level"
        ]

        for i in range(4):
            # Add the icon for each upgrade
            pixmap = QPixmap(f'resources/images/shop_upgrade_icon_{i + 1}.png').scaled(50, 50, Qt.KeepAspectRatio)
            icon_label = QLabel(self)
            icon_label.setPixmap(pixmap)
            descriptions_layout.addWidget(icon_label, i, 0)  # Add icon to the first column

            # Add the corresponding description text with word wrapping
            description_label = QLabel(descriptions_text[i], self)
            description_label.setStyleSheet("color: white; font-size: 18px;")
            description_label.setWordWrap(True)  # Enable word wrapping
            descriptions_layout.addWidget(description_label, i, 1)  # Add text to the second column

        scroll_layout.addLayout(descriptions_layout)

        # Initial scroll position
        scroll_area.verticalScrollBar().setValue(0)

    def upgrade_item(self, index):
        if self.main_window is not None:
            try:
                self.main_window.purchase_upgrade(index)
            except Exception as e:
                print(f'Error upgrading item: {e}')
        else:
            print('MainWindow is None!')
