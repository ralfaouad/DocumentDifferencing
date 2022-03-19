from utils import*
import numpy as np



def WagnerFisher(A,B):
    strA = A
    strB = B
    M=len(strA)
    N=len(strB)
    listA = []
    for char in strA:
        listA.append(char)
    # print("listA: ",listA) 

    listB = []
    for char in strB:
        listB.append(char)
    # print("listB: ",listB)

    Dist = np.zeros(shape=(M + 1, N + 1))
    Dist[0][0] = 0

    for i in range(1,Dist.shape[0]):
        Dist[i][0] = Dist[i-1][0] + cost_del(listA[i-1])
    
    for j in range(1,Dist.shape[1]):
        Dist[0][j] = Dist[0][j-1] + cost_ins(listB[j-1])

    for i in range(1,Dist.shape[0]):
        for j in range(1,Dist.shape[1]):
            update = Dist[i-1][j-1]+cost_upd(listA[i-1],B[j-1])
            delete = Dist[i-1][j]+cost_del(listA[i-1])
            insert = Dist[i][j-1]+cost_ins(listB[j-1])
            Dist[i][j] = min(insert,delete,update)
    return Dist[M][N]



WagnerFisher("Hi there","Hithor")



        