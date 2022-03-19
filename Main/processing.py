import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from utils import *

# step i and step iv: preprocessing and postprocessing methods.

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

    
######
# parsing Document
docA = ET.parse("C:/Users/ralf/Desktop/DocumentDifferencing/Main/treeA.xml")
docB = ET.parse("C:/Users/ralf/Desktop/DocumentDifferencing/Main/treeB.xml")
docC = ET.parse("treeC.xml")


# Transforming Document to Tree -> PreProcessing
element = docA.getroot()
element2 = docB.getroot()
element3 = docC.getroot()

treeA = preprocessing(element)
treeB = preprocessing(element2)
treeC = preprocessing(element3)

for x in treeA.iter():
    print(x.tag)

# def postprocessing(tree): 
#     root = tree.tag
#     str = ""

#     if(root[0]=='&'):
#         str = str + "<" + root[1:]
#         if(len(tree) == 0): str = str + ">"
#         counter_for_children = 0
#         counter_for_txt = 0

#         for child in tree:
#             if(child.tag[0] == '&'):
#                 if(counter_for_children == 0):
#                     str = str + ">"
#                 counter_for_children = counter_for_children + 1
#                 str = str + postprocessing(child)
#             elif(child.tag[0] == '@'):
#                     str = str + " " + postprocessing(child)
#             elif(child.tag[0] == '#'):
#                 if(counter_for_txt == 0):
#                     counter_for_txt = counter_for_txt + 1
#                     str = str + '>' + child.tag[1:]
#                 else: str = str + " " + child.tag[1:]
#             else: str = str + '>'
        
#         if(str[-1] != '>'): str = str + ">"            
#         str = str + "</" + root[1:] + ">" 

#     elif(root[0]=='@'):
#         str = str + root[1:] + " = \""  
#         for child in tree:
#             str = str + child.tag[1:] + "\""
            
#     else:
#         str = str + root[1:] + " "
#     return str

def postprocessing(root):
    if root is None:
        return None
    tree = Element(root.tag[1:])
    for child in root:
        # print(child)
        match child.tag[0]:
            case '@':
                for attr_value in child:
                    value = attr_value.tag[1:]
                    tree.set(child.tag[1:],value)
            case '#':
                txt=[]
                # if tree.text is not None:
                #     txt.append(tree.text)
                txt.append(child.tag[1:])
                tree.text = " ".join(txt)
            case '&':
                tree.append(postprocessing(child)) 
    return tree

# toWrite = postprocessing(treeA)
# tree = ET.ElementTree(toWrite)
# with open('output.xml','w') as f:
#     tree.write(f,encoding="unicode")

# print(get_tree("0.0.1.1",treeA))




