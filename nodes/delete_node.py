# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class DeleteNode(iograft.Node):
    """
    Delete the node with the given name.
    """
    node = iograft.InputDefinition("node", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("delete_node")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.node)
        return node

    @staticmethod
    def Create():
        return DeleteNode()

    @nuke_main_thread
    def Process(self, data):
        node_name = iograft.GetInput(self.node, data)

        # Get the node with the given name.
        node = nuke.toNode(node_name)
        if node is None:
            raise KeyError(
                    "Node with name: '{}' does not exist.".format(node_name))

        nuke.delete(node)


def LoadPlugin(plugin):
    node = DeleteNode.GetDefinition()
    plugin.RegisterNode(node, DeleteNode.Create)
