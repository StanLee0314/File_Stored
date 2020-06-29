import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.optimize as opt


# 此处只求了梯度
# repeat交给scipy.optimize.minimize参数
def gradient(theta, X, y):
    theta = theta.reshape(1, len(theta))
    parameters = theta.shape[1]
    error = sigmoid(X.dot(theta.T)) - y
    grad = np.zeros(parameters)
    for i in range(parameters):
        term = np.multiply(error, X[:, i].reshape(len(X[:, i]), 1))
        grad[i] = np.sum(term) / (X.shape[0])
    return grad


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def costFunction(theta, X, y):
    theta = theta.reshape(1, len(theta))
    first = np.multiply(-y, np.log(sigmoid(X.dot(theta.T))))
    second = np.multiply(1 - y, np.log(1 - sigmoid(X.dot(theta.T))))
    return np.sum(first - second) / len(X)


def predict(theta, X):
    theta = theta.reshape(1, len(theta))
    probability = sigmoid(X.dot(theta.T)).ravel()
    return [1 if x >= 0.5 else 0 for x in probability]


def two_varieables():
    path = 'ex2data1.txt'
    data = pd.read_csv(path, names=['exam1', 'exam2', 'Admitted'])
    positive = data[data['Admitted'].isin([1])]
    negative = data[data['Admitted'].isin([0])]
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(positive['exam1'], positive['exam2'], s=50, c='b', marker='o', label='Admitted')
    ax.scatter(negative['exam1'], negative['exam2'], s=50, c='r', marker='x', label='Not Admitted')
    ax.legend()
    ax.set_xlabel('Exam 1 Score')
    ax.set_ylabel('Exam 2 Score')
    plt.show()
    data.insert(0, 'Ones', 1)
    cols = data.shape[1]
    X = data.iloc[:, 0:cols - 1]
    y = data.iloc[:, cols - 1:cols]
    X = X.values
    y = y.values
    theta = np.zeros(3)
    # 初始theta
    theta1 = gradient(theta, X, y)
    result = opt.minimize(fun=costFunction, x0=theta, jac=gradient, args=(X, y), options={'maxiter': 100})
    # 梯度下降， 另一种
    # result = opt.fmin_tnc(func=costFunction, x0=theta, fprime=gradient, args=(X, y))
    predictions = predict(result.x, X)
    correct = np.zeros(len(predictions))
    for i in range(len(predictions)):
        if predictions[i] == y.ravel()[i]:
            correct[i] = 1
    # correct = [1 if ((a == 1 and b == 1) or (a == 0 and b == 0)) else 0 for (a, b) in zip(predictions, y.ravel())]
    print(list(zip(predictions, y.ravel())))
    # print(list(map(int, correct)))
    #返回的是一个迭代器,使其变成int
    accuracy = (sum(map(int, correct)) % len(correct))

    print('accuracy = {0}%'.format(accuracy))
    print(zip(predictions, y.ravel()))

two_varieables()
