import cProfile

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

def matcher(s,a):
    for i in range(len(a)):
        if s == a[i]:
            return i
#print(matcher("%HP",["HP", "ATK", "DEF", "%HP", "%ATK", "%DEF", "ER", "EM", "CR", "CD"]))

def cia(a1,a2,n):
    return len(set(a1) & set(a2)) >= n

#print(cia([1,2,3,4,5,6],[1,2,3,4,5],0))

def ca3(a, b, n):
    if len(a) != len(b):
        print(f"{a}, {b}")
        return False
    count = 0
    for i in range(len(a)):
        if type(a[i]) == list:
            for j in b[3]:
                if j in a[3]:
                    count += 1
            return count >= n
        else:
            if a[i] != b[i]:
                return False
    return True

#print(ca3([0, 1, 0, [1, 4, 8, 9]], [0, 1, 0, [8, 9, 12]], 1))
#print(ca3([0, 1, 0, [1, 4, 8, 9]], [0, 1, 0, [8, 4, 9]], 1))

def cso(di):
    d = {"HP": 6, "ATK": 6, "DEF": 6, "%HP": 4, "%ATK": 4, "%DEF": 4, "ER": 4, "EM": 4, "CR": 4, "CD": 4}
    tw,pr = sum(d.values()),1.0
    for i in di:
        if i in d:
            iw = d[i]
            pr *= iw / tw
            tw -= iw
            del d[i]
    return pr


di = ["CR"]

pr = cso(di)
#print("The probability of getting the desired items is:", pr)