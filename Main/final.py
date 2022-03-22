import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import regex as re
import PySimpleGUI as sg


# STEP 1: Document Preprocessing
def preprocessing(elt,depth=0,path=""):
    if elt is None:
        return None
    newtree = Element(path + str(depth) + ".&" + str(elt.tag))

    new_path = path + str(depth) + "." 
    d = 0

    for key,value in sorted(elt.attrib.items()):
        attr_path = new_path + str(d) + "."
        attr_key = SubElement(newtree, attr_path + "@" + str(key))
        attr_value = SubElement(attr_key, attr_path + "0." + "#" + str(value))
        d += 1
    
    for child in elt:
        newtree.append(preprocessing(child, d, new_path))
        d += 1

    if elt.text is not None:
        tokens = elt.text.split()
        for token in tokens:
            tk = SubElement(newtree, new_path + str(d) + ".#" + str(token))
            d+=1
    return newtree   

# STEP 2: Document Differencing
costs_del = {}
costs_ins = {}
edit_scripts = {}

def degree(root):
    deg = 0
    for child in root:
        deg+=1
    return deg
    
def cost_ins(n):
    return 1

def cost_del(n):
    return 1

def cost_upd(n1,n2):
    return 0 if (re.split('@|#|&',n1.tag)[1]) == (re.split('@|#|&',n2.tag)[1]) else 1

def cost_ins_tree(treeA, treeB):
    print("cost_ins_tree(",treeA,",",treeB,": ",1 if contained_in(treeA,treeB) else len(list(treeA.iter())))
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))

def cost_del_tree(treeA, treeB):
    print("cost_del_tree(",treeA,",",treeB,": ",1 if contained_in(treeA,treeB) else len(list(treeA.iter())))
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))

#  Contained-in as seen in slides
# def isMatching(treeA, treeB):
#     if re.split('@|#|&',treeA.tag)[1] != re.split('@|#|&',treeB.tag)[1]:
#         return False
#     else:
#         listA = []
#         for childA in treeA:
#             listA.append(childA)
#         listB = []
#         for childB in treeB:
#             listB.append(childB)
#         return contains(listB,listA)

# def contains(listA,listB):
#     newA = []
#     newB = []
#     minIndex = -1
#     for A in listA:
#         newA.append(re.split('@|#|&',A.tag)[1])
#     for B in listB:
#         newB.append(re.split('@|#|&',B.tag)[1])
#     for B in newB:
#         if B in newA and newA.index(B)>minIndex:
#             minIndex = newA.index(B)
#         else:
#             return False
#     return True
        

def get_size(root):
    # includes root
    count = 0
    for element in root.iter():
        count +=1
    return count

def contained_in(treeA, treeB):
    rootA = re.split('@|#|&',treeA.tag)[1]
    rootB = re.split('@|#|&',treeB.tag)[1]
    
    if(rootA == rootB):
        if get_size(treeA) == 1 and get_size(treeB) == 1:
            return True

        if get_size(treeA) > 1:
            children_B = []
            for child_B in treeB:
                children_B.append(child_B)
            for child_A in treeA:
                while(children_B):
                    if re.split('@|#|&',child_A.tag)[1] == re.split('@|#|&',children_B.pop(0).tag)[1] :
                        break
                if(children_B): return contained_in(child_A,treeB)
    
    a = False
    for child_B in treeB:
        a = a or contained_in(treeA, child_B)
    return a

def get_tree(path,tree):
    path_list = path.split(".")
    if(len(path_list) == 1):#2):
        return tree
    target = int(path_list[1])

    children =[]
    for child in tree:
        children.append(child)
    print("children list: \t"+str(children))
    if(len(children) == 0):
        return tree
    else: return get_tree(".".join(path_list[1:]) , children[target])

def path(element):
    return re.split('.@|.#|.&',element)[0]

def element_name(element):
    l = str(element).split(".")
    return l[-1]   

def save_to_ES(path1, path2, s):
    key = path1 + "," + path2
    edit_scripts[key] = s


def calculcate_costs(treeA,treeB):
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

def get_ES(edit_script):
    final_es = []
    for operation in edit_script:
        if operation[0]=="TED":
            to_find = str(re.split('@|#|&',operation[1])[0]) + "," + str(re.split('@|#|&',operation[2])[0])
            flattened = [item for sublist in get_ES(edit_scripts[to_find]) for item in sublist]
            final_es.append(flattened)
        else: final_es.append(operation)

    return final_es

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

def reformat(es):
    tr = []
    for i in range(len(es)):
        if op[i] == "Del":
            dellist = []
            for j in range(i,i+3):
                dellist.append(es[j])
            tr.append(dellist)
        elif op[i] == "Ins":
            inslist = []
            for j in range(i,i+4):
                inslist.append(es[j])
            tr.append(inslist)
        else:
            if op[i] == "Upd":
                updlist = []
                for j in range(i,i+3):
                    updlist.append(es[j])
                tr.append(updlist)
            
    return tr


# Storing the ES in an XML file
def ES_to_XML(final_ES,dest):
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
    
    with open(dest,'w') as f:
       return ElementTree(root).write(f,encoding="unicode")



# Step 4: Patching Document
def insTree(B, P, i):
    parent = get_tree(path(P), treeA)
    parent.insert(i, get_tree(path(B),treeB))

def delTree(A, P):
    parent = get_tree(path(P), treeA)
    parent.remove(get_tree(path(A),treeA))

def updTree(x, elt_l):
    element = get_tree(path(x),treeA)
    element.tag = path(x) + "." + element_name(elt_l)

def apply_patch(patch):
    operations = ET.parse(str(patch))
    root = operations.getroot()
    for op in root:
        if op.tag == "Ins":
            A = op.find("A").text
            P = op.find("P").text
            i = int(op.find("i").text)
            insTree(A,P,i)
        if op.tag == "Del":
            A = op.find("A").text
            P = op.find("P").text
            delTree(A,P)
        if op.tag == "Upd":
            X = op.find("X").text
            L = op.find("L").text
            updTree(X,L)


# GUI
layout = [[sg.Text("Document Differencing Tool")],
        [sg.Text('Document A', size=(15, 1)), sg.InputText(key="DOCA"), sg.FileBrowse(file_types=(("XML Files", "*.xml"), ("ALL Files", "*.*")))],
        [sg.Text('Document B', size=(15, 1)), sg.InputText(key="DOCB"), sg.FileBrowse(file_types=(("XML Files", "*.xml"), ("ALL Files", "*.*")))],
        [sg.Button("Start")],
        [sg.Text("", size=(0, 1), key='OUTPUT')],
        [sg.Text("", size=(0, 1), key='ES')],
        [sg.Text("Patch File Name: "),sg.InputText(key="PATCHNAME"), sg.FileBrowse(file_types=(("XML Files", "*.xml"), ("ALL Files", "*.*")))],
        [sg.Button("Patch")],
        [sg.Text('',size=(0,1),key="FLAG")]
]

window = sg.Window('Document Differencing', layout, finalize=True)
while True:
        event, values = window.read()
        print(event,values)
        if event in (sg.WIN_CLOSED, 'Exit'):
             break
        if event == 'Start':
            # print(event,values)

            # Preprocessing input files
            parsedA = ET.parse(values["DOCA"])
            parsedB = ET.parse(values["DOCB"])
            treeA = preprocessing(parsedA.getroot())
            treeB = preprocessing(parsedB.getroot())

            # Calculating TED
            calculcate_costs(treeA,treeB)
            distance = TED(treeA,treeB)

            # Displaying Distance and Similarity
            val = "Distance: "+str(distance)+"\t"
            val= val + "Similarity: "+ str(float(1/(1+distance)))

            # Getting the edit script
            edit_script = edit_scripts.popitem()[1]
            rev_es = reversed(get_ES(edit_script))
            es =[]
            for op in rev_es:
                es.append(op)
            # print(es)
            flat_es_list = [item for sublist in es for item in sublist]
            # print(flat_es_list)
            finalES = reformat(flat_es_list)
            #Patched File
            #XML
            window["OUTPUT"].update(value=val)
            window["ES"].update(value=finalES)
        if event == "Patch":
            filename = values["PATCHNAME"]
            print("FILENAMEEEE: ",filename)
            patch = ES_to_XML(finalES,filename)
            # print("PAATCH: ",patch)
            apply_patch(filename)
            window["FLAG"].update(value="File Successfully Patched.")
            print("*"*100)
            for x in treeA.iter():
                print(x)
window.close()


# Step of Calculations before applying TED (Nierman and Jagadish)
# calculcate_costs(treeA,treeB)

# Running the TED Algorithm
# distance = TED(treeA,treeB)
# print(distance)

# Getting the Edit Script
# edit_script = edit_scripts.popitem()[1]
# final_ES = reversed(get_ES(edit_script))
# es =[]
# for op in final_ES:
#     es.append(op)
# print(es)
# flat_es_list = [item for sublist in es for item in sublist]
# print(flat_es_list)
# finalfinalES = reformat(flat_es_list)
# ES_to_XML(finalfinalES)








