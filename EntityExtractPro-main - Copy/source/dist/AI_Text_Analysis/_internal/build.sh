#!/bin/bash

echo "Updating environment..."
conda remove pathlib -y

echo "Creating PyInstaller spec file..."

cat > AI_Text_Analysis.spec << EOL
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('en_core_web_sm', 'en_core_web_sm'),
                    ('azure', 'azure')] + 
                    (collect_data_files('example inputs') if os.path.exists('example inputs') else []),
             hiddenimports=['spacy', 'transformers', 'torch', 'PIL', 'docx', 'fitz', 'pytesseract', 'azure'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AI_Text_Analysis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
EOL

echo "Building AI Text Analysis executable..."

# Create executable
pyinstaller AI_Text_Analysis.spec

# Create package folder
mkdir -p AI_Text_Analysis_Package

# Copy executable and necessary folders
if [ -d "dist/AI_Text_Analysis" ]; then
    cp -R dist/AI_Text_Analysis AI_Text_Analysis_Package/
else
    echo "Warning: dist/AI_Text_Analysis not found. Build may have failed."
fi

for dir in logs results highlighted "example inputs"; do
    if [ -d "$dir" ]; then
        cp -R "$dir" "AI_Text_Analysis_Package/"
    else
        echo "Warning: $dir not found. Skipping..."
    fi
done

# Create README file
cat > AI_Text_Analysis_Package/README.txt << EOL
Instructions for running AI Text Analysis:
1. Open a terminal in this folder
2. Run the command: ./AI_Text_Analysis
3. Follow the on-screen instructions to analyze your documents
EOL

echo "Build complete!"