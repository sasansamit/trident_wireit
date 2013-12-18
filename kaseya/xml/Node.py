'''
Created on 18-Dec-2013

@author: ssasan
'''
from kaseya.xml.Utils import Utils


class Node:
    def __init__(self, module):
        self._nodeid = 'node_' + Utils.getUid()
        self._module = module
        self._nextNodes = []
        pass

    def visit(self, root, state):
        assert 0 & 'Not implemented'
        pass

    def module(self):
        return self._module

    def nextNodes(self):
        return self._nextNodes

    def isSource(self):
        return False

    def addDownStreamNode(self, node):
        self._nextNodes.append(node)
        pass

    def operations(self, state):
        operations = state[Utils.OPERATIONS_NAME]
        assert operations != None
        return operations

    def visitDownStreamNodes(self, root, state):
        node = self
        while node != None:
            node.visit(root, state)
            nextNodes = node.nextNodes();
            if len(nextNodes) == 0:
                node = None
            else:
                # TODO - Assumption is we are traversing a linear (1D) graph
                node = node.nextNodes()[0]
            pass
        pass

    def __repr__(self):
        return "Module: " + str(self._module) + ' nextNodes: ' + str(self._nextNodes)

    def __str__(self):
        return "Module: " + str(self._module) + ' nextNodes: ' + str(self._nextNodes)
