# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class SetKnobValue(iograft.Node):
    """
    Set the value of a knob on a node.
    """
    node = iograft.InputDefinition("node", iobasictypes.String())
    knob_name = iograft.InputDefinition("knob_name", iobasictypes.String())
    value = iograft.MutableInputDefinition("value")
    out_node = iograft.OutputDefinition("node", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("set_knob_value")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.node)
        node.AddInput(cls.knob_name)
        node.AddInput(cls.value)
        node.AddOutput(cls.out_node)
        return node

    @staticmethod
    def Create():
        return SetKnobValue()

    @nuke_main_thread
    def Process(self, data):
        node_name = iograft.GetInput(self.node, data)
        knob_name = iograft.GetInput(self.knob_name, data)
        value = iograft.GetInput(self.value, data)

        # Get the node with the given name.
        node = nuke.toNode(node_name)
        if node is None:
            raise KeyError(
                    "Node with name: '{}' does not exist.".format(node_name))

        # If the knob is a File_Knob, ensure that backslashes are doubled.
        # Nuke parses the input value for a File_Knob as a raw string even
        # if the value is escaped when we pass it from Python. This means
        # that a path with back slashes in Python: (i.e. C:\\projects), will
        # only be represented correctly by Nuke if it is actually passed
        # as "C:\\\\projects" from Python.
        if isinstance(node[knob_name], nuke.File_Knob):
            escaped_value = value.replace("\\", "\\\\")
            node[knob_name].setValue(escaped_value)
        else:
            # Set the value on the node.
            node[knob_name].setValue(value)

        # Passthrough the node name.
        iograft.SetOutput(self.out_node, data, node_name)


def LoadPlugin(plugin):
    node = SetKnobValue.GetDefinition()
    plugin.RegisterNode(node, SetKnobValue.Create)
