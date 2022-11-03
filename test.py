import math
import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle
#from plyfile import PlyData

#cfg = parse_args()

pipeline = rs.pipeline()
config = rs.config()
rs.config.enable_device_from_file(config, r"C:\Program Files\face\realsense data\cz2.bag", repeat_playback=False)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
pipeline.start(config)
align_to_color = rs.align(rs.stream.color)
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()
color = frames.get_color_frame()
pc = rs.pointcloud()
pc.map_to(color)
points = pc.calculate(depth)
verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, 3)

n_skip = 1
i = 0
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
cap_fps = 25
size = (512, 512)
video = cv2.VideoWriter('cz2.mp4', fourcc, cap_fps, size)

while i <= 1000:  # fps = 30, usually, each video lasts around 10 sec.
    frames = pipeline.wait_for_frames()
    frames = align_to_color.process(frames)
    #print("num", frames.frame_number)
    print("      "+repr(i)+",")

    if i % n_skip == 0:
        #print("Saving frame:", i)
        # saving depths
        #depth_frame = frames.get_depth_frame()
        #depth_image = np.asanyarray(depth_frame.get_data())
        #depth_image = cv2.resize(depth_image, (512, 512))
        #np.save(r"C:\Program Files\face\realsense data\test"+"/"+"frame_"+str(i).zfill(4)+"/"+"depth_0000.npy", depth_image)
        #depth_image = np.reshape(color_image, (512, 512, 3))
        #cv2.imwrite(r"C:\Program Files\face\realsense data\cz_depth_result" + "/" + str(i).zfill(6) + ".png", depth_image)
        # saving RGBs
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.resize(color_image, (512, 512))
        color_image = np.reshape(color_image, (512, 512, 3))
        video.write(color_image[:, :, ::-1])
        #print(color_image.shape)
        #cv2.imwrite(r"C:\Program Files\face\realsense data\rgb data" + "/" + str(i).zfill(6) + ".png", color_image[:, :, ::-1])
    i += 1
