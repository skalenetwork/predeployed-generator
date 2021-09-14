import os
from web3 import Web3

from ..contract_generator import ContractGenerator


class TransparentUpgradeableProxyGenerator(ContractGenerator):
    ARTIFACT_FILENAME = 'TransparentUpgradeableProxy.json'
    ROLLBACK_SLOT = int.from_bytes(Web3.solidityKeccak(['string'], ['eip1967.proxy.rollback']), byteorder='big') - 1
    IMPLEMENTATION_SLOT = int.from_bytes(Web3.solidityKeccak(['string'], ['eip1967.proxy.implementation']), byteorder='big') - 1
    ADMIN_SLOT = int.from_bytes(Web3.solidityKeccak(['string'], ['eip1967.proxy.admin']), byteorder='big') - 1

    def __init__(self, implementation_address: str, admin_address: str, initial_storage: dict):
        artifacts_dir = os.path.join(os.path.dirname(__file__), 'artifacts')
        artifacts_path = os.path.join(artifacts_dir, self.ARTIFACT_FILENAME)
        contract = ContractGenerator.from_hardhat_artifact(artifacts_path)
        super().__init__(bytecode=contract.bytecode)
        self._setup(implementation_address, admin_address)
        self.storage = {**initial_storage, **self.storage}

    # private

    def _setup(self, implementation_address: str, admin_address: str) -> None:
        self._write_address(self.IMPLEMENTATION_SLOT, implementation_address)
        self._write_address(self.ADMIN_SLOT, admin_address)