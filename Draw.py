from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np


def create_cube(center, xyz_length):
    if center is not None:
        # 根据中心坐标计算出八个顶点的坐标
        x, y, z = center
    else:
        x, y, z = 0, 0, 0
    x_length, y_length, z_length = xyz_length
    half_x_len, half_y_len, half_z_len = x_length / 2, y_length / 2, z_length / 2
    verts = [
        [x - half_x_len, y - half_y_len, z - half_z_len],
        [x + half_x_len, y - half_y_len, z - half_z_len],
        [x + half_x_len, y + half_y_len, z - half_z_len],
        [x - half_x_len, y + half_y_len, z - half_z_len],
        [x - half_x_len, y - half_y_len, z + half_z_len],
        [x + half_x_len, y - half_y_len, z + half_z_len],
        [x + half_x_len, y + half_y_len, z + half_z_len],
        [x - half_x_len, y + half_y_len, z + half_z_len]
    ]

    faces = [
        [verts[0], verts[1], verts[2], verts[3]],
        [verts[4], verts[5], verts[6], verts[7]],
        [verts[0], verts[1], verts[5], verts[4]],
        [verts[2], verts[3], verts[7], verts[6]],
        [verts[1], verts[2], verts[6], verts[5]],
        [verts[4], verts[7], verts[3], verts[0]]
    ]

    return faces


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=20., azim=9)

center1 = (0.5, 0, 0.5)
xyz_length1 = (1.2, 1.2, 1.2)
cube_verts1 = create_cube(xyz_length=xyz_length1, center=center1)

# 绘制第一个立方体
cube1 = Poly3DCollection(cube_verts1, alpha=0.25, edgecolor='k', linewidths=0.2)
face_color1 = (0.8, 0.8, 1.0)
cube1.set_facecolor(face_color1)
ax.add_collection3d(cube1)

# 绘制第二个立方体
# 输入中心坐标和长、宽、高画第二个立方体
center2 = (0.5, 1.88, 0.5)
xyz_length2 = (1.2, 1.2, 1.2)
cube_verts2 = create_cube(xyz_length=xyz_length2, center=center2)

cube2 = Poly3DCollection(cube_verts2, alpha=0.25, edgecolor='k', linewidths=0.2)
face_color2 = (1.0, 0.8, 0.8)
cube2.set_facecolor(face_color2)
ax.add_collection3d(cube2)

# 设置坐标轴范围
min_coord = np.array([min(center1[0], center2[0])])

# ax.set_ylim([-5, 5])
# ax.set_xlim([-5, 5])
# ax.set_zlim([-5, 5])
# ax.set_axis_off()

plt.tight_layout()
# fig.set_size_inches(18, 18)

plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
fig.savefig('myplot.pdf', bbox_inches='tight', dpi=600)  # 将图像
plt.show(aspect='auto')
