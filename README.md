## 使用文档

以特征层的形式可视化DNN的结构

Visualize DNN(Deep Neural Network) in the form of feature layers

#### yaml文件格式

```yaml
layers:
  conv1:
    type: 'conv' # required 'conv', 'relu', 'pool'
    size: [ 64, 122, 122 ] # required 
    caption: [ 64,122,122 ] # optional to adjust the size of cube
  relu1:
    type: 'relu'
    size: [ 16, 122, 122 ]
    space: 0 # the default of 'relu' layer's space is 0

  conn1:
    type: 'conn' # 'conn' 'skip conn'
    from: 'relu1' # previous layer
    to: 'layer1' # next layer
```
运行/run
```shell
python feature_ploty.py
```
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