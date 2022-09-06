# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class SetNodeDisabled(iograft.Node):
    """
    Toggle the "disabled" knob of a node with the given name.
    """
    node = iograft.InputDefinition("node", iobasictypes.String())
    disabled = iograft.InputDefinition("disabled", iobasictypes.Bool(),
                                       default_value=True)
    node_out = iograft.OutputDefinition("node", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("set_node_disabled")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.node)
        node.AddInput(cls.disabled)
        node.AddOutput(cls.node_out)
        return node

    @staticmethod
    def Create():
        return SetNodeDisabled()

    @nuke_main_thread
    def Process(self, data):
        node_name = iograft.GetInput(self.node, data)
        disabled = iograft.GetInput(self.disabled, data)

        # Get the node with the given name.
        node = nuke.toNode(node_name)
        if node is None:
            raise KeyError(
                "Node with name: '{}' does not exist.".format(node_name))

        # Toggle the disabled state.
        node["disable"].setValue(disabled)

        # Passthrough the node name.
        iograft.SetOutput(self.node_out, data, node_name)


def LoadPlugin(plugin):
    node = SetNodeDisabled.GetDefinition()
    plugin.RegisterNode(node, SetNodeDisabled.Create)
