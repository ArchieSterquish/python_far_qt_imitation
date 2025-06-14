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

"""
How buttons look
1[button] 2[button]
"""

class ButtonsBar(QWidget):
    def __init__(self):
        super().__init__()
        self._init_buttons()


    def _init_buttons(self):
        self.buttons = [QPushButton(parent=self,text='MARK') for i in range(12)]
        for button in self.buttons:
            button.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        layout = QGridLayout()
        for index,button in enumerate(self.buttons):
            label = QLabel(self)
            label.setText(str(index+1))
            label.setSizePolicy(
                QSizePolicy.Policy.Fixed,  # Horizontal
                QSizePolicy.Policy.Fixed   # Vertical
            )

            temp_widget = QWidget()       
            ll = QGridLayout()
            ll.addWidget(label,0,0)
            ll.addWidget(button,0,1)
            temp_widget.setLayout(ll)
            layout.addWidget(temp_widget,0,index)

        self.setLayout(layout)
