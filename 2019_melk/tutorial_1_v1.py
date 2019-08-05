from __future__ import division, print_function
import sys
import mmtbx.model
import iotbx.pdb

def run(args):
  if (len(args) != 1):
    raise RuntimeError("Please specify one model file name.")
  model_filename = args[0]
  pdb_inp = iotbx.pdb.input(file_name = model_filename)
  model = mmtbx.model.manager(model_input = pdb_inp)

  composition_obj = model.composition()
  #print(help(composition_obj))

  model.composition().show(log = sys.stdout)

if (__name__ == "__main__"):
  run(sys.argv[1:])
