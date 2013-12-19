'''
Created on 19-Dec-2013

@author: ssasan
'''

import ConfigParser
import json
import os.path


class Settings:
    SECTION_NAME = 'kaseya'
    FILE_NAME = 'config.prop'
    TEMPLATE_TOPIC_TUPLE_ = '{0}_tuple'

    DEFAULT_VALUES = {
                      'memory_tuple' : '["timestamp","deviceid","memory"]'
                      }

    def __init__(self):
        self._config = ConfigParser.SafeConfigParser(Settings.DEFAULT_VALUES);
        
        if not os.path.exists(Settings.FILE_NAME):
            self._config.add_section(Settings.SECTION_NAME)
            pass
        self._config.read(Settings.FILE_NAME)
        pass

    def get_(self, key):
        try:
            return self._config.get(Settings.SECTION_NAME, key)
        except ConfigParser.Error as ex:
            print('Exception : ' + str(ex))
            return None
        pass

    def getTupleForTopic(self, topic):
        t = self.get_(Settings.TEMPLATE_TOPIC_TUPLE_.format(topic));
        return json.loads(t)

    pass