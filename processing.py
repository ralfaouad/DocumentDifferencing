import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from utils import *
import lxml.etree as et

def preprocessing(elt):
    if elt is None:
        return None
    newtree = Element("&" + str(elt.tag))
    for key,value in sorted(elt.attrib.items()):
        attr_key = SubElement(newtree, "@" + str(key))
        attr_value = SubElement(attr_key, "#" + str(value))
    for child in elt:
        newtree.append(preprocessing(child))
    if elt.text is not None:
        tokens = elt.text.split()
        for token in tokens:
            tk = SubElement(newtree, "#" + str(token))
    return newtree    
    
######
# parsing Document
docA = ET.parse("SampleDoc1 (original).xml")
docB = ET.parse("treeB.xml")
docC = ET.parse("treeC.xml")


# Transforming Document to Tree -> PreProcessing
element = docA.getroot()
element2 = docB.getroot()
element3 = docC.getroot()

treeA = preprocessing(element)
treeB = preprocessing(element2)
treeC = preprocessing(element3)

def printtree(tree,level=0):
        out="\t"*level+tree.tag
        for child in tree:
            out=out+"\n"+ (printtree(child,level+1))
        return out


    
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
                if tree.text is not None:
                    txt.append(tree.text)
                txt.append(child.tag[1:])
                tree.text = " ".join(txt)
            case '&':
                tree.append(postprocessing(child)) 
    return tree

toWrite = postprocessing(treeB)
tree = ET.ElementTree(toWrite)
with open('output.xml','w') as f:
    tree.write(f,encoding="unicode")




