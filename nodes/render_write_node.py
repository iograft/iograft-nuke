# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class RenderWriteNode(iograft.Node):
    """
    Render one or more write nodes in the script.
    """
    write_node = iograft.InputDefinition("write_node", iobasictypes.String())
    start_frame = iograft.InputDefinition("start_frame", iobasictypes.Int())
    end_frame = iograft.InputDefinition("end_frame", iobasictypes.Int())
    increment = iograft.InputDefinition("increment", iobasictypes.Int(),
                                        default_value=1)

    output_file = iograft.OutputDefinition("file", iobasictypes.Path())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("render_write_node")
        node.AddInput(cls.write_node)
        node.AddInput(cls.start_frame)
        node.AddInput(cls.end_frame)
        node.AddInput(cls.increment)
        node.AddOutput(cls.output_file)
        return node

    @staticmethod
    def Create():
        return RenderWriteNode()

    @nuke_main_thread
    def Process(self, data):
        write_node = iograft.GetInput(self.write_node, data)
        start_frame = iograft.GetInput(self.start_frame, data)
        end_frame = iograft.GetInput(self.end_frame, data)
        increment = iograft.GetInput(self.increment, data)

        # Get the write node.
        node = nuke.toNode(write_node)
        if node is None:
            raise KeyError(
                    "Node with name: '{}' does not exist.".format(write_node))

        # Execute the node.
        nuke.execute(write_node, start_frame, end_frame, increment)

        # Pull the "file" knob from the write node to pass on as output
        # from the node.
        output_file = node["file"].getValue()
        iograft.SetOutput(self.output_file, data, output_file)


def LoadPlugin(plugin):
    node = RenderWriteNode.GetDefinition()
    plugin.RegisterNode(node, RenderWriteNode.Create)
