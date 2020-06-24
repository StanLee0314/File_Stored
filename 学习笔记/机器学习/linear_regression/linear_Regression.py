import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 误差方程
def computeCost(X, y, theta):
    inner = np.power((np.dot(X, (np.transpose(theta)))) - y, 2)
    return np.sum(inner) / (2 * len(X))


'''
梯度下降
theta : h(theta)里面的 theta0， theta1
alpha: 学习率
iters: 循环次数
'''

def gradientDescent(X, y, theta, alpha, iters):
    temp = np.zeros(theta.shape)
    parameters = int(theta.shape[1])
    cost = np.zeros(iters)

    for i in range(iters):
        error = X.dot(theta.T) - y

        for j in range(parameters):
#   对应位置乘积， reshape创造一个相同shape的二维数组
            term = np.multiply(error, np.array(X[:, j]).reshape(len(X[:, j]), 1))
            temp[0, j] = theta[0, j] - ((alpha / len(X)) * np.sum(term))

        theta = temp
        cost[i] = computeCost(X, y, theta)

    return theta, cost

def single_variable():
    path ='ex1data1.txt'
    data = pd.read_csv(path, header=None, names=['Population', 'Profit'])
    data.insert(0, 'Ones', 1)
    cols = data.shape[1]
    X = data.iloc[:,0:cols-1]#X是所有行，去掉最后一列
    y = data.iloc[:,cols-1:cols]#X是所有行，最后一列
    X = X.values
    y = y.values
    theta = np.array([[0, 0]])
    alpha = 0.01
    iters = 1000
    g, cost = gradientDescent(X, y, theta, alpha, iters)
    x = np.linspace(data.Population.min(), data.Population.max(), 100)
    f = g[0, 0] + (g[0, 1] * x)
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(np.arange(iters), cost, 'r')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cost')
    ax.set_title('Error vs. Training Epoch 0.02')
    plt.show()

    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(x, f, 'r', label='Prediction')
    ax.scatter(data.Population, data.Profit, label='Traning Data')
    ax.legend(loc=2)
    ax.set_xlabel('Population')
    ax.set_ylabel('Profit')
    ax.set_title('Predicted Profit vs. Population Size')
    plt.show()

def multi_variable():
    path ='ex1data2.txt'
    data = pd.read_csv(path, header=None, names=['Size', 'Bedrooms', 'Price'])
    data = (data - data.mean())/data.std()
    print(data.head())
    data.insert(0, 'Ones', 1)
    cols = data.shape[1]
    X = data.iloc[:,0:cols-1]#X是所有行，去掉最后一列
    y = data.iloc[:,cols-1:cols]#X是所有行，最后一列
    X = X.values
    y = y.values
    theta = np.array([[0, 0, 0]])
    alpha = 0.01
    iters = 1000
    g, cost = gradientDescent(X, y, theta, alpha, iters)
    print(g)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(np.arange(iters), cost, 'r')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cost')
    ax.set_title('Error vs. Training Epoch')
    plt.show()
# single_variable()
multi_variable()
