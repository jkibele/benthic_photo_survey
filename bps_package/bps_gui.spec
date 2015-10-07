# -*- mode: python -*-

# I'm manually copying the gdal_data, docs, and test_data dirs
# after running pyinstaller. In theory, I could modify this 
# spec file to make that happen but it's easier this way for now.

# $ pyinstaller -D bps_gui.py bps_gui.spec

a = Analysis(['bps_gui.py'],
             pathex=['C:\\Users\\jkibele\\benthic_photo_survey\\bps_package'],
             hiddenimports=['scipy.special._ufuncs_cxx'],
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
