from PyQt6.QtWidgets import QMessageBox

class ErrorDialog(QMessageBox):
    def __init__(self,parent,message):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Critical)  
        self.setWindowTitle("Error")
        self.setText(message)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()
