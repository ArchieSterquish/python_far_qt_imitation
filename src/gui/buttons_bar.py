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

# TODO:
#   1. Add buttons names
#   2. Make button text change depending on current pressed keys to get another set of functional keys (maybe have to recreate widget again?)
class ButtonsBar(QWidget):
    def __init__(self):
        super().__init__()
        self._init_buttons()

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
        self.buttons = [QPushButton(parent=self,text='MARK') for i in range(12)]
        for button in self.buttons:
            button.setFocusPolicy(Qt.FocusPolicy.ClickFocus) # so that it doesn't focus on these buttons

        layout = QGridLayout()
        for index,button in enumerate(self.buttons):
            temp_widget = self.create_numbered_button(index,button)
            layout.addWidget(temp_widget,0,index)

        self.setLayout(layout)
