/*
 * Copyright (c) 2018 Timothy Baldwin
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define _POSIX_C_SOURCE 2
#include <errno.h>
#include <error.h>
#include <stdbool.h>
#include <sys/ioctl.h>
#include <sys/prctl.h>
#include <unistd.h>

#include <seccomp.h>

static scmp_filter_ctx ctx;

static void ban(int syscall, const char* message) {
  int rc = seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(syscall), 0);
  if (rc) error(1, -rc, message);
}

#define BAN(s) ban(SCMP_SYS(s), "Unable to create " #s " rule")

int main(int argc, char **argv) {

  int rc;

  ctx = seccomp_init(SCMP_ACT_ALLOW);
  if (!ctx) error(1, errno, "Unable to create libseccomp context");

  // Don't allow inserting into terminal input buffer
  rc = seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(ioctl), 1, SCMP_A1(SCMP_CMP_EQ, TIOCSTI));
  if (rc) error(1, -rc, "Unable to create rule to block inserting into terminal input buffer");

  BAN(ptrace);
  BAN(keyctl);
  BAN(request_key);
  BAN(add_key);

  rc = seccomp_export_bpf(ctx, STDOUT_FILENO);
  if (rc) error(1, -rc, "Unable to load seccomp rules");

  return 0;
}
