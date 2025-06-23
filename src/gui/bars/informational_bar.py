from PyQt6.QtWidgets import (QHBoxLayout,QWidget,QLabel)
from PyQt6.QtCore import Qt

class TextInformationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def set_filepath(self,filepath):
        self.filepath_text = filepath

    def update_position_information(self,x,y):
        self.position_label.setText(f"|{x+1}|{y+1}")
        self.filepath_label.setText(f"{self.filepath_text}")

    def setup_ui(self):
        layout = QHBoxLayout()
        self.filepath_label = QLabel("BLANK")        
        self.position_label = QLabel("1:1")
        self.position_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.filepath_label)
        layout.addWidget(self.position_label)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.setLayout(layout)

