# RISC OS CVS to GIT converter

Converts a local copy of the the [RISC OS Open CVS repository](https://www.riscosopen.org/content/downloads/risc-os-tarballs) to [Git](https://git-scm.com/).

The RISC OS Open CVS repository requires [many fixes](https://github.com/TimothyEBaldwin/RO_cvsroot/commits/fixes) which are inculded as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

## Requirements

* GNU/Linux
* Bubblewrap
* C Compiler
* CVS
* Git
* Libgit2
* Libseccomp
* Make
* Python 2
* Python 3
* pyGit2

On Debian derived distributions `sudo sysctl kernel.unprivileged_userns_clone=1` may be required as nested Bubblewrap sandboxes are used.

It should be fairly simple to modify to run on other Unix systems, by removing the use of Bubblewrap. It does not run on RISC OS.

## How to Use

First download the submodules:

```
git submodule init
git submodule update
```

Then run it:

```
./RO_cvs2git
```

The output will be in the directory `git` (any existing repository will be deleted), and you can browse it like:

```
gitk --date-order --branches='apache_RiscOS_Sources_Kernel_*'
```
```
gitk --date-order IOMDHALDev_master
```
```
gitk --date-order unified_master
```

Please be advised that future versions of this converter will produce different commit ids, it will be like rebasing.

### Split mode

Split mode produces on Git repository for each CVS component.

```
split=1 ./RO_cvs2git
```

## Todo

 - [x] Understand the history of the CVS default branch.
 - [x] Provide a merged branch combining the history of all the development product files. This will use symbolic links in the Products directories to point to the right branch.
 - [ ] Add .gitmodules file to submodules branches.
 - [ ] Replace log message "/home/srevill-nfs/sandbox/rool/msg.txt" with something meaningful.
 - [x] Join up the 2 parts of `VFPSupport`.
 - [ ] Fix handling of `InetSetup`.
 - [ ] Convert CVS usernames to names (and email addresses if wished).
 - [ ] Try building some or all of the history.
 - [ ] Declare the conversion stable.
 - [x] Check the history of the Customer M Demo branch in the kernel.
 - [ ] Check remaining components for merges and missing tags.
 - [ ] Add the remaining products files.
