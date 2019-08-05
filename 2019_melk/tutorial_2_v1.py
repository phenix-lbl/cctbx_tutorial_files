from __future__ import division, print_function
import sys
import mmtbx.model
import iotbx.pdb

def run(args):
  if (len(args) != 1):
    raise RuntimeError("Please specify one pdb file name.")
  model_filename = args[0]
  pdb_inp = iotbx.pdb.input(file_name=model_filename)
  model = mmtbx.model.manager(model_input = pdb_inp)
  model.composition().show(log=sys.stdout)

  pdb_hierarchy = model.get_hierarchy()

  print('\nLoop over hierarchy:')
  for model in pdb_hierarchy.models():
    for chain in model.chains():
      print('Chain: ', chain.id)
      for rg in chain.residue_groups():
        print('  Resnumber: ', rg.resid())
        for ag in rg.atom_groups():
          print('    Resname: %s, Altloc: %s' % (ag.resname, ag.altloc))
          for atom in ag.atoms():
            print('      %s' % atom.name)

if (__name__ == "__main__"):
  run(sys.argv[1:])
