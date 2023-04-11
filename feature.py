import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import yaml


class feature():
    def __init__(self, name, id, channels, size, type, previous=None, caption=None, space=1., edgecolor='k', alpha=1,
                 linewidths=0.2,
                 face_color1=(0.8, 0.8, 1.0)):
        self.name = name
        self.id = id
        self.channels = channels
        self.size = size
        self.y = channels / 256
        self.xz = (size[0] / 128, size[1] / 128)

        self.caption = caption
        if space == 0:
            if previous.caption is not None:
                previous.caption = ('', previous.caption[0], '')
            else:
                previous.caption = ('', previous.channels, '')
        self.previous_center = previous.center if previous is not None else (0, 0, 0)
        self.center = (0, self.previous_center[1] + 0.4 * space + self.y, 0)
        self.alpha = alpha
        self.edgecolor = edgecolor
        self.linewidths = linewidths
        self.type = type

    def gen_cube(self):
        self.cube = self.create_cube(self.center, (self.y, *self.xz),
                                     alpha=self.alpha, edgecolor=self.edgecolor, linewidths=self.linewidths)

        if self.type == 'conv':
            self.cube.set_facecolor('#FFEAC1')
        elif self.type == 'relu':
            self.cube.set_facecolor('#FFC380')
        elif self.type == 'pool':
            self.cube.set_facecolor('#E16140')

    def get_cube(self):
        return self.cube

    def get_connect_point(self):
        point = list(self.center)
        point[2] += self.xz[1] / 2
        return tuple(point)

    def create_cube(self, center, xyz_length, alpha, edgecolor, linewidths):
        if center is not None:
            # 根据中心坐标计算出八个顶点的坐标
            x_center, y_center, z_center = center
        else:
            x_center, y_center, z_center = 0, 0, 0

        y_length, x_length, z_length = xyz_length
        verts = []  # 顶点坐标
        verts.append((x_center + x_length / 2, y_center + y_length / 2, z_center - z_length / 2))  # 右上前
        verts.append((x_center + x_length / 2, y_center + y_length / 2, z_center + z_length / 2))  # 右上后
        verts.append((x_center + x_length / 2, y_center - y_length / 2, z_center - z_length / 2))  # 右下前
        verts.append((x_center + x_length / 2, y_center - y_length / 2, z_center + z_length / 2))  # 右下后
        verts.append((x_center - x_length / 2, y_center + y_length / 2, z_center - z_length / 2))  # 左上前
        verts.append((x_center - x_length / 2, y_center + y_length / 2, z_center + z_length / 2))  # 左上后
        verts.append((x_center - x_length / 2, y_center - y_length / 2, z_center - z_length / 2))  # 左下前
        verts.append((x_center - x_length / 2, y_center - y_length / 2, z_center + z_length / 2))  # 左下后

        faces = [
            [verts[0], verts[1], verts[3], verts[2]],  # 前
            [verts[4], verts[5], verts[7], verts[6]],  # 后
            [verts[2], verts[3], verts[7], verts[6]],  # 左
            [verts[0], verts[1], verts[5], verts[4]],  # 右
            [verts[1], verts[3], verts[7], verts[5]],  # 上
            [verts[0], verts[2], verts[6], verts[4]],  # 下
        ]

        linex = (verts[0], verts[4])
        liney = (verts[0], verts[2])
        linez = (verts[0], verts[1])
        lines = [linex, liney, linez]
        rotation = ['x', 'y', 'z']
        for i, line in enumerate(lines):
            (x0, y0, z0), (x1, y1, z1) = line
            x = (x0 + x1) / 2 if rotation[i] != 'x' else (x0 + x1) / 2 + abs(x1 - x0) / 4
            y = (y0 + y1) / 2
            z = (z0 + z1) / 2 if rotation[i] != 'z' else (z0 + z1) / 2 - abs(z1 - z0) / 4
            if self.caption is None:
                label = self.channels if rotation[i] == 'y' else self.size[i - 1]
                label = int(label)
            else:
                label = self.caption[i]
            ax.text(x, y, z, label, rotation[i], ha='center', va='top',
                    color='k', fontsize=4, zorder=100, )
        poly = Poly3DCollection(faces, alpha=alpha, edgecolor=edgecolor, linewidths=0.2, zorder=np.exp(-self.id))

        # edge_coords = [[verts[6], verts[2]], [verts[6], verts[4]], [verts[6], verts[7]]]
        # poly_dash = Line3DCollection(edge_coords, alpha=1, colors='k', linewidths=0.5, linestyles='--')
        # ax.add_collection3d(poly_dash)
        poly.set_linestyle('--')
        return poly


if __name__ == '__main__':
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)  # 使用 FullLoader 避免安全漏洞

        fp = None
        feature_list = []
        id = 0
        for i, v in config['layers'].items():
            fe = feature(name=v.get('name', ''),
                         id=id,
                         previous=fp,
                         space=v.get('space', 1),
                         channels=v.get('size', (0, 0, 0))[0],
                         size=(v.get('size', (0, 0, 0))[1], v.get('size', (0, 0, 0))[2]),
                         type=v.get('type', 'conv'),
                         caption=v.get('caption', None)
                         )
            id += 1
            feature_list.append(fe)
            fp = fe

    fig = plt.figure(dpi=600)

    # ax = Axes3D(fig)
    ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
    ax.view_init(elev=5., azim=20)

    for i in feature_list:
        i.gen_cube()
    for i in feature_list:
        ax.add_collection3d(i.get_cube())

    # ax.autoscale(enable=True)
    ax.auto_scale_xyz([-2, 2], [0, 4 * 0.9], [0, 4])

    ax.set_axis_off()

    plt.tight_layout()
    fig.savefig('myplot.pdf', bbox_inches='tight', dpi=600)  # 将图像

    plt.show()
