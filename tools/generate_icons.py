# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pillow>=12.2.0",
# ]
# ///
"""
Generate installer icons from the VS Code extension logo.

Run from anywhere: writes sindlish.ico, wizard BMPs, sindlish.icns and
sindlish_icon.png into this tools/ directory.
"""

from pathlib import Path

from PIL import Image

TOOLS_DIR = Path(__file__).resolve().parent


def generate_icons():
    img_path = TOOLS_DIR.parent / "vscode-extension" / "logo.png"
    if not img_path.exists():
        print(f"Error: {img_path} not found")
        return

    img = Image.open(img_path)

    # 1. Generate Windows ICO
    ico_path = TOOLS_DIR / "sindlish.ico"
    img.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Created {ico_path}")

    # 2. Generate Inno Setup BMPs
    wizard_img = img.resize((164, 314), Image.Resampling.LANCZOS)
    wizard_img.save(TOOLS_DIR / "wizard.bmp")
    small_img = img.resize((55, 55), Image.Resampling.LANCZOS)
    small_img.save(TOOLS_DIR / "wizard_small.bmp")

    # 3. Generate macOS ICNS
    icns_path = TOOLS_DIR / "sindlish.icns"
    img.save(icns_path, format="ICNS")
    print(f"Created {icns_path}")

    # 4. Generate Linux PNG (High Res)
    linux_png = TOOLS_DIR / "sindlish_icon.png"
    img.resize((512, 512), Image.Resampling.LANCZOS).save(linux_png)
    print(f"Created {linux_png}")


if __name__ == "__main__":
    generate_icons()