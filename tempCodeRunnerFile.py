docA = ET.parse("treeA.xml")
docB = ET.parse("treeB.xml")
docC = ET.parse("treeC.xml")


# Transforming Document to Tree -> PreProcessing
element = docA.getroot()
element2 = docB.getroot()
element3 = docC.getroot()

treeA = preprocessing(element)
treeB = preprocessing(element2)
treeC = preprocessing(element3)