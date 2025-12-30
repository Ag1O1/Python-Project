from numpy import split
from sqlalchemy.orm.attributes import History
from jinja2.nodes import Output
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit, QSplitter
from PySide6.QtGui import QPalette
from convertions import decimal_to_base
import sys
import parser


def calculate():
    error_field.clear()
    string = input_field.text()
    print(string)
    try:
        res = parser.calc(string)
        combo_value = combobox.currentText()
        if combo_value == "Decimal":
            res = str(decimal_to_base(res,"dec"))
        elif combo_value == "Hexadecimal":
            res = str("0x%s"%decimal_to_base(res,"hex"))
        elif combo_value == "Octal":
            res = str("0o%s"%decimal_to_base(res,"oct"))
        elif combo_value == "Binary":
            res = str("0b%s"%decimal_to_base(res,"bin"))
        output_field.setText(res)
        history_text.append("%s = %s"%(string,res))
    except Exception as e:
        error_field.setText("ERROR:%s "%str(e))

app = QApplication(sys.argv)

palette = QApplication.palette()
bg_color = palette.color(QPalette.ColorRole.Window).name()
text_color = palette.color(QPalette.ColorRole.WindowText).name()
mid_color = palette.color(QPalette.ColorRole.Mid).name()
error_color = palette.color(QPalette.ColorRole.PlaceholderText).name()
highlight_color = palette.color(QPalette.ColorRole.Highlight).name()


input_field = QLineEdit()
input_field.setPlaceholderText("Input here")
input_field.setMinimumHeight(24)
input_field.setStyleSheet(f"""
QLineEdit {{
    border: 3px solid {mid_color};
    border-radius: 6px;
    padding: 6px;
    font-size: 16px;
}}
QLineEdit:focus {{
    border: 3px solid {highlight_color};  /* highlight on focus */
}}
""")

combobox = QComboBox()
combobox.setFixedWidth(150)
combobox.setMinimumHeight(30)
combobox.addItem("Decimal")
combobox.addItem("Hexadecimal")
combobox.addItem("Octal")
combobox.addItem("Binary")
combobox.setStyleSheet(f"""
QComboBox {{
    border: 3px solid {mid_color};
    border-radius: 6px;
    padding: 2px;
    font-size: 16px;
}}
QComboBox:hover {{
    border: 3px solid {highlight_color};
}}
""")

error_field = QLabel()
error_field.setMinimumHeight(24)
error_field.setStyleSheet(f"""
QLabel {{
    font-style: italic;
    font-size: 16px;
    color: {error_color};
    background-color: {bg_color};
}}
""")

output_field = QLabel()
output_field.setText("Output")
output_field.setMinimumHeight(24)
output_field.setStyleSheet(f"""
QLabel {{
    border: 3px solid {mid_color};
    border-radius: 6px;
    padding: 6px;
    font-weight: bold;
    font-size: 24px;
    background-color: {bg_color};
}}
""")

button = QPushButton("Calculate")
button.setMinimumHeight(32)
button.setMaximumWidth(240)
button.clicked.connect(calculate)
button.setStyleSheet(f"""
QPushButton {{
    border: 3px solid {mid_color};
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 24px;
}}
QPushButton:hover {{
    border: 3px solid {highlight_color};
}}
""")

history_text = QTextEdit()
history_text.setReadOnly(True)

history_label = QLabel("Operation History")
history_label.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")

window = QWidget()
window.setWindowTitle("BCD Calculator")

layout = QHBoxLayout(window)
layout.setContentsMargins(30,30,30,30)
splitter = QSplitter(Qt.Orientation.Horizontal)
splitter.setHandleWidth(5)
splitter.setStyleSheet(f"""
    QSplitter::handle {{
        margin: 0 1px;
        background: {mid_color};
        border-radius: 2px;
    }}
    QSplitter::handle:hover {{
        background: {highlight_color};
    }}
""")

button_layout = QHBoxLayout()
button_layout.setSpacing(2)
button_layout.setContentsMargins(0, 0, 0, 0)
button_layout.addWidget(button,alignment=Qt.AlignmentFlag.AlignCenter)
button_layout.addWidget(combobox,alignment=Qt.AlignmentFlag.AlignCenter)

input_layout = QVBoxLayout()
input_layout.setSpacing(2)
input_layout.setContentsMargins(0, 0, 0, 0)
input_layout.addWidget(input_field)
input_layout.addWidget(error_field)

calc_panel = QWidget()
calc_layout = QVBoxLayout(calc_panel)

calc_layout.addStretch()
calc_layout.setSpacing(25)

calc_layout.addLayout(input_layout)
calc_layout.addLayout(button_layout)
calc_layout.addWidget(output_field)
calc_layout.addStretch()

history_panel = QWidget()
history_layout = QVBoxLayout(history_panel)
history_layout.addWidget(history_label)
history_layout.addWidget(history_text)

splitter.addWidget(history_panel)
splitter.addWidget(calc_panel)
splitter.setSizes([250, 500])
layout.addWidget(splitter)

input_field.returnPressed.connect(calculate)

window.setFixedSize(750,450)
window.show()

sys.exit(app.exec())
