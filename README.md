## 开发文档
### 一、类
#### 1.特征层类
##### 类属性：

###### name: str 该层名称

###### channel: int 通道数，显示效果为横向厚度
###### size=(width, height)：特征图尺寸，宽和高

###### center=(x,y,z): 中心点坐标**

###### type: str 特征层类型，包括卷积层、池化层、激活层、全连接层、BN层，不同层不同颜色

##### 类方法：

初始：赋值各项属性，新建cube对象，并加入fig

get_cord：获得可以连线的点，顶部中间



#### 2.连接线类

##### 类属性：

###### name: str 连接名称

###### from_to=(obj, obj): 线条起始层和结尾层

###### type: 连接层类型，包括普通连接(默认)，跳层连接(从上跳、从下跳)

###### action: 添加操作，包括矩阵相加、Hadamard积

###### linewidths: 线条粗细

##### 类方法：



##### 二. yaml文件格式