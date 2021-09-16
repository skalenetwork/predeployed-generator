'''proxy_admin_generator.py

Module for generation of proxy admin

classes:
    ProxyAdminGenerator
'''

from .openzeppelin_contract_generator import OpenzeppelinContractGenerator


class ProxyAdminGenerator(OpenzeppelinContractGenerator):
    '''Generates ProxyAdmin
    '''

    ARTIFACT_FILENAME = 'ProxyAdmin.json'

    OWNER_SLOT = 0

    # ---------- storage ----------
    # -----------Context-----------
    # -----------Ownable-----------
    # 0:    _owner
    # ---------ProxyAdmin----------

    @staticmethod
    def generate_storage(**kwargs) -> dict:
        owner_address = kwargs['owner_address']
        storage = {}
        ProxyAdminGenerator._write_address(
            storage,
            ProxyAdminGenerator.OWNER_SLOT,
            owner_address)
        return storage

    def get_artifact_filename(self):
        return self.ARTIFACT_FILENAME
