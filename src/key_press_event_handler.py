from system_api import KEY
from PyQt6.QtCore import Qt

#from gui.make_folder_dialog import MakeFolderDialog
#from gui.error_dialog import ErrorDialog

ALT = Qt.KeyboardModifier.AltModifier 
CTRL = Qt.KeyboardModifier.ControlModifier
SHIFT = Qt.KeyboardModifier.ShiftModifier
NONE = Qt.KeyboardModifier.NoModifier

class KeyHandler:
    def handle_key(event):
        modifier = event.modifiers()
        key = event.key()

        try:
            if (modifier, key) in KeyHandler.commands:                
                return KeyHandler.commands[(modifier,key)]
        except:
            return lambda _: None
        return lambda _: None

    commands = {
            # NO MODIFIERS
            (NONE,KEY.F1):  lambda mainWindow: print('not implemented: help (basically manual'),
            (NONE,KEY.F2):  lambda mainWindow: print('not implemented: far says it\' UserMn but it just shows random menu to me'),
            (NONE,KEY.F3):  lambda mainWindow: print('not implemented: view (like using less command)'),
            (NONE,KEY.F4):  lambda mainWindow: print('not implemented:create and edit file'),
            (NONE,KEY.F5):  lambda mainWindow: print('not implemented:copy'),
            (NONE,KEY.F6):  lambda mainWindow: print('not implemented:move'),
            (NONE,KEY.F7):  lambda mainWindow: mainWindow.mainWidget.show_input_dialog(),
            (NONE,KEY.F8):  lambda mainWindow: mainWindow.mainWidget.show_deletion_dialog(),
            (NONE,KEY.F9):  lambda mainWindow: print('not implemented:options'),
            (NONE,KEY.F10): lambda mainWindow: mainWindow.close(),
            (NONE,KEY.F11): lambda mainWindow: print('not implemented: plugins'), # do I need them?
            (NONE,KEY.F12): lambda mainWindow: print('not implemented: screens'), # I don't use them myself, so hard to say

            # SINGLE MODIFIERS (ALT)
            (ALT,KEY.F1):  lambda mainWindow: print('not implemented: change left panel path '),
            (ALT,KEY.F2):  lambda mainWindow: print('not implemented: change right panel path'),
            (ALT,KEY.F3):  lambda mainWindow: print('not implemented: view (why does Far have same function key)'),
            (ALT,KEY.F4):  lambda mainWindow: print('not implemented: edit... (difference?)'),
            (ALT,KEY.F5):  lambda mainWindow: print('not implemented: Print (umm I doubt it applies to printers though)'),
            (ALT,KEY.F6):  lambda mainWindow: print('not implemented: Make link '),
            (ALT,KEY.F7):  lambda mainWindow: print('not implemented: Find'),
            (ALT,KEY.F8):  lambda mainWindow: print('not implemented: History (of commands)'),
            (ALT,KEY.F9):  lambda mainWindow: print('not implemented: Video (I dunno what it does)'),
            (ALT,KEY.F10): lambda mainWindow: print('not implemented: Tree (even interactable one)'),
            (ALT,KEY.F11): lambda mainWindow: print('not implemented: ViewHs (shows different history to me, but I can\'t tell the difference)'), # do I need them?
            (ALT,KEY.F12): lambda mainWindow: print('not implemented: FolderHistory (more confused)'), # I don't use them myself, so hard to say
            # SINGLE MODIFIERS (CTRL) mostly responsible for sortin
            (CTRL,KEY.F1):  lambda mainWindow: print('not implemented: Left (I guess change panel path'),
            (CTRL,KEY.F2):  lambda mainWindow: print('not implemented: Right (I guess change panel path'),
            (CTRL,KEY.F3):  lambda mainWindow: print('not implemented: sort by Name'),
            (CTRL,KEY.F4):  lambda mainWindow: print('not implemented: sort by Extension'),
            (CTRL,KEY.F5):  lambda mainWindow: print('not implemented: sort by Write Time'),
            (CTRL,KEY.F6):  lambda mainWindow: print('not implemented: sort by size'),
            (CTRL,KEY.F7):  lambda mainWindow: print('not implemented: unsort (:D)'),
            (CTRL,KEY.F8):  lambda mainWindow: print('not implemented: creatn (maybe by creation time?)'),
            (CTRL,KEY.F9):  lambda mainWindow: print('not implemented: access (dunno what it does)'),
            (CTRL,KEY.F10): lambda mainWindow: print('not implemented: descrp (dunno what it does)'),
            (CTRL,KEY.F11): lambda mainWindow: print('not implemented: owner  (maybe sorts by ownership)'), # do I need them?
            (CTRL,KEY.F12): lambda mainWindow: print('not implemented: sort (umm how?)'), # I don't use them myself, so hard to say
            # SINGLE MODIFIERS (SHIFT)
            (SHIFT,KEY.F1):  lambda mainWindow: print('not implemented: add to archive'),
            (SHIFT,KEY.F2):  lambda mainWindow: print('not implemented: extract (from archive)'),
            (SHIFT,KEY.F3):  lambda mainWindow: print('not implemented: archive commands (do I need that?)'),
            (SHIFT,KEY.F4):  lambda mainWindow: print('not implemented: create and edit file'),
            (SHIFT,KEY.F5):  lambda mainWindow: print('not implemented: copy'),
            (SHIFT,KEY.F6):  lambda mainWindow: print('not implemented: rename'),
            (SHIFT,KEY.F8):  lambda mainWindow: print('not implemented: delete'), # do I need this while using shift?
            (SHIFT,KEY.F9):  lambda mainWindow: print('not implemented: save options settings'),
            (SHIFT,KEY.F10): lambda mainWindow: print('not implemented: last used option (I don\'t use it)'),
            (SHIFT,KEY.F11): lambda mainWindow: print('not implemented: group (I dunno what it does)'), # do I need them?
            (SHIFT,KEY.F12): lambda mainWindow: print('not implemented: selUp (I dunno what it does)'), # I don't use them myself, so hard to say
        }


