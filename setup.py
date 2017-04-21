import sys
from cx_Freeze import setup, Executable
from os import path, remove
from shutil import copyfile

ver = "1.2.2"

build_exe_options = {
    "build_exe":r"build\v{}win64".format(ver),
    "include_msvcr": True,
    "include_files": [
        path.join(sys.exec_prefix, "VCRUNTIME140.dll") # Потому что include_msvcr=true, по какой-то причине, недостаточно, лол
    ],
    "excludes": [
        "email"
    ]
}

copyfile("frameserver.pyw", "frameserver-cli.py")

setup(
    name = "Advanced FrameServer companion ❤",
    version = ver,
    author = "MahouShoujoMivutilde",
    description = "Advanced FrameServer companion ❤",
    options = {"build_exe": build_exe_options},
    executables = [
        Executable("frameserver.pyw", base = "Win32GUI", icon = "server.ico"),
        Executable("frameserver-cli.py", base = None, icon = "server.ico")
    ] # Icon made by Nikita Golubev CC 3.0 BY - http://www.flaticon.com/free-icon/server_362565
)

remove("frameserver-cli.py")