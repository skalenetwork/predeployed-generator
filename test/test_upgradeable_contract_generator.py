import pytest
from web3.auto import w3

from .tools.test_openzeppelin import TestOpenzeppelin
from src.predeployed_generator.openzeppelin.proxy_admin_generator import ProxyAdminGenerator
from src.predeployed_generator.openzeppelin.transparent_upgradeable_proxy_generator import TransparentUpgradeableProxyGenerator
from src.predeployed_generator.upgradeable_contract_generator import UpgradeableContractGenerator

class TestTransparentUpgradeableProxyGenerator(TestOpenzeppelin):
    OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
    PROXY_ADMIN_ADDRESS = '0xd200000000000000000000000000000000000001'
    PROXY_ADDRESS = '0xD200000000000000000000000000000000000002'
    IMPLEMENTATION_ADDRESS = '0xd200000000000000000000000000000000000003'


    def get_transparent_upgradeable_proxy_abi(self) -> list:
        return self.get_abi('TransparentUpgradeableProxy')

    def get_proxy_admin_abi(self) -> list:
        return self.get_abi('ProxyAdmin')

    def prepare_genesis(self):
        proxy_admin_generator = ProxyAdminGenerator()
        upgradeable_contract_generator = UpgradeableContractGenerator(proxy_admin_generator)

        return self.generate_genesis({
            self.PROXY_ADMIN_ADDRESS: proxy_admin_generator.generate(owner_address=self.OWNER_ADDRESS),
            **upgradeable_contract_generator.generate_allocation(
                contract_address=self.PROXY_ADDRESS,
                implementation_address=self.IMPLEMENTATION_ADDRESS,
                proxy_admin_address=self.PROXY_ADMIN_ADDRESS,
                owner_address=self.OWNER_ADDRESS
            )
        })

    # tests

    def test_admin(self, tmpdir):        
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()
            
            proxy_admin = w3.eth.contract(address=self.PROXY_ADMIN_ADDRESS, abi=self.get_proxy_admin_abi())
            assert proxy_admin.functions.getProxyAdmin(self.PROXY_ADDRESS).call() == self.PROXY_ADMIN_ADDRESS

    def test_implementation(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()
            
            proxy_admin = w3.eth.contract(address=self.PROXY_ADMIN_ADDRESS, abi=self.get_proxy_admin_abi())
            assert proxy_admin.functions.getProxyImplementation(self.PROXY_ADDRESS).call() == self.IMPLEMENTATION_ADDRESS
    
    def test_owner(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()
            
            proxy_admin = w3.eth.contract(address=self.PROXY_ADDRESS, abi=self.get_proxy_admin_abi())
            assert proxy_admin.functions.owner().call() == self.OWNER_ADDRESS

    def test_wrong_generation(self):
        with pytest.raises(RuntimeError):
            contract_generator = UpgradeableContractGenerator(ProxyAdminGenerator())
            contract_generator.generate()

