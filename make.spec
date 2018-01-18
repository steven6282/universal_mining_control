# -*- mode: python -*-

block_cipher = None

added_files = [
    ( './pools', 'pools' ),
    ( './conf', 'conf' ),
    ( './bin', 'bin' )
]

a = Analysis(['launcher.py'],
             pathex=['V:\\Programming\\python\\universal_mining_controller'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='universal_mining_controller',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

coll = COLLECT( exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                name='universal_mining_controller' )