'''
Created on 18-Dec-2013

@author: ssasan
'''
from lxml import etree

from kaseya.xml.Node import Node
from kaseya.xml.Utils import Utils


class StreamNode(Node):
    def __init__(self, mod):
        Node.__init__(self, mod)
        pass

    def brokers(self):
        return 'localhost:2181'

    def topic(self):
        return 'memory'

    def isSource(self):
        return self._module['name'] == 'Stream'

    def visit(self, root, state):
        root.append(etree.Comment('Spout'))
        hostId = self._nodeid + '_ZkHosts'
        attribs = {
                  'id' : hostId,
                   'class' : 'storm.kafka.ZkHosts',
                   Utils.namespace(Utils.NS_C, 'brokerZkStr') : self.brokers(),
                   }
        etree.SubElement(root, 'bean', attrib = attribs)

        configId = self._nodeid + "_kafaConfig"
        attribs = {
                   'id' : configId,
                   'class' : 'com.kaseya.kafka.TridentKafkaConfigFactoryBean',
                   Utils.namespace(Utils.NS_C, 'hosts-ref') : hostId,
                   Utils.namespace(Utils.NS_C, 'topic') : self.topic(),
                   }
        etree.SubElement(root, 'bean', attribs)

        attribs = {
           'id' : self._nodeid,
           'class' : 'storm.kafka.trident.TransactionalTridentKafkaSpout',
           Utils.namespace(Utils.NS_C, 'config-ref') : configId,
           }
        self._spoutElement = etree.SubElement(root, 'bean', attribs)

        # Add implicit JSON parsing operation
        operationsId = 'operations_' + Utils.getUid()
        attribs = {
                   'id' : operationsId,
                   }
        state[Utils.OPERATIONS_NAME] = operations = etree.SubElement(root, Utils.namespace(Utils.NS_UTIL, 'list'), attribs)

        jsonOutputTupleId = 'jsonTuples_' + Utils.getUid()
        attribs = {
                   'id' : jsonOutputTupleId,
                   }
        state[Utils.JSONTUPLE_NAME] = jsonTuple = etree.SubElement(root, Utils.namespace(Utils.NS_UTIL, 'list'), attribs)
        etree.SubElement(jsonTuple, 'value').text = 'timestamp'
        etree.SubElement(jsonTuple, 'value').text = 'deviceid'
        etree.SubElement(jsonTuple, 'value').text = 'memory'

        jsonAdapterFunctionId = 'jsonAdapterFunction_' + Utils.getUid()
        attribs = {
                   'id' : jsonAdapterFunctionId,
                   'class' : 'com.kaseya.trident.functions.JSONAdapterFunction'
                   }
        etree.SubElement(root, 'bean', attribs)

        attribs = {
                   'class' : 'com.kaseya.trident.operations.EachOperation',
                   Utils.namespace(Utils.NS_C, 'inputTuples') : 'str',
                   Utils.namespace(Utils.NS_C, 'function-ref') : jsonAdapterFunctionId,
                   Utils.namespace(Utils.NS_C, 'outputTuples-ref') : jsonOutputTupleId,
                   }
        etree.SubElement(operations, 'bean', attribs)
        pass

    def visitDownStreamNodes(self, root, state):
        Node.visitDownStreamNodes(self, root, state)

        # Post processing jobs
        streams = state[Utils.STREAMS_NAME]

        # Add StreamWrapper
        streamId = 'stream_' + Utils.getUid()
        attribs = {
                   'id' : streamId,
                   'class' : 'com.kaseya.trident.StreamWrapper',
                   Utils.namespace(Utils.NS_C, 'spoutNodeName') : 'spout_' + Utils.getUid(),
                   Utils.namespace(Utils.NS_C, 'topology-ref') : state[Utils.TOPOLOGY_NAME].attrib['id'],
                   Utils.namespace(Utils.NS_C, 'operations-ref') : state[Utils.OPERATIONS_NAME].attrib['id'],
                   Utils.namespace(Utils.NS_C, 'spout-ref') : self._spoutElement.attrib['id'],
                   }
        etree.SubElement(root, 'bean', attribs)

        attribs = {
                   'bean' : streamId,
                   }
        etree.SubElement(streams, 'ref', attribs)
    pass