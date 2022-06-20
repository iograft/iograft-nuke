# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class OpenScriptNuke(iograft.Node):
    """
    Open a Nuke script.
    """
    filename = iograft.InputDefinition("filename", iobasictypes.Path())
    out_filename = iograft.OutputDefinition("filename", iobasictypes.Path())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("open_script")
        node.AddInput(cls.filename)
        node.AddOutput(cls.out_filename)
        return node

    @staticmethod
    def Create():
        return OpenScriptNuke()

    @nuke_main_thread
    def Process(self, data):
        filename = iograft.GetInput(self.filename, data)

        # Open the script.
        nuke.scriptOpen(filename)

        # Get the name of the opened script.
        out_filename = nuke.scriptName()
        iograft.SetOutput(self.out_filename, data, out_filename)


def LoadPlugin(plugin):
    node = OpenScriptNuke.GetDefinition()
    plugin.RegisterNode(node, OpenScriptNuke.Create)
