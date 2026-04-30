"""
NumerPy Solver — Gerador de Ícone
==================================
Cria assets/icon.ico para o app desktop.
Rode: python create_icon.py
"""

import os

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow não instalado. Instalando...")
    os.system(f"{os.sys.executable} -m pip install Pillow -q")
    from PIL import Image, ImageDraw, ImageFont

SIZE = 256
img = Image.new("RGBA", (SIZE, SIZE), (44, 62, 80, 255))  # #2C3E50
draw = ImageDraw.Draw(img)

# Círculo de destaque (fundo)
draw.ellipse([20, 20, SIZE - 20, SIZE - 20], fill=(52, 152, 219, 255))  # #3498DB

# Letra N centralizada
try:
    font = ImageFont.truetype("arialbd.ttf", 140)
except:
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140)
    except:
        font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), "N", font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
x = (SIZE - text_w) // 2
y = (SIZE - text_h) // 2 - 10

draw.text((x, y), "N", font=font, fill=(255, 255, 255, 255))

# Salvar em múltiplas resoluções para .ico
ico_path = os.path.join("assets", "icon.ico")
os.makedirs("assets", exist_ok=True)

sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
images = [img.resize(s, Image.Resampling.LANCZOS) for s in sizes]
img.save(ico_path, format="ICO", sizes=[(i.width, i.height) for i in images])

print(f"Ícone criado: {ico_path}")
