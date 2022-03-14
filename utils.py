from xml.etree.ElementTree import Element
import numpy as np

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
    return 0 if (n1.tag) == (n2.tag) else 1

def cost_ins_tree(treeA, treeB):
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))

def cost_del_tree(treeA, treeB):
    return 1 if contained_in(treeA,treeB) else len(list(treeA.iter()))


#  Contained-in as seen in slides
def contained_in(treeA, treeB):
    all_elts_in_treeA = list(treeA.iter())
    all_elts_in_treeB = list(treeB.iter())

    for elt in all_elts_in_treeB:
        if treeA.tag==elt.tag:
            children_of_elt=list(elt.iter())
            m=0 # pointer in treeA
            n=0 # pointer in treeB
            found=0

            while n<len(children_of_elt): # iterating over children_of_elt
                if len(all_elts_in_treeA) == found:
                    return True
                if all_elts_in_treeA[m].tag==children_of_elt[n].tag:
                    found=found+1
                    n=n+1
                    m=m+1
                else:
                    n=n+1
            if len(all_elts_in_treeA) == found:
                return True
    
        
                
    






