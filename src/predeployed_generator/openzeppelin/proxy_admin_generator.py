import os

from ..contract_generator import ContractGenerator


class ProxyAdminGenerator(ContractGenerator):
    ARTIFACT_FILENAME = 'ProxyAdmin.json'

    # ---------- storage ----------
    # -----------Context-----------
    # -----------Ownable-----------
    # 0:    _owner
    # ---------ProxyAdmin----------

    def __init__(self, owner_address: str):
        artifacts_dir = os.path.join(os.path.dirname(__file__), 'artifacts')
        artifacts_path = os.path.join(artifacts_dir, self.ARTIFACT_FILENAME)
        contract = ContractGenerator.from_hardhat_artifact(artifacts_path)
        super().__init__(bytecode=contract.bytecode)
        self._setup(owner_address)

    # private

    def _setup(self, owner_address: str) -> None:
        self._write_address(0, owner_address)
