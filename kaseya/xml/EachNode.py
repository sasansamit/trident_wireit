'''
Created on 18-Dec-2013

@author: ssasan
'''
from lxml import etree

from kaseya.xml.BaseDSLNode import BaseDSLNode
from kaseya.xml.Node import Node
from kaseya.xml.Utils import Utils


class EachNode(BaseDSLNode):
    def __init__(self, module):
        Node.__init__(self, module)
        pass
    
    def getDSLCode_(self):
        return self._module['value']['code']

    def visit(self, root, state):
        operations = self.operations(state)

        filePath = self.saveDSL_(self.getDSLCode_(), state)

        dslInvokerId = "dslInvoker_" + Utils.getUid()
        attribs = {
                   'id' : dslInvokerId,
                   'class' : 'com.kaseya.trident.dsl.GroovyDSLInvoker',
                   Utils.namespace(Utils.NS_C, 'filePath') : filePath,
                   Utils.namespace(Utils.NS_C, 'tuple-ref') : state[Utils.JSONTUPLE_NAME].attrib['id'],
                   }
        etree.SubElement(root, 'bean', attribs)

        attribs = {
                   'class' : 'com.kaseya.trident.operations.EachOperation',
                   Utils.namespace(Utils.NS_C, 'inputTuples-ref') : state[Utils.JSONTUPLE_NAME].attrib['id'],
                   Utils.namespace(Utils.NS_C, 'function-ref') : dslInvokerId,
                   Utils.namespace(Utils.NS_C, 'outputTuples') : '',
                   }
        etree.SubElement(operations, 'bean', attribs)
        pass
    pass