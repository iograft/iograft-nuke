# iograft for Nuke

This repository contains scripts and nodes for running iograft within Nuke. It includes two subcore commands (Python interpreter mode (`Nuke13.2 -t`) and using Nuke's python.exe suitable for use with `nuke_r`). It also includes an iograft plugin for Nuke and a few example iograft Nuke nodes.

## Getting started with a Nuke environment

Below are the steps required to setup a new environment in iograft for executing nodes in Nuke.

1. Clone this iograft-nuke repository.
2. Open the iograft Environment Manager and create a new environment for Nuke (i.e. "nuke").
3. Add the "nodes" directory of the iograft-nuke repository to the **Plugin Path**.
4. Update the **Subcore Launch Command** to either the `iognuke_subcore` command or `iognuker_subcore` if setting up for use with `nuke_r`. Note: On Windows these commands will automatically resolve to the `iognuke_subcore.bat` script.
5. Add the "bin" directory of the iograft-nuke repository to the **Path**.
6. Add the directory containing the Nuke executable to the **Path**. **IMPORTANT**: For Nuke's Qt libraries to resolve correctly, this Nuke executable path must be _first_ in the Path list.
7. Add the "python" directory of the iograft-nuke repository to the **Python Path**.
8. Depending on the version of Nuke, update the **Python Path** entry for `...\iograft\python39` by switching "python39" to the directory for the correct version of Python (for Nuke 13, this is "python37").
9. If building an environment for Nuke (not `nuke_r`) add an environment variable named `IOG_NUKE_COMMAND` that contains the name of the Nuke command (i.e. `Nuke13.2.exe`).

<details><summary>Example Nuke environment JSON</summary>
<p>
    
```json
{
    "plugin_path": [
        "C:\\Program Files\\iograft\\types",
        "C:\\Program Files\\iograft\\nodes",
        "{IOGRAFT_USER_CONFIG_DIR}\\types",
        "{IOGRAFT_USER_CONFIG_DIR}\\nodes",
        "C:\\Users\\dtkno\\Projects\\iograft-public\\iograft-nuke\\nodes"
    ],
    "subcore": {
        "launch_command": "iognuke_subcore"
    },
    "path": [
        "C:\\Program Files\\Nuke13.2v1",
        "C:\\Program Files\\iograft\\bin",
        "C:\\Users\\dtkno\\Projects\\iograft-public\\iograft-nuke\\bin"
    ],
    "python_path": [
        "C:\\Program Files\\iograft\\types",
        "C:\\Program Files\\iograft\\python37",
        "C:\\Users\\dtkno\\Projects\\iograft-public\\iograft-nuke\\python"
    ],
    "environment_variables": {
        "IOG_NUKE_COMMAND": "Nuke13.2.exe"
    },
    "appended_environments": [],
    "name": "nuke"
}
```
    
</p>
</details>

## Nuke Subcore for iograft

There are two available subcore commands for running Nuke headless-ly from iograft. The first (`iognuke_subcore`) makes use of the `-t` parameter to the Nuke command to execute the subcore script. The second (`iognuker_subcore`) is suitable for usage with `nuke_r` and uses Nuke's included Python interpreter directly.

## iograft Plugin for Nuke

The iograft Plugin for Nuke allows iograft to be run from inside an interactive Nuke session. The plugin creates an iograft menu on the "Nodes" toolbar and registers 3 operations:

1. **Start iograft** -
Used to initialize a local iograft session within Nuke. Starts an iograft Core using the builtin Nuke Python interpreter. A UI session can be connected to this iograft Core for graph authoring and monitoring.

2. **Stop iograft** -
Used to shutdown the iograft session within Nuke.

3. **Launch iograft UI** -
Launch the iograft UI as a subprocess and connect to the iograft Core running inside of Nuke. Note: The UI runs in a completely separate process and not internally in Nuke. Only the iograft Core runs inside of Nuke.

All other operations for interacting with the Core object should be completed using the iograft Python API.

When the **Start iograft** operation is executed, it registers a Core named "nuke" that can be retrieved with the Python API as shown below:

```python
import iograft
core = iograft.GetCore("nuke")
```

Using the Python API, we have access to useful functionality on the Core such as loading graphs, setting input values on a graph, and processing the graph.


## iograft Plugin for Nuke

To use iograft within a Nuke interactive session, we need to ensure the iograft libraries are accessible to Nuke (via the Path/Python Path), and tell iograft what environment we are in. These steps can either be done with a custom Nuke startup script, or by launching Nuke using `iograft_env`.

### Startup Script (`init.py`)

This method is the simplest method for ensuring iograft is available within Nuke. Nuke executes the `init.py` startup scripts on every launch and allows us to setup the necessary paths to load the iograft plugin and set the iograft environment. For details on setting up an `init.py` script, see the [Nuke Python Developer Guide](https://learn.foundry.com/nuke/developers/63/pythondevguide/startup.html).

Below is an example of an `init.py` script that sets up Nuke to use iograft:
```python
# Ensure that the iograft python modules can be found.
# NOTE: This path can also be set in a Maya.env file.
import os
import sys

import nuke

# Ensure that iograft is on the Python Path.
IOGRAFT_PYTHON_PATH = "C:/Program Files/iograft/python37"
if IOGRAFT_PYTHON_PATH not in sys.path:
    sys.path.append(IOGRAFT_PYTHON_PATH)

# Initialize the iograft environment so that it matches the environment
# set within iograft.
import iograft
environment_name = "nuke"
try:
    iograft.InitializeEnvironment(environment_name)
except KeyError as e:
    print("Failed to initialize iograft environment: {}: {}".format(
            environment_name, e))

# Add the iograft-nuke plugin to Nuke's plugin path.
IOGRAFT_NUKE_PLUGIN_PATH = "C:/Users/dtkno/Projects/iograft-public/iograft-nuke/plugin"
nuke.pluginAddPath(IOGRAFT_NUKE_PLUGIN_PATH)
```

Note: This method assumes that the iograft "bin" directory is on the user's PATH.

### iograft_env

The second method for launching Nuke so iograft can be used is via `iograft_env`. iograft_env first initializes all of the environment variables contained within the environment JSON and then launches the given command (Nuke13.2 in the example below).

```bat
iograft_env -e nuke -c Nuke13.2
```

Note: Using this method alone, the iograft plugin will not be added to Nuke unless the plugin's path has been added to Nuke's NUKE_PATH or added in a startup script.


## Threading in Nuke

Some of the available Nuke Python commands are expected to be run in the main thread (or else there is the possibility for errors and undefined behavior). To get around any threading issues, there are a couple of additions we can make to the Nuke scripts and nodes.

1. Nodes that execute Nuke commands that may be unsafe in a threaded environment must apply the `@nuke_main_thread` decorator to their `Process` function. When running iograft interactively in Nuke, this decorator makes use of Nuke's `executeInMainThreadWithResult` function to process the node in Nuke's main thread.

2. To avoid blocking the main thread when processing graphs in an interactive Nuke session, processing must be started with either the `StartGraphProcessing()` function which is non-blocking, or pass the `execute_in_main_thread` argument to `ProcessGraph(execute_in_main_thread=True)` to ensure that nodes that require the main thread can be completed successfully.

3. When processing Nuke nodes in batch (i.e. when using the Nuke Subcore), `iognukepy_subcore.py` executes all nodes in the main thread. To do this, it makes use of the `iograft.MainThreadSubcore` class which runs the primary `iograft.Subcore.ListenForWork` listener in a secondary thread while processing nodes in the main thread.


## Known Limitations

Currently on Windows, when executing different environments (i.e. Maya) from _within_ an interactive Nuke session, Nuke modifies the process' DLL search order which affects all child processes. This means that Nuke essentially inserts itself first in the DLL search path for ALL child processes leading to errors if there are library conflicts.

In a future release of iograft, we will address Nuke's behavior so subcores launched from Nuke for different environments are not affected. Note: This limitation ONLY affects interactive Nuke sessions.
