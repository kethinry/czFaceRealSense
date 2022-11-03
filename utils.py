from PIL import Image
import numpy as np
image = Image.open('depthv2.png')
img = np.array(image)
img[img<1000] = 0
img[img>2000] = 0
filtered = Image.fromarray(img)
filtered.save('filtered.png')