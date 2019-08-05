from __future__ import division, print_function
import sys
from iotbx import reflection_file_reader

def run(args):
  if (len(args) != 1):
    raise RuntimeError("Please specify one reflection file name.")
  reflection_file_name = args[0]
  miller_arrays = reflection_file_reader.any_reflection_file(
    file_name = reflection_file_name).as_miller_arrays()

if (__name__ == "__main__"):
  run(sys.argv[1:])
