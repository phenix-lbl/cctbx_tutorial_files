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
    if (ma.info().label_string()=='R-free-flags'):
      r_free_flags = ma


if (__name__ == "__main__"):
  run(sys.argv[1:])

