# custom_switch.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal


class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 40)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 1)
        self.slider.setFixedSize(60, 30)
        self.slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background-color: #ccc;
                height: 20px;
                border-radius: 10px;
            }
            QSlider::handle:horizontal {
                background-color: #fff;
                border: 1px solid #ccc;
                width: 25px;
                height: 25px;
                border-radius: 12px;
                margin: -3px 0;
            }
            QSlider::handle:horizontal:pressed {
                background-color: #aaa;
            }
        """
        )

        self.label_left = QLabel("Single-Task", self)
        self.label_right = QLabel("Multi-Task", self)

        layout = QHBoxLayout()
        layout.addWidget(self.label_left)
        layout.addWidget(self.slider)
        layout.addWidget(self.label_right)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.emit_toggled)

    def emit_toggled(self, value):
        self.toggled.emit(bool(value))

    def set_value(self, value):
        self.slider.setValue(int(value))

    def value(self):
        return bool(self.slider.value())
