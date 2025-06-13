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
from panel import PanelsWidget
from console_interaction_panel import ConsoleInteractionPanel  
from error_dialog import ErrorDialog
from make_folder_dialog import MakeFolderDialog

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
        #self.showFullScreen()

    def keyPressEvent(self, event):
        # MODIFIERS
        ALT = Qt.KeyboardModifier.AltModifier 
        CTRL = Qt.KeyboardModifier.ControlModifier
        SHIFT = Qt.KeyboardModifier.ShiftModifier
        NONE = Qt.KeyboardModifier.NoModifier

        commands = {
            KEY.F1:  lambda: print('not implemented'),
            KEY.F2:  lambda: print('not implemented'),
            KEY.F3:  lambda: print('not implemented'),
            KEY.F4:  lambda: print('not implemented:create and edit file'),
            KEY.F5:  lambda: print('not implemented:copy'),
            KEY.F6:  lambda: print('not implemented:move'),
            KEY.F7:  lambda: self.mainWidget.show_input_dialog(),
            KEY.F8:  lambda: self.mainWidget.show_deletion_dialog(),
            KEY.F9:  lambda: print('not implemented:options'),
            KEY.F10: lambda: self.close(),
            KEY.F11: lambda: print('not implemented: plugins'), # do I need them?
            KEY.F12: lambda: print('not implemented: screens'), # I don't use them myself, so hard to say
        }

        commands_with_modifiers = {
            # NO MODIFIERS
            (NONE,KEY.F1):  lambda: print('not implemented'),
            (NONE,KEY.F2):  lambda: print('not implemented'),
            (NONE,KEY.F3):  lambda: print('not implemented'),
            (NONE,KEY.F4):  lambda: print('not implemented:create and edit file'),
            (NONE,KEY.F5):  lambda: print('not implemented:copy'),
            (NONE,KEY.F6):  lambda: print('not implemented:move'),
            (NONE,KEY.F7):  lambda: self.mainWidget.show_input_dialog(),
            (NONE,KEY.F8):  lambda: self.mainWidget.show_deletion_dialog(),
            (NONE,KEY.F9):  lambda: print('not implemented:options'),
            (NONE,KEY.F10): lambda: self.close(),
            (NONE,KEY.F11): lambda: print('not implemented: plugins'), # do I need them?
            (NONE,KEY.F12): lambda: print('not implemented: screens'), # I don't use them myself, so hard to say

            # SINGLE MODIFIERS (ALT)
            (ALT,KEY.F1):  lambda: print('not implemented'),
            (ALT,KEY.F2):  lambda: print('not implemented'),
            (ALT,KEY.F3):  lambda: print('not implemented'),
            (ALT,KEY.F4):  lambda: print('not implemented:create and edit file'),
            (ALT,KEY.F5):  lambda: print('not implemented:copy'),
            (ALT,KEY.F6):  lambda: print('not implemented:move'),
            (ALT,KEY.F7):  lambda: print('not implemented:move'),
            (ALT,KEY.F8):  lambda: print('not implemented:move'),
            (ALT,KEY.F9):  lambda: print('not implemented:options'),
            (ALT,KEY.F10): lambda: print('not implemented:move'),
            (ALT,KEY.F11): lambda: print('not implemented: plugins'), # do I need them?
            (ALT,KEY.F12): lambda: print('not implemented: screens'), # I don't use them myself, so hard to say
            # SINGLE MODIFIERS (CTRL) mostly responsible for sortin
            (CTRL,KEY.F1):  lambda: print('not implemented'),
            (CTRL,KEY.F2):  lambda: print('not implemented'),
            (CTRL,KEY.F3):  lambda: print('not implemented'),
            (CTRL,KEY.F4):  lambda: print('not implemented:create and edit file'),
            (CTRL,KEY.F5):  lambda: print('not implemented:copy'),
            (CTRL,KEY.F6):  lambda: print('not implemented:move'),
            (CTRL,KEY.F7):  lambda: print('not implemented:options'),
            (CTRL,KEY.F8):  lambda: print('not implemented:options'),
            (CTRL,KEY.F9):  lambda: print('not implemented:options'),
            (CTRL,KEY.F10): lambda: print('not implemented:options'),
            (CTRL,KEY.F11): lambda: print('not implemented: plugins'), # do I need them?
            (CTRL,KEY.F12): lambda: print('not implemented: screens'), # I don't use them myself, so hard to say
            # SINGLE MODIFIERS (SHIFT)
            (SHIFT,KEY.F1):  lambda: print('not implemented'),
            (SHIFT,KEY.F2):  lambda: print('not implemented'),
            (SHIFT,KEY.F3):  lambda: print('not implemented'),
            (SHIFT,KEY.F4):  lambda: print('not implemented:create and edit file'),
            (SHIFT,KEY.F5):  lambda: print('not implemented:copy'),
            (SHIFT,KEY.F6):  lambda: print('not implemented:move'),
            (SHIFT,KEY.F7):  lambda: print('not implemented:options'),
            (SHIFT,KEY.F8):  lambda: print('not implemented:options'),
            (SHIFT,KEY.F9):  lambda: print('not implemented:options'),
            (SHIFT,KEY.F10): lambda: print('not implemented:options'),
            (SHIFT,KEY.F11): lambda: print('not implemented: plugins'), # do I need them?
            (SHIFT,KEY.F12): lambda: print('not implemented: screens'), # I don't use them myself, so hard to say
        }

        modifier = event.modifiers()
        key = event.key()
        #print(event.key())

        try:
            if (modifier, key) in commands_with_modifiers:                
                print(f'here {modifier}:{key}')
                commands_with_modifiers[(modifier,key)]()
            #if modifiers == NONE: # so we didn't press alt shift ctrl
            #    commands[key]()
            #elif modifiers == CTRL: # only pressed ctrl
            #    print("CTRL is pressed")
            #elif modifiers == ALT: # only pressed ctrl
            #    print("ALT is pressed")
            #elif modifiers == SHIFT: # only pressed ctrl
            #    if key == KEY.F4:
            #        print("SHIFT + F4 is pressed")
        except:
            pass

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
