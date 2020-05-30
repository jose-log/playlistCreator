

d = {}
l = []

for i in range(10):
	d['a'] = i
	d['b'] = i * i
	l.append(d.copy())
	print(d)

print(l)
print(l[0])
print(l[5])