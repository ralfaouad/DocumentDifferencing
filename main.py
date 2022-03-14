import numpy as np
from preprocessing import preprocessing
from utils import *
import xml.etree.ElementTree as ET
treeA = preprocessing(ET.parse("treeA.xml").getroot())
treeB = preprocessing(ET.parse("treeB.xml").getroot())


def TED(A,B):
    M = degree(A)
    N = degree(B)
    print("M: ",M,"\tN: ",N)
    listA = []
    for subA in A:
        listA.append(subA)
    print("listA: ",listA) 

    listB = []
    for subB in B:
        listB.append(subB)
    print("listB: ",listB)

    Dist = np.zeros(shape=(M + 1, N + 1))
    Dist[0][0] = cost_upd(A,B)

    for i in range(1,Dist.shape[0]):
        Dist[i][0] = Dist[i-1][0] + cost_del_tree(listA[i-1],B)
    
    for j in range(1,Dist.shape[1]):
        Dist[0][j] = Dist[0][j-1] + cost_ins_tree(listB[j-1],A)

    for i in range(1,Dist.shape[0]):
        for j in range(1,Dist.shape[1]):
            Dist[i][j] = min(Dist[i-1][j-1]+TED(listA[i-1],B[j-1]),
                            Dist[i-1][j]+cost_del_tree(listA[i-1],B),
                            Dist[i][j-1]+cost_ins_tree(listB[j-1],A))
    print("DIST MATRIX\n",Dist)
    return(Dist[M][N])




x = TED(treeA,treeB)
print(x)