#!/usr/bin/env python

import json
import os.path
import shutil
import subprocess

from kaseya.xml.TopologyXMLGenerator import TopologyXMLGenerator
from kaseya.xml.Utils import Utils
from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web


define("port", default = 8088, help = "run on the given port", type = int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("workflow/index.html")
        pass

class XMLHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Method Not Supported")
        pass

    def post(self):
        topology_data = self.get_argument("json_data", None)
        topology_name = self.get_argument("name", None)

        state = {}
        state[Utils.OUTPUTPATH_NAME] = outputFolder = os.path.join(os.path.dirname(__file__), 'output')

        try:
            shutil.rmtree(outputFolder)
        except OSError as ex:
            print 'No output folder to delete.'

        try:
            os.makedirs(outputFolder)
        except OSError as ex:
            print "Folder already exists"


        generator = TopologyXMLGenerator(state);
        generator.generate(json.loads(topology_data))
        topologyXmlPath = os.path.join(outputFolder, 'topology.xml')
        generator.saveToFile(topologyXmlPath)

        cmdStr = 'sh ktrident/bin/app "{0}"'.format(os.path.relpath(topologyXmlPath))
        print(cmdStr)
        subprocess.call(cmdStr, shell=True)

        pass

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/xml/generate", XMLHandler),
        ],
        cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "templates/static"),
        xsrf_cookies = False,

        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
