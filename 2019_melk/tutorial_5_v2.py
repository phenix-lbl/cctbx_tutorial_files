from __future__ import division, print_function
import sys, os
from iotbx import reflection_file_reader
import iotbx.pdb
import mmtbx.model

def run(args):
  if (len(args) != 2):
    raise RuntimeError("Please specify two file names.")
  fn_1 = args[0]
  fn_2 = args[1]
  model_filename, reflection_filename = None, None

  for fn in (fn_1, fn_2):
    if os.path.splitext(fn)[1] == '.mtz' and reflection_filename is None:
      reflection_filename = fn
    elif os.path.splitext(fn)[1] == '.pdb' and model_filename is None:
      model_filename = fn
    else:
      raise RuntimeError("Please specify one model file and one reflection file.")

  print('Model file name: ', model_filename)
  print('Reflection file name: ', reflection_filename)

  pdb_inp = iotbx.pdb.input(file_name=model_filename)
  model = mmtbx.model.manager(model_input = pdb_inp)

  miller_arrays = reflection_file_reader.any_reflection_file(
    file_name = reflection_filename).as_miller_arrays()

  for ma in miller_arrays:
    if (ma.info().label_string()=="FOBS,SIGFOBS"):
      f_obs = ma
    if (ma.info().label_string() in ['R-free-flags','FreeR_flag']):
      r_free = ma

  f_obs, r_free = f_obs.common_sets(r_free)
  r_free_flags = r_free.array(data = r_free.data()==0)

  xray_structure = model.get_xray_structure()

  f_model = mmtbx.f_model.manager(
   f_obs          = f_obs,
   r_free_flags         = r_free_flags,
   xray_structure = xray_structure)
  f_model.update_all_scales()

  print('\nRwork: ', f_model.r_work())
  print('\nRfree:', f_model.r_free())

#  print()

#  for ma in miller_arrays:
#    if (ma.info().label_string()=="FOBS,SIGFOBS"):
#      f_obs = ma

#    if (ma.info().label_string()=='R-free-flags'):
#      r_free_flags = ma
#      print('Size R-free-flags: ', ma.size())

#  print('\nResolution limits: ', f_obs.d_max_min())
#  print('\nSpace group: ', f_obs.space_group_info())
#  print('\nCompleteness: ', f_obs.completeness())
#  print('\nSize: ', f_obs.size())
#  print()
#  f_obs.show_summary()
#  print()
#  match_result = f_obs.match_indices(r_free_flags)
#  print('\nCommon reflections: ', match_result.pairs().size())
#  print('\nSingle reflections in FOBS,SIGFOBS: ', match_result.singles(0).size())
#  print('\nSingle reflections in R-free-flags: ', match_result.singles(1).size())
#  #print(r_free_flags.match_indices(f_obs).singles)
#  #print(help(match_result.singles))
#  print(dir(match_result.singles(0)))

#  print()

#  f_obs, r_free_flags = f_obs.common_sets(r_free_flags)
#  print(f_obs.size(), r_free_flags.size())


if (__name__ == "__main__"):
  run(sys.argv[1:])

