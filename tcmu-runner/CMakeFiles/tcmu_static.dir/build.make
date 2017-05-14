# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

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
CMAKE_SOURCE_DIR = /home/denis/tcmu-runner

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/denis/tcmu-runner

# Include any dependencies generated for this target.
include CMakeFiles/tcmu_static.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/tcmu_static.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/tcmu_static.dir/flags.make

tcmuhandler-generated.c: tcmu-handler.xml
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating tcmuhandler-generated.c, tcmuhandler-generated.h"
	gdbus-codegen /home/denis/tcmu-runner/tcmu-handler.xml --generate-c-code /home/denis/tcmu-runner/tcmuhandler-generated --c-generate-object-manager --interface-prefix org.kernel

tcmuhandler-generated.h: tcmuhandler-generated.c
	@$(CMAKE_COMMAND) -E touch_nocreate tcmuhandler-generated.h

CMakeFiles/tcmu_static.dir/configfs.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/configfs.c.o: configfs.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/tcmu_static.dir/configfs.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/configfs.c.o   -c /home/denis/tcmu-runner/configfs.c

CMakeFiles/tcmu_static.dir/configfs.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/configfs.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/configfs.c > CMakeFiles/tcmu_static.dir/configfs.c.i

CMakeFiles/tcmu_static.dir/configfs.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/configfs.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/configfs.c -o CMakeFiles/tcmu_static.dir/configfs.c.s

CMakeFiles/tcmu_static.dir/configfs.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/configfs.c.o.requires

CMakeFiles/tcmu_static.dir/configfs.c.o.provides: CMakeFiles/tcmu_static.dir/configfs.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/configfs.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/configfs.c.o.provides

CMakeFiles/tcmu_static.dir/configfs.c.o.provides.build: CMakeFiles/tcmu_static.dir/configfs.c.o


CMakeFiles/tcmu_static.dir/api.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/api.c.o: api.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/tcmu_static.dir/api.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/api.c.o   -c /home/denis/tcmu-runner/api.c

CMakeFiles/tcmu_static.dir/api.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/api.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/api.c > CMakeFiles/tcmu_static.dir/api.c.i

CMakeFiles/tcmu_static.dir/api.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/api.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/api.c -o CMakeFiles/tcmu_static.dir/api.c.s

CMakeFiles/tcmu_static.dir/api.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/api.c.o.requires

CMakeFiles/tcmu_static.dir/api.c.o.provides: CMakeFiles/tcmu_static.dir/api.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/api.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/api.c.o.provides

CMakeFiles/tcmu_static.dir/api.c.o.provides.build: CMakeFiles/tcmu_static.dir/api.c.o


CMakeFiles/tcmu_static.dir/libtcmu.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/libtcmu.c.o: libtcmu.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/tcmu_static.dir/libtcmu.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/libtcmu.c.o   -c /home/denis/tcmu-runner/libtcmu.c

CMakeFiles/tcmu_static.dir/libtcmu.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/libtcmu.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/libtcmu.c > CMakeFiles/tcmu_static.dir/libtcmu.c.i

CMakeFiles/tcmu_static.dir/libtcmu.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/libtcmu.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/libtcmu.c -o CMakeFiles/tcmu_static.dir/libtcmu.c.s

CMakeFiles/tcmu_static.dir/libtcmu.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/libtcmu.c.o.requires

CMakeFiles/tcmu_static.dir/libtcmu.c.o.provides: CMakeFiles/tcmu_static.dir/libtcmu.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/libtcmu.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/libtcmu.c.o.provides

CMakeFiles/tcmu_static.dir/libtcmu.c.o.provides.build: CMakeFiles/tcmu_static.dir/libtcmu.c.o


CMakeFiles/tcmu_static.dir/libtcmu-register.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/libtcmu-register.c.o: libtcmu-register.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/tcmu_static.dir/libtcmu-register.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/libtcmu-register.c.o   -c /home/denis/tcmu-runner/libtcmu-register.c

CMakeFiles/tcmu_static.dir/libtcmu-register.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/libtcmu-register.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/libtcmu-register.c > CMakeFiles/tcmu_static.dir/libtcmu-register.c.i

CMakeFiles/tcmu_static.dir/libtcmu-register.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/libtcmu-register.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/libtcmu-register.c -o CMakeFiles/tcmu_static.dir/libtcmu-register.c.s

CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.requires

CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.provides: CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.provides

CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.provides.build: CMakeFiles/tcmu_static.dir/libtcmu-register.c.o


CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o: tcmuhandler-generated.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o   -c /home/denis/tcmu-runner/tcmuhandler-generated.c

CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/tcmuhandler-generated.c > CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.i

CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/tcmuhandler-generated.c -o CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.s

CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.requires

CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.provides: CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.provides

CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.provides.build: CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o


CMakeFiles/tcmu_static.dir/libtcmu_log.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/libtcmu_log.c.o: libtcmu_log.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object CMakeFiles/tcmu_static.dir/libtcmu_log.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/libtcmu_log.c.o   -c /home/denis/tcmu-runner/libtcmu_log.c

CMakeFiles/tcmu_static.dir/libtcmu_log.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/libtcmu_log.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/libtcmu_log.c > CMakeFiles/tcmu_static.dir/libtcmu_log.c.i

CMakeFiles/tcmu_static.dir/libtcmu_log.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/libtcmu_log.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/libtcmu_log.c -o CMakeFiles/tcmu_static.dir/libtcmu_log.c.s

CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.requires

CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.provides: CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.provides

CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.provides.build: CMakeFiles/tcmu_static.dir/libtcmu_log.c.o


CMakeFiles/tcmu_static.dir/libtcmu_config.c.o: CMakeFiles/tcmu_static.dir/flags.make
CMakeFiles/tcmu_static.dir/libtcmu_config.c.o: libtcmu_config.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object CMakeFiles/tcmu_static.dir/libtcmu_config.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tcmu_static.dir/libtcmu_config.c.o   -c /home/denis/tcmu-runner/libtcmu_config.c

CMakeFiles/tcmu_static.dir/libtcmu_config.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tcmu_static.dir/libtcmu_config.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/denis/tcmu-runner/libtcmu_config.c > CMakeFiles/tcmu_static.dir/libtcmu_config.c.i

CMakeFiles/tcmu_static.dir/libtcmu_config.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tcmu_static.dir/libtcmu_config.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/denis/tcmu-runner/libtcmu_config.c -o CMakeFiles/tcmu_static.dir/libtcmu_config.c.s

CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.requires:

.PHONY : CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.requires

CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.provides: CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.requires
	$(MAKE) -f CMakeFiles/tcmu_static.dir/build.make CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.provides.build
.PHONY : CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.provides

CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.provides.build: CMakeFiles/tcmu_static.dir/libtcmu_config.c.o


# Object files for target tcmu_static
tcmu_static_OBJECTS = \
"CMakeFiles/tcmu_static.dir/configfs.c.o" \
"CMakeFiles/tcmu_static.dir/api.c.o" \
"CMakeFiles/tcmu_static.dir/libtcmu.c.o" \
"CMakeFiles/tcmu_static.dir/libtcmu-register.c.o" \
"CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o" \
"CMakeFiles/tcmu_static.dir/libtcmu_log.c.o" \
"CMakeFiles/tcmu_static.dir/libtcmu_config.c.o"

# External object files for target tcmu_static
tcmu_static_EXTERNAL_OBJECTS =

libtcmu_static.a: CMakeFiles/tcmu_static.dir/configfs.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/api.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/libtcmu.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/libtcmu-register.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/libtcmu_log.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/libtcmu_config.c.o
libtcmu_static.a: CMakeFiles/tcmu_static.dir/build.make
libtcmu_static.a: CMakeFiles/tcmu_static.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/denis/tcmu-runner/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Linking C static library libtcmu_static.a"
	$(CMAKE_COMMAND) -P CMakeFiles/tcmu_static.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tcmu_static.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/tcmu_static.dir/build: libtcmu_static.a

.PHONY : CMakeFiles/tcmu_static.dir/build

CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/configfs.c.o.requires
CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/api.c.o.requires
CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/libtcmu.c.o.requires
CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/libtcmu-register.c.o.requires
CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/tcmuhandler-generated.c.o.requires
CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/libtcmu_log.c.o.requires
CMakeFiles/tcmu_static.dir/requires: CMakeFiles/tcmu_static.dir/libtcmu_config.c.o.requires

.PHONY : CMakeFiles/tcmu_static.dir/requires

CMakeFiles/tcmu_static.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/tcmu_static.dir/cmake_clean.cmake
.PHONY : CMakeFiles/tcmu_static.dir/clean

CMakeFiles/tcmu_static.dir/depend: tcmuhandler-generated.c
CMakeFiles/tcmu_static.dir/depend: tcmuhandler-generated.h
	cd /home/denis/tcmu-runner && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/denis/tcmu-runner /home/denis/tcmu-runner /home/denis/tcmu-runner /home/denis/tcmu-runner /home/denis/tcmu-runner/CMakeFiles/tcmu_static.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/tcmu_static.dir/depend

