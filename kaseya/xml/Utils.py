'''
Created on 18-Dec-2013

@author: ssasan
'''
class Utils:
    NS_P = 'p'
    NS_C = 'c'
    NS_UTIL = 'util'
    NS_XSI = 'xsi'
    NS_CONTEXT = 'context'
    NAMESPACES = {
                    None : 'http://www.springframework.org/schema/beans',
                    NS_XSI : 'http://www.w3.org/2001/XMLSchema-instance',
                    NS_P : 'http://www.springframework.org/schema/p',
                    NS_C : 'http://www.springframework.org/schema/c',
                    NS_UTIL : 'http://www.springframework.org/schema/util',
                    NS_CONTEXT : 'http://www.springframework.org/schema/context'
                    }
    SCHEMALOCATION = "http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util-3.0.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd"

    OPERATIONS_NAME = 'operations'
    STREAMS_NAME = 'streams'
    TOPOLOGY_NAME = 'topology'
    JSONTUPLE_NAME = 'jsontuple'
    OUTPUTPATH_NAME = 'output_path'
    SETTINGS_NAME = 'settings'

    _gIdCount = 0

    @staticmethod
    def namespace(ns, attrib):
        return '{{{0}}}'.format(Utils.NAMESPACES[ns]) + attrib

    @staticmethod
    def getUid():
        Utils._gIdCount += 1;
        return str(Utils._gIdCount)
    pass

class StreamState:
    def __init__(self):
        self._spout = None
        self._operations = [];
        pass
    pass