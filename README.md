# File manager
Two-panel file manager clone written in python. Doing for myself as small project

# TODO:  
  Panels:
  - [x] Add highlighting for folders/files
    - [x] Add option to configure color for different set of files (partially done needs another dialog window to configure it)
  - [ ] Add ability to select multiple files  
  - [ ] (AFTER SELECTION IMPLEMENTATION): Add info at the bottom of the a panel
    - [ ] Current files usage space
    - [ ] Selected file count
    - [ ] Selected folder count
  - [ ] Add ability to hide one or both panels with Ctrl+O or Ctrl+P shortcut
  - [ ] Add info at the bottom of a panel for a folder:
    - [ ] Current files usage space
    - [ ] Selected file count
    - [ ] Selected folder count    
  - [ ] Add info about current file/folder:
    - [ ] File/folder name
    - [ ] Size
    - [ ] Creation date: 01-01-1970 12:00
  - [ ] Add ability to quickly jump to folder/file by using Alt+\<Any characacter\>
  - [ ] Add ability to quickly watch file contents without opening an editor by using Ctrl+Q shortcut (more like mode)
  - [x] Add buttons cheat sheet bar at the bottom
  - [ ] Add current time on right panel path label
  - [ ] (AFTER CTRL KEY EVENTS IMPLEMENTATION) Add character representing what sort is currently in use
  - [ ] Make panel hide current selected item if it loses focus

  Buttons bar cheat sheet:
  - [ ] Add ability to hide buttons bar py pressing Ctrl+B
  - [ ] Add buttons functionality when clicking
  
  Text editor:  
  - [ ] Add information about editor in some sort of bar with following information:
    - [ ] Name of opened file
    - [ ] Encoding of the file
    - [ ] Current cursor position in file like line number and column number
    - [ ] Character code (like for 0-9 codes are 48-57)
    - [ ] Current time
           
  Some plugins implementation:
  - [ ] NameEditor:
    - [ ] Add ability to bulk rename files by using template
    - [ ] Add ability to bulk rename files by passing list of selected files and passing it to editor       
  - [ ] Audio music player: play any music in app itself
  
# FIX:
  Text editor:
  - [ ] - Editor still remembers opened file and if trying to open another and caughting an exception you'd open last opened file
