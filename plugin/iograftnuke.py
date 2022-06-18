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

import atexit
import os

import iograft
import nuke

# The name of the Core object to be registered for the Nuke session.
IOGRAFT_NUKE_CORE_NAME = "nuke"


# Function to be used with atexit to ensure that iograft has been cleaned
# up and doesn't prevent Nuke from exiting.
@atexit.register
def _ensureUninitialized():
    if iograft.IsInitialized():
        iograft.Uninitialize()


def start_iograft():
    """
    Start an iograft session for the current nuke process. This creates a
    single Core object that can be shared/accessed throughout the current
    Nuke process.
    """
    if not iograft.IsInitialized():
        iograft.Initialize()

    # Ensure there is a "nuke" iograft Core object created and setup to
    # handle requests.
    core = iograft.GetCore(IOGRAFT_NUKE_CORE_NAME, True)

    # Start the request handler so that a UI can be connected to the session.
    core.StartRequestHandler()

    # Get the core address that clients (such as a UI) can connect to.
    core_address = core.GetClientAddress()
    nuke.message("iograft Core: '{}' running at: {}".format(
                    IOGRAFT_NUKE_CORE_NAME,
                    core_address))


def stop_iograft():
    """
    Shutdown the Core object current running inside of Nuke. If no Core is
    currently running, this function takes no action.
    """
    if not iograft.IsInitialized():
        nuke.message("The iograft API is not currently initialized.")
        return

    # Otherwise, clear the "nuke" Core object and uninitialize iograft.
    try:
        iograft.UnregisterCore(IOGRAFT_NUKE_CORE_NAME)
    except KeyError:
        pass

    # Uninitialize iograft.
    iograft.Uninitialize()
    nuke.message("The iograft API has been uninitialized.")


def launch_iograft_ui():
    """
    Launch an iograft UI session that can connect to the iograft Core
    object running inside of Nuke.
    """
    import subprocess

    # Check that iograft is initialized.
    if not iograft.IsInitialized():
        nuke.message("The iograft API has not been initialized.")
        return

    # Try to get the "nuke" Core object.
    core_address = ""
    try:
        core = iograft.GetCore(IOGRAFT_NUKE_CORE_NAME, create_if_needed=False)
        core_address = core.GetClientAddress()
    except KeyError:
        nuke.message("No iograft Core: '{}' is currently running.".format(
                        IOGRAFT_NUKE_CORE_NAME))
        return

    # Sanitize the environment for the iograft_ui session; removing the
    # LD_LIBRARY_PATH so we don't conflict with Nuke's Qt libraries and
    # clearing the IOGRAFT_ENV environment variable since the UI process
    # will no longer be running under the Nuke interpreter.
    subprocess_env = os.environ.copy()
    subprocess_env.pop("LD_LIBRARY_PATH", None)
    subprocess_env.pop("IOGRAFT_ENV", None)

    # Launch the iograft_ui subprocess.
    subprocess.Popen(["iograft_ui", "-c", core_address], env=subprocess_env)
