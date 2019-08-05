from __future__ import division, print_function
import sys, os
from iotbx import reflection_file_reader

def run(args):
  if (len(args) != 2):
    raise RuntimeError("Please specify two file names.")
  fn_1 = args[0]
  fn_2 = args[1]
  model_file_name, reflection_file_name = None, None

  for fn in (fn_1, fn_2):
    if os.path.splitext(fn)[1] == '.mtz' and reflection_file_name is None:
      reflection_file_name = fn
    elif os.path.splitext(fn)[1] == '.pdb' and model_file_name is None:
      model_file_name = fn
    else:
      raise RuntimeError("Please specify one model file and one reflection file.")

  print('Model file name: ', model_file_name)
  print('Reflection file name: ', reflection_file_name)

if (__name__ == "__main__"):
  run(sys.argv[1:])

