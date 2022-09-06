# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class GetKnobValue(iograft.Node):
    """
    Get the value of a knob on a node.
    """
    node = iograft.InputDefinition("node", iobasictypes.String())
    knob_name = iograft.InputDefinition("knob_name", iobasictypes.String())
    value = iograft.MutableOutputDefinition("value")

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("get_knob_value")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.node)
        node.AddInput(cls.knob_name)
        node.AddOutput(cls.value)
        return node

    @staticmethod
    def Create():
        return GetKnobValue()

    @nuke_main_thread
    def Process(self, data):
        node_name = iograft.GetInput(self.node, data)
        knob_name = iograft.GetInput(self.knob_name, data)

        # Get the node with the given name.
        node = nuke.toNode(node_name)
        if node is None:
            raise KeyError(
                    "Node with name: '{}' does not exist.".format(node_name))

        # Access the knob value on the node.
        value = node[knob_name].getValue()

        # If the knob is a file knob, unescape any backslashes that might
        # have been previously escaped.
        if isinstance(node[knob_name], nuke.File_Knob):
            value = value.replace("\\\\", "\\")

        iograft.SetOutput(self.value, data, value)


def LoadPlugin(plugin):
    node = GetKnobValue.GetDefinition()
    plugin.RegisterNode(node, GetKnobValue.Create)
