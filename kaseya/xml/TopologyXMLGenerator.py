'''
Created on 18-Dec-2013

@author: ssasan
'''
from lxml import etree

from kaseya.xml.NodeFactory import NodeFactory
from kaseya.xml.Utils import Utils


class TopologyXMLGenerator:

    def __init__(self, state):
        self._state = state
        pass

    def generate(self, data):
        nodes = {}
        sources = []

        # TODO - Expectation is we only have a 1D DAG
        modules = data['modules']
        wires = data['wires']

        for wire in wires:
            srcNode = self.getNode_(nodes, wire['src']['moduleId'], modules, sources)
            dstNode = self.getNode_(nodes, wire['tgt']['moduleId'], modules, sources)

            srcNode.addDownStreamNode(dstNode)
            pass

        state = {}
        state.update(self._state)

        self._beans = self.rootElement_()
        self.addCommonBeans_(self._beans, state)

        # Iterate Over the sources
        for src in sources:
            src.visitDownStreamNodes(self._beans, state)
            pass

        pass

    def saveToFile(self, filePath):
        xmlFile = open(filePath, 'w')
        xmlFile.write(etree.tostring(self._beans, xml_declaration = True, encoding = 'UTF-8', pretty_print = True))
        xmlFile.close()
        pass

    def getNode_(self, nodes, moduleIndex, modules, sources):
        ret = {}
        if nodes.has_key(moduleIndex):
            ret = nodes[moduleIndex]
        else:
            ret = NodeFactory.createNode(modules[moduleIndex])
            nodes[moduleIndex] = ret
            pass

        if ret.isSource():
            sources.append(ret)
            pass
        return ret

    def addCommonBeans_(self, beans, state):
        etree.SubElement(beans, Utils.namespace(Utils.NS_CONTEXT, 'annotation-config'))

        # Adding Trident Config
        beans.append(etree.Comment('Trident Config'))
        tridentConfigId = 'config_' + Utils.getUid();
        attribs = {
                   'id' : tridentConfigId,
                   'class' : 'backtype.storm.Config',
                   Utils.namespace(Utils.NS_P, 'debug') : 'false'
        }
        etree.SubElement(beans, 'bean', attrib = attribs)

        # Adding Trident Topology
        beans.append(etree.Comment('Trident Topology'))
        attribs = {
                   'id':'topology',
                   'class':'storm.trident.TridentTopology'
        }
        state[Utils.TOPOLOGY_NAME] = etree.SubElement(beans, 'bean', attrib = attribs)

        # Adding streams
        streamsId = "streams_" + Utils.getUid()
        attribs = {
                   'id' : streamsId
                   }
        state[Utils.STREAMS_NAME] = etree.SubElement(beans, Utils.namespace(Utils.NS_UTIL, 'list'), attribs)

        # Adding topology submission
        beans.append(etree.Comment('Topology Submission'))
        attribs = {
                   'id' : 'topologySubmission',
                   'class' : 'com.kaseya.trident.SingleTopologySubmission',
                   Utils.namespace(Utils.NS_C, 'topologyId') : 'topology',
                   Utils.namespace(Utils.NS_C, 'topology-ref') : 'topology',
                   Utils.namespace(Utils.NS_C, 'config-ref') : tridentConfigId,
                   Utils.namespace(Utils.NS_P, 'streams-ref') : streamsId
        }
        etree.SubElement(beans, 'bean', attrib = attribs)
        pass

    def rootElement_(self):
        beans = etree.Element("beans", nsmap = Utils.NAMESPACES)
        beans.set(Utils.namespace(Utils.NS_XSI, "schemaLocation"), Utils.SCHEMALOCATION)

        return beans
