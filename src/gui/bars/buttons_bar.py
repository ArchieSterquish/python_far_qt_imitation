from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QSizePolicy
)
from PyQt6.QtCore import Qt
import json

#from system_api import KEY


import os


if os.name == "nt": # WINDOWS
    TEMP_PATH_SOLUTION = os.path.join('gui','bars','config','buttons.json') 
if os.name == "posix": # LINUX
    TEMP_PATH_SOLUTION = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config','buttons.json')
# Loading config for buttons
with open(TEMP_PATH_SOLUTION) as f:
    print(TEMP_PATH_SOLUTION)
    CONFIG_BUTTONS = json.load(f)

# TODO:
#    1. Add buttons names
#    2. Make button text change depending on current pressed keys to get another set of functional keys (maybe have to recreate widget again?)
class ButtonsBar(QWidget):
    def __init__(self):
        super().__init__()
        self._init_buttons()

    def update_buttons_text(self,modifier_key):
        for button,text in zip(self.buttons,CONFIG_BUTTONS[modifier_key]):            
            button.setText(text)

    def keyPressEvent(self, event):
        ALT   = Qt.KeyboardModifier.AltModifier 
        CTRL  = Qt.KeyboardModifier.ControlModifier
        SHIFT = Qt.KeyboardModifier.ShiftModifier
    
        if event.key() == ALT:
            self.update_buttons_text("ALT")
        if event.key() == CTRL:
            self.update_buttons_text("CTRL")
        if event.key() == SHIFT:
            self.update_buttons_text("SHIFT")
        super().keyPressEvent(event)

    def keyReleaseEvent(self,event):
        self.update_buttons_text("NONE")
        super().keyPressEvent(event)

    def create_numbered_button(self,index,button):
        label = QLabel(self)
        label.setText(str(index+1))
        label.setSizePolicy(            # setting up the policy so label takes as little space as possible
            QSizePolicy.Policy.Fixed,  
            QSizePolicy.Policy.Fixed   
        )
        layout = QGridLayout()
        layout.addWidget(label,0,0)
        layout.addWidget(button,0,1)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _init_buttons(self):
        self.buttons = [QPushButton(parent=self,text=button) for button in CONFIG_BUTTONS["NONE"]]
        for button in self.buttons:
            button.setFocusPolicy(Qt.FocusPolicy.ClickFocus) # so that it doesn't focus on these buttons

        layout = QGridLayout()
        for index,button in enumerate(self.buttons):
            temp_widget = self.create_numbered_button(index,button)
            layout.addWidget(temp_widget,0,index)

        self.setLayout(layout)
