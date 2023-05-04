import word2vec as w2v
import plotter
import tokenizer as tkn


def main():
    text = tkn.tokenize(tkn.song)
    vv = w2v.Veccy()
    vv.train(text)
    print(vv.predict("baby"))
    plot(vv)
    return


def plot(model):
    plotter.graph(model.LOSS)
    plotter.show_emb(model.Wo.T, model.vocab)
    pass


if __name__ == '__main__':
    main()
