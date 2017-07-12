file(REMOVE_RECURSE
  "cscope.files"
  "cscope.in.out"
  "cscope.out"
  "cscope.po.out"
  "CMakeFiles/handler_file.dir/file_example.c.o"
  "handler_file.pdb"
  "handler_file.so"
)

# Per-language clean rules from dependency scanning.
foreach(lang C)
  include(CMakeFiles/handler_file.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
