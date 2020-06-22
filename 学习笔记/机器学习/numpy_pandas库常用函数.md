#numpy库
shape 它的功能是查看矩阵或者数组的维数
```
c = array([[1,1],[1,2],[1,3],[1,4]]) 
c.shape      >>>(4, 2) 
c.shape[0]   >>>4 
c.shape[1]   >>>2
```
# pandas库
数据读取
```
df = pd.read_csv(path='file.csv')
dfjs = pd.read_json('file.json')  可以传入json格式字符串
dfex = pd.read_excel('file.xls', sheetname=[0,1..]) 读取多个sheet页，返回多个df的字典
data.head()
```

#matplotlib.pyplot库

