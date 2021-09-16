import os

from ..contract_generator import ContractGenerator


class ProxyAdminGenerator(ContractGenerator):
    ARTIFACT_FILENAME = 'ProxyAdmin.json'

    OWNER_SLOT = 0

    # ---------- storage ----------
    # -----------Context-----------
    # -----------Ownable-----------
    # 0:    _owner
    # ---------ProxyAdmin----------

    def __init__(self):
        artifacts_dir = os.path.join(os.path.dirname(__file__), 'artifacts')
        artifacts_path = os.path.join(artifacts_dir, self.ARTIFACT_FILENAME)
        contract = ContractGenerator.from_hardhat_artifact(artifacts_path)
        super().__init__(bytecode=contract.bytecode)

    @staticmethod
    def generate_storage(**kwargs) -> dict:
        owner_address = kwargs['owner_address']
        storage = {}
        ContractGenerator._write_address(
            storage,
            ProxyAdminGenerator.OWNER_SLOT,
            owner_address)
        return storage
