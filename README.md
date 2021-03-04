<img src="/res/icon.png" alt="hb_icon" width="100"/>

# Hummingbird Editor

This is a little notebook, with two visible editors. First one for main long notes. Second one for easy accessible additional side notes. Notebook also contains a simple task list.

Current version is `0.8`

![Hummingbird main window](/res/screenshot_01.png)

## How to run

You can run Hummingbird by downloading this repository and go with `python3 hb.py` command in root directory. For now. Windows and Linux executables are planned for next releases.

## Features

In this version contains:

- Two editors
- Task list
- Autosave
- Light / Dark theme
- Focus mode
- Possibility of storing multiple notebooks

## Keyboard shortcuts

You can work with Hummingbird using only keyboard. Available shortcuts are listed below:

- `F1`: show info panel
- `F2`: focus on main note
- `F3`: focus on side note
- `F4`: focus on tasks list
- `F5`: switch notebooks
- `F7`: switch between light and dark theme
- `F8`: switch between normal and focus mode of main editor
- `F9`: show settings panel
- `F10`: save all notes and tasks, then quit application
- `F11`: toggle fullscreen
- `ESC`: hide dialogs
- `Ctrl+S`: Save all notes immediately

## Development

To organize development of this app I prepared simple roadmap document. It is available [here](ROADMAP.md)

## Credits

The beautiful Hummingbird logo is made by [Freepik](https://www.flaticon.com/authors/freepik) and came from [flaticon.com]("http://www.flaticon.com) site.

## Changelog

#### Ver. 0.4
- Last 40 saves are stored in database

#### Ver. 0.5
- Many editor parameters are now stored in database. Those are settings, window size and position.

#### Ver. 0.6
- Editor now has dark theme and focus mode, but only theme is remembered in database.

#### Ver. 0.7
- Full screen mode
- Now you can create and switch between multiple notebooks
- App information now has special separate window

#### Ver. 0.8
- Focus mode setting is stored into database
- Application settings dialog now has mode and theme switches
- Notebook now has a task list:

![Hummingbird task list view](/res/screenshot_02.png)

#### Ver. 0.9
_tbc_