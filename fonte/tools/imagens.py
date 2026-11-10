"""Recorta e padroniza as fotos da clinica.
Paisagem = 3:2 (1080x720) | Retrato = 4:5 (720x900). Saida em WebP + JPG de reserva."""
import sys
from PIL import Image, ImageFilter
SRC = sys.argv[1]; OUT = sys.argv[2]
L = (1080, 720); P = (720, 900)
# nome: (arquivo, caixa de recorte (x0,y0,x1,y1), tamanho final)
JOBS = {
 "laserterapia":      ("1.png", (0, 96, 510, 436), L),
 "estudio-pilates":   ("2.png", (4, 120, 490, 444), L),
 "sala-avaliacao":    ("3.png", (0, 120, 510, 460), L),
 "sala-avaliacao-v":  ("3.png", (70, 0, 478, 510), P),
 "pilates-aluna":     ("4.png", (0, 40, 340, 465), P),
 "luanna-carvalho":   ("6.png", (62, 60, 262, 310), P),
 "bota-pneumatica":   ("7.png", (0, 135, 450, 435), L),
 "pilates-orientado": ("8.png", (0, 0, 340, 425), P),
}
for name, (f, box, size) in JOBS.items():
    im = Image.open(f"{SRC}/{f}").convert("RGB").crop(box)
    r = (box[2]-box[0])/(box[3]-box[1]); assert abs(r - size[0]/size[1]) < 0.01, (name, r)
    im = im.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=82, method=6)
    im.save(f"{OUT}/{name}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    print(name, im.size)
