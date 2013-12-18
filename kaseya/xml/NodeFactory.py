'''
Created on 18-Dec-2013

@author: ssasan
'''
from kaseya.xml.AggregateNode import AggregateNode
from kaseya.xml.EachNode import EachNode
from kaseya.xml.GroupByNode import GroupByNode
from kaseya.xml.StreamNode import StreamNode


class NodeFactory:
    @staticmethod
    def createNode(module):
        name = module['name']

        if name == 'Stream':
            return StreamNode(module)
        elif name == 'Each':
            return EachNode(module)
        elif name == 'GroupBy':
            return GroupByNode(module)
        elif name == 'Aggregate':
            return AggregateNode(module);
        else:
            assert 0 & 'unknow module type'
#             return Node(module)
        pass
    pass