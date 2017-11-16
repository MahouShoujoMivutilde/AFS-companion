# -*- mode: python -*-

from os import path

# Windows 10 SDK ddls
dlls = r'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'

pathex = ['frameserver.pyw']
if path.isdir(dlls):
    pathex += [dlls]

block_cipher = None

a = Analysis(['frameserver.pyw'],
             pathex = pathex,
             binaries = [],
             datas = [],
             hiddenimports = [],
             hookspath = [],
             runtime_hooks = [],
             excludes = [],
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             cipher = block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher = block_cipher)

exe_cli = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name = 'afs-companion-cli',
          debug = False,
          strip = False,
          upx = False,
          runtime_tmpdir = None,
          console = True,
          icon = 'server-cli.ico')

exe_no_cli = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name = 'afs-companion-d',
          debug = False,
          strip = False,
          upx = False,
          runtime_tmpdir = None,
          console = False,
          icon = 'server.ico')