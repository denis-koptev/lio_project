file(REMOVE_RECURSE
  "cscope.files"
  "cscope.in.out"
  "cscope.out"
  "cscope.po.out"
  "CMakeFiles/cscope"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/cscope.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
