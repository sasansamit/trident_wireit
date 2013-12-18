'''
Created on 18-Dec-2013

@author: ssasan
'''
import os.path

from kaseya.xml.Node import Node
from kaseya.xml.Utils import Utils


class BaseDSLNode(Node):

    def saveDSL_(self, dslCode, state):
        outputFolder = state[Utils.OUTPUTPATH_NAME]
        filePath = self.getUniqueDSLFile_(outputFolder)
        dslFile = open(filePath, "wb")
        dslFile.write(dslCode)
        dslFile.close()

        return filePath
        pass

    def getUniqueDSLFile_(self, folder):
        i = 0
        dslNameTemplate = os.path.join(folder, 'dsl_{0}.groovy')
        while True:
            filePath = dslNameTemplate.format(i)
            if not os.path.exists(filePath):
                return filePath
                pass
            i += 1
            pass
        pass
    pass