# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class SetNodeInput(iograft.Node):
    """
    Wrapper around a Nuke node's setInput function to connect
    the input with the given index to the requested node.
    """
    node = iograft.InputDefinition("node", iobasictypes.String())
    index = iograft.InputDefinition("index", iobasictypes.UnsignedInt())
    input_node = iograft.InputDefinition("input_node", iobasictypes.String())
    node_out = iograft.OutputDefinition("node", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("set_node_input")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.node)
        node.AddInput(cls.index)
        node.AddInput(cls.input_node)
        node.AddOutput(cls.node_out)
        return node

    @staticmethod
    def Create():
        return SetNodeInput()

    @nuke_main_thread
    def Process(self, data):
        node_name = iograft.GetInput(self.node, data)
        index = iograft.GetInput(self.index, data)
        input_node_name = iograft.GetInput(self.input_node, data)

        # Get the node with the given name.
        node = nuke.toNode(node_name)
        if node is None:
            raise KeyError(
                    "Node with name: '{}' does not exist.".format(node_name))

        # Get the input node.
        input_node = nuke.toNode(input_node_name)
        if input_node is None:
            raise KeyError(
                "Node with name: '{}' does not exist.".format(input_node_name))

        # Try to make the connection.
        success = node.setInput(index, input_node)
        if not success:
            raise ValueError(
                "Failed to set input '{}' on node: '{}'.".format(index,
                                                                 node_name))

        # Passthrough the node name.
        iograft.SetOutput(self.node_out, data, node_name)


def LoadPlugin(plugin):
    node = SetNodeInput.GetDefinition()
    plugin.RegisterNode(node, SetNodeInput.Create)
