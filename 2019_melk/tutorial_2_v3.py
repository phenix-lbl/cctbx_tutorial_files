from __future__ import division, print_function
import sys
import mmtbx.model
import iotbx.pdb
import iotbx.pdb.amino_acid_codes

aa_resnames = iotbx.pdb.amino_acid_codes.one_letter_given_three_letter
ala_atom_names = set([" N  ", " CA ", " C  ", " O  ", " CB "])

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
          if (ag.resname in aa_resnames):
            print('    Resname: %s, Altloc: %s' % (ag.resname, ag.altloc))
            for atom in ag.atoms():
              if (atom.name not in ala_atom_names):
                print('      %s' % atom.name)
                ag.remove_atom(atom=atom)

  #print(help(pdb_hierarchy.write_pdb_file))
  pdb_hierarchy.write_pdb_file(file_name = 'polyala.pdb')

if (__name__ == "__main__"):
  run(sys.argv[1:])
