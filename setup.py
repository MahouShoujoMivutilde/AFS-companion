import sys
from cx_Freeze import setup, Executable
from os import path

base = None
if sys.platform == "win32":
    base = "Win32GUI"

ver = "1.2.1"

build_exe_options = {
    "build_exe":"build/v{}win64".format(ver),
    "include_msvcr": True,
    "include_files": [
        path.join(sys.exec_prefix, "VCRUNTIME140.dll") # Потому что include_msvcr=true, по какой-то причине, недостаточно, лол
    ],
    "excludes": [
        "email"
    ]
}

setup(
    name = "Advanced FrameServer companion ❤",
    version = ver,
    author = "MahouShoujoMivutilde",
    description = "Advanced FrameServer companion ❤",
    options = {"build_exe": build_exe_options},
    executables = [Executable("frameserver.pyw", base = base, icon = "server.ico")] # Icon made by Nikita Golubev CC 3.0 BY - http://www.flaticon.com/free-icon/server_362565
)