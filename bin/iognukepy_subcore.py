#!/usr/bin/env python
# Copyright 2022 Fabrica Software, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys

import iograft

# Importing the "nuke" module modifies the sys.argv, so we have to store
# the initial args before importing nuke. This bug has been reported, but
# no action taken by the Foundry yet:
# https://support.foundry.com/hc/en-us/articles/360000037550
original_args = sys.argv

import nuke


def parse_args(args):
    parser = argparse.ArgumentParser(
                description="Start an iograft subcore to process in Maya")
    parser.add_argument("--core-address", dest="core_address", required=True)
    return parser.parse_args(args)


def StartSubcore(core_address):
    # Initialize iograft.
    iograft.Initialize()

    # Create the Subcore object and listen for nodes to be processed. Use
    # the MainThreadSubcore to ensure that all nodes are executed in the
    # main thread.
    subcore = iograft.MainThreadSubcore(core_address)
    subcore.ListenForWork()

    # Uninitialize iograft.
    iograft.Uninitialize()


if __name__ == "__main__":
    # When passed an arg list, Argparse expects a list of args NOT including
    # the script name (sys.argv[0]).
    args = parse_args(original_args[1:])

    # Start the subcore.
    StartSubcore(args.core_address)
