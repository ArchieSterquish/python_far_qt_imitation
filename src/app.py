from PyQt6.QtWidgets import(
    QApplication, 
    QMainWindow, 
    QMessageBox,
    QStackedWidget,
)
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

    def keyPressEvent(self,event):
        # temporary workaround to open TextEditorWidget
        from system_api import KEY
        if isinstance(self.currentWidget(),MainWidget):
            if event.key() == KEY.F4:
                filepath = self.mainWidget.get_focused_file_or_folder()
                try:
                    self.textWidget.open_file_temp(filepath)
                    self.setCurrentWidget(self.textWidget)
                except ValueError as e:
                    print(e)
        elif isinstance(self.currentWidget(),TextEditorWidget):
            if event.key() == KEY.F4:
                self.setCurrentWidget(self.mainWidget)
        KeyHandler.handle_key_press(event,self.currentWidget())(self.currentWidget())

    def keyReleaseEvent(self,event):
        KeyHandler.handle_key_release(event,self.currentWidget())(self.currentWidget())

    def closeEventFromWidget(self,event):
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
