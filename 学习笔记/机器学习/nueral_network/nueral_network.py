import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import matplotlib
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
    # fig, ax_array = plt.subplots(nrows=10, ncols=10, figsize=(8, 8))

    for r in range(10):
        for c in range(10):
            ax_array[r, c].matshow(sample_images[10 * r + c].reshape((size, size)),
                                   cmap=matplotlib.cm.binary)
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))


def cost(theta, X, y):
    ''' cost fn is -l(theta) for you to minimize'''
    return np.mean(-y * np.log(sigmoid(X @ theta)) - (1 - y) * np.log(1 - sigmoid(X @ theta)))

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def regularized_cost(theta, X, y, l=1):
    '''you don't penalize theta_0'''
    theta_j1_to_n = theta[1:]
    regularized_term = (l / (2 * len(X))) * np.power(theta_j1_to_n, 2).sum()

    return cost(theta, X, y) + regularized_term

def regularized_gradient(theta, X, y, l=1):
    '''still, leave theta_0 alone'''
    theta_j1_to_n = theta[1:]
    regularized_theta = (l / len(X)) * theta_j1_to_n

    # by doing this, no offset is on theta_0
    regularized_term = np.concatenate([np.array([0]), regularized_theta])

    return gradient(theta, X, y) + regularized_term

def gradient(theta, X, y):
    '''just 1 batch gradient'''
    return (1 / len(X)) * X.T @ (sigmoid(X @ theta) - y)

def logistic_regression(X, y, l=1):
    """generalized logistic regression
    args:
        X: feature matrix, (m, n+1) # with incercept x0=1
        y: target vector, (m, )
        l: lambda constant for regularization

    return: trained parameters
    """
    # init theta
    theta = np.zeros(X.shape[1])

    # train it
    res = opt.minimize(fun=regularized_cost,
                       x0=theta,
                       args=(X, y, l),
                       method='TNC',
                       jac=regularized_gradient,
                       options={'disp': True})
    # get trained parameters
    final_theta = res.x

    return final_theta

def predict(x, theta):
    prob = sigmoid(x @ theta)
    return (prob >= 0.5).astype(int)

def nueral_network():
    #数据准备
    X, raw_y = load_data('ex3data1.mat')
    # 插入常数项，截距
    X = np.insert(X, 0, values=np.ones(X.shape[0]), axis=1)
    y_matrix = []
    # 使其向量化，具体看配图
    for i in range(1,11):
        y_matrix.append((raw_y == i).astype(int))
    # 最后一列是10，其实是数字0，最后一列放在第一列
    y_matrix = [y_matrix[-1]] + y_matrix[:-1]  # list里面前九个，加上list第一个
    y = np.array(y_matrix)
    # 一维训练
    t0 = logistic_regression(X, y[0])
    y_pred =predict(X, t0)
    print('Accuracy={}'.format(np.mean(y[0] == y_pred)))
    # K维训练
    k_theta = np.array([logistic_regression(X, y[k]) for k in range(10)])
    print(k_theta.shape)
    #k维预测
    prob_matrix = sigmoid(X @ k_theta.T)
    y_pred = np.argmax(prob_matrix, axis=1)
    print(y_pred.shape)

    y_answer = raw_y.copy()
    y_answer[y_answer == 10] = 0
    print(classification_report(y_answer, y_pred))

    # print(y.shape)
    # pick_one = np.random.randint(0, 5000)
    # plot_an_image(X[pick_one, :])
    # plt.show()
    # print('this should be {}'.format(y[pick_one]))
    # plot_100_image(X)
    # plt.show()

def feed_forward_prediction():
    theta1, theta2 = load_weight('ex3weights.mat')
    print(theta1.shape, theta2.shape)
    #原数据不转置
    X, y = load_data('ex3data1.mat', transpose=False)
    X = np.insert(X, 0, values=np.ones(X.shape[0]), axis=1)  # intercept
    a1 = X
    z2 = a1 @ theta1.T  # (5000, 401) @ (25,401).T = (5000, 25)
    print(z2.shape)
    z2 = np.insert(z2, 0, values=np.ones(z2.shape[0]), axis=1)
    a2 = sigmoid(z2)
    z3 = a2 @ theta2.T
    a3 = sigmoid(z3)
    y_pred = np.argmax(a3, axis=1) + 1  # numpy is 0 base index, +1 for matlab convention，返回沿轴axis最大值的索引，axis=1代表行
    print(y_pred.shape)
    print(classification_report(y, y_pred))


def load_weight(path):
    data = sio.loadmat(path)
    return data['Theta1'], data['Theta2']

# nueral_network()
feed_forward_prediction()