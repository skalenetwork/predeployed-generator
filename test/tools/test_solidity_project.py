import json
from os.path import join, dirname, normpath
from subprocess import run

from .test_predeployed import TestPredeployed

class TestSolidityProject(TestPredeployed):
    def get_abi(self, contract: str) -> list:
        with open(self.get_artifacts_path(contract)) as f:
            data = json.load(f)
            return data['abi']

    @staticmethod
    def get_artifacts_dir():
        return normpath(join(dirname(__file__), '../test_solidity_project/artifacts/'))

    def get_artifacts_path(self, contract: str) -> str:
        return join(self.get_artifacts_dir(),
                    f'contracts/{contract}.sol/',
                    f'{contract}.json')
