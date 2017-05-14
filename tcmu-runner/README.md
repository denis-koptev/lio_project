# tcmu-runner

## Installation

Tested with Ubuntu 16.04 LTS

### Downloading sources

Sources are in this folder, but if you want to download it manually, you can clone it from git

Install git 
`> sudo apt-get install git`

Clone repo 
`> git clone https://github.com/open-iscsi/tcmu-runner.git`

### Dependencies installation

* `> sudo apt-get install cmake`
* `> sudo apt-get install libnl-3-dev`
* `> sudo apt-get install libglib2.0-dev`
* `> sudo apt-get install libpthread-*`
* `> sudo apt-get install libdlib-dev`
* `> sudo apt-get install libkmod-dev`
* `> sudo apt-get install glusterfs-*` (instead of libgfapi)
* `> sudo apt-get install librbd-dev`
* `> sudo apt-get install zlib*`

### Building sources

`> cd tcmu-runner`
`> cmake .`

You can have errors like this:

*Please set them or make sure they are set and tested correctly in the CMake files:*
*LIBNL_GENL_LIB*
*linked by target "tcmu" in directory /root/tcmu-runner*

It means, that you have to install one more lib: 
`> sudo apt-get install libnl-genl-3-dev`

Finishing build 
`> make`

### Launching

`> sudo ./tcmu-runner`



