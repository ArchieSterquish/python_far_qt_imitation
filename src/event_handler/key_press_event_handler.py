from PyQt6.QtGui import QKeyEvent
from .main_window_events import commands_pressed as main_pressed,commands_released as main_released
from .text_editor_events import commands_pressed as editor_pressed, commands_released as editor_released

from gui import MainWidget,TextEditorWidget

class KeyHandler:
    def get_key_handler(commands,key,modifier):
        try:
            if (modifier,key) in commands:
                return commands[(modifier,key)]
            if (modifier) in commands:
                return commands[(modifier)]
        except:
            return lambda _: None
        return lambda _:None

    def handle_key_press(event:QKeyEvent,widget):
        if isinstance(widget,MainWidget):       return KeyHandler.get_key_handler(main_pressed,event.key(),event.modifiers())
        if isinstance(widget,TextEditorWidget): return KeyHandler.get_key_handler(editor_pressed,event.key(),event.modifiers())

    def handle_key_release(event:QKeyEvent,widget):
        if isinstance(widget,MainWidget):       return KeyHandler.get_key_handler(main_released,event.key(),event.modifiers())
        if isinstance(widget,TextEditorWidget): return KeyHandler.get_key_handler(editor_released,event.key(),event.modifiers())
