'''transparent_upgradeable_proxy_generator.py

Module for generation of transparent upgradeable proxy

classes:
    TransparentUpgradeableProxyGenerator
'''

import os
from web3.auto import w3

from ..contract_generator import ContractGenerator


class TransparentUpgradeableProxyGenerator(ContractGenerator):
    '''Generates transparent upgradeable proxy
    '''
    ARTIFACT_FILENAME = 'TransparentUpgradeableProxy.json'
    ROLLBACK_SLOT = int.from_bytes(
        w3.solidityKeccak(['string'], ['eip1967.proxy.rollback']),
        byteorder='big') - 1
    IMPLEMENTATION_SLOT = int.from_bytes(
        w3.solidityKeccak(['string'], ['eip1967.proxy.implementation']),
        byteorder='big') - 1
    ADMIN_SLOT = int.from_bytes(
        w3.solidityKeccak(['string'], ['eip1967.proxy.admin']),
        byteorder='big') - 1

    def __init__(self):
        artifacts_dir = os.path.join(os.path.dirname(__file__), 'artifacts')
        artifacts_path = os.path.join(artifacts_dir, self.ARTIFACT_FILENAME)
        contract = ContractGenerator.from_hardhat_artifact(artifacts_path)
        super().__init__(bytecode=contract.bytecode)

    @staticmethod
    def generate_storage(**kwargs) -> dict:
        implementation_address = kwargs['implementation_address']
        admin_address = kwargs['admin_address']
        initial_storage = kwargs.get('initial_storage', None)
        storage = {}
        ContractGenerator._write_address(
            storage,
            TransparentUpgradeableProxyGenerator.IMPLEMENTATION_SLOT,
            implementation_address)
        ContractGenerator._write_address(
            storage,
            TransparentUpgradeableProxyGenerator.ADMIN_SLOT,
            admin_address)
        if initial_storage is not None:
            storage.update(initial_storage)
        return storage
