import os
import subprocess
import platform

# --- Configuration ---
script_name = 'main.py'
executable_name = 'TerminalIF'
# On Linux it is common to use a PNG icon.
# (If you only have an ICO file, consider converting it to PNG.)
icon_path = './icon.png'
spec_file_name = f'{executable_name}.spec'
python_version = f"{platform.python_version_tuple()[0]}.{platform.python_version_tuple()[1]}"
virtual_env_path = './.venv'

# --- Build the Spec File for Linux ---
if platform.system() == "Linux":
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['{script_name}'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Include necessary data files for matplotlib and PIL
        ('./.venv/lib/python{python_version}/site-packages/PIL', 'PIL'),
        ('./.venv/lib/python{python_version}/site-packages/matplotlib/mpl-data', 'mpl-data'),
    ],
    hiddenimports=['PIL._tkinter_finder', 'tkinter', 'matplotlib.backends.backend_tkagg', 'PIL.ImageTk', '_tkinter', 'serial'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{executable_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='{icon_path}',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{executable_name}',
)
"""
else:
    # For Windows (or other OS), you can adapt the spec file accordingly.
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['{script_name}'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('./.venv/Lib/site-packages/PIL', 'PIL'),
        ('./.venv/Lib/site-packages/matplotlib/mpl-data', 'mpl-data'),
    ],
    hiddenimports=['PIL._tkinter_finder', 'tkinter', 'matplotlib.backends.backend_tkagg', 'PIL.ImageTk', '_tkinter', 'serial'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{executable_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='{icon_path}',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{executable_name}',
)
"""
    
# Write the spec content to the spec file
with open(spec_file_name, 'w') as file:
    file.write(spec_content)

# Step 1: Create the executable using PyInstaller and the generated spec file
subprocess.run([
    f"{virtual_env_path}/bin/pyinstaller", 
    '--onefile', 
    '--windowed', 
    f'--name={executable_name}', 
    f'--icon={icon_path}', 
    script_name
])


# Step 2: Create an install script (install.sh) that copies the executable and icon,
# and creates a desktop entry for Linux.
install_script = f"""#!/bin/bash

# Copy the executable to /usr/local/bin
sudo cp ./dist/{executable_name} /usr/local/bin/{executable_name}

# Copy the icon to /usr/share/pixmaps
sudo cp {icon_path} /usr/share/pixmaps/{executable_name}.png

# Create the desktop entry
sudo tee /usr/share/applications/{executable_name}.desktop > /dev/null <<EOF
[Desktop Entry]
Version=1.0
Name=TerminalIF
Comment=Microcontroller Interface
Exec=/usr/local/bin/{executable_name}
Icon=/usr/share/pixmaps/{executable_name}.png
Terminal=false
Type=Application
Categories=Utility;
EOF

echo "Installation complete. You can find your app in the applications menu."
"""

# Write the install script to a file
with open('install.sh', 'w') as file:
    file.write(install_script)

# Make the install script executable
os.chmod('install.sh', 0o755)

print("Compilation and installation script generation complete.")
