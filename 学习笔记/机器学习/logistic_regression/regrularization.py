import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt




def gradient(theta, X, y, learningRate):
    theta = theta.reshape(1, len(theta))
    parameters = theta.shape[1]
    error = sigmoid(X.dot(theta.T)) - y
    grad = np.zeros(parameters)
    for i in range(parameters):
        term = np.multiply(error, X[:, i].reshape(len(X[:, i]), 1))
        if i ==0:
            grad[i] = np.sum(term) / (X.shape[0])
        else:
            grad[i] = np.sum(term) / (X.shape[0]) + (learningRate)/ (X.shape[0]) * theta[:, i]
    return grad


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def costFunction(theta, X, y, learningRate):
    theta = theta.reshape(1, len(theta))
    first = np.multiply(-y, np.log(sigmoid(X.dot(theta.T))))
    second = np.multiply(1 - y, np.log(1 - sigmoid(X.dot(theta.T))))
    reg = (learningRate / (2 * len(X))) * np.sum(np.power(theta[:,1:theta.shape[1]], 2))
    return np.sum(first - second) / len(X) + reg


def predict(theta, X):
    theta = theta.reshape(1, len(theta))
    probability = sigmoid(X.dot(theta.T)).ravel()
    return [1 if x >= 0.5 else 0 for x in probability]

def regularization():
    path = 'ex2data2.txt'
    data = pd.read_csv(path, header=None, names=['test1', 'test2', 'Admitted'])
    positive = data[data['Admitted'].isin([1])]
    negative = data[data['Admitted'].isin([0])]
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(positive['test1'], positive['test2'], s=50, c='g', marker='o', label= 'Admitted')
    ax.scatter(negative['test1'], negative['test2'], s=50, c='r', marker='x', label= 'Rejected')
    ax.legend()
    ax.set_xlabel('test1')
    ax.set_xlabel('test2')
    plt.show()
    data.insert(3, 'Ones', 1)
    x1 = data['test1'].values
    x2 = data['test2'].values
    # 多项式阶数为五层，根据泰勒公式展开, F32 = x1^(3-2) * x2^2
    degree = 5
    for i in range(1, degree):
        for j in range(0, i):
            data['F' + str(i) + str(j)] = np.power(x1,  i - j) * np.power(x2, j)
    # 默认删除行， axis为1 时为删除列
    data.drop('test1', inplace= True, axis=1)
    data.drop('test2', inplace= True, axis=1)
    print(data.head())
    cols = data.shape[1]
    X = data.iloc[:, 1:cols]
    y = data.iloc[:, 0:1]
    X = np.array(X.values)
    y = np.array(y.values)
    theta = np.zeros(11,dtype=float)
    learningRate = float(1)
    cost = gradient(theta, X, y, learningRate)
    print(cost)
    result = opt.minimize(fun=costFunction, x0=theta, jac=gradient, args=(X, y, float(1)), options={'maxiter': 100})
    # 梯度下降， 另一种
    # result = opt.fmin_tnc(func=costFunction, x0=theta, fprime=gradient, args=(X, y))
    predictions = predict(result.x, X)
    correct = np.zeros(len(predictions))
    for i in range(len(predictions)):
        if predictions[i] == y.ravel()[i]:
            correct[i] = 1
    # correct = [1 if ((a == 1 and b == 1) or (a == 0 and b == 0)) else 0 for (a, b) in zip(predictions, y.ravel())]
    # print(list(zip(predictions, y.ravel())))
    # print(list(map(int, correct)))
    #返回的是一个迭代器,使其变成int
    accuracy = (sum(map(int, correct)) % len(correct))
    print('accuracy = {0}%'.format(accuracy))

    # 虽然我们实现了这些算法，值得注意的是，我们还可以使用高级Python库像scikit-learn来解决这个问题
    from sklearn import linear_model  # 调用sklearn的线性回归包
    model = linear_model.LogisticRegression(penalty='l2', C=1.0)
    model.fit(X, y.ravel())
    print('python高级包准确率：')
    print(model.score(X,y))


regularization()