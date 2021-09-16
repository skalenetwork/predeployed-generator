'''upgradeable_contract_generator.py

The module is used to generate predeployed smart contracts in genesis block
that is upgradeable using EIP-1967 tranparent upgradeable proxy

Classes:
    UpgradeableContractGenerator
'''

from .openzeppelin.transparent_upgradeable_proxy_generator \
    import TransparentUpgradeableProxyGenerator
from .contract_generator import ContractGenerator


class UpgradeableContractGenerator(TransparentUpgradeableProxyGenerator):
    '''Generates transparent upgradeable proxy based on implementation generator'''
    def __init__(
            self,
            implementation_generator: ContractGenerator):
        super().__init__()
        self.implementation_generator = implementation_generator

    def generate_storage(self, **kwargs) -> dict:
        proxy_admin_address = kwargs.pop('proxy_admin_address')
        implementation_address = kwargs.pop('implementation_address')
        storage = TransparentUpgradeableProxyGenerator.generate_storage(
            proxy_admin_address=proxy_admin_address,
            implementation_address=implementation_address
        )
        storage.update(self.implementation_generator.generate(**kwargs))
        return storage
