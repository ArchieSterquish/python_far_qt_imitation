from PyQt6.QtWidgets import(
    QTextEdit,
    QApplication, 
    QMainWindow, 
    QPushButton,
    QListWidget,
    QWidget,
    QGridLayout,
    QMessageBox,
    QLineEdit,
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon  
import sys

# custom modules
#from panel import PanelsWidget
from event_handler import KeyHandler

from gui import ConsoleInteractionPanel  
from gui import ErrorDialog
from gui import MakeFolderDialog
from gui import PanelsWidget

from gui import ButtonsBar

from system_api import SystemAPI
from system_api import KEY

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget_1 = PanelsWidget()
        self.widget_2 = ConsoleInteractionPanel(self)
        self.widget_3 = ButtonsBar()

        layout = QGridLayout()
        layout.addWidget(self.widget_1)
        layout.addWidget(self.widget_2)
        layout.addWidget(self.widget_3)
        self.setLayout(layout)

    def get_focused_panel_path(self):
        return self.widget_1.get_focused_panel_path()

    def get_focused_file_or_folder(self):
        return self.widget_1.get_focused_file_or_folder()

    def update_panel(self,focused_panel):
        self.widget_1.update_panel(focused_panel)

    def show_deletion_dialog(self):
        focused_path,focused_panel = self.get_focused_panel_path()
        focused_file_or_folder = self.get_focused_file_or_folder()
        filename = SystemAPI.basename(focused_file_or_folder)
        reply = QMessageBox.question(self, 
                'Deletion Confirmation', 
                f'Are you sure you want to delete {filename}?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes: 
            SystemAPI.remove_file_or_directory(focused_file_or_folder)
            self.update_panel(focused_panel)

    def show_input_dialog(self):
        """Create and show the input dialog."""
        focused_path,focused_panel = self.get_focused_panel_path()

        dialog = MakeFolderDialog(self)  
        dialog.exec()  
        
        # TODO:
        # add multiple_spaces check
        # add check for space in the beginnig
        if dialog.user_input not in ["",None]:
            print(f'user input: {dialog.user_input}')
            result = SystemAPI.make_directory(focused_path,dialog.user_input)
            if result != None:
                ErrorDialog(self,result)
                return
            self.update_panel(focused_panel)

class MainWindow(QMainWindow):
    def __init__(self):        
        super().__init__()
        self.setWindowTitle("My App")

        width = 500
        height = 500
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

    def keyPressEvent(self,event):
        KeyHandler.handle_key(event)(self)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 
                'Close Confirmation', 
                'Are you sure you want to exit?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes: 
            event.accept()  
        else:
            event.ignore() 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
