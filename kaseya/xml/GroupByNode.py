'''
Created on 18-Dec-2013

@author: ssasan
'''
from lxml import etree

from kaseya.xml.Node import Node
from kaseya.xml.Utils import Utils


class GroupByNode(Node):
    def __init__(self, module):
        Node.__init__(self, module)
        pass

    def groupBy(self):
        return 'deviceid'

    def visit(self, root, state):
        operations = self.operations(state)

        attribs = {
                   'class' : 'com.kaseya.trident.operations.GroupByOperation',
                   Utils.namespace(Utils.NS_C, 'groupBy') : self.groupBy(),
                   }
        etree.SubElement(operations, 'bean', attribs)
        pass
    pass