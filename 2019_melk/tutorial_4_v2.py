from __future__ import division, print_function
import sys
from iotbx import reflection_file_reader

def run(args):
  if (len(args) != 1):
    raise RuntimeError("Please specify one reflection file name.")
  reflection_file_name = args[0]
  miller_arrays = reflection_file_reader.any_reflection_file(
    file_name = reflection_file_name).as_miller_arrays()

  for ma in miller_arrays:
    print(ma.info().label_string(), ma.size())

  print()

  for ma in miller_arrays:
    if (ma.info().label_string()=="FOBS,SIGFOBS"):
      f_obs = ma

    if (ma.info().label_string()=='R-free-flags'):
      r_free = ma
      print('Size R-free array: ', ma.size())

  print('\nResolution limits: ', f_obs.d_max_min())
  print('\nSpace group: ', f_obs.space_group_info())
  print('\nCompleteness: ', f_obs.completeness())
  print('\nSize: ', f_obs.size())
  print()
  f_obs.show_summary()
  print()
  match_result = f_obs.match_indices(r_free)
  print('\nCommon reflections: ', match_result.pairs().size())
  print('\nSingle reflections in FOBS,SIGFOBS: ', match_result.singles(0).size())
  print('\nSingle reflections in R-free-flags: ', match_result.singles(1).size())
  print()
  f_obs, r_free = f_obs.common_sets(r_free)
  print('\nAfter using common_sets:')
  print('Size FOBS,SIGFOBS: ', f_obs.size())
  print('Size R-free-flags: ', r_free.size())

  #print(help(match_result.singles))
  #print(dir(match_result.singles(0)))

if (__name__ == "__main__"):
  run(sys.argv[1:])

