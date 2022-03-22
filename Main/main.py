import math
import numpy as np
from save import *
from utils import *
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from patching import *


# treeA = preprocessing(ET.parse("C:/Users/ralf/Desktop/DocumentDifferencing/Main/treeA.xml").getroot())
# treeB = preprocessing(ET.parse("C:/Users/ralf/Desktop/DocumentDifferencing/Main/treeB.xml").getroot())


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
    M = degree(A)
    N = degree(B)
    
    listA = []
    for subA in A:
        listA.append(subA) 

    listB = []
    for subB in B:
        listB.append(subB)

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
            if(element_name(A)[0] == element_name(B)[0]):
                update = int(Dist[i-1][j-1])+TED(listA[i-2],B[j-2])
                delete = int(Dist[i-1][j])+int(costs_del[re.split('@|#|&',listA[i-2].tag)[0]])
                insert = int(Dist[i][j-1])+int(costs_ins[re.split('@|#|&',listB[j-2].tag)[0]])
                Dist[i][j] = min(insert,delete,update)
            else:
                delete = int(Dist[i-1][j])+int(costs_del[re.split('@|#|&',listA[i-2].tag)[0]])
                insert = int(Dist[i][j-1])+int(costs_ins[re.split('@|#|&',listB[j-2].tag)[0]])
                Dist[i][j] = min(insert,delete)

    save_to_ES(re.split('@|#|&',A.tag)[0], re.split('@|#|&',B.tag)[0], ES(Dist))
    # print_matrix(Dist)
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
            # Del(A, P) => Delete treeA (matrix[i][0]) from parent P (matrix[1][0])
            es.append(["Del", matrix[i][0], matrix[1][0]])
            i = i - 1
        elif current == matrix[i][j-1] + costs_ins[re.split('@|#|&',matrix[0][j])[0]]:
            # Ins(B, P, i) => Insert subtreeB (matrix[0][j]) at i-th child  of root P (matrix[1][0])
            es.append(["Ins",matrix[0][j],matrix[1][0],i-1])
            j = j - 1
        else:
            # TED of treeA (matrix[i][0]) and treeB (matrix[0][j])
            es.append(["TED",matrix[i][0],matrix[0][j]])
            i = i-1
            j = j - 1

    # If left with deletes   
    while(i > 1):
        current = matrix[i][j]
        es.append(["Del", matrix[i][0], matrix[1][0]])
        i = i - 1

    # If left with inserts   
    while(j > 1):
        current = matrix[i][j]
        es.append(["Ins",matrix[0][j],matrix[1][0],i-1])
        j = j - 1
    
    # At root:
    if(matrix[i][j] == 1):
        # Upd(x,elt_l) => Update node x (matrix[1][0]) with the label of treeB (matrix[0][1])
        es.append(["Upd",matrix[1][0],matrix[0][1]])

    return es   


def get_ES(edit_script):
    final_es = []
    for operation in edit_script:
        if operation[0]=="TED":
            to_find = str(re.split('@|#|&',operation[1])[0]) + "," + str(re.split('@|#|&',operation[2])[0])
            flattened = [item for sublist in get_ES(edit_scripts[to_find]) for item in sublist]
            final_es.append(flattened)
        else: final_es.append(operation)

    return final_es

# x = TED(treeA,treeB)
# print(edit_scripts)
edit_script = edit_scripts.popitem()[1]
final_ES = reversed(get_ES(edit_script))
# final_ES = [item for sublist in flat_list for item in sublist]
for x in final_ES:
    print(x)

for op in get_ES(edit_script):
    if op[0] == "Ins":
        insTree(op[1], op[2], op[3])
    elif op[0] == "Del":
        delTree(op[1], op[2])
    else: updTree(str(op[1]), str(op[2]))

def ES_to_XML(final_ES):
    root = ET.Element("Operations")

    for op in final_ES:
        if op[0] == "Ins":
            current_op = ET.SubElement(root, "Ins")
            A = ET.SubElement(current_op, "A")
            A.text = str(op[1])
            P = ET.SubElement(current_op, "P")
            P.text = str(op[2])
            i = ET.SubElement(current_op, "i")
            i.text = str(op[3])
        elif op[0] == "Del":
            current_op = ET.SubElement(root, "Del")
            A = ET.SubElement(current_op, "A")
            A.text = str(op[1])
            P = ET.SubElement(current_op, "P")
            P.text = str(op[2])
        else: 
            current_op = ET.SubElement(root, "Upd")
            x = ET.SubElement(current_op, "X")
            x.text = str(op[1])
            elt_l = ET.SubElement(current_op, "L")
            elt_l.text = str(op[2])
    
    with open('EditScript.xml','w') as f:
       ElementTree(root).write(f,encoding="unicode")

ES_to_XML(final_ES)
for x in treeA.iter():
    print(x)

