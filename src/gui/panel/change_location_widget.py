from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget,QGridLayout,QLabel
from PyQt6.QtCore import Qt, pyqtSignal,QEvent

import json
import os

if os.name == "nt": # WINDOWS
    LOCATIONS_CONFIGURATION = os.path.join('gui','panel','config','mount_points_list.json') 
if os.name == "posix": # LINUX
    LOCATIONS_CONFIGURATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config','mount_points_list.json')
     
class ChangeLocationWidget(QWidget):
    returnPressed = pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.mounts_list = QListWidget()
        self.mounts_list.installEventFilter(self) # TODO: read about installEventFilter
        
        with open(LOCATIONS_CONFIGURATION) as f:
            data = json.load(f)
            mounts = data["LOCATIONS"]
        
        for m in mounts:
            self.mounts_list.addItem(QListWidgetItem(m))

        self.labels = [QLabel('Location'), QLabel(' Ins Del Shift+Del F4 F9 Ctrl+Alt+F')]

        layout = QGridLayout()
        layout.addWidget(self.labels[0])
        layout.addWidget(self.mounts_list)
        layout.addWidget(self.labels[1])
        self.setLayout(layout)

        self.setAutoFillBackground(True) 
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True) # initially widget doesn't have background color at all
        self.hide()

    def eventFilter(self,obj,event):
        # to fix losing control if mounts_list loses focus
        if obj == self.mounts_list and event.type() == QEvent.Type.FocusOut:
            self.hide()
            return True

        return super().eventFilter(obj,event)

    def keyPressEvent(self,event):
        from system_api import KEY
        if event.key() == KEY.ENTER:
            self.returnPressed.emit(self.mounts_list.currentItem().text())

    def setFocus(self):
        self.mounts_list.setFocus()

    def hasFocus(self):
        return self.mounts_list.hasFocus()
