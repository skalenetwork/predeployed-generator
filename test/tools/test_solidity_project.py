import json
import os

from .test_predeployed import TestPredeployed

class TestSolidityProject(TestPredeployed):
    def get_abi(self, contract: str) -> list:
        with open(os.path.join(
            os.path.dirname(__file__),
            f'../test_solidity_project/artifacts/contracts/{contract}.sol/',
            f'{contract}.json')) as f:
            data = json.load(f)
            return data['abi']