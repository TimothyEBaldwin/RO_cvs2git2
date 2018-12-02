#!/bin/bash

set -xe -o pipefail

bwrap=(bwrap --unsetenv TMPDIR --cap-drop ALL --die-with-parent --unshare-all --proc /proc --dev /dev --dir /tmp)

for i in /etc/alternatives /usr /bin /sbin /lib*
do
  if [[ -L $i ]]; then
    bwrap+=(--symlink "$(readlink "$i")" "$i")
  else
    bwrap+=(--ro-bind "$i" "$i")
  fi
done

exec "${bwrap[@]}" "$@"
