# -*- mode: python -*-
a = Analysis(['/home/hal/workspace/TDrafter/TDrafter.py'],
             pathex=['/home/hal/Downloads/PyInstaller-2.1/TDrafter'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='TDrafter',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='TDrafter')
