from web3.auto import w3

from .tools.test_openzeppelin import TestOpenzeppelin
from src.predeployed_generator.openzeppelin.proxy_admin_generator import ProxyAdminGenerator

class TestProxyAdminGenerator(TestOpenzeppelin):
    def get_proxy_admin_abi(self) -> list:
        return self.get_abi('ProxyAdmin')


    def test_owner(self, tmpdir):
        owner_address = '0xd200000000000000000000000000000000000000'
        proxy_admin_address = '0xd200000000000000000000000000000000000001'
        generator = ProxyAdminGenerator(owner_address)
        with self.run_geth(tmpdir, self.generate_genesis({proxy_admin_address: generator.generate()})):
            assert w3.isConnected()
            
            proxy_admin = w3.eth.contract(address=proxy_admin_address, abi=self.get_proxy_admin_abi())
            assert proxy_admin.functions.owner().call() == owner_address