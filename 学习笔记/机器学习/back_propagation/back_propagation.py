import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import matplotlib
from sklearn.preprocessing import OneHotEncoder
import scipy.optimize as opt
#这个包是评价报告
from sklearn.metrics import classification_report


def load_data(path, transpose=True):
    data = sio.loadmat(path)
    y = data.get('y')  # (5000,1)
    y = y.reshape(y.shape[0])  # make it back to column vector
    X = data.get('X')  # (5000,400)

    if transpose:
        # for this dataset, you need a transpose to get the orientation right
        X = np.array([im.reshape((20, 20)).T for im in X])

        # and I flat the image again to preserve the vector presentation
        X = np.array([im.reshape(400) for im in X])

    return X, y


#绘图函数
def plot_an_image(image):
#     """
#     image : (400,)
#     """
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.matshow(image.reshape((20, 20)), cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))  # just get rid of ticks
    plt.yticks(np.array([]))


# 绘图函数，画100张图片
def plot_100_image(X):

    size = int(np.sqrt(X.shape[1]))

    # 在所有数据里面选一百条数据
    sample_idx = np.random.choice(np.arange(X.shape[0]), 100)  # 100*400
    sample_images = X[sample_idx, :]

    fig, ax_array = plt.subplots(nrows=10, ncols=10, sharey=True, sharex=True, figsize=(8, 8))

    for r in range(10):
        for c in range(10):
            ax_array[r, c].matshow(sample_images[10 * r + c].reshape((size, size)),
                                   cmap=matplotlib.cm.binary)
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))

def expand_y(y):
    # encoder = OneHotEncoder(sparse=False)
    y = y.reshape(len(y), 1)
    encoder = OneHotEncoder(sparse=False)
    y_onehot = encoder.fit_transform(y)
    print(y_onehot.shape)
    return y_onehot

def load_weight(path):
    data = sio.loadmat(path)
    return data['Theta1'], data['Theta2']

def serialize(a,b):
    # 序列化2矩阵
    # 在这个nn架构中，我们有theta1（25,401），theta2（10,26），它们的梯度是delta1，delta2
    return np.concatenate((np.ravel(a), np.ravel(b)))

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 前向传播函数
def forward_propagate(X, theta1, theta2):
    m = X.shape[0]
    a1 = np.insert(X, 0, np.ones(X.shape[0]), axis=1)
    z2 = a1.dot(theta1.T)
    a2 = np.insert(sigmoid(z2),0, values=np.ones(m), axis=1)
    z3 = a2.dot(theta2.T)
    h = sigmoid(z3)
    return a1, z2, a2, z3, h

# 代价函数
def costFunction(params, input_size, hidden_size, num_labels, X, y, learning_rate):
    m = X.shape[0]
    X = np.array(X)
    y = np.array(y)
    # reshape the parameter array into parameter matrices for each layer
    theta1 = np.array(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
    theta2 = np.array(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))

    # run the feed-forward pass
    a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

    # compute the cost
    J = 0
    for i in range(m):
        first_term = np.multiply(-y[i, :], np.log(h[i, :]))
        second_term = np.multiply((1 - y[i, :]), np.log(1 - h[i, :]))
        J += np.sum(first_term - second_term)

    J = J / m
    # 增加正则化
    J += (float(learning_rate) / (2 * m)) * (np.sum(np.power(theta1[:, 1:], 2)) + np.sum(np.power(theta2[:, 1:], 2)))

    return J

# 接下来是反向传播算法。 反向传播参数更新计算将减少训练数据上的网络误差。
# 我们需要的第一件事是计算我们之前创建的Sigmoid函数的梯度的函数
def sigmoid_gradient(z):
    return np.multiply(sigmoid(z), (1 - sigmoid(z)))

# 反向传播
def backprop(params, input_size, hidden_size, num_labels, X, y, learning_rate):
    m = X.shape[0]
    X = np.array(X)
    y = np.array(y)

    # reshape the parameter array into parameter matrices for each layer
    theta1 = np.array(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
    theta2 = np.array(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))

    # run the feed-forward pass
    a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

    # initializations
    J = 0
    delta1 = np.zeros(theta1.shape)  # (25, 401)
    delta2 = np.zeros(theta2.shape)  # (10, 26)

    # compute the cost
    for i in range(m):
        first_term = np.multiply(-y[i, :], np.log(h[i, :]))
        second_term = np.multiply((1 - y[i, :]), np.log(1 - h[i, :]))
        J += np.sum(first_term - second_term)

    J = J / m

    # add the cost regularization term
    J += (float(learning_rate) / (2 * m)) * (np.sum(np.power(theta1[:, 1:], 2)) + np.sum(np.power(theta2[:, 1:], 2)))

    # perform backpropagation
    for t in range(m):
        a1t = a1[t, :]  # (1, 401)
        z2t = z2[t, :]  # (1, 25)
        a2t = a2[t, :]  # (1, 26)
        ht = h[t, :]  # (1, 10)
        yt = y[t, :]  # (1, 10)

        d3t = ht - yt  # (1, 10)

        z2t = np.insert(z2t, 0, values=np.ones(1))  # (1, 26)
        d2t = np.multiply((theta2.T * d3t.T).T, sigmoid_gradient(z2t))  # (1, 26)

        delta1 = delta1 + (d2t[:, 1:]).T * a1t
        delta2 = delta2 + d3t.T * a2t

    delta1 = delta1 / m
    delta2 = delta2 / m

    # add the gradient regularization term
    delta1[:, 1:] = delta1[:, 1:] + (theta1[:, 1:] * learning_rate) / m
    delta2[:, 1:] = delta2[:, 1:] + (theta2[:, 1:] * learning_rate) / m

    # unravel the gradient matrices into a single array
    grad = np.concatenate((np.ravel(delta1), np.ravel(delta2)))

    return J, grad


def main():
    path = 'ex4data1.mat'
    X, y = load_data(path)
    # 增加全部为1的一列
    plot_100_image(X)
    plt.show()
    y_onehot = expand_y(y)
    t1, t2 = load_weight('ex4weights.mat')
    theta = serialize(t1, t2)  # 扁平化参数，25*401+10*26=10285
    #theta.shape ,(10285,)
    # 初始化设置
    input_size = 400
    hidden_size = 25
    num_labels = 10
    learning_rate = 1
    # 随机初始化完整网络参数大小的参数数组
    # 长度10285
    params = (np.random.random(size=hidden_size * (input_size + 1) + num_labels * (hidden_size + 1)) - 0.5) * 0.25
    m = X.shape[0]
    X = np.array(X)
    y = np.array(y)

    # 将参数数组解开为每个层的参数矩阵
    # theta1 维度[25,401] 在前向传播时 +1 特征值
    # theta2 维度[10,26]
    theta1 = np.array(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
    theta2 = np.array(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))
    a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)
    cost = costFunction(params, input_size, hidden_size, num_labels, X, y_onehot, learning_rate)
    print(cost)

if __name__ == '__main__':
    main()