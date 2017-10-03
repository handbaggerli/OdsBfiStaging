# -*- mode: python -*-

block_cipher = None


a = Analysis(['OdsBfiStaging.py'],
             pathex=['D:\\GitRepos\\OdsBfiStaging\\Python'],
             binaries=[],
              datas=[('database/config/*', 'database/config'), 
			        ('database/indexes/*', 'database/indexes'),
					('database/packages/KND200/*', 'database/packages/KND200'),
					('database/packages/*', 'database/packages'),
					('database/tables/*', 'database/tables'),
					('network-connect-2.ico', ''),
					('database-refresh.ico', '')
					],
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
          name='OdsBfiStaging',
          debug=False,
          strip=False,
          upx=True,
          console=True,
		  icon='database-refresh.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='OdsBfiStaging')
