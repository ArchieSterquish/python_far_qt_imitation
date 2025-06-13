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
from PyQt6.QtGui import QIcon  # Optional: For custom icons
from system_api import SystemAPI
from system_api import KEY

import sys
# custom modules
from gui.error_dialog import ErrorDialog
from gui.make_folder_dialog import MakeFolderDialog
from console_interaction_panel import ConsoleInteractionPanel  
from panel import PanelsWidget
import key_press_event_handler as KeyPressEventHandler

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget_1 = PanelsWidget()
        self.widget_2 = ConsoleInteractionPanel(self)

        layout = QGridLayout()
        layout.addWidget(self.widget_1)
        layout.addWidget(self.widget_2)
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

        dialog = MakeFolderDialog(self)  # Passing `self` as parent
        dialog.exec()  # Blocking call
        
        if dialog.user_input is not None:
            print(focused_path,dialog.user_input)
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
        #if (event.key() == KEY.F7):
        #    self.mainWidget.show_input_dialog()
        KeyPressEventHandler.KeyHandler.handle_key(self,event)

    def closeEvent(self, event):
       
        reply = QMessageBox.question(self, 
                'Close Confirmation', 
                'Are you sure you want to exit?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes: 
            event.accept()  # Accept the close event, closing the window
        else:
            event.ignore()  # Ignore the close event, keeping the window open

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
