import glob
import os
import sys
import re
#import mmap

if len(sys.argv) != 2:
	print("USAGE: # python tracer.py +headers [or -headers, if working only with .c files]")
	sys.exit()

c_path = os.getcwd() + '/*.c'
#print(c_path)

c_files = glob.glob(c_path)

print(c_files)

for c_file in c_files:
	fd = open(c_file, 'r+')
	fd_content = fd.read()
	#fd_content = mmap.mmap(fd.fileno(), 0)

	fd_content = re.sub(r"([a-zA-Z0-9_*:-]+[ \s*]+[a-zA-Z0-9_*-]+[ \s]*\([ \sa-zA-Z0-9_*&,:-]*\))[ \s]*{", 
		r'\1\n{\n\tprintf("%s : %s \\n",__func__,__FILE__);\n', 
		fd_content, re.DOTALL | re.VERBOSE | re.MULTILINE)

	fd.seek(0)
	fd.write(fd_content)
	fd.truncate()
	#print(fd_content)

if sys.argv[1] == '+headers':
	h_path = os.getcwd() + '/*.h'
	h_files = glob.glob(h_path)
	print(h_files)
	for h_file in h_files:
		fd = open(h_file, 'r+')
		fd_content = fd.read()

		fd_content = re.sub(r"([a-zA-Z0-9_*:-]+[ \s*]+[a-zA-Z0-9_*-]+[ \s]*\([ \sa-zA-Z0-9_*&,:-]+\))[ \s]*{", 
			r'\1\n{\n\tprintf("%s : %s \\n",__func__,__FILE__);\n', 
			fd_content, re.DOTALL | re.VERBOSE | re.MULTILINE)
		
		fd.seek(0)
		fd.write(fd_content)
		fd.truncate()