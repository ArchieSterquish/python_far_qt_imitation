from PyQt6.QtWidgets import QWidget,QGridLayout,QLabel,QLineEdit
from PyQt6.QtCore import Qt

class QuickSearchPanelWidget(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        self.search_label = QLabel('Search')
        self.quick_search = QLineEdit()

        layout.addWidget(self.search_label)
        layout.addWidget(self.quick_search)
        self.setLayout(layout)
        
        self.quick_search.setFixedSize(120,30)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.hide()

        self.setAutoFillBackground(True) 
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True) # initially widget doesn't have background color at all

        self.setStyleSheet("""
            background-color: gray;
        """)

        self.quick_search.setStyleSheet("""
            background-color: #00ffff;
            color: #000000;
        """)

        self.search_label.setStyleSheet("""
            color: #ffffff;
        """)

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
