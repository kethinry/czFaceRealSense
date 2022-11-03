import numpy as np
import os
from sklearn.cluster import DBSCAN
from argparse import Namespace
from collections import Counter
from PIL import Image
import matplotlib
from matplotlib.collections import LineCollection

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

camera_matrix = {'xc': 127.5, 'zc': 127.5, 'f': 128}
camera_matrix = Namespace(**camera_matrix)
def get_point_cloud_from_z(Y, camera_matrix, scale=1):
    x, z = np.meshgrid(np.arange(Y.shape[-1]),
                       np.arange(Y.shape[-2] - 1, -1, -1))
    for i in range(Y.ndim - 2):
        x = np.expand_dims(x, axis=0)
        z = np.expand_dims(z, axis=0)
    X = (x[::scale, ::scale] - camera_matrix.xc) * Y[::scale, ::scale] / camera_matrix.f
    Z = (z[::scale, ::scale] - camera_matrix.zc) * Y[::scale, ::scale] / camera_matrix.f
    XYZ = np.concatenate((X[..., np.newaxis], Y[::scale, ::scale][..., np.newaxis]
                          ,Z[..., np.newaxis]), axis=X.ndim)
    return XYZ
path = "./cz_depth_result"
dirpath = "./denoise_depth_result"
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
files= os.listdir(path)
cnt = 1
for file in files:
    cnt = cnt+1
    image = Image.open(path+"/"+file)
    img = np.array(image)
    img[img < 1000] = 0
    img[img > 2000] = 0
    x, y = np.indices(img.shape)
    idx = img > 0
    data = np.stack([x[idx], y[idx], img[idx]]).T
    recon = np.zeros_like(img)
    recon[data[:, 0], data[:, 1]] = data[:, 2]
    assert (recon == img).all()
    cluter = DBSCAN(eps=5, min_samples=5).fit(data)
    cluter.labels_
    ct = Counter(cluter.labels_)
    keys = set(k for k, v in ct.most_common()[:10] if k != -1)
    iidx = np.zeros_like(cluter.labels_, dtype=bool)
    for k in keys:
        iidx = np.logical_or(iidx, cluter.labels_ == k)
    new_data = data.copy()
    new_data[:, 2][~iidx] = 0

    recon = np.zeros_like(img)
    recon[new_data[:, 0], new_data[:, 1]] = new_data[:, 2]
    XYZ = get_point_cloud_from_z(recon, camera_matrix, scale=1)
    ax = plt.axes(projection='3d')
    ax.plot(np.ndarray.flatten(XYZ[::, ::, 0]), np.ndarray.flatten(XYZ[::, ::, 1]), np.ndarray.flatten(XYZ[::, ::, 2]),
            'b.', markersize=0.2)

    plt.title('point cloud')
    Image.fromarray(recon).save(dirpath+'/filtered'+str(cnt)+".png")