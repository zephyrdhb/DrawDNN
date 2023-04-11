# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
#
# import matplotlib.pyplot as plt
#
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
#
# # Demo 1: zdir
# zdirs = (None, 'x', 'y', 'z', (1, 1, 0), (1, 1, 1))
# xs = (1, 4, 4, 9, 4, 1)
# ys = (2, 5, 8, 10, 1, 2)
# zs = (10, 3, 6, 12, 1, 8)
#
# for zdir, x, y, z in zip(zdirs, xs, ys, zs):
#     label = '(%d, %d, %d), dir=%s' % (x, y, z, zdir)
#     ax.text(x, y, z, label, zdir)
#
# # Demo 2: color
# ax.text(9, 0, 0, "red", color='red')
#
# # Demo 3: text2D
# # Placement 0, 0 would be the bottom left, 1, 1 would be the top right.
# ax.text2D(0.05, 0.95, "2D Text", transform=ax.transAxes)
#
# # Tweaking display region and labels
# ax.set_xlim(0, 10)
# ax.set_ylim(0, 10)
# ax.set_zlim(0, 10)
# ax.set_xlabel('X axis')
# ax.set_ylabel('Y axis')
# ax.set_zlabel('Z axis')
#
# plt.show()



import plotly.graph_objs as go

# 创建数据
x = [0, 1, 2, 3, 4, 5, 6]
y1 = [0, 1, 2, 3, 2, 1, 0]
y2 = [0, -1, -2, -3, -2, -1, 0]
z = [0, 1, 2, 1, 2, 1, 0]

# 创建图表对象
fig = go.Figure()

# 添加折线
fig.add_trace(go.Scatter3d(x=x, y=y1, z=z, mode='lines', name='线段1',
                           line=dict(color='blue', width=2)))
fig.add_trace(go.Scatter3d(x=x, y=y2, z=z, mode='lines',  name='线段2',
                           line=dict(color='red', width=2)))

# 更新布局
fig.update_layout(title='折回来的三维折线图', scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

# 显示图表
fig.show()







