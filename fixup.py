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

if repo_name == "apache/RiscOS/Sources/FileSys/FileCore":
    merge("FileCore-3_28", "FileCore-3_25-4_9_2_2")
    merge("FileCore-3_26", "FileCore-3_22-4_6_2_1")
    merge("FileCore-3_21", "Ursula_merge")
    merge("Ursula_merge", "ROL_Ursula_merge")
    merge("FileCore-2_99", "Spinner")

if repo_name == "apache/RiscOS/Sources/FileSys/FileSwitch":
    merge("FileSwitch-2_40", "dcotton_Spin_merge")
    merge("FileSwitch-2_50", "FileSwitch-2_43")
    merge("FileSwitch-2_51", "FileSwitch-2_45")

if repo_name == "apache/RiscOS/Sources/Programmer/HdrSrc":
    merge("nicke_HdrSrc_21_9_98", "Spin_merge")
    merge("HdrSrc-0_63", "HdrSrc-0_57-4_58_2_9")
    merge("HdrSrc-1_62-4_162_2_3", "HdrSrc-1_65")
    merge("HdrSrc-1_62-4_162_2_4", "HdrSrc-1_67")
    merge("HdrSrc-1_62-4_162_2_7", "HdrSrc-1_68")
    merge("HdrSrc-1_62-4_162_2_14", "HdrSrc-1_74")
    merge("HdrSrc-1_62-4_162_2_15", "HdrSrc-1_75")
    merge("HdrSrc-1_76", "HdrSrc-1_62-4_162_2_15")

if repo_name == "mixed/RiscOS/Sources/HAL/BCM2835":
    merge("BCM2835-0_71-1_70_2_2", "BCM2835-0_71")
    merge("BCM2835-0_73-1_70_2_3", "BCM2835-0_73")
    merge("BCM2835-0_75-1_70_2_4", "BCM2835-0_75")
    merge("BCM2835-0_76", "BCM2835-0_75-1_70_2_4")
    #merge("", "Pi3APlus_merge")

if repo_name == "mixed/RiscOS/Sources/HAL/iMx6":
    merge("iMx6-0_80-1_4_2_1", "iMx6-0_80")
    merge("iMx6-0_82-1_4_2_3", "iMx6-0_82")
    merge("iMx6-0_82-1_4_2_4", "iMx6-0_84")
    merge("iMx6-0_82-1_4_2_5", "iMx6-0_85")
    merge("iMx6-0_82-1_4_2_6", "iMx6-0_86")
    merge("iMx6-0_87-1_4_2_7", "iMx6-0_87")
    merge("iMx6-0_87-1_4_2_8", "iMx6-0_88")
    merge("iMx6-0_87-1_4_2_9", "iMx6-0_89")
    merge("iMx6-0_90-1_4_2_10", "iMx6-0_90")
    merge("iMx6-0_90-1_4_2_11", "iMx6-0_96")
    merge("iMx6-0_96-1_4_2_12", "iMx6-0_96")
    merge("iMx6-0_97", "iMx6-0_96-1_4_2_12")

if repo_name == "mixed/RiscOS/Sources/HAL/OMAP5":
    merge("OMAP5-0_06-1_5_2_1", "OMAP5-0_06")
    merge("OMAP5-0_07-1_5_2_3", "OMAP5-0_07")
    merge("OMAP5-0_10-1_5_2_4", "OMAP5-0_10")
    merge("OMAP5-0_11", "OMAP5-0_10-1_5_2_4")

if repo_name == "apache/RiscOS/Sources/Apps/Alarm":
    merge("Alarm-2_71", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Apps/Draw":
    merge("Draw-1_11", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Apps/Edit":
    merge("Edit-1_55", "Ursula_merge")
    reparent_tag("Edit-1_66", "Edit-1_67", 2)

if repo_name == "apache/RiscOS/Sources/Apps/FontEd":
    merge("Manager-3_42", "Manager-3_41-4_2_2_13")

if repo_name == "apache/RiscOS/Sources/Apps/Help":
    merge("Help-2_30", "dcotton_Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Apps/Help2":
    merge("Help2-3_09", "Ursula_merge")
    merge("Help2-3_09", "Ursula_RiscPC_merge")

if repo_name == "apache/RiscOS/Sources/Apps/Paint":
    merge("Paint-1_94", "mstphens_UrsulaRiscPCBuild_20Nov98")

if repo_name == "apache/RiscOS/Sources/Desktop/DragASprit":
    merge("DragASprit-0_13", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Desktop/Filer":
    merge("Filer-1_96", "Ursula_merge", 1)

if repo_name == "apache/RiscOS/Sources/Desktop/FilerAct":
    merge("FilerAct-0_42", "Spin_merge", 1)
    merge("FilerAct-0_42", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Desktop/Filter":
    merge("Filter-0_21", "Spin_merge")
    merge("Filter-0_21", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Desktop/Free":
    merge("Free-0_32", "Ursula_merge", 1)
    merge("Free-0_33", "ROL_Free-0_33")
    merge("Free-0_32", "Spin_merge", 3)

if repo_name == "apache/RiscOS/Sources/Desktop/Pinboard":
    merge("Pinboard-0_75", "Ursula_merge", 1)

if repo_name == "apache/RiscOS/Sources/Desktop/ShellCLI":
    merge("ShellCLI-0_30", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Desktop/Switcher":
    merge("Switcher-1_10", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Desktop/TaskWindow":
    merge("TaskWindow-0_58", "Ursula_merge")
    merge("nturton_TaskWindow-0_56", "RO_3_71")

if repo_name == "apache/RiscOS/Sources/Desktop/Wimp":
    merge("bavison_Wimp-4_00_TRUNK", "bavison_Wimp-4_00")
    merge("Wimp-4_01", "nicke_Wimp_3_96M", 1)

if repo_name == "apache/RiscOS/Sources/FileSys/ADFS/ADFS":
    merge("ADFS-3_32", "Ursula_RiscPC_merge")

if repo_name == "apache/RiscOS/Sources/FileSys/ADFS/ADFSFiler":
    merge("ADFSFiler-0_89", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/FileSys/NetFS/NetFiler":
    merge("NetFiler-0_78", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/FileSys/NetFS/NetFS":
    merge("NetFS-5_91", "UrsulaBuild_FinalSoftload")

if repo_name == "apache/RiscOS/Sources/FileSys/NetPrint":
    merge("NetPrint-5_54", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/FileSys/PCCardFS/PCCardFS":
    merge("PCCardFS-0_10", "UrsulaBuild_FinalSoftload")

if repo_name == "apache/RiscOS/Sources/FileSys/PipeFS":
    merge("PipeFS-0_17", "Spin_merge")
    merge("PipeFS-0_17", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/FileSys/RAMFS/RAMFS":
    merge("RAMFS-2_15", "Ursula_merge", 1)

if repo_name == "apache/RiscOS/Sources/FileSys/RAMFS/RAMFSFiler":
    merge("RAMFSFiler-0_35", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/FileSys/ResourceFS/ResFiler":
    merge("ResFiler-0_16", "Ursula_merge", 2)

if repo_name == "apache/RiscOS/Sources/FileSys/ResourceFS/ResourceFS":
    merge("ResourceFS-0_16", "Spinner_RCA116", 1)
    merge("ResourceFS-0_20", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/HAL/IOMD":
    merge("IOMD-0_01", "HAL_merge")

if repo_name == "apache/RiscOS/Sources/HAL/OMAP4":
    merge("OMAP4-0_54-1_52_2_2", "OMAP4-0_54")
    merge("OMAP4-0_59-1_52_2_3", "OMAP4-0_59")
    merge("OMAP4-0_60", "OMAP4-0_59-1_52_2_3")

if repo_name == "apache/RiscOS/Sources/HWSupport/ARM":
    merge("nicke_ARM-0_13", "Spin_merge")
    merge("ARM-0_14", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/BatMgr":
    merge("BatMgr-0_24", "Spin_merge", 3)

if repo_name == "apache/RiscOS/Sources/HWSupport/Buffers":
    merge("Buffers-0_26", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/DMA":
    merge("DMA-0_16", "HAL_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/DualSerial":
    merge("DualSerial-0_25", "kbracey_32bit_merge")
    merge("DualSerial-0_18", "Daytona_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/Parallel":
    merge("Parallel-0_51", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/Portable":
    merge("Ursula_bp", "Spin_merge", 1)

if repo_name == "apache/RiscOS/Sources/HWSupport/Portable75":
    merge("Portable75-0_05", "kbracey_32bit")

if repo_name == "apache/RiscOS/Sources/HWSupport/PS2Driver":
    merge("PS2Driver-0_26", "Spin_merge", 1)

if repo_name == "apache/RiscOS/Sources/HWSupport/SmartCard/SCInter":
    merge("SCInter-0_18", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/Sound/Sound0":
    merge("Sound0-1_56", "Spin_merge")
    merge("Sound0-1_56", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/Sound/Sound1":
    merge("Sound1-1_32", "Spin_merge")
    merge("Sound1-1_32", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/Sound/Sound2":
    merge("Sound2-1_24", "Spin_merge")
    merge("Sound2-1_24", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/HWSupport/UnSqzAIF":
    merge("UnSqzAIF-0_05", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Internat/Inter":
    merge("Inter-1_50", "Ursula_merge", 1)

if repo_name == "apache/RiscOS/Sources/Internat/Territory/Manager":
    merge("Manager-0_27", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Internat/Messages":
    merge("Messages-0_85", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Lib/callx":
    get_ref("callx-0_03").parents = [get_ref("callx-0_02-1_1_2_3")]

if repo_name == "apache/RiscOS/Sources/Lib/DebugLib":
    merge("DebugLib-0_10", "jberanek_debuglib-0_09", 1)

if repo_name == "apache/RiscOS/Sources/Lib/MemLib":
    merge("MemLib-1_01", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Lib/HTMLLib":
    merge("ahodgkin_204release", "Web", 1)
    merge("Web_bp", "ARTtmp_merge")

if repo_name == "apache/RiscOS/Sources/Networking/AUN/AUNMsgs":
    merge("AUNMsgs-0_10", "Spin_merge", 1)

if repo_name == "apache/RiscOS/Sources/Networking/AUN/BootNet":
    merge("BootNet-0_90", "Ursula_13May1998_merge")

if repo_name == "apache/RiscOS/Sources/Networking/AUN/Net":
    merge("Net-6_18", "Ursula_13May1998_merge", 1)

if repo_name == "apache/RiscOS/Sources/Networking/NetStatus":
    merge("NetStatus-2_08", "Ursula_13May1998_merge", 2)

if repo_name == "apache/RiscOS/Sources/Networking/NetTime":
    merge("NetTime-0_04", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Printing/Modules/MakePSFont":
    merge("nturton_MakePSFont-1_08", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Printing/Modules/PDModules":
    merge("PDModules-4_44", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Printing/Modules/PDriver":
    merge("PDriver-3_34", "PDriver-3_33-4_7_2_1")

if repo_name == "apache/RiscOS/Sources/Printing/Modules/PDumperSpt":
    merge("Ursula_31Mar1998", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Printing/PPrimer":
    merge("PPrimer-0_16", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Programmer/BASIC":
    merge("BASIC-1_18", "Ursula_merge", 3)
    merge("BASIC-1_18", "Spin_merge", 4)

if repo_name == "apache/RiscOS/Sources/Programmer/Debugger":
    merge("Debugger-1_57", "UrsulaBuild_FinalSoftload", 1)

if repo_name == "apache/RiscOS/Sources/Programmer/KeyWatch":
    merge("KeyWatch-0_09", "KeyWatch-0_08-1_1_2_10", 1)

if repo_name == "apache/RiscOS/Sources/Programmer/Obey":
    merge("Obey-0_36", "Spin_merge")
    merge("Obey-0_36", "Ursula_merge")

if repo_name == "apache/RiscOS/Sources/Utilities/HForm":
    merge("HForm-2_52", "Ursula_merge", 3)

if repo_name == "apache/RiscOS/Sources/Video/Render/Colours":
    merge("Colours-1_67", "Spin_merge")

if repo_name == "apache/RiscOS/Sources/Video/Render/Fonts/ROMFonts":
    merge("ROMFonts-0_24", "Spinner_RCA116")
    merge("ROMFonts-0_24", "Ursula_merge", 2)

if repo_name == "apache/RiscOS/Sources/Video/Render/Hourglass":
    merge("Hourglass-2_14", "bavison_Hourglass_213")

if repo_name == "apache/RiscOS/Sources/Video/Render/ScrBlank":
    merge("nturton_ScrBlank-2_27", "Spin_merge", 1)

if repo_name == "apache/RiscOS/Sources/Video/UserI/ScrSaver":
    merge("ScrSaver-0_15", "Spinner")

if repo_name == "apache/RiscOS/Sources/Video/UserI/ScrSavers/AcornLogo":
    merge("AcornLogo-0_01", "rleggett_AcornLogo-0_02")

if repo_name == "apache/RiscOS/Sources/Video/UserI/ScrSavers/Slider":
    merge("Slider-0_01", "UrsulaBuild_FinalSoftload", 2)

if repo_name == "apache/RiscOS/Utilities/CVSUtils/EraseCVS":
    merge("EraseCVS-0_05", "Spin_merge", 2)

if repo_name == "apache/RiscOS/Utilities/Release/srcbuild":
    merge("srcbuild-0_25", "srcbuild-0_24-1_23_2_4")

if repo_name == "apache/RiscOS/Utilities/Release/builder":
    merge("builder-0_06", "builder-0_06-1_1_2_2")

if repo_name == "bsd/RiscOS/Sources/Audio/SharedSnd":
    merge("SharedSnd-0_48", "Spin_merge")
    merge("SharedSnd-1_06", "ESP_SharedSnd-1_06_merge")

if repo_name == "mixed/RiscOS/Sources/Lib/zlib":
    merge("zlib-1_13", "zlib_1_1_3")


repo.apply_replacements()
repo.save()

#verify_ancestry("Ursula", "Ursula_bp")
#verify_ancestry("Daytona", "Daytona_bp")
#verify_ancestry("ARTtmp", "ARTtmp_bp")


