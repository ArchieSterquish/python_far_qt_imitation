from PyQt6.QtWidgets import QWidget,QGridLayout,QLabel,QLineEdit
from PyQt6.QtCore import Qt,QEvent

class QuickSearchPanelWidget(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        self.search_label = QLabel('Search')
        self.quick_search = QLineEdit()

        self.quick_search.installEventFilter(self)

        layout.addWidget(self.search_label)
        layout.addWidget(self.quick_search)
        self.setLayout(layout)
        
        self.quick_search.setFixedSize(120,30)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.hide()

        self.setAutoFillBackground(True) 
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True) # initially widget doesn't have background color at all

    def eventFilter(self,obj,event):
        if obj == self.quick_search and event.type() == QEvent.Type.FocusOut:
            self.hide()
            return True

        return super().eventFilter(obj,event)

    def textChangedConnect(self,callback):
        self.quick_search.textChanged.connect(callback)

    def setText(self,text):
        self.quick_search.setText(text)

    def clear(self):
        self.quick_search.clear()

    def setFocus(self):
        self.quick_search.setFocus()

    def hasFocus(self):
        return self.quick_search.hasFocus()
