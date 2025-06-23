from PyQt6.QtWidgets import(QApplication, QMainWindow, QMessageBox,QStackedWidget,)
import sys
import os

# custom modules
from event_handler import KeyHandler
from gui import MainWidget
from gui import TextEditorWidget

# TODO:
#   either find a fix for FIXME in MainWindow
#   or change so Panel or PanelsWidget gets keyHandler
#   or redirect keys from Panel or PanelsWidget from corresponding methods

class MainWindow(QMainWindow):
    def __init__(self):        
        super().__init__()
        self.setWindowTitle("My App")
        self.setup_ui()
        self.mainWidget.close_app_signal.connect(self.closeEventFromWidget) # exit only available main widget 
        self.keyHandler = KeyHandler(self)
        #self.showMaximized()

    def setup_ui(self):
        width = 500
        height = 500
        self.stacked_widget = QStackedWidget()
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.mainWidget = MainWidget()
        self.textWidget = TextEditorWidget()
        self.stacked_widget.addWidget(self.mainWidget)
        self.stacked_widget.addWidget(self.textWidget)
        self.setCentralWidget(self.stacked_widget)

    def currentWidget(self):
        return self.stacked_widget.currentWidget()

    def setCurrentWidget(self,widget):
        self.stacked_widget.setCurrentWidget(widget)

    def switchWidget(self):
        widget = self.currentWidget()
        if isinstance(widget,MainWidget):
            self.setCurrentWidget(self.textWidget)
        else:
            self.setCurrentWidget(self.mainWidget)

    def update_buttons_text(self,modifier_key):
        self.currentWidget().update_buttons_text(modifier_key)
    
    # FIXME:
    # after adding ChangeLocationWidget mainWidget stopped recieving any keys so usual exit doesn't work now
    def keyPressEvent(self,event):
        self.keyHandler.handle_key_press(event)

    # FIXME:
    # after adding ChangeLocationWidget mainWidget stopped recieving any keys so usual exit doesn't work now
    def keyReleaseEvent(self,event):
        self.keyHandler.handle_key_release(event)

    def closeEventFromWidget(self,_):
        self.close()

    def closeEvent(self, event):
        YES = QMessageBox.StandardButton.Yes 
        NO  = QMessageBox.StandardButton.No
        reply = QMessageBox.question(self, 
                'Close Confirmation', 
                'Are you sure you want to exit?',
                YES | NO, 
                YES
        )
        if reply == YES: 
            event.accept()  
        else:
            event.ignore() 

def main():
    app = QApplication(sys.argv)
    path_to_theme = os.path.join(os.getcwd(),"theme","theme.qss")
    with open(path_to_theme,"r") as f:
        style_sheet = f.read()
    app.setStyleSheet(style_sheet)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
