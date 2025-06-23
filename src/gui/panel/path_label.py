from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette,QColor

class PathLabel(QLabel):
    def __init__(self,text,palette):
        super().__init__(text)
        self.palette = QPalette()
        self.palette.setColor(QPalette.ColorRole.WindowText, QColor("cyan"))
        self.palette.setColor(QPalette.ColorRole.Highlight, QColor("#008080"))
        self.palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def apply_style(self,style):
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {style['bg']};
                color: {style['text']};
                border: {style['border']};
            }}
        """)
        self.style().unpolish(self)
        self.style().polish(self)

    def highlight(self):
        self.apply_style({  
            'bg': self.palette.highlight().color().name(),
            'text': self.palette.highlightedText().color().name(),
            'border': 'none'
        })

    def unhighlight(self):
        self.apply_style({  
            'bg': 'transparent',
            'text': self.palette.windowText().color().name(),
            'border': 'none'
        })
