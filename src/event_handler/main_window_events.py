from system_api import KEY
from PyQt6.QtCore import Qt

ALT   = Qt.KeyboardModifier.AltModifier 
CTRL  = Qt.KeyboardModifier.ControlModifier
SHIFT = Qt.KeyboardModifier.ShiftModifier
NONE  = Qt.KeyboardModifier.NoModifier

commands_released = {
    NONE:lambda window: window.mainWidget.update_buttons_text("NONE"),
}

commands_pressed = {
    CTRL:             lambda window: window.update_buttons_text("CTRL"),
    SHIFT:            lambda window: window.update_buttons_text("SHIFT"),
    ALT:              lambda window: window.update_buttons_text("ALT"),

    KEY.F1:           lambda window: print('not implemented: help (basically manual'),
    KEY.F2:           lambda window: print('not implemented: far says it\' UserMn but it just shows random menu to me'),
    KEY.F3:           lambda window: print('not implemented: view (like using less command)'),
    KEY.F4:           lambda window: (
                            filepath := window.mainWidget.get_focused_file_or_folder(),
                            window.textWidget.open_file_temp(filepath),
                            window.switchWidget(),
    ),
    KEY.F5:           lambda window: print('not implemented:copy'),
    KEY.F6:           lambda window: print('not implemented:move'),
    KEY.F7:           lambda window: window.mainWidget.show_input_dialog(),
    KEY.F8:           lambda window: window.mainWidget.show_deletion_dialog(),
    KEY.F9:           lambda window: print('not implemented:options'),
    KEY.F10:          lambda window: window.close(),
    KEY.F11:          lambda window: print('not implemented: plugins'), # do I need them?
    KEY.F12:          lambda window: print('not implemented: screens'), # I don't use them myself, so hard to say

    #(ALT,KEY.F1):       lambda window: print('not implemented: change left panel path '),
    #(ALT,KEY.F2):       lambda window: print('not implemented: change right panel path'),
    (ALT,KEY.F3):       lambda window: print('not implemented: view (why does Far have same function key)'),
    (ALT,KEY.F4):       lambda window: print('not implemented: edit... (difference?)'),
    (ALT,KEY.F5):       lambda window: print('not implemented: Print (umm I doubt it applies to printers though)'),
    (ALT,KEY.F6):       lambda window: print('not implemented: Make link '),
    (ALT,KEY.F7):       lambda window: print('not implemented: Find'),
    (ALT,KEY.F8):       lambda window: print('not implemented: History (of commands)'),
    (ALT,KEY.F9):       lambda window: print('not implemented: Video (I dunno what it does)'),
    (ALT,KEY.F10):      lambda window: print('not implemented: Tree (even interactable one)'),
    (ALT,KEY.F11):      lambda window: print('not implemented: ViewHs (shows different history to me, but I can\'t tell the difference)'), # do I need them?
    (ALT,KEY.F12):      lambda window: print('not implemented: FolderHistory (more confused)'), # I don't use them myself, so hard to say

    (CTRL,KEY.F1):      lambda window: print('not implemented: Left (I guess change panel path'),
    (CTRL,KEY.F2):      lambda window: print('not implemented: Right (I guess change panel path'),
    (CTRL,KEY.F3):      lambda window: print('not implemented: sort by Name'),
    (CTRL,KEY.F4):      lambda window: print('not implemented: sort by Extension'),
    (CTRL,KEY.F5):      lambda window: print('not implemented: sort by Write Time'),
    (CTRL,KEY.F6):      lambda window: print('not implemented: sort by size'),
    (CTRL,KEY.F7):      lambda window: print('not implemented: unsort (:D)'),
    (CTRL,KEY.F8):      lambda window: print('not implemented: creatn (maybe by creation time?)'),
    (CTRL,KEY.F9):      lambda window: print('not implemented: access (dunno what it does)'),
    (CTRL,KEY.F10):     lambda window: print('not implemented: descrp (dunno what it does)'),
    (CTRL,KEY.F11):     lambda window: print('not implemented: owner  (maybe sorts by ownership)'), # do I need them?
    (CTRL,KEY.F12):     lambda window: print('not implemented: sort (umm how?)'), # I don't use them myself, so hard to say
    
    (SHIFT,KEY.F1):     lambda window: print('not implemented: add to archive'),
    (SHIFT,KEY.F2):     lambda window: print('not implemented: extract (from archive)'),
    (SHIFT,KEY.F3):     lambda window: print('not implemented: archive commands (do I need that?)'),
    (SHIFT,KEY.F4):     lambda window: print('not implemented: create and edit file'),
    (SHIFT,KEY.F5):     lambda window: print('not implemented: copy'),
    (SHIFT,KEY.F6):     lambda window: print('not implemented: rename'),
    (SHIFT,KEY.F8):     lambda window: print('not implemented: delete'), # do I need this while using shift?
    (SHIFT,KEY.F9):     lambda window: print('not implemented: save options settings'),
    (SHIFT,KEY.F10):    lambda window: print('not implemented: last used option (I don\'t use it)'),
    (SHIFT,KEY.F11):    lambda window: print('not implemented: group (I dunno what it does)'), # do I need them?
    (SHIFT,KEY.F12):    lambda window: print('not implemented: selUp (I dunno what it does)'), # I don't use them myself, so hard to say
}
