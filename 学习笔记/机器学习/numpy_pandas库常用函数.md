# numpy库

1. shape 它的功能是查看矩阵或者数组的维数

```
c = array([[1,1],[1,2],[1,3],[1,4]]) 
c.shape      >>>(4, 2) 
c.shape[0]   >>>4 
c.shape[1]   >>>2
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

​       参数介绍：

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

#python list np.ndarray  np.matrix区别
list和java里的数组不同之处在于, python的list可以包含任意类型的对象, 一个list里可以包含int, string或者其他任何对象, 另外list是可变长度的(list有append, extend和pop等方法).

ndarray是numpy的基石, 其实它更像一个java里面的标准数组: 所有元素有一个相同数据类型(dtype), 不过大小不是固定的.

ndarray对于大计算量的性能非常好, 所以list要做运算的时候一定要先转为array(np.array(a_list)).

matrix是ndarray的子类, 所以前面ndarray那些优点都保留了.

同时, matrix全部都是二维的, 并且加入了一些更符合直觉的函数, 比如对于matrix对象而言, 乘号运算符得到的是矩阵乘法的结果. 另外mat.I就是逆矩阵…
