# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


import os, glob, shutil


for root, dirs, files in os.walk(DISTPATH):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))


def build_datas_recursive(paths):
  datas = []

  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      dest_dirname = os.path.dirname(filename)
      if dest_dirname == "":
        dest_dirname = "."

      data_entry = (filename, dest_dirname)
      datas.append(data_entry)
      print(data_entry)

  return datas


a = Analysis(
    ['setupcheck.py'],
    pathex=[],
    binaries=[],
    datas=build_datas_recursive(['resources/**']),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Rando Setup Checker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

shutil.make_archive('Rando Setup Checker', 'zip', DISTPATH)
