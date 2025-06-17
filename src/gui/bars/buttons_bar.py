from PyQt6.QtWidgets import (QPushButton,QWidget,QGridLayout,QLabel,QSizePolicy)
from PyQt6.QtCore import Qt
import json
import os

if os.name == "nt": # WINDOWS
    MAIN_BUTTONS_CONFIGURATION = os.path.join('gui','bars','config','main_widget_buttons.json') 
    TEXT_EDITOR_BUTTONS_CONFIGURATION = os.path.join('gui','bars','config','text_editor_buttons.json') 
if os.name == "posix": # LINUX
    MAIN_BUTTONS_CONFIGURATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config','main_widget_buttons.json')
    TEXT_EDITOR_BUTTONS_CONFIGURATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config','text_editor_buttons.json')

class ButtonsBar(QWidget):
    def __init__(self,parent_widget_text):
        super().__init__()
        self.load_config_for_buttons(parent_widget_text)
        self.setup_ui()

    # NOTE: Maybe add factory instead of load method with if statements? 
    def load_config_for_buttons(self,parent_widget_text):
        BUTTONS_CONFIGURATION = MAIN_BUTTONS_CONFIGURATION # temp solution if parent_widget_text isn't suited for our cases
        if parent_widget_text == "main widget":
            BUTTONS_CONFIGURATION = MAIN_BUTTONS_CONFIGURATION
        if parent_widget_text == "text editor":
            BUTTONS_CONFIGURATION = TEXT_EDITOR_BUTTONS_CONFIGURATION
        else:
            print("what the fuck bars ???:(")

        with open(BUTTONS_CONFIGURATION) as f:
            self.CONFIG_BUTTONS = json.load(f)
    def create_numbered_button(self,index,button):
        label = QLabel(self)
        label.setText(str(index+1))
        label.setSizePolicy( # setting up the policy so label takes as little space as possible
            QSizePolicy.Policy.Fixed,  
            QSizePolicy.Policy.Fixed   
        )
        layout = QGridLayout()
        layout.addWidget(label,0,0)
        layout.addWidget(button,0,1)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def setup_ui(self):
        self.buttons = [QPushButton(parent=self,text=button) for button in self.CONFIG_BUTTONS["NONE"]]
        for button in self.buttons:
            button.setFocusPolicy(Qt.FocusPolicy.ClickFocus) # so that it doesn't focus on these buttons

        layout = QGridLayout()
        for index,button in enumerate(self.buttons):
            temp_widget = self.create_numbered_button(index,button)
            layout.addWidget(temp_widget,0,index)

        self.setLayout(layout)

    def update_buttons_text(self,modifier_key):
        for button,text in zip(self.buttons,self.CONFIG_BUTTONS[modifier_key]):
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
