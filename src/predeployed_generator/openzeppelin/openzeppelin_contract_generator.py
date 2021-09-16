'''
Creates ContractGenerator based on hardhat artifact file from `artifacts` folder

classes:
    OpenzeppelinContractGenerator
'''

import os

from ..contract_generator import ContractGenerator

class OpenzeppelinContractGenerator(ContractGenerator):
    '''Creates contract generator based on hardhat artifact file from `artifacts` folder'''
    ARTIFACT_FILENAME = None

    def __init__(self):
        if OpenzeppelinContractGenerator.ARTIFACT_FILENAME is None:
            raise TypeError('ARTIFACT_FILENAME is not overloaded in the class')
        artifacts_dir = os.path.join(os.path.dirname(__file__), 'artifacts')
        artifacts_path = os.path.join(artifacts_dir, self.ARTIFACT_FILENAME)
        contract = ContractGenerator.from_hardhat_artifact(artifacts_path)
        super().__init__(bytecode=contract.bytecode)
