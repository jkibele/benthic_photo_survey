# -*- mode: python -*-
a = Analysis(['bps_gui.py', 'bps_gui.spec'],
             pathex=['C:\\Users\\jkibele\\benthic_photo_survey\\bps_package'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='bps_gui.exe',
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
               name='bps_gui')
