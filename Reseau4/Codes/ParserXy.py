import sys


def Parser(filename):
    X = []
    y = []
    f = open(filename, 'r')
    text = f.readlines()
    l = len(text)
    for i in range(l):
        line = text[i]
        line = line.replace('\n', "")
        bouts_line = line.split(' ')
        y.append(int(bouts_line[0]))
        data = []
        for i in range(len(bouts_line)-1):
            data.append(float(bouts_line[i]))
        X.append(data)
    cut = y.copy()
    for i in range(l):  # Changement de features
        prev = 1
        nex = 1
        while (i - prev) >= 0 and cut[i - prev] != 1:
            prev += 1
        while (i + nex) <= (l-1) and cut[i + nex] != 1:
            nex += 1
        X[i][0] = prev
        y[i] = nex
    return (X, y)


filename = sys.argv[1]
(X, y) = Parser(filename)
print(X)
print(y)
