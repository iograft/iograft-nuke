# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class CreateNode(iograft.Node):
    """
    Create a node with the given type.
    """
    node_class = iograft.InputDefinition("node_class", iobasictypes.String())
    input_node = iograft.InputDefinition("input_node", iobasictypes.String(),
                                         default_value="")
    select_node = iograft.InputDefinition("select_node",
                                            iobasictypes.Bool(),
                                            default_value=False)
    node = iograft.OutputDefinition("node", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("create_node")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.node_class)
        node.AddInput(cls.input_node)
        node.AddInput(cls.select_node)
        node.AddOutput(cls.node)
        return node

    @staticmethod
    def Create():
        return CreateNode()

    @nuke_main_thread
    def Process(self, data):
        node_class = iograft.GetInput(self.node_class, data)
        input_node_name = iograft.GetInput(self.input_node, data)
        select_node = iograft.GetInput(self.select_node, data)

        # If we aren't selecting the newly created node, store the
        # previous selection so we can restore it.
        selected_nodes = nuke.selectedNodes()

        # Create the node.
        node = nuke.createNode(node_class)
        if not select_node:
            node["selected"].setValue(False)

            # Restore the selection.
            for selected in selected_nodes:
                selected.setSelected(True)

        # If there is an input node defined, set that as the input for the
        # newly created node.
        if input_node_name != "":
            input_node = nuke.toNode(input_node_name)
            if input_node is None:
                raise KeyError(
                 "Node with name: '{}' does not exist.".format(input_node_name))

            # Set the input.
            success = node.setInput(0, input_node)
            if not success:
                raise ValueError(
                    "Failed to input on node: '{}'.".format(node.name()))

        # Get the name of the node and set the output.
        node_name = node.name()
        iograft.SetOutput(self.node, data, node_name)


def LoadPlugin(plugin):
    node = CreateNode.GetDefinition()
    plugin.RegisterNode(node, CreateNode.Create)
