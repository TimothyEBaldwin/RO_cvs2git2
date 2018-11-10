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

import pygit2
import pprint
import pdb
import re
import sys
import datetime
import heapq

repo = pygit2.Repository('.')


class commit:

    def __init__(self):
        self.oid = None
        self.replaced = False

    def __lt__(a, b):
        return (a.committer.time, a.tree_id) < (b.committer.time, b.tree_id)

commits = dict()
refs = dict()


def load_commit(repo, oid):
    if oid in commits:
        return commits[oid]
    c1 = repo[oid]
    c = commit()
    c.author = c1.author
    c.committer = c1.committer
    c.message = c1.message
    c.tree_id = c1.tree_id
    c.parents = [load_commit(repo, i) for i in c1.parent_ids]
    c.repo = repo
    commits[oid] = c
    return c

for ref1 in repo.listall_references():
    ref = repo.lookup_reference(ref1)
    if ref.type == pygit2.GIT_REF_OID:
        if ref1.startswith("refs/original/"):
            refs["refs/" + ref1[14:]] = load_commit(repo, ref.target)
            # ref.delete()


def rewrite(c):
    if c.oid is None:
        c.oid = False
        c.replaced = False
        parents = [rewrite(x) for x in c.parents if x.oid is not False]
        c.oid = repo.create_commit(
            None,
            c.author,
            c.committer,
            c.message,
            c.tree_id,
            parents)
    assert isinstance(c.oid, pygit2.Oid)
    return c.oid


def fix_redudant_commits():
    for key, c in refs.items():
        if c.message.startswith("Synthetic commit for incomplete tag ") and c.tree_id == c.parents[0].tree_id:
            refs[key] = c.parents[0]


def merge_base(b):
    global merge__base
    merge__base = b
    return "refs/heads/" + merge__base + "_master" in refs


def merge_ref(c):
    return refs["refs/tags/" + merge__base + "_" + c]


def merge(c, p, i=0):
    try:
        c = merge_ref(c)
        while i > 0:
            i -= 1
            c = c.parents[0]
        c.replaced = True
        c.parents.append(merge_ref(p))
    except KeyError:
        pass


fix_redudant_commits()

if merge_base("apache_RiscOS_Sources_Kernel"):
    merge_ref("Kernel-5_35-4_79_2_1").parents = [merge_ref("Kernel-5_35")]
    merge("Kernel-5_35-4_79_2_44", "Kernel-5_35-4_79_2_25_2_2")
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
    merge_ref("Kernel-6_01-3").parents[
        0].tree_id = merge_ref("Kernel-6_01-3").tree_id
    refs["refs/tags/apache_RiscOS_Sources_Kernel_Kernel-6_01-3"] = merge_ref(
        "Kernel-6_01-3").parents[0]

if merge_base("bsd_RiscOS_Sources_Audio_SharedSnd"):
    merge("SharedSnd-0_48", "Spin_merge")
    merge("SharedSnd-1_06", "SharedSnd-ESP_SharedSnd-1_06_merge")

if merge_base("bsd_RiscOS_Sources_HWSupport_Sound_BCMSound"):
    pass

if merge_base("bsd_RiscOS_Sources_HWSupport_VFPSupport"):
    pass

if merge_base("bsd_RiscOS_Sources_Lib_SyncLib"):
    pass

if merge_base("bsd_RiscOS_Sources_Lib_UtilLib"):
    pass

if merge_base("bsd_RiscOS_Sources_Networking_Ethernet_EtherCPSW"):
    pass

if merge_base("bsd_RiscOS_Sources_Networking_Ethernet_EtherUSB"):
    pass

if merge_base("bsd_RiscOS_Sources_Networking_Ethernet_EtherY"):
    pass

if merge_base("bsd_RiscOS_Sources_Networking_MimeMap"):
    pass

if merge_base("bsd_RiscOS_Sources_Programmer_ZeroPain"):
    pass

if merge_base("bsd_RiscOS_Sources_Programmer_ZLib"):
    pass

if merge_base("bsd_RiscOS_Sources_SystemRes_ThemeDefs"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_7thsoftware_Video_UserI_ScrSavers_DeskBall"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_7thsoftware_Video_UserI_ScrSavers_Rain"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_7thsoftware_Video_UserI_ScrSavers_Random"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_7thsoftware_Video_UserI_ScrSavers_Shred"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_7thsoftware_Video_UserI_ScrSavers_Snow"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_7thsoftware_Video_UserI_ScrSavers_SprBounce"):
    pass

if merge_base("bsd_RiscOS_Sources_ThirdParty_TankStage_HWSupport_GPIO"):
    pass

if merge_base("bsd_RiscOS_Sources_Utilities_SDCreate"):
    pass

if merge_base("bsd_RiscOS_Sources_Utilities_Usage"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_HWSupport_GC320Video"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_HWSupport_OMAP4Video"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_HWSupport_OMAPVideo"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_Render_BlendTable"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_Render_PsychoEffects"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_Render_VideoOverlay"):
    pass

if merge_base("bsd_RiscOS_Sources_Video_UserI_BootFX"):
    pass

if merge_base("bsd_RiscOS_Tools_Sources_SameFile"):
    pass

if merge_base("apache_RiscOS_BuildSys"):
    merge("BuildSys-6_00-1_142_2_2", "BuildSys-6_11")
    merge("BuildSys-6_00-1_142_2_3", "BuildSys-6_19")
    merge("BuildSys-6_00-1_142_2_4", "BuildSys-6_34", 1)
    merge("BuildSys-6_00-1_142_2_5", "BuildSys-6_52")
    merge("BuildSys-6_00-1_142_2_6", "BuildSys-6_64")
    merge("BuildSys-6_00-1_142_2_9", "BuildSys-7_04")
    merge("BuildSys-6_00-1_142_2_10", "BuildSys-7_08")

if merge_base("apache_RiscOS_Export"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Alarm"):
    merge("Alarm-2_71", "Ursula_merge")

if merge_base("apache_RiscOS_Sources_Apps_Alarm"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Browse"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_CDPlayer"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Chars"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_CloseUp"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Blocks"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Clock"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Diversions"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Flasher"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Madness"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_MemNow"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_MineHunt"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Patience"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Diversions_Puzzle"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Draw"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Edit"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_FontEd"):
    merge("Manager-3_42", "Manager-3_41-4_2_2_13")

if merge_base("apache_RiscOS_Sources_Apps_Help"):
    merge("Help-2_30", "dcotton_Ursula_merge")

if merge_base("apache_RiscOS_Sources_Apps_Help2"):
    merge("Help2-3_09", "Ursula_merge")
    merge("Help2-3_09", "Ursula_RiscPC_merge")

if merge_base("apache_RiscOS_Sources_Apps_Maestro"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_MakeModes"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Paint"):
    merge("Paint-1_94", "mstphens_UrsulaRiscPCBuild_20Nov98")

if merge_base("apache_RiscOS_Sources_Apps_Sampler"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_SciCalc"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Squash"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_SrcEdit"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Toolbox_ResCreate"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Toolbox_ResEd"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_Toolbox_ResTest"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_TTXTViewer"):
    pass

if merge_base("apache_RiscOS_Sources_Apps_WebServe"):
    pass

if merge_base("apache_RiscOS_Sources_Audio_SoundCtrl"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_Clipboard"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_Desktop"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_DragAnObj"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_DragASprit"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_Filer"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_FilerAct"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_FilerSWIs"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_Filter"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_Free"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_Pinboard"):
    merge("Pinboard-0_75", "Ursula_merge", 1)

if merge_base("apache_RiscOS_Sources_Desktop_RedrawMgr"):
    # merge("RedrawMgr-0_06",
    pass

if merge_base("apache_RiscOS_Sources_Desktop_ShellCLI"):
    merge("ShellCLI-0_30", "Ursula_merge")

if merge_base("apache_RiscOS_Sources_Desktop_Switcher"):
    pass

if merge_base("apache_RiscOS_Sources_Desktop_TaskWindow"):
    merge("TaskWindow-0_58", "Ursula_merge")
    merge("nturton_TaskWindow-0_56", "TaskWindow_RO_3_71")

if merge_base("apache_RiscOS_Sources_Desktop_Wimp"):
    merge("bavison_Wimp-4_00_TRUNK", "bavison_Wimp-4_00")
    merge("Wimp-4_01", "nicke_Wimp_3_96M", 1)
    # TODO

if merge_base("apache_RiscOS_Sources_FileSys_ADFS_ADFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_ADFS_ADFSFiler"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_CDFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_CDFS_CDFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_CDFS_CDFSFiler"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_FileCore"):
    merge("FileCore-3_28", "FileCore-3_25-4_9_2_2")
    merge("FileCore-3_26", "FileCore-3_22-4_6_2_1")
    merge("FileCore-3_21", "Ursula_merge")
    merge("Ursula_merge", "ROL_Ursula_merge")
    merge_ref("FileCore-2_99").parents[0].parents.append(
        refs["refs/heads/apache_RiscOS_Sources_FileSys_FileCore_Spinner"])

if merge_base("apache_RiscOS_Sources_FileSys_FileSwitch"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_FSLock"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_ImageFS_DOSFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_NetFS_NetFiler"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_NetFS_NetFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_NetPrint"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_PCCardFS_PCCardFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_PCCardFS_PCCFiler"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_PipeFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_RAMFS_RAMFS"):
    merge("dellis_autobuild_BaseSW", "Ursula_merge")

if merge_base("apache_RiscOS_Sources_FileSys_RAMFS_RAMFSFiler"):
    merge("RAMFSFiler-0_35", "Ursula_merge")
    pass

if merge_base("apache_RiscOS_Sources_FileSys_ResourceFS_ResFiler"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_ResourceFS_ResourceFS"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_SCSIFS_PartMan"):
    pass

if merge_base("apache_RiscOS_Sources_FileSys_SCSIFS_SCSIFS"):
    pass

if merge_base("apache_RiscOS_Sources_HAL_IOMD"):
    merge("IOMD-0_01", "IOMD_HAL_merge")

if merge_base("apache_RiscOS_Sources_HAL_OMAP4"):
    merge("OMAP4-0_54-1_52_2_2", "OMAP4-0_54")
    merge("OMAP4-0_59-1_52_2_3", "OMAP4-0_59")
    merge("OMAP4-0_60", "OMAP4-0_59-1_52_2_3")

if merge_base("apache_RiscOS_Sources_HWSupport_ARM"):
    merge("nicke_ARM-0_13", "Spin_merge")
    merge("ARM-0_14", "Ursula_merge")

if merge_base("apache_RiscOS_Sources_HWSupport_Buffers"):
    merge("Buffers-0_26", "Spin_merge")
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_CD"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_CD_ATAPI"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_CD_CDFSDriver"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_CMOSUtils"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_DeviceFS"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_DMA"):
    merge("DMA-0_16", "HAL_merge")

if merge_base("apache_RiscOS_Sources_HWSupport_DualSerial"):
# merge("DualSerial-0_25", "DualSerial-kbracey_32bit_merge")
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_FPASC"):
# merge("FPASC-sbrodie_sedwards_16Mar2000", "FPASC-kbracey_32bit_merge")
# merge("FPASC-4_11", "FPASC-4_10-4_3_2_1")
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_IIC"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_IRQUtils2"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Joystick"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Mouse"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_NVRAM"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Parallel"):
# merge("Parallel-0_64", "Parallel-kbracey_32bit_merge")
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_PCI"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Podule"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Portable"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_PortableHAL"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_PortMan"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_PS2Driver"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_RTCAdjust"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SCSI_AHCIDriver"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SCSI_SCSIDriver"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SCSI_SCSISwitch"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Serial"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SerialSpt"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SerKeyMouse"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SerMouse"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SmartCard_SCInter"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Sound0"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Sound0HAL"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Sound0Trid"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Sound1"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Sound2"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Voices_Percussion"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Voices_StringLib"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_Sound_Voices_WaveSynth"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SPIDriver"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_SystemDevs"):
    pass

if merge_base("apache_RiscOS_Sources_HWSupport_UnSqzAIF"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Inter"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_IntKey"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Messages"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_MsgTrans"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Territory_Japan"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Territory_Manager"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Territory_Module"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Territory_UK"):
    pass

if merge_base("apache_RiscOS_Sources_Internat_Territory_USA"):
    pass

if merge_base("apache_RiscOS_Sources_Kernel"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_AcornNC"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_AsmUtils"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_callx"):
# merge("callx-0_03", "callx-0_02-1_1_2_3")
    pass

if merge_base("apache_RiscOS_Sources_Lib_CLXLite"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_Configure"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_DebugLib"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_Email_Common"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_HALLib"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_HTML"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_HTMLLib"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_MemLib"):
# merge("MemLib-1_01", "MemLib-1_00-1_1_2_3")
    pass

if merge_base("apache_RiscOS_Sources_Lib_ModMalloc"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_ModuleTask"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_NBLib"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_PDebug"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_PlainArgv"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_PRISMLib"):
    pass

if merge_base("apache_RiscOS_Sources_Lib_remotedb"):
# merge("remotedb-0_02", "remotedb-0_01-1_1_2_5")
    pass

if merge_base("apache_RiscOS_Sources_Lib_RISC_OSLib"):
# merge("RISC_OSLib-5_06", "RISC_OSLib-4_97-4_12_2_8")
# merge("RISC_OSLib-5_34", "RISC_OSLib-5_33-4_50_2_1")
    pass

if merge_base("apache_RiscOS_Sources_Lib_Unicode"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_AUN_AUNMsgs"):
    merge("AUNMsgs-0_10", "Spin_merge", 1)

if merge_base("apache_RiscOS_Sources_Networking_AUN_BootNet"):
    merge("BootNet-0_90", "Ursula_13May1998_merge")

if merge_base("apache_RiscOS_Sources_Networking_AUN_Net"):
    merge("Net-6_18", "Ursula_13May1998_merge", 1)

if merge_base("apache_RiscOS_Sources_Networking_NetStatus"):
    merge("NetStatus-2_08", "Ursula_13May1998_merge", 2)

if merge_base("apache_RiscOS_Sources_Networking_NetTime"):
    merge("NetTime-0_04", "Spin_merge")

if merge_base("apache_RiscOS_Sources_Networking_NetUtils2"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_Omni_Apps_Omni"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_Omni_Protocols_Access"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_Omni_Protocols_LanManFS"):
# merge("LanManFS-2_00", "LanManFS-1_87-1_1_1_1_2_13")
    pass

if merge_base("apache_RiscOS_Sources_Networking_Omni_Protocols_NetFiler"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_Omni_Protocols_OmniNFS"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_Resolver"):
    pass

if merge_base("apache_RiscOS_Sources_Networking_URI"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_FontPrint"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_Manager"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_Modules_MakePSFont"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_Modules_PDModules"):
# merge("PDModules-4_45", "PDModules-4_44-4_1_2_7")
    pass

if merge_base("apache_RiscOS_Sources_Printing_Modules_PDriver"):
    merge("PDriver-3_34", "PDriver-3_33-4_7_2_1")
    merge("Ursula_31Mar1998", "Spin_merge_28May97")

if merge_base("apache_RiscOS_Sources_Printing_Modules_PDumperSpt"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_Modules_PMonitor"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_Modules_RemPrnSpt"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_PDumpers"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_PPrimer"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_PrintDefs"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_PrintEdit"):
    pass

if merge_base("apache_RiscOS_Sources_Printing_T1ToFont"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_ArmBE"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_BASIC"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_BASICTrans"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_BootCmds"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_DADebug"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_DDEUtils"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_DDT"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_DebugButtn"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_Debugger"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_DebugTools"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_FrontEnd"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_HdrSrc"):
    merge("HdrSrc-0_63", "HdrSrc-0_57-4_58_2_9")
    merge("HdrSrc-1_62-4_162_2_3", "HdrSrc-1_65")
    merge("HdrSrc-1_62-4_162_2_4", "HdrSrc-1_67")
    merge("HdrSrc-1_62-4_162_2_7", "HdrSrc-1_68")
    merge("HdrSrc-1_62-4_162_2_14", "HdrSrc-1_74")
    merge("HdrSrc-1_62-4_162_2_15", "HdrSrc-1_75")
    merge("HdrSrc-1_76", "HdrSrc-1_62-4_162_2_15")

if merge_base("apache_RiscOS_Sources_Programmer_HeapUtils"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_HostFS"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_KeyWatch"):
# merge("KeyWatch-0_09", "KeyWatch-0_08-1_1_2_10")
    pass

if merge_base("apache_RiscOS_Sources_Programmer_MemInfo"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_MsgQueue"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_Obey"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_RMVersion"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_RTSupport"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_ShrinkWrap"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_Squash"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_SysLoad"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_TrapError"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_WatchAbort"):
    pass

if merge_base("apache_RiscOS_Sources_Programmer_WatchUserSWIs"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Boot"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_Installer"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_Main"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_Boot"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_Bootxxxx"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_DiscSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_FilrSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_FontSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_HelpSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_KbdSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_LockSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_MousSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_PinSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_ScrnSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_SndSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_SndSetupVIDC"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_ThemeSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_TimeSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_WindSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Configure2_PlugIns_xxxxMerge"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Fonts"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_HeroNames"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_InetSetup"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_LoadWimp"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Patch"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Public"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_ResApp"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_RPiFiles"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Scrap"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_System"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_Unicode"):
    pass

if merge_base("apache_RiscOS_Sources_SystemRes_UserGuide"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_ColourDbox"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_ColourMenu"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Common"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_DCS"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Docs"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_FileDbox"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_FileInfo"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_FontDbox"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_FontMenu"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Gadgets"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_IconBar"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Libs"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Menu"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_PrintDbox"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_ProgInfo"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_ResDisplay"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_SaveAs"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Scale"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_TinyStubs"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_ToolAction"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Toolbox"):
    pass

if merge_base("apache_RiscOS_Sources_Toolbox_Window"):
    pass

if merge_base("apache_RiscOS_Sources_Utilities_Allocate"):
    pass

if merge_base("apache_RiscOS_Sources_Utilities_HForm"):
    pass

if merge_base("apache_RiscOS_Sources_Utilities_Patches_BorderUtils"):
    pass

if merge_base("apache_RiscOS_Sources_Utilities_Patches_CallASWI"):
    pass

if merge_base("apache_RiscOS_Sources_Utilities_Patches_Patch"):
    pass

if merge_base("apache_RiscOS_Sources_Utilities_ShowScrap"):
    pass

if merge_base("apache_RiscOS_Sources_Video_HWSupport_IMXVideo"):
    pass

if merge_base("apache_RiscOS_Sources_Video_HWSupport_VIDC20Video"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Colours"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Draw"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_DrawFile"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Fonts_ITable"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Fonts_Manager"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Fonts_ROMFonts"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Hourglass"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Hourglass2"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_ScrBlank"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_ScreenFX"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_SpriteUtil"):
    pass

if merge_base("apache_RiscOS_Sources_Video_Render_Super"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_Display"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_GameModes2"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_Picker"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrModes"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSaver"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_AcornLogo"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_Circles"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_Pogo"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_ScrBounce"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_Scrolling"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_Slider"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_Smear"):
    pass

if merge_base("apache_RiscOS_Sources_Video_UserI_ScrSavers_Swarm"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_destroy"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_diff"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_FileCRC"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_find"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_LibUtils"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_modsqz"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_rompress"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_ROMUnjoin"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_squeeze"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_stripdepnd"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_TarExtend"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_toansi"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_ToGPA"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_tokenise"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_topcc"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_Translate"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_UNIX_chmod"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_UNIX_mkdir"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_unmodsqz"):
    pass

if merge_base("apache_RiscOS_Tools_Sources_xpand"):
    pass

if merge_base("apache_RiscOS_Utilities_Autobuild_ABRelease"):
    pass

if merge_base("apache_RiscOS_Utilities_CVSUtils_EraseCVS"):
    pass

if merge_base("apache_RiscOS_Utilities_Debugging_SoftLoad"):
    pass

if merge_base("apache_RiscOS_Utilities_Release_bigsplit2"):
    pass

if merge_base("apache_RiscOS_Utilities_Release_builder"):
    pass

if merge_base("apache_RiscOS_Utilities_Release_crc32"):
    pass

if merge_base("apache_RiscOS_Utilities_Release_romlinker"):
    pass

if merge_base("apache_RiscOS_Utilities_Release_srcbuild"):
# merge("srcbuild-0_25", "srcbuild-0_24-1_23_2_4")
    pass

if merge_base("apache_RiscOS_Utilities_WinEdit"):
    pass

if merge_base("cddl_RiscOS_Sources_FileSys_ADFS_ADFS"):
    pass

if merge_base("cddl_RiscOS_Sources_FileSys_SDFS_SDFS"):
    pass

if merge_base("cddl_RiscOS_Sources_HAL_Titanium"):
    pass

if merge_base("cddl_RiscOS_Sources_HWSupport_ATA_SATADriver"):
    pass

if merge_base("cddl_RiscOS_Sources_HWSupport_SD_SDCMOS"):
    pass

if merge_base("cddl_RiscOS_Sources_HWSupport_SD_SDIODriver"):
    pass

if merge_base("cddl_RiscOS_Sources_ThirdParty_Endurance_Lib_DThreads"):
    pass

if merge_base("gpl_RiscOS_Apps_!GCC"):
    pass

if merge_base("gpl_RiscOS_Apps_!gcc2_95_4"):
    pass

if merge_base("gpl_RiscOS_Apps_!Perl"):
    pass

if merge_base("gpl_RiscOS_Sources_ThirdParty_JSmith_Lib_DDTLib"):
    pass

if merge_base("gpl_RiscOS_Sources_ThirdParty_JSmith_Lib_Trace"):
    pass

if merge_base("gpl_RiscOS_Sources_ThirdParty_JSmith_Lib_Wild"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_bison"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_defmod"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_diff"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_flex"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_gawk"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_grep"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_ident"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_libgnu"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_libgnu4"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_readelf"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_sed"):
    pass

if merge_base("gpl_RiscOS_Tools_Sources_GNU_textutils"):
    pass

if merge_base("gpl_RiscOS_Utilities_Perl"):
    pass

if merge_base("mixed_RiscOS_Apps_!SharedLibs"):
    pass

if merge_base("mixed_RiscOS_Library"):
    pass

if merge_base("mixed_RiscOS_Modules"):
    pass

if merge_base("mixed_RiscOS_Sources_Apps_ChangeFSI"):
    pass

if merge_base("mixed_RiscOS_Sources_HAL_BCM2835"):
    pass

if merge_base("mixed_RiscOS_Sources_HAL_iMx6"):
    pass

if merge_base("mixed_RiscOS_Sources_HAL_OMAP5"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_BCMSupport"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_FPASC"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_SCSI_SCSISoftUSB"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_Controllers_DWCDriver"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_Controllers_EHCIDriver"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_Controllers_MUSBDriver"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_Controllers_OHCIDriver"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_Controllers_XHCIDriver"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_NetBSD"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_USB_USBDriver"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_VCHIQ"):
    pass

if merge_base("mixed_RiscOS_Sources_HWSupport_VFPSupport"):
    pass

if merge_base("mixed_RiscOS_Sources_Lib_ImageLib"):
    pass

if merge_base("mixed_RiscOS_Sources_Lib_JSLib"):
    pass

if merge_base("mixed_RiscOS_Sources_Lib_NSPRLib"):
    pass

if merge_base("mixed_RiscOS_Sources_Lib_TCPIPLibs"):
    pass

if merge_base("mixed_RiscOS_Sources_Lib_zlib"):
    pass

if merge_base("mixed_RiscOS_Sources_Networking_AUN_Internet"):
    pass

if merge_base("mixed_RiscOS_Sources_Networking_AUN_RouteD"):
    pass

if merge_base("mixed_RiscOS_Sources_Networking_Ethernet_EtherK"):
    pass

if merge_base("mixed_RiscOS_Sources_Networking_Ethernet_EtherTH"):
    pass

if merge_base("mixed_RiscOS_Sources_Networking_NFS"):
    pass

if merge_base("mixed_RiscOS_Sources_Programmer_Squash"):
    pass

if merge_base("mixed_RiscOS_Sources_SystemRes_Internet"):
    pass

if merge_base("mixed_RiscOS_Sources_ThirdParty_Desk_Lib_Desk"):
    pass

if merge_base("mixed_RiscOS_Sources_ThirdParty_DPilling_Apps_SparkFS"):
    pass

if merge_base("mixed_RiscOS_Sources_ThirdParty_OSLib_Lib_OSLib"):
    pass

if merge_base("mixed_RiscOS_Sources_ThirdParty_SHarrison_Audio_QTheMusic"):
    pass

if merge_base("mixed_RiscOS_Sources_Utilities_Connector"):
    pass

if merge_base("mixed_RiscOS_Sources_Video_HWSupport_BCMVideo"):
    pass

if merge_base("mixed_RiscOS_Sources_Video_HWSupport_NVidia"):
    pass

if merge_base("mixed_RiscOS_Sources_Video_Render_JCompMod"):
    pass

if merge_base("mixed_RiscOS_Sources_Video_Render_SprExtend"):
    pass

if merge_base("Prepare"):
    pass


# merge("sbrodie_TextGadgets_merged_19Jun98", "sbrodie_Spin_merge_18Jun98")


# Now rewrite the repository
for key, value in refs.items():
    value.repo.create_reference(key, rewrite(value), force=True)

# Now the late addtions that use replace refs.

# Write replace refs and parent lists
for c in commits.values():
    if c.replaced:
        repo.create_commit(
            "refs/replace/" + str(c.oid),
            c.author,
            c.committer,
            c.message,
            c.tree_id,
            [x.oid for x in c.parents])


class Tree(dict):

    def __init__(self):
        self.oid = None

    def __missing__(self, key):
        t = Tree()
        self[key] = t
        self.oid = None
        return t

    def getObject(self, repo):
        if self.oid is None:
            tb = repo.TreeBuilder()
            for name, blob in self.items():
                oid, attr = blob.getObject(repo)
                tb.insert(name, oid, attr)
            self.oid = tb.write()
        return self.oid, pygit2.GIT_FILEMODE_TREE

    def pathAdd(self, path, node):
        path = path.split("/")
        path.reverse()
        while len(path) > 1:
            self.oid = None
            self = self[path.pop()]
        self.oid = None
        self[path[0]] = node


class Blob:

    def __init__(self, oid, attr):
        self.oid = oid
        self.attr = attr

    def getObject(self, repo):
        return self.oid, self.attr


def process_tree(products, name, subtree_add):

    def find_commit_in_branch(c):
        c.child = None
        while c > current:
            n = c.parents[0]
            n.child = c
            c = n
        if c.child is not None:
            heapq.heappush(heap, (c.child, path, tag))
        return c

    heap = []
    for commit, path in products:
        while len(commit.parents) > 0:
            commit = commit.parents[0]
        heapq.heappush(heap, (commit, "Products_" + path, "master"))

    c2 = None
    while len(heap) > 0:

        current, current_path, tag = heap[0]
        print(
            datetime.datetime.utcfromtimestamp(
                current.committer.time).strftime(
                    '%Y-%m-%d %H:%M:%S'))

        if not current_path.startswith("Products_"):
            # print("Y", current, current.child, current_path)
            heapq.heappop(heap)
            if current.child is not None:
                heapq.heappush(heap, (current.child, current_path, tag))
            subtree_add(tree, current_path, tag, current)
        else:
            # print("X")
            heap = []
            tree = Tree()
            mods = set()
            for branch, path in products:
                path = "Products_" + path
                tag = "master"
                commit = find_commit_in_branch(branch)
                subtree_add(tree, path, "master", commit)

                blob_id = commit.repo[commit.tree_id]["modules"].id
                text = commit.repo[blob_id].read_raw().decode('cp437')
                for i in parse_modules.finditer(text):
                    path = i.group(1)
                    tag = i.group(2)
                    if tag == "TRUNK" or tag == "HEAD":
                        tag = "master"
                    path = path.replace(".", "/")
                    mods.add((path, tag))

            for path, tag in mods:
                rpath = path.replace("/", "_")
                commit = refs.get("refs/tags/" + rpath + "_" + tag)
                if commit is None:
                    commit = refs.get("refs/heads/" + rpath + "_" + tag)
                    if commit is None:
                        continue
                    commit = find_commit_in_branch(commit)
                subtree_add(tree, path, tag, commit)

        c2 = branch.repo.create_commit(
            None,
            current.author,
            current.committer,
            current_path + ": " + current.message,
            tree.getObject(branch.repo)[0],
            [] if c2 is None else [c2])
    products[0][0].repo.create_reference(
        "refs/heads/" + name + "_master",
        c2,
     force=True)


def subtree_add(tree, path, tag, commit):
    tree.pathAdd(path, Blob(commit.tree_id, pygit2.GIT_FILEMODE_TREE))


def submodule_add(tree, path, tag, commit):
    tree.pathAdd(path, Blob(commit.oid, pygit2.GIT_FILEMODE_COMMIT))

parse_modules = re.compile(r"^[\t ]*([^#]\S*)[\t ]*(\S*)[\t ]*$", re.MULTILINE)
products = [
    "IOMDHALDev",
    "BCM2835Dev",
    "OMAP3Dev",
    "OMAP4Dev",
    "OMAP5Dev",
    "TitaniumDev",
    "TungstenDev",
    "iMx6Dev"
]

for x in products:
    x = (refs["refs/heads/Products_" + x + "_master"], x)
    process_tree([x], x[1], subtree_add)
    process_tree([x], x[1] + "_submodules", submodule_add)
