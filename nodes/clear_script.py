import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class ClearScriptNuke(iograft.Node):
    """
    Clear the current Nuke script.
    """
    reset_to_defaults = iograft.InputDefinition("reset_to_compiled_defaults",
                                                iobasictypes.Bool(),
                                                default_value=False)

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("clear_script_nuke")
        node.AddInput(cls.reset_to_defaults)
        return node

    @staticmethod
    def Create():
        return ClearScriptNuke()

    @nuke_main_thread
    def Process(self, data):
        reset_to_defaults = iograft.GetInput(self.reset_to_defaults, data)
        nuke.scriptClear(resetToCompiledDefaults=reset_to_defaults)


def LoadPlugin(plugin):
    node = ClearScriptNuke.GetDefinition()
    plugin.RegisterNode(node, ClearScriptNuke.Create)
