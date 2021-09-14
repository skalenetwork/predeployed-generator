import json
import os

from .test_predeployed import TestPredeployed

class TestOpenzeppelin(TestPredeployed):
    def get_abi(self, contract: str) -> list:
        with open(os.path.join(
            os.path.dirname(__file__),
            '../../src/predeployed_generator/openzeppelin/artifacts/',
            f'{contract}.json')) as f:
            data = json.load(f)
            return data['abi']