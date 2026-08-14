from PIL import Image
from pathlib import Path
base = Path(r'C:\Asif_all_python_projects\INL\Improved -- blind iterations\21')
raw = Image.open(base/'Input resources'/'raw -- synthetic_npp_electrical_schematic_fixed.png')
outdir = base/'Codes and artifacts'
# x1,y1,x2,y2 around right-side 4.16kV EDG feeder chains
crops = {
    'diego_zoom_edg_201b': (3800, 650, 4850, 850),
    'diego_zoom_edg_202a': (3800, 850, 4850, 1050),
    'diego_zoom_edg_202b': (3800, 1050, 4850, 1250),
    'diego_zoom_edg_201a': (4050, 450, 4850, 650),
}
for name, box in crops.items():
    img = raw.crop(box)
    img = img.resize((img.width*3, img.height*3))
    img.save(outdir/f'{name}.png')
