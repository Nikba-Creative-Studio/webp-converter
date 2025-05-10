import os
import subprocess
import sys
import platform

def build_app():
    # Create the spec file content
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['webp_converter.py'],
    pathex=[],
    binaries=[('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload/_lzma.cpython-311-darwin.so', 'lib-dynload')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WebP Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.icns' if '{platform.system()}' == 'Darwin' else 'app_icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WebP Converter',
)

if '{platform.system()}' == 'Darwin':
    app = BUNDLE(
        coll,
        name='WebP Converter.app',
        icon='app_icon.icns',
        bundle_identifier='com.nikba.webpconverter',
        info_plist={{
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
            'NSRequiresAquaSystemAppearance': 'False',
        }},
    )
"""
    
    # Write the spec file
    with open('webp_converter.spec', 'w') as f:
        f.write(spec_content)

    # Run PyInstaller
    subprocess.run(['pyinstaller', 'webp_converter.spec', '--clean'])

    print("\nBuild completed! The distribution can be found in the 'dist' folder.")
    if platform.system() == 'Darwin':
        print("You can now move 'WebP Converter.app' to your Applications folder.")
    else:
        print("You can find the executable in the 'dist/WebP Converter' folder.")

if __name__ == '__main__':
    build_app()