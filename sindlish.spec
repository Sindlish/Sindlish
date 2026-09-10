# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the Sindlish CLI executable.

Bundles interpreter/offline_docs.txt so `sindlish docs` works inside the
frozen binary, and picks the matching installer icon per platform.
"""

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent / "tools"

icon = ""
if sys.platform == "win32":
    icon = str(TOOLS_DIR / "sindlish.ico")
elif sys.platform == "darwin":
    icon = str(TOOLS_DIR / "sindlish.icns")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[(str(TOOLS_DIR.parent / "interpreter" / "offline_docs.txt"), ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="sindlish",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=icon or [],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="sindlish",
)