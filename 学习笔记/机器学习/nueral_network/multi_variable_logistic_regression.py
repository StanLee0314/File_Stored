import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat
import  scipy.optimize as opt


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
    #正则化添加 punishment
    reg = (learningRate / (2 * len(X))) * np.sum(np.power(theta[:,1:theta.shape[1]], 2))
    return np.sum(first - second) / len(X) + reg


def predict(theta, X):
    theta = theta.reshape(1, len(theta))
    probability = sigmoid(X.dot(theta.T)).ravel()
    return [1 if x >= 0.5 else 0 for x in probability]


# 构建分类器，因为有十个数字，所以需要十个分类器
# 每行为一个参数的分类器
def one_vs_all(X, y, num_labels, learning_rate):
    rows = X.shape[0]
    params = X.shape[1]
    # 二维数组，增加截距
    all_theta = np.zeros((num_labels, params + 1))
    X = np.insert(X, 0, values=np.ones(rows), axis=1)
    # labels are 1-indexed instead of 0-indexed
    for i in range(1, num_labels + 1):
        theta = np.zeros(params + 1)
        y_i = np.array([1 if label == i else 0 for label in y])
        y_i = np.reshape(y_i, (rows, 1))

        # minimize the objective function
        fmin = opt.minimize(fun=costFunction, x0=theta, args=(X, y_i, learning_rate), method='TNC', jac=gradient)
        all_theta[i - 1, :] = fmin.x

    return all_theta

def regularization():

    path = 'ex3data1.mat'
    data = loadmat(path)
    X = data['X']
    y = data['y']
    learningRate = 1
    num_labels = int(10)
    all_theta = one_vs_all(X, y, num_labels, learningRate)
    h_prediction = predict_all(X,all_theta)
    correct = [1 if a == b else 0 for(a, b) in zip(h_prediction, y)]
    accuracy = sum(map(int, correct))/len(correct)
    print('accurracy is {0}%'.format(accuracy * 100))

def predict_all(X, all_theta):
    rows = X.shape[0]
    params = X.shape[1]
    num_labels = all_theta.shape[0]

    # same as before, insert ones to match the shape
    X = np.insert(X, 0, values=np.ones(rows), axis=1)

    # compute the class probability for each class on each training instance
    h = sigmoid(X.dot(all_theta.T))

    # create array of the index with the maximum probability
    h_argmax = np.argmax(h, axis=1)

    # 从第0行开始，所以预测的数字应该+1
    h_argmax = h_argmax + 1

    return h_argmax

regularization()