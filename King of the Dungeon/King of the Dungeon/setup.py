import sys
from cx_Freeze import setup, Executable

build_exe_options = {"includes": ["pyglet.resource",
                                  "pyglet.clock",
                                  "pyglet.sprite"],
                     "include_files": ["resources"],
                     "include_msvcr": True}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "king_of_the_dungeon",
      version = "0.1",
      description = "A submit for Ludum Dare 33",
      options = {"build_exe": build_exe_options},
      executables = [Executable("king_of_the_dungeon.py", base=base)])