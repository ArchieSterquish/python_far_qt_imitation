from PyQt6.QtWidgets import (QWidget, QTextEdit, QVBoxLayout, QPushButton, QMessageBox)
from system_api import SystemAPI
from .bars import ButtonsBar
from .bars import TextInformationBar

class TextEditorWidget(QWidget):
    def __init__(self):
        super().__init__()        
        self.setWindowTitle("Simple Text Editor")
        self.resize(600, 400)
        self.setup_ui()

    def open_file_temp(self,filepath):
        self.filepath = filepath
        if not SystemAPI.is_file(self.filepath):
            QMessageBox.warning(self, "Error", f"{self.filepath} isn't a file")
            raise ValueError(f"{self.filepath} isn't a file")
        self.open_file()

    def setup_ui(self):
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("font-size: 14px;")
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_file)

        self.buttons_bar = ButtonsBar("text editor")

        self.info_bar = TextInformationBar()
        
        layout = QVBoxLayout()
        layout.addWidget(self.info_bar)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.buttons_bar)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.text_edit.cursorPositionChanged.connect(self.update_position_info)

    def update_position_info(self):
        cursor = self.text_edit.textCursor()
        x,y = cursor.blockNumber(),cursor.positionInBlock()
        self.info_bar.update_position_information(x,y)

    def update_buttons_text(self,key):
        self.buttons_bar.update_buttons_text(key)

    def open_file(self):
        try:
            with open(self.filepath, 'r') as f:
                self.info_bar.set_filepath(self.filepath)
                self.text_edit.setPlainText(f.read())
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file:\n{str(e)}")
            raise e

    def save_file(self):
        try:
            with open(self.filepath, 'w') as f:
                f.write(self.text_edit.toPlainText())
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save file:\n{str(e)}")
            raise e
