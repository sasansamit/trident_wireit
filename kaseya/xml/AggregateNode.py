'''
Created on 18-Dec-2013

@author: ssasan
'''
from lxml import etree

from kaseya.xml.BaseDSLNode import BaseDSLNode
from kaseya.xml.Node import Node
from kaseya.xml.Utils import Utils


class AggregateNode(BaseDSLNode):
    def __init__(self, module):
        Node.__init__(self, module)
        pass

    def visit(self, root, state):
        operations = self.operations(state)

        filePath = self.saveDSL_(self._module['value']['code'], state)

        # Add memory state factory
        memStateFactoryId = 'memStateObject_' + Utils.getUid()
        attribs = {
                   'id' : memStateFactoryId,
                   'class' : 'com.kaseya.trident.dsl.MemoryStateObject.Factory',
                   }
        etree.SubElement(root, 'bean', attribs)

        dslInvokerId = 'dslInvoker_' + Utils.getUid()
        attribs = {
                   'id' : dslInvokerId,
                   'class' : 'com.kaseya.trident.dsl.GroovyDSLInvoker',
                   Utils.namespace(Utils.NS_C, 'filePath') : filePath,
                   }
        etree.SubElement(root, 'bean', attribs)

        attribs = {
                   'class' : 'com.kaseya.trident.operations.PartitionPersistOperation',
                   Utils.namespace(Utils.NS_C, 'stateFactory-ref') : memStateFactoryId,
                   Utils.namespace(Utils.NS_C, 'updater-ref') : dslInvokerId,
                   }
        etree.SubElement(operations, 'bean', attribs)
        pass
    pass