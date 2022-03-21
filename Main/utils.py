from xml.etree.ElementTree import Element
import regex as re

def degree(root):
    deg = 0
    for child in root:
        deg+=1
    return deg

def get_size(root):
    # includes root
    count = 0
    for element in root.iter():
        count +=1
    return count

def cost_ins(n):
    return 1

def cost_del(n):
    return 1

def cost_upd(n1,n2):
    return 0 if (re.split('@|#|&',n1.tag)[1]) == (re.split('@|#|&',n2.tag)[1]) else 1

def cost_ins_tree(treeA, treeB):
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))

def cost_del_tree(treeA, treeB):
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))


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
    print(path_list)
    # print("Awal l method abel l if:\t "+ str(path_list))
    if(len(path_list) == 1):
        return tree
    # print(path_list)
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



