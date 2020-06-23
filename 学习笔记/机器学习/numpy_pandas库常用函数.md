# numpy库

1. shape 它的功能是查看矩阵或者数组的维数

```
c = array([[1,1],[1,2],[1,3],[1,4]]) 
c.shape      >>>(4, 2) 
c.shape[0]   >>>4 
c.shape[1]   >>>2
```

###### zeros函数

创建全0    array

```python
temp = np.zeros(theta.shape())
```

multiply函数: 对应位置乘积，如果多了会按照最大轴加1 

```python
np.multiply(a,b)
```

a.T 转置

a.dot(b)   矩阵相乘

函数：：numpy.linspace(start,stop,num=50,endpoint=True,retstep=False,dtype=None)

参数：

start：scalar类型（个人理解是标量的意思，这不是一个具体的数据类型，而是指某一些数据类型，比如int,float,bool,long,str等等都属于sclar类型）。这个数参数表示这个序列的开始值。
stop：scalar类型。如果endpoint=True。那么stop就是序列的终止数值。当endpoint=False时，返回值中不包含最后一个端点，并且步长会改变。
num：int型，可选参数，默认值为50。表示要生成的样本数，必须是非负值。
endpoint：bool类型。可选参数，默认值为True，这时stop就是最后的样本。为False时，不包含stop的值。
retstep：bool类型。可选参数，默认值为True，这时返回值是(samples,step)，前面的是数组，后面是步长。
dtype：表示输出的数组的数据类型，如果没有给出就从其他输入中推断输出的类型

```python
>>> import numpy as np
>>> a,b = np.linspace(1,49,25,True,True)
>>> a
array([ 1.,  3.,  5.,  7.,  9., 11., 13., 15., 17., 19., 21., 23., 25.,
       27., 29., 31., 33., 35., 37., 39., 41., 43., 45., 47., 49.])
>>> b
2.0
```

不包含了endpoint的情况，注意此时的step返回值，与上一个例子不一样。步长是1+25y=49，也就是stop参数跟start参数相差了(num)，并且返回的样本中不包含stop的值

```python
>>> sample,step = np.linspace(1,49,25,False,True)
>>> sample
array([ 1.  ,  2.92,  4.84,  6.76,  8.68, 10.6 , 12.52, 14.44, 16.36,
       18.28, 20.2 , 22.12, 24.04, 25.96, 27.88, 29.8 , 31.72, 33.64,
       35.56, 37.48, 39.4 , 41.32, 43.24, 45.16, 47.08])
>>> step
1.92
```

# pandas库

1. ###### 数据读取

```python
df = pd.read_csv(path='file.csv')
dfjs = pd.read_json('file.json')  可以传入json格式字符串
dfex = pd.read_excel('file.xls', sheetname=[0,1..]) 读取多个sheet页，返回多个df的字典
data.head()
data.describe()
```

2. ###### 数据插入

   Dataframe.insert(loc, column, value, allow_duplicates=False): 在Dataframe的指定列中插入数据。

       参数介绍：
        
       loc:  int型，表示第几列；若在第一列插入数据，则 loc=0
        
       column: 给插入的列取名，如 column='新的一列'
        
       value：数字，array，series等都可（可自己尝试）
        
       allow_duplicates: 是否允许列名重复，选择Ture表示允许新的列名与已存在的列名重复。

3. ###### 行， 列提取 loc, iloc

   ```python
   data.loc['a'] #通过索引提取行
   data.loc[['a','b'],['A','B']] #提取index为'a','b',列名为'A','B'中的数据
   date.iloc[0]  #通过数字提取行
   data.iloc[0:3,] #提取 0-2 行
   data.iolc[[0:3],[3,4]]  #提取0-2行，3列
   ```


#matplotlib.pyplot库

```

```

# python list np.ndarray  np.matrix区别

list和java里的数组不同之处在于, python的list可以包含任意类型的对象, 一个list里可以包含int, string或者其他任何对象, 另外list是可变长度的(list有append, extend和pop等方法).

ndarray是numpy的基石, 其实它更像一个java里面的标准数组: 所有元素有一个相同数据类型(dtype), 不过大小不是固定的.

ndarray对于大计算量的性能非常好, 所以list要做运算的时候一定要先转为array(np.array(a_list)).

matrix是ndarray的子类, 所以前面ndarray那些优点都保留了.

同时, matrix全部都是二维的, 并且加入了一些更符合直觉的函数, 比如对于matrix对象而言, 乘号运算符得到的是矩阵乘法的结果. 另外mat.I就是逆矩阵…



一个Series的完整结构包括：

数据内容部分Series.values

行索引部分Series.index

列索引 Series.columns

行索引的名字Series.index.name

相关链接： https://zhuanlan.zhihu.com/p/35592464

![img](https://pic1.zhimg.com/80/v2-b03baaccf0ca7ec26c97a979fc6540f0_720w.jpg)
