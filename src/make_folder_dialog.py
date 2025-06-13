from PyQt6.QtWidgets import(
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QVBoxLayout,
    QDialog,
)

from error_dialog import ErrorDialog

class MakeFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Make folder")
        self.setGeometry(300, 300, 300, 150)
        
        self.user_input = None  # Stores the input
        
        # Widgets
        self.label = QLabel("Enter folder name:")
        self.input_field = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)
        
        # Signals (button clicks)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
    
    def on_ok(self):
        """Store input and close when OK is pressed."""
        self.user_input = self.input_field.text()
        if not self.user_input:  # Empty input
            ErrorDialog(self,"Input cannot be empty!")
            return
        self.close()
    
    def on_cancel(self):
        """Close without saving on Cancel."""
        self.close()
