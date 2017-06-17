
## Differences from code in article Linux/Documentation/target/tcmu-design.txt

* All code in one file

* We need to include some libraries to make it work:

      for codes O_RDONLY and etc 
      `#include <fcntl.h>`

      for stroull 
      `#include <stdlib.h>`

      for io 
      `#include <stdio.h>`

      for open, read, etc 
      `#include <unistd.h>`

      for strncmp 
      `#include <string.h>`

      for bool 
      `#include <stdbool.h>`

      for mmap 
      `#include <sys/mman.h>`

      trivial 
      `#include <linux/target_core_user.h>`

      for uint32_t 
      `#include <stdint.h>`

* Need to define codes for SCSI (such as NO_SENSE)

* Some variable declarations lost in article
*i.e.: unsigned int ret*

* We must check file-opening error
*i.e.: if (fd == -1)*

* Type cast (__u32) added for tcmu_hdr_get_len function call


## Compilation and execution


* Compiled with gcc and clang in terminal
* Compiled with JetBrains Clion

* Compilation: gcc -o tcmu_example -c tcmu_example.c

* See uio creation in scripts folder of rep


## Problem

With uio0 program pauses trying to read from dev_fd in while cycle.
Maybe it happens because we don't get any info from uio (nothing to read) or it's busy
