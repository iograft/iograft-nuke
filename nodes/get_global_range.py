# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class GetGlobalFrameRange(iograft.Node):
    """
    Get the global (project) frame range for the loaded script.
    """
    first_frame = iograft.OutputDefinition("first_frame", iobasictypes.Int())
    last_frame = iograft.OutputDefinition("last_frame", iobasictypes.Int())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("get_global_range")
        node.SetMenuPath("Nuke")
        node.AddOutput(cls.first_frame)
        node.AddOutput(cls.last_frame)
        return node

    @staticmethod
    def Create():
        return GetGlobalFrameRange()

    @nuke_main_thread
    def Process(self, data):
        first_frame = nuke.root().firstFrame()
        last_frame = nuke.root().lastFrame()
        iograft.SetOutput(self.first_frame, data, first_frame)
        iograft.SetOutput(self.last_frame, data, last_frame)


def LoadPlugin(plugin):
    node = GetGlobalFrameRange.GetDefinition()
    plugin.RegisterNode(node, GetGlobalFrameRange.Create)
