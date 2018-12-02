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

if repo_name == "apache/RiscOS/Sources/Video/Render/Fonts/Manager":
    raise_tag("Manager-3_41-4_2_2_1")
    raise_tag("Manager-3_41-4_2_2_2")
    raise_tag("Manager-3_41-4_2_2_3")
    raise_tag("Manager-3_41-4_2_2_4")
    raise_tag("Manager-3_41-4_2_2_5")
    raise_tag("Manager-3_41-4_2_2_6")

    raise_tag("Manager-3_41-4_2_2_8")
    raise_tag("Manager-3_41-4_2_2_9")
    raise_tag("Manager-3_41-4_2_2_10")
    raise_tag("Manager-3_41-4_2_2_11")
    raise_tag("Manager-3_41-4_2_2_12")
    raise_tag("Manager-3_41-4_2_2_13")

if repo_name == "apache/RiscOS/Utilities/Autobuild/ABRelease":
    merge("ABRelease-0_89", "RISC_OS-5_26_merge")
    raise_tag("ABRelease-0_34")
    raise_tag("ABRelease-0_37")
    raise_tag("ABRelease-0_39")
    raise_tag("ABRelease-0_40")
    raise_tag("ABRelease-0_41")
    raise_tag("ABRelease-0_42")
    raise_tag("ABRelease-0_43")
    raise_tag("ABRelease-0_44")
    # Fix spelling error in commit message
    c = get_ref("ABRelease-0_85-1_84_2_1")
    c.message = c.message.replace("Uupdate", "Update")

if repo_name == "apache/RiscOS/Sources/Kernel":
    merge("Kernel-5_35-4_79_2_123", "Kernel-5_35-4_79_2_98_2_54")
    merge("Kernel-5_35-4_79_2_147_2_1", "Kernel-5_35-4_79_2_98_2_52_2_1")
    merge("Kernel-5_35-4_79_2_147_2_23", "Kernel-5_35-4_79_2_164")
    merge("Kernel-5_35-4_79_2_165", "Kernel-5_35-4_79_2_147_2_23")
    merge("Kernel-5_48", "Kernel-5_35-4_79_2_327")
    merge("Kernel-5_86-4_129_2_1", "Kernel-5_86")
    merge("Kernel-5_88-4_129_2_4", "Kernel-5_88")
    merge("Kernel-5_89-4_129_2_6", "Kernel-5_89")
    merge("Kernel-5_97-4_129_2_7", "Kernel-5_97")
    merge("Kernel-6_05-4_129_2_8", "Kernel-6_05")
    merge("Kernel-6_08-4_129_2_9", "Kernel-6_08")
    merge("Kernel-6_09", "Kernel-6_08-4_129_2_10")

if repo_name == "apache/RiscOS/BuildSys":
    merge("BuildSys-6_00-1_142_2_2", "BuildSys-6_11")
    merge("BuildSys-6_00-1_142_2_3", "BuildSys-6_19")
    merge("BuildSys-6_00-1_142_2_4", "BuildSys-6_34", 1)
    merge("BuildSys-6_00-1_142_2_5", "BuildSys-6_52")
    merge("BuildSys-6_00-1_142_2_6", "BuildSys-6_64")
    merge("BuildSys-6_00-1_142_2_9", "BuildSys-7_04")
    merge("BuildSys-6_00-1_142_2_10", "BuildSys-7_08")

if repo_name == "apache/RiscOS/Sources/Programmer/HdrSrc":
    merge("nicke_HdrSrc_21_9_98", "Spin_merge")
    merge("HdrSrc-0_63", "HdrSrc-0_57-4_58_2_9")
    merge("HdrSrc-1_62-4_162_2_3", "HdrSrc-1_65")
    merge("HdrSrc-1_62-4_162_2_4", "HdrSrc-1_67")
    merge("HdrSrc-1_62-4_162_2_7", "HdrSrc-1_68")
    merge("HdrSrc-1_62-4_162_2_14", "HdrSrc-1_74")
    merge("HdrSrc-1_62-4_162_2_15", "HdrSrc-1_75")
    merge("HdrSrc-1_76", "HdrSrc-1_62-4_162_2_15")


repo.apply_replacements()
repo.save()

#verify_ancestry("Ursula", "Ursula_bp")
#verify_ancestry("Daytona", "Daytona_bp")
#verify_ancestry("ARTtmp", "ARTtmp_bp")


