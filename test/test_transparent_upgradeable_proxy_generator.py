from web3.auto import w3

from .tools.test_openzeppelin import TestOpenzeppelin
from src.predeployed_generator.openzeppelin.proxy_admin_generator import ProxyAdminGenerator
from src.predeployed_generator.openzeppelin.transparent_upgradeable_proxy import TransparentUpgradeableProxyGenerator

class TestTransparentUpgradeableProxyGenerator(TestOpenzeppelin):
    OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
    PROXY_ADMIN_ADDRESS = '0xd200000000000000000000000000000000000001'
    PROXY_ADDRESS = '0xD200000000000000000000000000000000000002'
    IMPLEMENTATION_ADDRESS = '0xd200000000000000000000000000000000000003'


    def get_transparent_upgradeable_proxy_abi(self) -> list:
        return self.get_abi('TransparentUpgradeableProxy')


    def get_proxy_admin_abi(self) -> list:
        return self.get_abi('ProxyAdmin')

    # tests

    def test_admin(self, tmpdir):        
        proxy_admin_generator = ProxyAdminGenerator(self.OWNER_ADDRESS)
        proxy_generator = TransparentUpgradeableProxyGenerator(
            self.IMPLEMENTATION_ADDRESS,
            self.PROXY_ADMIN_ADDRESS,
            proxy_admin_generator.generate()['storage'])

        genesis = self.generate_genesis({
            self.PROXY_ADMIN_ADDRESS: proxy_admin_generator.generate(),
            self.PROXY_ADDRESS: proxy_generator.generate(),
            self.IMPLEMENTATION_ADDRESS: proxy_admin_generator.generate()
        })

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()
            
            proxy_admin = w3.eth.contract(address=self.PROXY_ADMIN_ADDRESS, abi=self.get_proxy_admin_abi())
            assert proxy_admin.functions.getProxyAdmin(self.PROXY_ADDRESS).call() == self.PROXY_ADMIN_ADDRESS
