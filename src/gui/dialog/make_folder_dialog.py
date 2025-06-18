from PyQt6.QtWidgets import(QLabel,QPushButton,QLineEdit,QVBoxLayout,QDialog,)
from .error_dialog import ErrorDialog
# TODO:
#   1. Change button placement from vertical to horizontal
#   2. Add ability to shift focus from input field to buttons 
class MakeFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Make folder")
        self.setGeometry(300, 300, 300, 150)
        
        self.user_input = None  
        
        self.label = QLabel("Enter folder name:")
        self.input_field = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
    
    def on_ok(self):
        self.user_input = self.input_field.text()
        if not self.user_input:  
            ErrorDialog(self,"Input cannot be empty!")
            return
        self.close()
    
    def on_cancel(self):
        self.close()
