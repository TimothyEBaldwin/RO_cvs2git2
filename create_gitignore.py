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

"Add .gitignore files everywhere there ever was a .cvstag file."

import datetime
import os
import sys
import pygit2

path = os.path.dirname(__file__)
mods = open(path + "/components.txt", "rt")
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
cvsroot = sys.argv[1] if len(sys.argv) >= 2 else path + "/cvsroot"

for sm in mods:
    sm = sm.strip()
    if sm.startswith("#") or sm == "":
        continue
    repo = pygit2.Repository(path + "/submodules/" + sm.replace("/", "_"))

    for dirpath, dirnames, filenames in os.walk(cvsroot + "/" + sm):
        for file in filenames:
            if file != ".cvstag,v":
                continue

            if dirpath == "mixed/RiscOS/Sources/Lib/ImageLib/JPEG/log/Attic":
                # No .gitignore file wanted here as csvtag file was errounously commited.
                continue

            if dirpath.endswith("/Attic"):
                dirpath = dirpath[:-6]

            branch = 2
            gitignore = open(dirpath + "/.gitignore,v", "wt")
            gitignore.write("head\t1.1;\naccess;\nsymbols")
            for ref in repo.listall_references():
                if ref.startswith("refs/heads/") and ref != "refs/heads/master" and not ref.startswith("refs/heads/unlabeled"):
                    gitignore.write("\n\t" + ref[11:] + ":1.1.0." + str(branch))
                    branch += 2
                if ref.startswith("refs/tags/") and ref != "refs/tags/unused":
                    gitignore.write("\n\t" + ref[10:] + ":1.1")
            gitignore.write(r""";
locks; strict;
comment	@# @;


1.1
date	96.11.05.00.00.02;	author rool;	state Exp;
branches;
next	;


desc
@@


1.1
log
@Add .gitignore files everywhere there ever was a .cvstag file.
Real commit date """ + now + """
@
text
@*
!.gitignore
@
""")
