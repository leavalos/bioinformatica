# coding=utf-8
from flask import Flask, request
from flask_cors import CORS, cross_origin


from src.backend.environment_strategies.environment_strategy import LinuxClustalRunner, WindowsClustalRunner
from src.backend.service.clustal_service import ClustalService
from src.backend.service.blast_service import BlastService
from src.backend.service.dssp_service import DSSPService
from src.backend.service.pdb_service import PDBService
from src.backend.service.align_service import AlignService
import json


app = Flask(__name__)
CORS(app, suppport_credentials=True)

#clustal_runner = LinuxClustalRunner()
clustal_runner = WindowsClustalRunner()

pdb_service = PDBService()
blast_service = BlastService()
clustal_service = ClustalService(clustal_runner)
dssp_service = DSSPService()
align_service = AlignService()


@app.route('/sequences', methods=['POST'])
@cross_origin(support_credentials=True)
def getSequences():
    pdb_code = request.json['pdbcode']

    result = pdb_service.get_sequence_from(pdb_code)

    return json.dumps(result)


@app.route('/homologousSequence', methods=['POST'])
@cross_origin(support_credentials=True)
def homologous_sequences():
    pdb_code = request.json['pdbcode']

    result = blast_service.blast_records_just_sequences(pdb_code)

    return json.dumps(result)


@app.route('/analyze', methods=['POST'])
@cross_origin(support_credentials=True)
def analyze():
    sequence = request.json['sequence']
    coverage = int(request.json['coverage'])
    evalue = float(request.json['evalue'])
    sequences = blast_service.blast_records(sequence, expected_coverage=coverage, evalue=evalue)

    primary_structure = clustal_service.get_alignment_from(sequences)
    chains = sequence.split('|')[1].replace('Chains', '').replace('Chain', '')
    result = dssp_service.get_alignment_from(primary_structure, chains)

    return json.dumps(result)


@app.route('/alignStructures', methods=['POST'])
@cross_origin(support_credentials=True)
def align_structures():
    mobile = request.json['mobile']
    mobile_protein = mobile["name"]
    mobile_chain = mobile["chain"]

    references = request.json['reference']

    references = [(pdb.split(",")[0].lower(), pdb.split(",")[1]) for pdb in references]

    result = align_service.get_alignments(mobile_protein.lower(), mobile_chain,
                                         references)

    return json.dumps(result)


if __name__ == '__main__':
    app.run()
