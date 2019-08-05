from __future__ import division, print_function
import sys, os
import mmtbx.model
import iotbx.pdb
import iotbx.pdb.amino_acid_codes

aa_resnames = iotbx.pdb.amino_acid_codes.one_letter_given_three_letter
ala_atom_names = set([" N  ", " CA ", " C  ", " O  ", " CB "])

def rg_has_amino_acid(rg):
  for ag in rg.atom_groups():
    if (ag.resname in aa_resnames):
      return True
  return False

def run(args):
  if (len(args) != 1):
    raise RuntimeError("Please specify one pdb file name.")
  model_filename = args[0]
  pdb_inp = iotbx.pdb.input(file_name=model_filename)
  model = mmtbx.model.manager(model_input = pdb_inp)
  model.composition().show(log=sys.stdout)

  pdb_hierarchy = model.get_hierarchy()

  n_amino_acid_residues = 0
  n_other_residues = 0
  n_atoms_removed = 0

  for model in pdb_hierarchy.models():
    for chain in model.chains():
      for rg in chain.residue_groups():
        if rg_has_amino_acid(rg):
          n_amino_acid_residues += 1
          for ag in rg.atom_groups():
            for atom in ag.atoms():
              if (atom.name not in ala_atom_names):
                ag.remove_atom(atom=atom)
                n_atoms_removed += 1
        else:
          n_other_residues += 1

  print("\nNumber of amino acid residues:", n_amino_acid_residues)
  print("Number of other residues:", n_other_residues)
  print("Number of atoms removed:", n_atoms_removed)

  if (n_atoms_removed != 0):
    output_pdb = os.path.splitext(model_filename)[0] + "_truncated_to_ala.pdb"
    print("Writing file: ", output_pdb)
    pdb_hierarchy.write_pdb_file(
      file_name=output_pdb,
      crystal_symmetry=pdb_inp.crystal_symmetry())

if (__name__ == "__main__"):
  run(sys.argv[1:])
