import xml.etree.ElementTree as ET
from utils import *


# treeA = preprocessing(ET.parse("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 1/DocumentDifferencing-1/Main/treeA.xml").getroot())
# treeB = preprocessing(ET.parse("C:/Users/User/Desktop/Sara/LAU ELE/Spring2022/IDPA/Project 1/DocumentDifferencing-1/Main/treeB.xml").getroot())

def insTree(B, P, i):
    parent = get_tree(path(P), treeA)
    parent.insert(i, get_tree(path(B),treeB))

def delTree(A, P):
    parent = get_tree(path(P), treeA)
    parent.remove(get_tree(path(A),treeA))

def updTree(x, elt_l):
    element = get_tree(path(x),treeA)
    element.tag = path(x) + "." + element_name(elt_l)

# delTree("0.0.0.&c", "0.0.&b")
# insTree("0.0.&m", "0.0.&b", 0)
# updTree("0.0.&b","0.0.0.0.&c")
# for x in treeA.iter():
#     print(x)