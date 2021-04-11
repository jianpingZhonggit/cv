import os
from PIL import Image
path = 'F:/voice/train/train/'
for img_name in os.listdir(path+'image'):
    img = Image.open(path+'image/'+img_name)
    img.save(path+'img/'+img_name.replace('.bmp', '.jpg'))
    # break
