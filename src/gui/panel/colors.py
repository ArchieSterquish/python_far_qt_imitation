from PyQt6.QtGui import QBrush,QColor

COLOR_FOLDER = QBrush(QColor(255,165,0))
COLOR_FILE = QBrush(QColor(255,255,255))

COLOR_EXTENSIONS ={
    # Folders
    "folder": QBrush(QColor(255, 165, 0)),  
    
    ".py":   QBrush(QColor(65, 105, 225)),    
    ".cpp":  QBrush(QColor(100, 149, 237)),  
    ".js":   QBrush(QColor(240, 219, 79)),    
    ".html": QBrush(QColor(227, 79, 56)),   
    ".css":  QBrush(QColor(86, 61, 124)),    
    
    # Documents
    ".pdf":  QBrush(QColor(220, 20, 60)),    
    ".docx": QBrush(QColor(0, 100, 0)),     
    ".doc":  QBrush(QColor(0, 100, 0)),     
    ".xlsx": QBrush(QColor(0, 128, 0)),     
    
    # Media
    ".jpg": QBrush(QColor(218, 165, 32)),   
    ".mp3": QBrush(QColor(138, 43, 226)),   
    ".mp4": QBrush(QColor(219, 112, 147)), 

    # archives
    ".7z":  QBrush(QColor(255,0,255)), 
    ".zip": QBrush(QColor(255,0,255)), 
    ".tar": QBrush(QColor(255,0,255)), 
    ".rar": QBrush(QColor(255,0,255)), 
    
    # Default file color
    "_default": QBrush(QColor(200, 200, 200))  
}
