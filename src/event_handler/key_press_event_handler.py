from .main_window_events import commands_pressed as main_pressed,commands_released as main_released
from .text_editor_events import commands_pressed as editor_pressed, commands_released as editor_released

from gui import MainWidget,TextEditorWidget

class KeyHandler:
    def __init__(self,main_window):
        self.main_window = main_window

    def get_key_handler(self,commands,key,modifier):
        if (modifier,key) in commands:
            return commands[(modifier,key)]
        if modifier in commands:
            return commands[(modifier)]
        if key in commands:
            return commands[(key)]
        return lambda _: None

    def handle_key_press(self,event):
        widget = self.main_window.currentWidget()
        try:
            if isinstance(widget,MainWidget):       
                self.get_key_handler(main_pressed,event.key(),event.modifiers())(self.main_window)
            if isinstance(widget,TextEditorWidget): 
                self.get_key_handler(editor_pressed,event.key(),event.modifiers())(self.main_window)
        except Exception as e:
            print(str(e))

    def handle_key_release(self,event):
        widget = self.main_window.currentWidget()
        try:
            if isinstance(widget,MainWidget):       
                self.get_key_handler(main_released,event.key(),event.modifiers())(self.main_window)
            if isinstance(widget,TextEditorWidget): 
                self.get_key_handler(editor_released,event.key(),event.modifiers())(self.main_window)
        except Exception as e:
            print(str(e))
