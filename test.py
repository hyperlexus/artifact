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

print(ca3([0, 1, 0, [1, 4, 8, 9]], [0, 1, 0, [8, 9, 12]], 1))
print(ca3([0, 1, 0, [1, 4, 8, 9]], [0, 1, 0, [8, 4, 9]], 1))