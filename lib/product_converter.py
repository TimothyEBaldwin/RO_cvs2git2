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

import re
import heapq
import datetime
import pygit2
import repository
import os

class Repos(dict):
    def __missing__(self, key):
        r = repository.Repository(os.path.join(submodules, key.replace("/", "_"))).refs
        self[key] = r
        return r

repos = Repos()

# Security, components may not start with "/" or "."
__parse_modules_re = re.compile(r"^[\t ]*([^#/.\s]\S*)[\t ]*(\S*)[\t ]*$", re.MULTILINE)

def parse_modules(text):
    # Parse Products/*/modules whilst applying corrections
    for i in __parse_modules_re.finditer(text):
        path = i.group(1)
        tag = i.group(2)

        # Sometimes "." is used a directory separator
        path = path.replace(".", "/")

        # Convert from CVS to git
        if tag == "TRUNK" or tag == "HEAD":
            tag = "master"

        # Fix mistakes

        if path == "private/RiscOS/Sources/HAL/iMx6":
            continue # Early versions of the iMx6 HAL are not public.
        if path == "private/RiscOS/Sources/Video/HWSupport/IMXVideo":
            continue # Early versions of IMXVideo are not public.
        if path == "private/RiscOS/Sources/Networking/Ethernet/EtherTH":
            continue # Early versions of EtherTH are not public.
        if path == "private/RiscOS/Sources/Networking/Ethernet/EtherET":
            continue # And EtherET is completely missing.
        if path == "private/patcher" or path == "private/patcher/modules":
            continue # Also from iMx6.
        if path == "private/RiscOS/BuildSys":
            continue # Also from iMx6.
        if path == "private/RiscOS/Env":
            continue # Also from iMx6.
        if path == "private/RiscOS/Sources/FileSys/SATAFS/SATAFS":
            continue # Also from iMx6.
        if path == "private/RiscOS/Sources/HWSupport/SD/SDCMOS":
            continue # Also from iMx6.
        if path == "private/Products":
            continue # Also from iMx6.

        if path == "closed/RiscOS/Sources/SystemRes/LiveDisc" and not have_closed:
            continue # But this is from OMAP3Live

        if path == "apache/RiscOS/Apps/Makefile":
            continue # FIXME

        if path == "apache/RiscOS/Sources/Video/UserI/BootFX":
            continue # Wrong path given in BCM2835Dev

        if path == "bsd/RiscOS/Sources/Utilties/SDCreate":
            continue # Spelling error, Utilities mispelled


        if path == "mixed/RiscOS/Sources/HWSupport/USB":
            pass # FIXME
        elif path == "apache/RiscOS/Sources/FileSys/CDFS":
            yield "apache/RiscOS/Sources/FileSys/CDFS/CDFS", tag
            yield "apache/RiscOS/Sources/FileSys/CDFS/CDFSFiler", tag

        elif path == "apache/RiscOS/Sources/HAL/OMAP3" and tag == "OMAP3-0_867":
            pass # Tag name typo

        else:
            assert have_closed or not path.startswith("closed")
            yield path, tag


def convert(name):

    def add_module(commit, path):
        index.add(pygit2.IndexEntry(path, commit.oid, pygit2.GIT_FILEMODE_COMMIT))
        mods[path] = commit.oid

    # Find first commit in source branch
    # and create child
    commit = repo.refs["refs/heads/Products_" + name]
    commit.child = None
    while len(commit.parents) > 0:
        commit2 = commit.parents[0]
        commit2.child = commit
        commit = commit2

    heap = [(commit, "")]
    parents = []
    mods_list = []
    empty = repository.Commit()

    while len(heap) > 0:

        current, current_path = heap[0]
        print(name,
            datetime.datetime.utcfromtimestamp(
                current.committer.time).strftime(
                    '%Y-%m-%d %H:%M:%S'))

        if current_path == "":
            heap = [] if current.child is None else [(current.child, "")]
            mods = dict()
            index = pygit2.Index()

            # Read modules
            blob_id = repo.repo[current.tree_id]["modules"].id
            index.add(pygit2.IndexEntry("Products/" + name + "/modules", blob_id, pygit2.GIT_FILEMODE_BLOB))

            text = repo.repo[blob_id].read_raw()
            modules = ""
            text = text.decode('cp437')
            for path, tag in parse_modules(text):
                branch = False

                # Convert checkout location to CVS location
                rpath = path
                if rpath == "apache/RiscOS/Sources/HWSupport/AHCIDriver":
                    rpath = "apache/RiscOS/Sources/HWSupport/SCSI/AHCIDriver"

                if rpath == "apache/RiscOS/Sources/HAL/OMAP5":
                    rpath = "mixed/RiscOS/Sources/HAL/OMAP5"

                if rpath == "bsd/RiscOS/Sources/HWSupport/VFPSupport":
                    rpath = "mixed/RiscOS/Sources/HWSupport/VFPSupport"
                    if tag == "master":
                        tag = "VFPSupport-0_05"
                        branch = True

                if rpath == "mixed/RiscOS/Sources/HWSupport/USB/NetBSD":
                    rpath = "mixed/RiscOS/Sources/HWSupport/USB/USBDriver"
                    if tag == "master":
                        tag = "NetBSD-1_19"
                        branch = True

                # Generate .gitmodules entry
                # FIXME Make binary submodules shallow
                modules += ("[submodule \"" + rpath + "\"]\n"
                            "\tpath = " + path + "\n"
                            "\turl = " + submodules_out + "/" + rpath.replace("/", "_") + "\n")

                # Get reference to submodule repository
                refs = repos[rpath]

                # Load tag or branch
                commit = refs.get("refs/tags/" + tag)
                if commit is None:
                    commit = refs["refs/heads/" + tag]
                    branch = True
                    # Add branch to .gitmodules entry
                    modules += "\tbranch = " + tag + "\n"

                if branch:
                    # Find latest commit before current
                    # And also create links to forwards
                    commit.child = None
                    while commit > current:
                        # Commit is too recent
                        commit2 = commit.parents[0] if len(commit.parents) > 0 else current
                        commit2.child = commit
                        commit = commit2

                    if commit.child is not None:
                        heapq.heappush(heap, (commit.child, path))

                if commit is not current:
                    add_module(commit, path)

            index.add(pygit2.IndexEntry(".gitmodules", repo.repo.create_blob(modules), pygit2.GIT_FILEMODE_BLOB))
        else: # current_path == ""
            add_module(current, current_path)
            heapq.heappop(heap)
            if current.child is not None:
                heapq.heappush(heap, (current.child, current_path))

        out = repository.Commit()
        out.author    = current.author
        out.committer = current.committer
        out.message   = name + " " + current_path + " " + current.message
        out.tree_id   = index.write_tree(repo.repo)
        out.parents   = parents
        mods_list.append((out, frozenset(mods.items())))
        parents = [out]
    repo.refs["refs/heads/" + name] = out
    print(name + " branch conversion finished")
    return mods_list

def merge_branches(dev, stable):
    # For each commit in the stable branch
    for stable_commit, stable_mods in stable:
        # Find closest matching commit in the Dev branch
        cost = 1000000
        for dev_commit, dev_mods in dev:
            c = len(dev_mods ^ stable_mods)
            if c < cost:
                cost = c
                best = dev_commit

        # Add best development commit as additional parent of stable commit
        stable_commit.parents.append(best)
        stable_commit.message += "\n\nCost = " + str(cost) # FIXME Remove?
        del best
