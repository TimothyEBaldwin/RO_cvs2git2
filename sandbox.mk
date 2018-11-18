#!/usr/bin/make -f
#
# Copyright (c) 2018, Timothy Baldwin
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
#

.DELETE_ON_ERROR:

lib_depends := $(wildcard /etc/alternatives /etc/ld.so.* Support/*.mk)

seccomp: gen_seccomp
	./gen_seccomp $* > $@

gen_seccomp: gen_seccomp.c $(lib_depends)
	gcc -std=c99 -Wall -Os gen_seccomp.c -o gen_seccomp -lseccomp
