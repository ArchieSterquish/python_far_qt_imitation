from PyQt6.QtWidgets import(QApplication, QMainWindow, QMessageBox,QStackedWidget,)
import sys

# custom modules
from event_handler import KeyHandler
from gui import MainWidget
from gui import TextEditorWidget

class MainWindow(QMainWindow):
    def __init__(self):        
        super().__init__()
        self.setWindowTitle("My App")
        self.setup_ui()
        self.mainWidget.close_app_signal.connect(self.closeEventFromWidget) # exit only available main widget 
        self.keyHandler = KeyHandler(self)

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

    def keyPressEvent(self,event):
        self.keyHandler.handle_key_press(event)

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
    app.setStyle("fusion") # temp dark mode replacement (IT'S ACTUALLY PERMANENT >:D)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
