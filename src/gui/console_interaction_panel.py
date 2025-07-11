from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt
from system_api import KEY
from system_api import SystemAPI

class ConsoleInteractionPanel(QLineEdit):
    def __init__(self,parent):
        initial_message = "~%some user>"
        super().__init__(initial_message,parent = parent)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def updatePanel(self):
        command = self.text()
        self.clear()
        SystemAPI.execute_command(command)

    def keyPressEvent(self, event):
        if (event.key() == KEY.ENTER): 
            self.updatePanel()
        else:
            super().keyPressEvent(event)

