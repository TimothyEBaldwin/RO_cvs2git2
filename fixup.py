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

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

import datetime
import repository
import fixup

# Load repository
fixup.repo_name = sys.argv[2]
fixup.repo = repository.Repository(sys.argv[1])
from fixup import *
refs = repo.refs

use_original_refs()
remove_unneeded_branch_and_tag_commits()
#tidy_default_branch_copies(remove_default = False)
repo.apply_replacements()

# Mark components that have branches for closer review
if have_branch():
    open(os.path.join(sys.argv[1], "have_branch"), "wt").close()



repo.apply_replacements()
repo.save()

#verify_ancestry("Ursula", "Ursula_bp")
#verify_ancestry("Daytona", "Daytona_bp")
#verify_ancestry("ARTtmp", "ARTtmp_bp")


