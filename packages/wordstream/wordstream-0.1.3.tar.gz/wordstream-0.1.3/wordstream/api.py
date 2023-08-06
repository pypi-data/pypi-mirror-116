from urllib.request import urlopen
from random import shuffle

class Corpus(dict):

    def __init__(self, corpus=None):
        dict.__init__(corpus or {})

    def feed(self, word, association):
        self.setdefault(word, []).append(association)

    def eat(self, word):
        if word in self:
            if self[word]:
                return self[word].pop()
            else:
                del self[word]

    def feed_stream(self, stream):
        if isinstance(stream, bytes):
            stream = stream.decode('utf-8')
        if isinstance(stream, str):
            stream = stream.split()
        while len(stream) > 1:
            self.feed(stream[-2], stream[-1])
            stream.pop()

    def feed_stuff(self, *args):
        for arg in args:
            if arg.startswith('https://') or arg.startswith('http://'):
                with urlopen(arg) as response:
                    text = response.read()
            else:
                text = open(arg).read()
            self.feed_stream(text)

    def scramble(self):
        for i in self:
            shuffle(self[i])

    def save(self, f):
        named = False
        if isinstance(f, str):
            named = True
            f = open(f)
        for key in sorted(self.keys()):
            f.write("%s %s\n" % (key, ' '.join(self[key])))
        if named:
            f.close()

    def load(self, f):
        if isinstance(f, str):
            f = open(f)

    @classmethod
    def restore(cls, filename):
        corpus = cls()
        corpus.load(filename)
