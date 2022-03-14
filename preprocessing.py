import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from utils import *

def preprocessing(elt):
    if elt is None:
        return None
    newtree = Element(elt.tag)
    for key,value in elt.attrib.items():
        attr_key = SubElement(newtree,key)
        attr_value = SubElement(attr_key,value)
    for child in elt:
        newtree.append(preprocessing(child))
    if elt.text is not None:
        tokens = elt.text.split()
        for token in tokens:
            tk = SubElement(newtree, token)
    return newtree    
    
######
# parsing Document
doc = ET.parse("treeA.xml")
docB = ET.parse("treeB.xml")
docC = ET.parse("treeC.xml")


# Transforming Document to Tree -> PreProcessing
element = doc.getroot()
element2 = docB.getroot()
element3 = docC.getroot()

# tree = preprocessing(element)
# treeB = preprocessing(element2)
# treeC = preprocessing(element3)

def printtree(tree,level=0):
        out="\t"*level+tree.tag
        for child in tree:
            out=out+"\n"+ (printtree(child,level+1))
        return out


# x = printtree(tree)
# print(x)


# for elt in tree.iter():
#     print(elt)

# treeB = preprocessing(element)
# print(tree.iter() == treeB.iter())

# print(degree(tree))

# for x in tree.iter():
#     print(x)
# print("\n")
# for x in treeB.iter():
#     print(x)
    
#print(treeB.iter())
# print(bool(contained_in(tree,treeB)))
# print(bool(contained_in(treeC,treeB)))
