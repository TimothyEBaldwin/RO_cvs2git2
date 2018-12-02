#!/usr/bin/python3

# Copyright 2018 Timothy Baldwin
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

"Generate a list of sed and cvs commands to make LICENSE files appear in all revisions."

import os
import pygit2

os.chdir(os.path.dirname(__file__))
mods = open("components.txt", "rt")

for sm in mods:
    sm = sm.strip()
    if sm.startswith("#") or sm == "":
        continue
    name = sm + "/LICENSE"
    repo = pygit2.Repository("submodules/" + sm.replace("/", "_"))
    master = repo[repo.lookup_reference("refs/heads/master").target]
    if "LICENSE" in master.tree:
        print(r"sed -i 's/2018\.11\.08\.00\.05\.29/84.01.02.00.00.00/g'", "'" + name + ",v'")
        for ref in repo.listall_references():
            if ref.startswith("refs/heads/") and ref != "refs/heads/master":
                print("cvs rtag -r1.1 -b", "%-37s" % ref[11:], "'" + name + "'")
            if ref.startswith("refs/tags/"):
                print("cvs rtag -r1.1   ", "%-37s" % ref[10:], "'" + name + "'")
        print()
