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

import nuke
import iograftnuke

# Create the iograft menu.
toolbar = nuke.menu("Nodes")
iograft_menu = toolbar.addMenu("iograft", icon="iograft_icon.png")

# Add the iograft commands to the menu.
iograft_menu.addCommand("Start iograft", "iograftnuke.start_iograft()")
iograft_menu.addCommand("Stop iograft", "iograftnuke.stop_iograft()")
iograft_menu.addCommand("Launch iograft UI", "iograftnuke.launch_iograft_ui()")
