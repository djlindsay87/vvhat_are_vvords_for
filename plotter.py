import matplotlib.pyplot as plt
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=np.ComplexWarning)


def graph(loss):
    plt.plot(loss, label='loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.show()
    return


def show_emb(emb, labels):
    emb = pca(emb)
    x, y, z = zip(*emb)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x, y, z)
    for i, lab in enumerate(labels):
        ax.text(x[i], y[i], z[i], lab)
    plt.show()
    pass


def pca(data, k=3):
    data -= np.mean(data, axis=0)
    cov = np.cov(data, rowvar=False)
    eig_val, eig_vec = np.linalg.eig(cov)
    idx = np.argsort(eig_val)[::-1]
    eig_vec = eig_vec[:, idx]
    return np.dot(data, eig_vec[:, :k])
