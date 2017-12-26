# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
# OpenGL registry parser
# See https://github.com/KhronosGroup/OpenGL-Registry/tree/master/xml
# -----------------------------------------------------------------------------
import re
from lxml import etree


class Node:
    """ Represents a registry element """

    def __init__(self, node):
        self.required = False
        self.node = node

    def reset(self):
        self.required = False

    def find(self, key):
        return self.node.find(key)

    def get(self, key):
        if key in self.node.attrib:
            return self.node.get(key)
        return self.node.find(key)

    def findall(self, key):
        return self.node.findall(key)


class Registry(object):
    """ OpenGL Registry """

    def __init__(self):
        self.tree = None

    def load(self, xml):
        """ Load the given xml registry and parse it """

        self.tree = etree.parse(xml)
        self.parse()

    def reset(self):
        """
        Reset type/enum/command dictionaries before generating another API
        """

        # for item in self.types.values():
        #     item.reset()
        for item in self.enums.values():
            item.reset()
        for item in self.commands.values():
            item.reset()
        for item in self.features.values():
            item.reset()

    def parse(self):
        """ Parse the current xml registry """

        registry = self.tree.getroot()

        # Get types
        # ---------
        # self.types = {}
        # for node in registry.findall('types/type'):
        #     if (node.get('name') == None):
        #         node.attrib['name'] = node.find('name').text
        #     key = node.get('name')
        #     if 'api' in node.attrib:
        #         key = node.get('name'), node.get('api')
        #     self.types[key] = Node(node)

        # Get groups
        # ----------
        # self.groups = {}
        # for node in registry.findall('groups/group'):
        #     key = node.get('name')
        #     if 'api' in node.attrib:
        #         key = node.get('name'), node.get('api')
        #     self.groups[key] = Node(node)

        # Get enums
        # ---------
        self.enums = {}
        for node in registry.findall('enums/enum'):
            key = node.get('name')
            if 'api' in node.attrib:
                key = node.get('name'), node.get('api')
            self.enums[key] = Node(node)

        # Get commands
        # ------------
        self.commands = {}
        for node in registry.findall('commands/command'):
            if node.get('name') is None:
                node.attrib['name'] = node.find('proto/name').text
            key = node.get('name')
            if 'api' in node.attrib:
                key = node.get('name'), node.get('api')
            self.commands[key] = Node(node)

        # Get features
        # ------------
        self.features = {}
        for node in registry.findall('feature'):
            key = node.get('name')
            if 'api' in node.attrib:
                key = node.get('name'), node.get('api')
            self.features[key] = Node(node)

        # Get extensions
        # --------------
        self.extensions = {}
        for node in registry.findall('extensions/extension'):
            key = node.get('name')
            if 'api' in node.attrib:
                key = node.get('name'), node.get('api')
            self.extensions[key] = Node(node)

    def match(self, element, api, profile):
        """ Check whether an element match a given api and profile """

        if 'api' in element.attrib:
            if api != element.get('api'):
                return False
        if 'profile' in element.attrib:
            if profile != element.get('profile'):
                return False
        return True

    def get_extension(self, api="gl", vendor=None):
        """ Get a specific extension """

        # Known vendors
        # vendors = ["3DFX","AMD", "ANGLE", "APPLE", "ARB", "ATI", "DMP",
        #            "EXT", "FJ", "GREMEDY", "HP", "IBM", "IMG", "INGR",
        #            "INTEL", "KHR", "MESAX", "MESA", "NVX", "NV", "OES",
        #            "OML", "PGI", "QCOM", "S3", "SGIS", "SGIX", "SUNX",
        #            "SUN", "VIV", "WIN"]

        prefix = "GL_%s_" % vendor
        extensions = {}
        for name, extension in self.extensions.items():
            if name.startswith(prefix):
                supported = re.compile(extension.get("supported"))
                if re.match(supported, api):
                    extensions[name] = extension
        return extensions

    def get_api(self, api="gl", version="2.1", profile=None, extensions=[]):
        """ Get a specific api as lists of enums and functions """

        self.reset()

        # Find all requested features (any version <= given version)
        features = []
        for feature in self.features.values():
            if feature.get("api") == api and feature.get("number") <= version:
                features.append(feature)

        # Find all requested extensions (by vendor)
        for vendor in extensions:
            prefix = "GL_%s_" % vendor
            for name, extension in self.extensions.items():
                if name.startswith(prefix):
                    supported = re.compile(extension.get("supported"))
                    if re.match(supported, api):
                        features.append(extension)

        # Tag all elements related to a feature
        for feature in features:

            # Tag required items
            for request in feature.findall("require"):
                if not self.match(request, api, profile):
                    continue

                for item in request.findall('enum'):
                    name = item.get("name")
                    self.enums[name].required = True

                for item in request.findall('command'):
                    name = item.get("name")
                    self.commands[name].required = True

            # Tag removed items
            for request in feature.findall("remove"):

                if not self.match(request, api, profile):
                    continue

                for item in request.findall('enum'):
                    name = item.get("name")
                    self.enums[name].required = False

                for item in request.findall('command'):
                    name = item.get("name")
                    self.commands[name].required = False

        # Retrieve requested enums
        enums = {}
        for name, value in self.enums.items():
            if self.enums[name].required:
                enums[name] = value

        # Retrieve requested commands
        commands = {}
        for name, value in self.commands.items():
            if self.commands[name].required:
                commands[name] = value

        return enums, commands


if __name__ == '__main__':

    registry = Registry()
    registry.load("./gl.xml")
    versions = ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5",
                "2.0", "2.1",
                "3.0", "3.1", "3.2", "3.3",
                "4.0", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6"]
    for version in versions:
        enums, commands = registry.get_api("gl", version, "core", extensions=[])

        for enum in enums.keys():
            if 'SHADER' in enum:
                print(enum)
        
        print("GL %s:  %4d constants, %3d functions" %
              (version, len(enums), len(commands)))

    enums, commands = registry.get_api("gles1", "1.0")
    print("GLES 1.0: %3d constants, %3d functions" % (len(enums), len(commands)))

    enums, commands = registry.get_api("gles2", "2.0")
    print("GLES 2.0: %3d constants, %3d functions" % (len(enums), len(commands)))
