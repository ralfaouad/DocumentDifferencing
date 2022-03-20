import math
import numpy as np
from processing import *
from save import *
from utils import *
import xml.etree.ElementTree as ET


treeA = preprocessing(ET.parse("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 1/DocumentDifferencing-1/Main/treeA.xml").getroot())
treeB = preprocessing(ET.parse("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 1/DocumentDifferencing-1/Main/treeB.xml").getroot())


def TED(A,B):
    # if A.tag[0] != B.tag[0]:
    #     return math.inf
    script = []
    M = degree(A)
    N = degree(B)
    # print("M: ",M,"\tN: ",N)
    listA = []
    for subA in A:
        listA.append(subA)
    # print("listA: ",listA) 

    listB = []
    for subB in B:
        listB.append(subB)
    # print("listB: ",listB)

    Dist = np.zeros(shape = (M + 1, N + 1))
    ES = [[0 for i in range(N+1)] for j in range(M+1)]
    Dist[0][0] = cost_upd(A,B)
    ES[0][0] = str(A.tag) + ":" + str(B.tag)

    for i in range(1,Dist.shape[0]):
        Dist[i][0] = Dist[i-1][0] + cost_del_tree(listA[i-1],B)
        ES[i][0] = str(listA[i-1].tag) + ":" + str(B.tag)
    
    for j in range(1,Dist.shape[1]):
        Dist[0][j] = Dist[0][j-1] + cost_ins_tree(listB[j-1],A)
        ES[0][j] = str(listB[j-1].tag) + ":" + str(A.tag)

    for i in range(1,Dist.shape[0]):
        for j in range(1,Dist.shape[1]):
            update = Dist[i-1][j-1]+TED(listA[i-1],B[j-1])
            delete = Dist[i-1][j]+cost_del_tree(listA[i-1],B)
            insert = Dist[i][j-1]+cost_ins_tree(listB[j-1],A)
            Dist[i][j] = min(insert,delete,update)

            if Dist[i][j] == update:
                s = str(listA[i-1].tag) + ":" + str(B[j-1].tag)
            else:
                delete_matrix()
                if Dist[i][j] == delete:
                    s = str(listA[i-1].tag) + ":" + str(B[j].tag)
                else: s = str(listA[i].tag) + ":" + str(B[j-1].tag)

            ES[i][j] = s
            # if Dist[i][j] == insert and cost_ins_tree(listB[j-1],A) != 0: 
            #     script.append("ins("+str(listB[j-1])+")")
            # elif Dist[i][j] == delete and cost_del_tree(listA[i-1],B) != 0:
            #     script.append("del("+str(listA[i-1])+")")
            # else:
            #     if TED(listA[i-1],B[j-1])!= 0:
            #         script.append("ted("+str(listA[i-1])+", "+str(listB[j-1])+")")
    print("DIST MATRIX\n",Dist)
    save_matrix(Dist)
    
    # save_script(ES)
    # print(ES)

    return(Dist[M][N])

# def ES(matrices,index=0):
#     script=[]
#     matrix = matrices[index]
#     for i in reversed(range(matrix.shape[0])):
#         for j in reversed(range(matrix.shape[1])):
#             current = matrix[i][j]
#             if(matrix[i-1][j]+cost_del_tree(listA[i-1],B)==current):
#                 script.append("Del()")
#             if(matrix[i][j-1]+cost_ins_tree(listB[j-1],A)==current):
#                 script.append("Del()")

    
# mtrx = get_matrices()
# for x in mtrx:
#     print("test",x)
#     print()

x = TED(treeA,treeB)
print(x)



# ES(mtrx)