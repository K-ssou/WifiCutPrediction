import sys
def Parser(filename):
	X=[]
	y=[]
	f = open(filename, 'r')
	text=f.readlines()
	l = len(text)
	for i in range(l-1):
		line = text[i]
		line = line.replace('\n','')
		result = text[i+1]
		result = result.replace('\n','')
		bouts_line = line.split(' ')
		bouts_res = result.split(' ')
		y.append(int(bouts_res[0]))
		data = []
		for i in range(len(bouts_line)-1):
			data.append(float(bouts_line[i]))
		X.append(data)
	return (X, y)

filename = sys.argv[1]
(X, y) = Parser(filename)
print(len(X))
print(len(y))