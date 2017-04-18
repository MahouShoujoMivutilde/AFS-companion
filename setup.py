import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Advanced FrameServer companion ❤",
    version = "1.1",
    author = "MahouShoujoMivutilde",
    description = "Advanced FrameServer companion ❤",
    executables = [Executable("frameserver.pyw", base = base, icon = "server.ico")] # Icon made by Nikita Golubev CC 3.0 BY - http://www.flaticon.com/free-icon/server_362565
)