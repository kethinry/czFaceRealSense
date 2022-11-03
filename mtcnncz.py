import open3d as o3d
import numpy as np

dirpath = "./denoise_depth_result"
depth_image = o3d.io.read_image(r"./denoise_depth_result/filtered906.png")
param = o3d.io.read_pinhole_camera_parameters(
                r"zero_view.json")
pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_image, param.intrinsic, param.extrinsic)
points = np.array(pcd.points)
# n = np.random.choice(len(points), 15135, replace=False)
# pcd.points = o3d.utility.Vector3dVector(points[n])
# num = np.asarray(pcd.points).shape[0]
# pcd = pcd.random_down_sample(15135 / num)
points = np.asarray(pcd.points)
vis = o3d.visualization.Visualizer()
vis.create_window('mesh', 512, 512, 50, 50, True)
vis.add_geometry(pcd)
vis.run()
print(points.shape[0])
