from PyQt6.QtWidgets import (
    QApplication, 
    QListWidget, 
    QLineEdit, 
    QVBoxLayout, 
    QWidget, 
    QListWidgetItem
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent

# TODO: adapt to panel widget
class QuickSearchListWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        # Create the quick search box
        self.quick_search = QLineEdit()
        self.quick_search.setFixedSize(120, 30)
        self.quick_search.setWindowFlags(Qt.WindowType.Popup)
        self.quick_search.hide()
        self.quick_search.installEventFilter(self)
        self.quick_search.textChanged.connect(self.search_items)
        
        # Add some sample items
        items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", 
                "Fig", "Grape", "Honeydew", "Krane","Kiwi", "Lemon", "Mango"]
        for item in items:
            self.list_widget.addItem(item)
        
        self.list_widget.setFocus()
    
    def eventFilter(self, obj, event):
        # Handle events for the quick search box
        if obj == self.quick_search:
            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Escape:
                    self.quick_search.clear()
                    self.quick_search.hide()
                    self.list_widget.setFocus()
                    return True
        return super().eventFilter(obj, event)
    
    def keyPressEvent(self, event: QKeyEvent):
        # Handle Alt+character to show quick search
        if event.modifiers() == Qt.KeyboardModifier.AltModifier and event.text().isprintable():
            self.show_quick_search(event.text())
        else:
            super().keyPressEvent(event)
    
    def show_quick_search(self, initial_char=""):
        # Position the search box near the current item
        if self.list_widget.currentItem():
            rect = self.list_widget.visualItemRect(self.list_widget.currentItem())
            pos = self.list_widget.mapToGlobal(rect.topRight())
        else:
            pos = self.list_widget.mapToGlobal(self.list_widget.rect().topRight())
        
        self.quick_search.setText(initial_char)
        self.quick_search.move(pos)
        self.quick_search.show()
        self.quick_search.setFocus()
    
    def search_items(self, text):
        if not text:
            return
            
        # Search case-insensitively
        items = [self.list_widget.item(i) for i in range(self.list_widget.count())]
        
        for item in items:
            if text.lower() in item.text().lower():
                self.list_widget.setCurrentItem(item)
                self.list_widget.scrollToItem(item)
                break

