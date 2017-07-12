# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/denis/Desktop/lio_project/tcmu-runner

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/denis/Desktop/lio_project/tcmu-runner

# Include any dependencies generated for this target.
include CMakeFiles/tcmu.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/tcmu.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/tcmu.dir/flags.make

tcmuhandler-generated.c: tcmu-handler.xml
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating tcmuhandler-generated.c, tcmuhandler-generated.h"
	gdbus-codegen /home/denis/Desktop/lio_project/tcmu-runner/tcmu-handler.xml --generate-c-code /home/denis/Desktop/lio_project/tcmu-runner/tcmuhandler-generated --c-generate-object-manager --interface-prefix org.kernel

tcmuhandler-generated.h: tcmuhandler-generated.c
	@$(CMAKE_COMMAND) -E touch_nocreate tcmuhandler-generated.h

CMakeFiles/tcmu.dir/configfs.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/configfs.c.o: configfs.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/tcmu.dir/configfs.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/configfs.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/configfs.c

CMakeFiles/tcmu.dir/configfs.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/configfs.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/configfs.c > CMakeFiles/tcmu.dir/configfs.c.i

CMakeFiles/tcmu.dir/configfs.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/configfs.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/configfs.c -o CMakeFiles/tcmu.dir/configfs.c.s

CMakeFiles/tcmu.dir/configfs.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/configfs.c.o.requires

CMakeFiles/tcmu.dir/configfs.c.o.provides: CMakeFiles/tcmu.dir/configfs.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/configfs.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/configfs.c.o.provides

CMakeFiles/tcmu.dir/configfs.c.o.provides.build: CMakeFiles/tcmu.dir/configfs.c.o


CMakeFiles/tcmu.dir/api.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/api.c.o: api.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/tcmu.dir/api.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/api.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/api.c

CMakeFiles/tcmu.dir/api.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/api.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/api.c > CMakeFiles/tcmu.dir/api.c.i

CMakeFiles/tcmu.dir/api.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/api.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/api.c -o CMakeFiles/tcmu.dir/api.c.s

CMakeFiles/tcmu.dir/api.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/api.c.o.requires

CMakeFiles/tcmu.dir/api.c.o.provides: CMakeFiles/tcmu.dir/api.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/api.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/api.c.o.provides

CMakeFiles/tcmu.dir/api.c.o.provides.build: CMakeFiles/tcmu.dir/api.c.o


CMakeFiles/tcmu.dir/libtcmu.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/libtcmu.c.o: libtcmu.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/tcmu.dir/libtcmu.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/libtcmu.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/libtcmu.c

CMakeFiles/tcmu.dir/libtcmu.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/libtcmu.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/libtcmu.c > CMakeFiles/tcmu.dir/libtcmu.c.i

CMakeFiles/tcmu.dir/libtcmu.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/libtcmu.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/libtcmu.c -o CMakeFiles/tcmu.dir/libtcmu.c.s

CMakeFiles/tcmu.dir/libtcmu.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/libtcmu.c.o.requires

CMakeFiles/tcmu.dir/libtcmu.c.o.provides: CMakeFiles/tcmu.dir/libtcmu.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/libtcmu.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/libtcmu.c.o.provides

CMakeFiles/tcmu.dir/libtcmu.c.o.provides.build: CMakeFiles/tcmu.dir/libtcmu.c.o


CMakeFiles/tcmu.dir/libtcmu-register.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/libtcmu-register.c.o: libtcmu-register.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/tcmu.dir/libtcmu-register.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/libtcmu-register.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/libtcmu-register.c

CMakeFiles/tcmu.dir/libtcmu-register.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/libtcmu-register.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/libtcmu-register.c > CMakeFiles/tcmu.dir/libtcmu-register.c.i

CMakeFiles/tcmu.dir/libtcmu-register.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/libtcmu-register.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/libtcmu-register.c -o CMakeFiles/tcmu.dir/libtcmu-register.c.s

CMakeFiles/tcmu.dir/libtcmu-register.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/libtcmu-register.c.o.requires

CMakeFiles/tcmu.dir/libtcmu-register.c.o.provides: CMakeFiles/tcmu.dir/libtcmu-register.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/libtcmu-register.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/libtcmu-register.c.o.provides

CMakeFiles/tcmu.dir/libtcmu-register.c.o.provides.build: CMakeFiles/tcmu.dir/libtcmu-register.c.o


CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o: tcmuhandler-generated.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/tcmuhandler-generated.c

CMakeFiles/tcmu.dir/tcmuhandler-generated.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/tcmuhandler-generated.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/tcmuhandler-generated.c > CMakeFiles/tcmu.dir/tcmuhandler-generated.c.i

CMakeFiles/tcmu.dir/tcmuhandler-generated.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/tcmuhandler-generated.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/tcmuhandler-generated.c -o CMakeFiles/tcmu.dir/tcmuhandler-generated.c.s

CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.requires

CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.provides: CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.provides

CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.provides.build: CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o


CMakeFiles/tcmu.dir/libtcmu_log.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/libtcmu_log.c.o: libtcmu_log.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object CMakeFiles/tcmu.dir/libtcmu_log.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/libtcmu_log.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_log.c

CMakeFiles/tcmu.dir/libtcmu_log.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/libtcmu_log.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_log.c > CMakeFiles/tcmu.dir/libtcmu_log.c.i

CMakeFiles/tcmu.dir/libtcmu_log.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/libtcmu_log.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_log.c -o CMakeFiles/tcmu.dir/libtcmu_log.c.s

CMakeFiles/tcmu.dir/libtcmu_log.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/libtcmu_log.c.o.requires

CMakeFiles/tcmu.dir/libtcmu_log.c.o.provides: CMakeFiles/tcmu.dir/libtcmu_log.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/libtcmu_log.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/libtcmu_log.c.o.provides

CMakeFiles/tcmu.dir/libtcmu_log.c.o.provides.build: CMakeFiles/tcmu.dir/libtcmu_log.c.o


CMakeFiles/tcmu.dir/libtcmu_config.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/libtcmu_config.c.o: libtcmu_config.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object CMakeFiles/tcmu.dir/libtcmu_config.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/libtcmu_config.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_config.c

CMakeFiles/tcmu.dir/libtcmu_config.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/libtcmu_config.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_config.c > CMakeFiles/tcmu.dir/libtcmu_config.c.i

CMakeFiles/tcmu.dir/libtcmu_config.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/libtcmu_config.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_config.c -o CMakeFiles/tcmu.dir/libtcmu_config.c.s

CMakeFiles/tcmu.dir/libtcmu_config.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/libtcmu_config.c.o.requires

CMakeFiles/tcmu.dir/libtcmu_config.c.o.provides: CMakeFiles/tcmu.dir/libtcmu_config.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/libtcmu_config.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/libtcmu_config.c.o.provides

CMakeFiles/tcmu.dir/libtcmu_config.c.o.provides.build: CMakeFiles/tcmu.dir/libtcmu_config.c.o


CMakeFiles/tcmu.dir/libtcmu_time.c.o: CMakeFiles/tcmu.dir/flags.make
CMakeFiles/tcmu.dir/libtcmu_time.c.o: libtcmu_time.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building C object CMakeFiles/tcmu.dir/libtcmu_time.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu.dir/libtcmu_time.c.o   -c /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_time.c

CMakeFiles/tcmu.dir/libtcmu_time.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu.dir/libtcmu_time.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_time.c > CMakeFiles/tcmu.dir/libtcmu_time.c.i

CMakeFiles/tcmu.dir/libtcmu_time.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu.dir/libtcmu_time.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/Desktop/lio_project/tcmu-runner/libtcmu_time.c -o CMakeFiles/tcmu.dir/libtcmu_time.c.s

CMakeFiles/tcmu.dir/libtcmu_time.c.o.requires:

.PHONY : CMakeFiles/tcmu.dir/libtcmu_time.c.o.requires

CMakeFiles/tcmu.dir/libtcmu_time.c.o.provides: CMakeFiles/tcmu.dir/libtcmu_time.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu.dir/build.make CMakeFiles/tcmu.dir/libtcmu_time.c.o.provides.build
.PHONY : CMakeFiles/tcmu.dir/libtcmu_time.c.o.provides

CMakeFiles/tcmu.dir/libtcmu_time.c.o.provides.build: CMakeFiles/tcmu.dir/libtcmu_time.c.o


# Object files for target tcmu
tcmu_OBJECTS = \
"CMakeFiles/tcmu.dir/configfs.c.o" \
"CMakeFiles/tcmu.dir/api.c.o" \
"CMakeFiles/tcmu.dir/libtcmu.c.o" \
"CMakeFiles/tcmu.dir/libtcmu-register.c.o" \
"CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o" \
"CMakeFiles/tcmu.dir/libtcmu_log.c.o" \
"CMakeFiles/tcmu.dir/libtcmu_config.c.o" \
"CMakeFiles/tcmu.dir/libtcmu_time.c.o"

# External object files for target tcmu
tcmu_EXTERNAL_OBJECTS =

libtcmu.so.1: CMakeFiles/tcmu.dir/configfs.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/api.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu-register.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu_log.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu_config.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu_time.c.o
libtcmu.so.1: CMakeFiles/tcmu.dir/build.make
libtcmu.so.1: /lib/x86_64-linux-gnu/libnl-3.so
libtcmu.so.1: /lib/x86_64-linux-gnu/libnl-genl-3.so
libtcmu.so.1: CMakeFiles/tcmu.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Linking C shared library libtcmu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tcmu.dir/link.txt --verbose=$(VERBOSE)
	$(CMAKE_COMMAND) -E cmake_symlink_library libtcmu.so.1 libtcmu.so.1 libtcmu.so

libtcmu.so: libtcmu.so.1
	@$(CMAKE_COMMAND) -E touch_nocreate libtcmu.so

# Rule to build all files generated by this target.
CMakeFiles/tcmu.dir/build: libtcmu.so

.PHONY : CMakeFiles/tcmu.dir/build

# Object files for target tcmu
tcmu_OBJECTS = \
"CMakeFiles/tcmu.dir/configfs.c.o" \
"CMakeFiles/tcmu.dir/api.c.o" \
"CMakeFiles/tcmu.dir/libtcmu.c.o" \
"CMakeFiles/tcmu.dir/libtcmu-register.c.o" \
"CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o" \
"CMakeFiles/tcmu.dir/libtcmu_log.c.o" \
"CMakeFiles/tcmu.dir/libtcmu_config.c.o" \
"CMakeFiles/tcmu.dir/libtcmu_time.c.o"

# External object files for target tcmu
tcmu_EXTERNAL_OBJECTS =

CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/configfs.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/api.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu-register.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu_log.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu_config.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/libtcmu_time.c.o
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/build.make
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: /lib/x86_64-linux-gnu/libnl-3.so
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: /lib/x86_64-linux-gnu/libnl-genl-3.so
CMakeFiles/CMakeRelink.dir/libtcmu.so.1: CMakeFiles/tcmu.dir/relink.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Linking C shared library CMakeFiles/CMakeRelink.dir/libtcmu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tcmu.dir/relink.txt --verbose=$(VERBOSE)
	$(CMAKE_COMMAND) -E cmake_symlink_library CMakeFiles/CMakeRelink.dir/libtcmu.so.1 CMakeFiles/CMakeRelink.dir/libtcmu.so.1 CMakeFiles/CMakeRelink.dir/libtcmu.so

CMakeFiles/CMakeRelink.dir/libtcmu.so: CMakeFiles/CMakeRelink.dir/libtcmu.so.1
	@$(CMAKE_COMMAND) -E touch_nocreate CMakeFiles/CMakeRelink.dir/libtcmu.so

# Rule to relink during preinstall.
CMakeFiles/tcmu.dir/preinstall: CMakeFiles/CMakeRelink.dir/libtcmu.so

.PHONY : CMakeFiles/tcmu.dir/preinstall

CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/configfs.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/api.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/libtcmu.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/libtcmu-register.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/tcmuhandler-generated.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/libtcmu_log.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/libtcmu_config.c.o.requires
CMakeFiles/tcmu.dir/requires: CMakeFiles/tcmu.dir/libtcmu_time.c.o.requires

.PHONY : CMakeFiles/tcmu.dir/requires

CMakeFiles/tcmu.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/tcmu.dir/cmake_clean.cmake
.PHONY : CMakeFiles/tcmu.dir/clean

CMakeFiles/tcmu.dir/depend: tcmuhandler-generated.c
CMakeFiles/tcmu.dir/depend: tcmuhandler-generated.h
	cd /home/denis/Desktop/lio_project/tcmu-runner && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/denis/Desktop/lio_project/tcmu-runner /home/denis/Desktop/lio_project/tcmu-runner /home/denis/Desktop/lio_project/tcmu-runner /home/denis/Desktop/lio_project/tcmu-runner /home/denis/Desktop/lio_project/tcmu-runner/CMakeFiles/tcmu.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/tcmu.dir/depend

