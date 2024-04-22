def notin(x, y):
    return not any(all(x_elem == y_elem for x_elem, y_elem in zip(x, sub_array)) for sub_array in y)

a = [1,2]
b = [[1,3],[2,3]]

#print(notin(a,b))

def ami(x, y):
    for i, row in enumerate(y):
        if all(elem == val for elem, val in zip(x, row)):
            return i
    return -1

a2 = [2,4]
b2 = [[1,2], [1,3], [2, 3]]
#print(ami(a2, b2))

def rin(n,x):
    s = f"{{:.{x}f}}".format(n)
    return float(s)

r = rin(3.141595, 8)
#print(r)


arr = [1,2]
arr.append([])
arr[2].append(1)
#print(arr)

def matcher(s,a):
    for i in range(len(a)):
        if s == a[i]:
            return i

print(matcher("%HP",["HP", "ATK", "DEF", "%HP", "%ATK", "%DEF", "ER", "EM", "CR", "CD"]))

