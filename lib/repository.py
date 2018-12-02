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

import pygit2

class Commit:

    def __init__(self):
        self.oid = None
        self.replacement = None

    def __lt__(a, b):
        return (a.committer.time, a.tree_id) < (b.committer.time, b.tree_id)

    def __iter__(c):
        while len(c.parents) > 0:
            yield c
            c = c.parents[0]
        yield c



class Repository:

    def __init__(self, path):
        self.commits = dict()
        self.refs = dict()
        self.repo = pygit2.Repository(path)
        for ref1 in self.repo.listall_references():
            ref = self.repo.lookup_reference(ref1)
            if ref.type == pygit2.GIT_REF_OID:
                self.refs[ref1] = self.__load_commit(ref.target)

    def __load_commit(self, oid):
        c = self.commits.get(oid)
        if c is not None:
            return c
        c1 = self.repo[oid]
        c = Commit()
        c.oid = oid
        c.author = c1.author
        c.committer = c1.committer
        c.message = c1.message.strip()
        c.tree_id = c1.tree_id
        c.parents = [self.__load_commit(i) for i in c1.parent_ids]
        c.is_tag = c.message.startswith("This commit was manufactured by cvs2svn to create tag")
        c.is_branch = c.message.startswith("This commit was manufactured by cvs2svn to create branch")
        self.commits[oid] = c
        return c

    def save(self):
        for c in self.commits.values():
            c.oid = None
        for key, value in self.refs.items():
            self.repo.create_reference(key, self.__rewrite(value), force=True)

    def __rewrite(self, c):
        if c.oid is None:
            c.oid = False
            parents = [self.__rewrite(x) for x in c.parents if x.oid is not False]
            c.oid = self.repo.create_commit(
                None,
                c.author,
                c.committer,
                c.message,
                c.tree_id,
                parents)
        assert isinstance(c.oid, pygit2.Oid)
        return c.oid

    def apply_replacements(self):
        def do_replace(c):
            while c.replacement is not None:
                c = c.replacement
            return c
        for c in self.commits.values():
            c.parents = [do_replace(x) for x in c.parents]
        for key, c in self.refs.items():
            self.refs[key] = do_replace(c)
