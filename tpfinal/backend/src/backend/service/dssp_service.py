from Bio.PDB import PDBList
from Bio.PDB.DSSP import DSSP
from Bio.PDB import PDBParser
from src.backend.constants.constants import *
import os

cwd = os.getcwd()
PDB_PATH = os.path.join(cwd, 'pdb')


class DSSPService:

    def get_alignment_from(self, sequences, chains):
        return [{'dssp': self._get_alignment(sequence, chains), 'sequence': sequence} for sequence in sequences]

    def _get_alignment(self, sequence, expected_chains):
        pdbcode = sequence.get('pdbcode').lower()
        self._generate_pdb(pdbcode)
        secondary_structure, data_structure = self._run(pdbcode, sequence.get('chains'))
        return {'alignment': self._align(secondary_structure, sequence.get('sequence')), 'chain': data_structure}

    def _align(self, secondary_structure, alignmed_primary_structure):

        for index in range(len(alignmed_primary_structure)):
            if alignmed_primary_structure[index] == '-':
                secondary_structure.insert(index, (1, '-', '_'))

        r = ''.join([st[2] if not st[2] == '-' else '0' for st in secondary_structure])
        return r

    def _generate_pdb(self, pdbcode):
        pdbl = PDBList()
        pdbl.retrieve_pdb_file(pdbcode, pdir=PDB_PATH, file_format='pdb', overwrite=True)

    def _run(self, pdbcode, chains):
        pdb_file = os.path.join(PDB_PATH, 'pdb' + pdbcode + '.ent')
        p = PDBParser()
        structure = p.get_structure(pdbcode, pdb_file)
        model = structure[0]
        dssp = DSSP(model, pdb_file, dssp=dssp_route)
        valid_keys = [key for key in dssp.keys() if key[0] in chains]
        chain = dssp.keys()[0][0]

        return [dssp[key] for key in valid_keys], chain
