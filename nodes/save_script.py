# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class SaveScriptNuke(iograft.Node):
    """
    Save the current Nuke script.
    """
    filename = iograft.InputDefinition("filename", iobasictypes.Path())

    # Whether or not to overwrite the file if it exists. 1 (True) means
    # overwrite, 0 (False) means overwrite. -1 means "Ask the User" if in
    # GUI mode, or False in headless execution.
    overwrite = iograft.InputDefinition("overwrite", iobasictypes.Int(),
                                        default_value=-1)

    out_filename = iograft.OutputDefinition("out_filename", iobasictypes.Path())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("save_script")
        node.AddInput(cls.filename)
        node.AddInput(cls.overwrite)
        node.AddOutput(cls.out_filename)
        return node

    @staticmethod
    def Create():
        return SaveScriptNuke()

    @nuke_main_thread
    def Process(self, data):
        filename = iograft.GetInput(self.filename, data)
        overwrite = iograft.GetInput(self.overwrite, data)

        # Verify that the overwrite parameter is valid.
        if overwrite < -1 or overwrite > 1:
            raise ValueError("Value for overwrite parameter is invalid. Must",
                             " be one of -1, 0, or 1.")

        # Run the save script operation.
        nuke.scriptSaveAs(filename, overwrite=overwrite)

        # Get the script's updated filename.
        out_filename = nuke.scriptName()
        iograft.SetOutput(self.out_filename, data, out_filename)


def LoadPlugin(plugin):
    node = SaveScriptNuke.GetDefinition()
    plugin.RegisterNode(node, SaveScriptNuke.Create)
