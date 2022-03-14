import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from utils import *

def preprocessing(elt):
    if elt is None:
        return None
    newtree = Element("&" + str(elt.tag))
    for key,value in elt.attrib.items():
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


for x in tree.iter():
    print(x)
print("\n")
for x in treeB.iter():
    print(x)
    
#print(treeB.iter())
# print(bool(contained_in(tree,treeB)))
# print(bool(contained_in(treeC,treeB)))

#print(ET.tostring(treeB, encoding='utf8').decode('utf8'))

def postprocessing(tree): 
    root = tree.tag
    str = ""

    if(root[0]=='&'):
        str = str + "<" + root[1:]
        if(len(tree) == 0): str = str + ">"
        counter_for_children = 0
        counter_for_txt = 0

        for child in tree:
            if(child.tag[0] == '&'):
                if(counter_for_children == 0):
                    str = str + ">"
                counter_for_children = counter_for_children + 1
                str = str + postprocessing(child)
            elif(child.tag[0] == '@'):
                    str = str + " " + postprocessing(child)
            elif(child.tag[0] == '#'):
                if(counter_for_txt == 0):
                    str = str + ">" + postprocessing(child)
                else: str = str + postprocessing(child)
            else: str = str + ">"
                    
        str = str + "</" + root + ">" 

    elif(root[0]=='@'):
        str = str + root[1:] + " : "
        for child in tree:
            str = str + postprocessing(child)
            
    else:
        str = str + root[1:] + " "

    return str 
        
print(postprocessing(treeB))
