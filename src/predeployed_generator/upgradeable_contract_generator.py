'''upgradeable_contract_generator.py

The module is used to generate predeployed smart contracts in genesis block
that is upgradeable using EIP-1967 tranparent upgradeable proxy

Classes:
    UpgradeableContractGenerator
'''

# from .openzeppelin.transparent_upgradeable_proxy_generator \
#     import TransparentUpgradeableProxyGenerator
# from .contract_generator import ContractGenerator


# class UpgradeableContractGenerator(TransparentUpgradeableProxyGenerator):
#     '''Generates transparent upgradeable proxy based on implementation generator'''
#     def __init__(
#             self,
#             implementation_address: str,
#             proxy_admin_address,
#             implementation_generator: ContractGenerator):
#         super().__init__(
#             implementation_address,
#             proxy_admin_address,
#             implementation_generator.generate()['storage'])
