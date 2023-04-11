import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
import numpy as np
import yaml


class feature():
    def __init__(self, name, id, channels, size, type, previous=None, caption=None, space=1., edgecolor='k', alpha=0.6,
                 linewidths=0.2,
                 face_color1=(0.8, 0.8, 1.0)):
        self.name = name
        self.id = id
        self.channels = channels
        self.size = size
        self.y = channels
        self.xz = (size[0], size[1])

        self.caption = caption

        self.type = type
        self.space = space
        if self.type == 'conv':
            self.facecolor = '#FFEAC1'
        elif self.type == 'relu':
            self.facecolor = '#FFC380'
            self.space = 0
        elif self.type == 'pool':
            self.facecolor = '#E16140'
        else:
            self.facecolor = '#FFEAC1'

        if previous == None:
            self.center = (0, 0, 0)
        else:
            previous_center = previous.center
            self.center = (0, previous_center[1] + previous.y / 2 + + self.y / 2 + 16 * self.space, 0)
            if self.space == 0:
                if previous.caption is not None:
                    previous.caption = (previous.caption[0], '', '')
                else:
                    previous.caption = (previous.channels, '', '')

                if self.caption is not None:
                    self.caption = ('', self.caption[0], self.caption[1])
                else:
                    self.caption = ('', self.size[0], self.size[1])

        self.alpha = alpha
        self.edgecolor = edgecolor
        self.linewidths = linewidths

    def gen_cube(self):
        self.cube = self.create_cube(self.center, (self.y, *self.xz),
                                     alpha=self.alpha, facecolor=self.facecolor, edgecolor=self.edgecolor,
                                     linewidths=self.linewidths)

        return self.cube

    def get_arrow_point(self):
        center = [*self.center]
        top = center
        top[1] += self.xz[1] / 2
        center[0] += self.y / 2
        return top, center

    def create_cube(self, center, xyz_length, alpha, facecolor, edgecolor, linewidths):
        if center is not None:
            # 根据中心坐标计算出八个顶点的坐标
            x_center, y_center, z_center = center
        else:
            x_center, y_center, z_center = 0, 0, 0

        y_length, x_length, z_length = xyz_length
        verts = []  # 顶点坐标
        verts.append((x_center - x_length / 2, y_center - y_length / 2, z_center - z_length / 2))  # 后左下
        verts.append((x_center - x_length / 2, y_center + y_length / 2, z_center - z_length / 2))  # 后右下
        verts.append((x_center + x_length / 2, y_center + y_length / 2, z_center - z_length / 2))  # 前右下
        verts.append((x_center + x_length / 2, y_center - y_length / 2, z_center - z_length / 2))  # 前左下
        verts.append((x_center - x_length / 2, y_center - y_length / 2, z_center + z_length / 2))  # 后左上
        verts.append((x_center - x_length / 2, y_center + y_length / 2, z_center + z_length / 2))  # 后右上
        verts.append((x_center + x_length / 2, y_center + y_length / 2, z_center + z_length / 2))  # 前右上
        verts.append((x_center + x_length / 2, y_center - y_length / 2, z_center + z_length / 2))  # 前左上
        vertsT = np.array(verts).T

        # 创建三维立方体的面
        cube = go.Mesh3d(
            x=vertsT[0],
            y=vertsT[1],
            z=vertsT[2],
            i=[0, 0, 4, 4, 1, 5, 0, 4, 1, 1, 2, 6],
            j=[1, 2, 5, 6, 2, 2, 3, 3, 5, 4, 3, 3],
            k=[2, 3, 6, 7, 5, 6, 4, 7, 4, 0, 6, 7],
            opacity=alpha,
            color=facecolor,
            flatshading=False,
            showscale=True,
        )

        lines = [
            # 底部两条线+一条竖线=需要标注的三条线
            [2, 3], [1, 2], [2, 6],
            # 顶部四条线
            [4, 5], [5, 6], [6, 7], [7, 4],
            # 三条竖线
            [3, 7], [1, 5],
            # 虚线的三条线
            [3, 0], [0, 1], [0, 4]
        ]
        # 创建线段并添加标签
        edge_traces = []
        annos = []
        for i, line in enumerate(lines):
            line = np.array([verts[line[0]], verts[line[1]]]).T
            if i <= 2:
                if self.caption is not None:
                    text = self.caption[i]
                else:
                    text = [self.channels, *self.size][i]
                anno = dict(x=line[0].mean(), y=line[1].mean(), z=line[2].mean(),
                            text=text, textangle=90 if i == 2 else 0,
                            showarrow=False)
                annos.append(anno)
            dash = 'solid' if i < 9 else 'dash'
            edge_trace = go.Scatter3d(
                x=line[0],
                y=line[1],
                z=line[2],
                mode='lines+text',
                line=dict(color='black', width=1, dash=dash),  # 线条颜色和宽度
                showlegend=False
            )

            edge_traces.append(edge_trace)

        return edge_traces + [cube], annos


class conn():
    def __init__(self, name, id, channels, size, type, previous=None, caption=None, space=1., edgecolor='k', alpha=0.6,
                 linewidths=0.2,
                 face_color1=(0.8, 0.8, 1.0)):
        self.name = name
        self.id = id
        self.channels = channels
        self.size = size
        self.y = channels
        self.xz = (size[0], size[1])

        self.caption = caption

        self.type = type
        self.space = space
        if self.type == 'conv':
            self.facecolor = '#FFEAC1'
        elif self.type == 'relu':
            self.facecolor = '#FFC380'
            self.space = 0
        elif self.type == 'pool':
            self.facecolor = '#E16140'
        else:
            self.facecolor = '#FFEAC1'

        if previous == None:
            self.center = (0, 0, 0)
        else:
            previous_center = previous.center
            self.center = (0, previous_center[1] + previous.y / 2 + + self.y / 2 + 16 * self.space, 0)
            if self.space == 0:
                if previous.caption is not None:
                    previous.caption = (previous.caption[0], '', '')
                else:
                    previous.caption = (previous.channels, '', '')

                if self.caption is not None:
                    self.caption = ('', self.caption[0], self.caption[1])
                else:
                    self.caption = ('', self.size[0], self.size[1])

        self.alpha = alpha
        self.edgecolor = edgecolor
        self.linewidths = linewidths

    def gen_cube(self):
        self.cube = self.create_cube(self.center, (self.y, *self.xz),
                                     alpha=self.alpha, facecolor=self.facecolor, edgecolor=self.edgecolor,
                                     linewidths=self.linewidths)

        return self.cube

    def create_cube(self, center, xyz_length, alpha, facecolor, edgecolor, linewidths):
        if center is not None:
            # 根据中心坐标计算出八个顶点的坐标
            x_center, y_center, z_center = center
        else:

            x_center, y_center, z_center = 0, 0, 0

        y_length, x_length, z_length = xyz_length
        verts = []  # 顶点坐标
        verts.append((x_center - x_length / 2, y_center - y_length / 2, z_center - z_length / 2))  # 后左下
        verts.append((x_center - x_length / 2, y_center + y_length / 2, z_center - z_length / 2))  # 后右下
        verts.append((x_center + x_length / 2, y_center + y_length / 2, z_center - z_length / 2))  # 前右下
        verts.append((x_center + x_length / 2, y_center - y_length / 2, z_center - z_length / 2))  # 前左下
        verts.append((x_center - x_length / 2, y_center - y_length / 2, z_center + z_length / 2))  # 后左上
        verts.append((x_center - x_length / 2, y_center + y_length / 2, z_center + z_length / 2))  # 后右上
        verts.append((x_center + x_length / 2, y_center + y_length / 2, z_center + z_length / 2))  # 前右上
        verts.append((x_center + x_length / 2, y_center - y_length / 2, z_center + z_length / 2))  # 前左上
        vertsT = np.array(verts).T

        # 创建三维立方体的面
        cube = go.Mesh3d(
            x=vertsT[0],
            y=vertsT[1],
            z=vertsT[2],
            i=[0, 0, 4, 4, 1, 5, 0, 4, 1, 1, 2, 6],
            j=[1, 2, 5, 6, 2, 2, 3, 3, 5, 4, 3, 3],
            k=[2, 3, 6, 7, 5, 6, 4, 7, 4, 0, 6, 7],
            opacity=alpha,
            color=facecolor,
            flatshading=False,
            showscale=True,
        )

        lines = [
            # 底部两条线+一条竖线=需要标注的三条线
            [2, 3], [1, 2], [2, 6],
            # 顶部四条线
            [4, 5], [5, 6], [6, 7], [7, 4],
            # 三条竖线
            [3, 7], [1, 5],
            # 虚线的三条线
            [3, 0], [0, 1], [0, 4]
        ]
        # 创建线段并添加标签
        edge_traces = []
        annos = []
        for i, line in enumerate(lines):
            line = np.array([verts[line[0]], verts[line[1]]]).T
            if i <= 2:
                if self.caption is not None:
                    text = self.caption[i]
                else:
                    text = [self.channels, *self.size][i]
                anno = dict(x=line[0].mean(), y=line[1].mean(), z=line[2].mean(),
                            text=text, textangle=90 if i == 2 else 0,
                            showarrow=False)
                annos.append(anno)
            dash = 'solid' if i < 9 else 'dash'
            edge_trace = go.Scatter3d(
                x=line[0],
                y=line[1],
                z=line[2],
                mode='lines+text',
                line=dict(color='black', width=1, dash=dash),  # 线条颜色和宽度
                showlegend=False
            )

            edge_traces.append(edge_trace)

        return edge_traces + [cube], annos


if __name__ == '__main__':
    feature_list = []
    annos = []
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)  # 使用 FullLoader 避免安全漏洞

        fp = None

        id = 0
        fes = []
        for i, v in config['layers'].items():
            if v.get('type') in ['conv', 'relu', 'pool']:
                fe = feature(name=v.get('name', ''),
                             id=id,
                             previous=fp,
                             space=v.get('space', 1),
                             channels=v.get('size', (0, 0, 0))[0],
                             size=(v.get('size', (0, 0, 0))[1], v.get('size', (0, 0, 0))[2]),
                             type=v.get('type', 'conv'),
                             caption=v.get('caption', None)
                             )
                fes.append(fe)
                id += 1
                fp = fe
            elif v.get('type') in ['conn', ]:
                pass

        for fe in fes:
            # fe.gen_cube()
            feature_list += fe.gen_cube()[0]
            annos += fe.gen_cube()[1]

    # 设置布局和相机参数
    layout = go.Layout(
        scene=dict(
            aspectmode="data",
            aspectratio=dict(x=1, y=1, z=1),
            xaxis=dict(showbackground=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showticklabels=False, title=""),
            annotations=annos
        ),

    )

    fig = go.Figure(data=feature_list, layout=layout)

    fig.show()
    # pyo.plot(fig, filename='scatter_plot.html')
