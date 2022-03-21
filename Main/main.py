import math
import numpy as np
from processing import preprocessing
from save import *
from utils import *
import xml.etree.ElementTree as ET


treeA = preprocessing(ET.parse("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 1/DocumentDifferencing-1/Main/treeA.xml").getroot())
treeB = preprocessing(ET.parse("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 1/DocumentDifferencing-1/Main/treeB.xml").getroot())


costs_del = {}
costs_ins = {}
edit_scripts = {}

for subA in treeA.iter():
    path = re.split('@|#|&',subA.tag)[0]
    cdel = cost_del_tree(subA,treeB)
    costs_del[path] = cdel
print(costs_del)


for subB in treeB.iter():
    path = re.split('@|#|&',subB.tag)[0]
    cins = cost_ins_tree(subB,treeA)
    costs_ins[path] = cins
print(costs_ins)

def save_to_ES(path1, path2, s):
    key = path1 + "," + path2
    edit_scripts[key] = s

def TED(A,B):
    # if A.tag[0] != B.tag[0]:
    #     return math.inf
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

    Dist = [[0 for i in range(N+2)] for j in range(M+2)]

    # Headers:
    Dist[0][0] = "A  B"
    Dist[1][0] = A.tag
    Dist[0][1] = B.tag
    for i in range(2,len(Dist)):
        Dist[i][0] = listA[i-2].tag
    
    for j in range(2,len(Dist[0])):
        Dist[0][j] = listB[j-2].tag

    # Actual TED Matrix:
    Dist[1][1] = cost_upd(A,B)

    for i in range(2,len(Dist)):
        Dist[i][1] = int(Dist[i-1][1]) + costs_del[re.split('@|#|&',listA[i-2].tag)[0]]
    
    for j in range(2,len(Dist[0])):
        Dist[1][j] = int(Dist[1][j-1]) + costs_ins[re.split('@|#|&',listB[j-2].tag)[0]]

    for i in range(2,len(Dist)):
        for j in range(2,len(Dist[0])):
            update = int(Dist[i-1][j-1])+TED(listA[i-2],B[j-2])
            delete = int(Dist[i-1][j])+int(costs_del[re.split('@|#|&',listA[i-2].tag)[0]])
            insert = int(Dist[i][j-1])+int(costs_ins[re.split('@|#|&',listB[j-2].tag)[0]])
            Dist[i][j] = min(insert,delete,update)

            # print("Update: " + str(update) + "; Delete: " + str(delete) + "; Insert: " + str(insert))

    save_matrix(Dist)
    save_to_ES(re.split('@|#|&',A.tag)[0], re.split('@|#|&',B.tag)[0], ES(Dist))
    print_matrix(Dist)
    # print("Edit Script: " + ES())
    return(int(Dist[M+1][N+1]))

def ES(matrix):
    m = len(matrix)
    n = len(matrix[0])
    es = []

    # Pointers and value of the last element in the matrix (obtained TED)
    i = m-1
    j = n-1

    # Tracing back to start
    while(j>1 and i>1):
        current = matrix[i][j]

        if current == matrix[i-1][j] + costs_del[re.split('@|#|&',matrix[i][0])[0]]:
            # Delete treeA with path matrix[i][0]
            # current = matrix[i-1][j]
            es.append(["Delete", matrix[i][0]])
            i = i - 1
        elif current == matrix[i][j-1] + costs_ins[re.split('@|#|&',matrix[0][j])[0]]:
            # Insert treeB with path matrix[0][j]
            # current = matrix[i][j-1]
            es.append(["Insert",matrix[0][j]])
            j = j-1
        else:
            # TED of treeA of path matrix[i][0] and treeB of path matrix[0][j]
            # current = matrix[i-1][j-1]
            es.append(["TED",matrix[i][0],matrix[0][j]])
            # es += ES(TED(matrix[i][0],matrix[0][j]))
            i = i-1
            j = j - 1

    # If left with deletes   
    while(i > 1):
        current = matrix[i][j]
        es.append(["Delete",matrix[i][0]])
        i = i - 1

    # If left with inserts   
    while(j > 1):
        current = matrix[i][j]
        es.append(["Insert",matrix[i][0]])
        j = j - 1
    
    # At root:
    if(matrix[i][j] == 1):
        es.append(["Update",matrix[1][0],matrix[0][1]])

    return es   


def get_ES(edit_script):
    final_es = []
    for operation in edit_script:
        if operation[0]=="TED":
            to_find = str(re.split('@|#|&',operation[1])[0]) + "," + str(re.split('@|#|&',operation[2])[0])
            final_es.append(get_ES(edit_scripts[to_find]))
        else: final_es.append(operation)

    return final_es

x = TED(treeA,treeB)
print(edit_scripts)
edit_script = edit_scripts.popitem()[1]
print(get_ES(edit_script))
# y = get_ES(edit_script)
# print("ES: ",y)
# # print(x)

