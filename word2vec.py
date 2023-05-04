import numpy as np

rng = np.random.Generator(np.random.PCG64(0))

parameters = {
    "lr":   .007,
    "window":  5,
    "neurons": 300,
    "epochs":  1000
}


class Veccy:
    def __init__(self, params=None, cbow=True):
        if params is None:
            params = parameters
        self.lr = params["lr"]
        self.window = params["window"]
        self.neurons = params["neurons"]
        self.epochs = params["epochs"]

        self.CBOW = cbow
        self.LOSS = []

        self.words, self.vocab = None, None
        self.w_len, self.v_len = None, None
        self.v2dict, self.idx2dict = None, None

        self.Wi, self.Wo = None, None
        pass

    def init_data(self, text):
        self.words = np.array(text).flatten()
        self.vocab = sorted(set(self.words))

        self.w_len = len(self.words)
        self.v_len = len(self.vocab)

        self.v2dict = {v: i for i, v in enumerate(self.vocab)}
        self.idx2dict = {v: k for k, v in self.v2dict.items()}

        self.Wi = rng.uniform(size=(self.v_len, self.neurons))
        self.Wo = rng.uniform(size=(self.neurons, self.v_len))
        pass

    def generate(self):
        target, context = [], []
        for i in range(self.w_len):
            target.append(self.one_hot_encode(self.words[i]))
            j_context = []
            for j in range(i - self.window, i + self.window + 1):
                if j != i and self.w_len > j >= 0:
                    j_context.append(self.one_hot_encode((self.words[j])))
            context.append(np.array(j_context).sum(axis=0))
        return np.array(target), np.array(context)

    def one_hot_encode(self, word):
        tok = self.v2dict[word]
        np.put(hot := np.zeros(self.v_len), tok, 1)
        return hot

    def forward(self, x):
        h = x @ self.Wi
        y = self.softmax(h @ self.Wo)
        return h, y

    def backward(self, x, h, ei):
        dwo = h.T @ ei
        dwi = (self.Wo @ ei.T) @ x
        self.Wi -= self.lr * dwi.T
        self.Wo -= self.lr * dwo
        pass

    def train(self, text):
        self.init_data(text)
        targ, cont = self.generate()
        cont /= cont.sum(axis=1, keepdims=True)
        if self.CBOW: x_tr, y_tr = cont, targ
        else: x_tr, y_tr = targ, cont
        for e in range(self.epochs):
            h, y = self.forward(x_tr)
            ei = y-y_tr
            loss = self.loss(y_tr, y)
            self.backward(x_tr, h, ei)
            self.LOSS.append(loss)
            print(f"LOSS: {loss:.6f}")
        pass

    @staticmethod
    def loss(y, p):
        loss = y * np.log(p + 10e-6)
        return -np.mean(loss)

    @staticmethod
    def softmax(x):
        x -= np.max(x, axis=1, keepdims=True)
        return np.exp(x) / np.exp(x).sum(axis=1, keepdims=True)

    def predict(self, word):
        tok = self.one_hot_encode(word)
        emb = self.forward(tok[np.newaxis, :])[1].flatten()
        print(tok.shape, emb.shape)
        return list(map(self.idx2dict.get, np.argsort(emb)[::-1]))


def vprint(*args):
    for r in zip(*args): print(*r)
