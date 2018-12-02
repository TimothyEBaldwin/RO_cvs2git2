# RISC OS CVS to GIT converter

Converts a local copy of the the [RISC OS Open CVS repository](https://www.riscosopen.org/content/downloads/risc-os-tarballs) to [Git](https://git-scm.com/).

## Requirements

* GNU/Linux
* Bubblewrap
* Git
* Libgit2
* Python 2
* Python 3
* pyGit2

It should be fairly simple to modify to run on other Unix systems, by removing the use of Bubblewrap in `RO_cvs2git`. It does not run on RISC OS.

## How to Use

First place a copy of the RISC OS CVS in the directory `cvsroot` next to this README file. Then to run  whole conversion process run `RO_cvs2git`. To just create the superproject run `RO_cvs2git_phase2`

The directory `submodules` will contain a git repository for every component in the CVS, as listed in `components.txt`.

The directory `super` will be a git repository which is superproject fot the submodules with a branch for Product in the CVS repository.

## Todo

 - [ ] Add git remotes to the published locations.
 - [ ] Add some more comments describing the operation.
 - [ ] Add test case for CVS keywords in BASIC program.
 - [ ] Add the merge of the `NRaine` branch in `apache/RiscOS/Sources/Video/Render/Fonts/Manager`?
 - [ ] Add the merge of the `Pi3APlus` branch in `mixed/RiscOS/Sources/HAL/BCM2835`.
 - [ ] Apply tags to output branches in superproject.
 - [ ] Check for missing components.
 - [ ] Convert CVS usernames to names (and email addresses if wished).
 - [ ] Convert `PlingSystem` product.
 - [ ] Eliminate `InstallTools`?
 - [ ] Eliminate `Prepare` by moving submodules to the required location.
 - [ ] Fix character set conversion of commit messages.
 - [ ] Fix handling of `InetSetup`.
 - [ ] Handle broken Batch1to6Dev modules file, which refers to a few directories of componments instead of the componments themselves, `apache/RiscOS/Sources/SystemRes/Configure2`, `mixed/RiscOS/Sources/HWSupport/USB`, `apache/RiscOS/Sources/HWSupport/CD`.
 - [ ] In superproject refer to submodules their published location.
 - [ ] Make binary submodules shallow.
 - [ ] Remove master branch if it is an exact copy another branch.
 - [ ] Remove trailing spaces from C, C++ and assmebler files.
 - [ ] Untag, redate, or otherwise clean clean recommits in `mixed/RiscOS/Sources/HWSupport/FPASC`.

 - [x] Add .gitmodules file to submodules branches.
 - [x] Add the remaining products files.
 - [x] Check remaining components for merges and missing tags.
 - [x] Check the history of the Customer M Demo branch in the kernel.
 - [x] Join up the 2 parts of `VFPSupport`.
 - [x] PrintDefs-0.42 is a branch.
 - [x] Replace log message "/home/srevill-nfs/sandbox/rool/msg.txt" with something meaningful.
 - [x] Understand the history of the CVS default branch.

 - [ ] Check against CVS checkout.
 - [ ] Check against development tar archives.
 - [ ] Check against stable source tar archives.
 - [ ] Try building some or all of the history.
 - [ ] Declare the conversion stable.

## Redactions

For copyright and/or confidentiality reasons there are many redaction is the RISC OS Open CVS:

The early versions of the are following componments incomplete and unbuildable:

* `apache/RiscOS/Sources/Apps/Browse`
* `apache/RiscOS/Sources/Lib/CLXLite`
* `apache/RiscOS/Sources/Lib/PRISMLib`
* `apache/RiscOS/Sources/Programmer/HdrSrc`
* `mixed/RiscOS/Sources/HWSupport/FPASC`

The following componment have minor redactiosn in history and have a (slightly) fictuious pre-redaction history in the hope early versions are buildable:

* `apache/RiscOS/Sources/HAL/Tungsten`
* `apache/RiscOS/Sources/Kernel`
* `apache/RiscOS/Sources/Lib/RISC_OSLib`
* `apache/RiscOS/Sources/Networking/URI`
* `mixed/RiscOS/Sources/Networking/NFS`

 ## After Conversion Suggestions

 * Make superprojects mergeable - allows easier testing of changes in different builds
 * Merge superprojects
 * Move per Env/ROOL/* and Buildsys/components/ROOL out of the submodules and into the relvant superproject.
