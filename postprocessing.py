from processing import preprocessing
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


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


  