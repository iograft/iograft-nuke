# Copyright 2022 Fabrica Software, LLC

import iograft

import nuke
from iognuke_threading import nuke_main_thread


class AutoplaceAll(iograft.Node):
    """
    Wrapper around Nuke's "autoplace" command to layout the Nuke nodes.
    """
    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("autoplace_all")
        node.SetMenuPath("Nuke")
        return node

    @staticmethod
    def Create():
        return AutoplaceAll()

    @nuke_main_thread
    def Process(self, data):
        # In order to layout the nodes, the nodes to be autoplaced must
        # be selected. Store the previous selection so we can restore it
        # properly.
        selected_nodes = nuke.selectedNodes()

        # Select all nodes and run the autoplace.
        nuke.selectAll()
        nuke.autoplace_all()

        # Restore the previous selection.
        nuke.invertSelection()
        for node in selected_nodes:
            node.setSelected(True)


def LoadPlugin(plugin):
    node = AutoplaceAll.GetDefinition()
    plugin.RegisterNode(node, AutoplaceAll.Create)
