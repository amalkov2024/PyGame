def main():
    '''lab = []
    rdl = list(map(int,input().split()))
    n = rdl[0]
    m = rdl[1]
    for i in range(n):
        rdl = input()
        stroka = []
        for k in range(len(rdl)):
            if int(rdl[k]) == 1:
                stroka.append(-1)
            else:
                stroka.append(int(rdl[k]))
        lab.append(stroka)
    rdl = list(map(int,input().split()))
    x1 = rdl[0] -1
    y1 = rdl[1] -1
    rdl = list(map(int,input().split()))
    x2 = rdl[0]
    y2 = rdl[1]
'''
    lab=[[-1, 0, 0, 0, 0, 0, 0, -1, 0, 0], [-1, 0, -1, -1, -1, -1, 0, -1, 0, 0], [-1, 0, 0, 0, 1, -1, 0, -1, 0, 0], [-1, -1, -1, -1, -1, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    print(lab)
    x1 = 2
    y1 = 4
    x2 = 6
    y2 = 1
    n=len(lab)
    m=len(lab[0])
    #finalout = voln(x1,y1,1,n,m,lab)
    if lab[x2][y2] > 0:
        print("Mozhet")
        print(lab)
    else:
        print("Ne mozhet")
def voln(x,y,cur,n,m,lab):
    lab[x][y] = cur
    if y+1<m:
        if lab[x][y+1] == 0 or (lab[x][y+1] != -1 and lab[x][y+1] > cur):
            voln(x,y+1,cur+1,n,m,lab)
    if x+1<n:
        if lab[x+1][y] == 0 or (lab[x+1][y] != -1 and lab[x+1][y] > cur):
            voln(x+1,y,cur+1,n,m,lab)
    if x-1>=0:
        if lab[x-1][y] == 0 or (lab[x-1][y] != -1 and lab[x-1][y] > cur):
            voln(x-1,y,cur+1,n,m,lab)
    if y-1>=0:
        if lab[x][y-1] == 0 or (lab[x][y-1] != -1 and lab[x][y-1] > cur):
            voln(x,y-1,cur+1,n,m,lab)
    return lab
main()

'''
2 4 6 1
[[-1, 0, 0, 0, 0, 0, 0, -1, 0, 0], [-1, 0, -1, -1, -1, -1, 0, -1, 0, 0], [-1, 0, 0, 0, 1, -1, 0, -1, 0, 0], [-1, -1, -1, -1, -1, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, -1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

'''