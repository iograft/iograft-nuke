# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes

import nuke
from iognuke_threading import nuke_main_thread


class PromptUser(iograft.Node):
    """
    Display a Yes/No dialog to the user asking for confirmation. If the user
    responds 'No', this node is marked as failed.
    """
    prompt = iograft.InputDefinition("prompt", iobasictypes.String(),
                                     default_value="Do you want to continue?")

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("prompt_user")
        node.SetMenuPath("Nuke")
        node.AddInput(cls.prompt)
        return node

    @staticmethod
    def Create():
        return PromptUser()

    @nuke_main_thread
    def Process(self, data):
        prompt = iograft.GetInput(self.prompt, data)

        # If this is a batch section, we cannot prompt the user so simply
        # passthrough this node.
        if not nuke.GUI:
            return

        # Show the prompt.
        confirmed = nuke.ask(prompt)
        if not confirmed:
            raise Exception("User cancelled the execution.")


def LoadPlugin(plugin):
    node = PromptUser.GetDefinition()
    plugin.RegisterNode(node, PromptUser.Create)
