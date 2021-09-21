from os.path import join, isdir, normpath
from subprocess import run
from typing import Dict

from web3.auto import w3

from src.predeployed_generator.openzeppelin.access_control_enumerable_generator import AccessControlEnumerableGenerator
from .tools.test_solidity_project import TestSolidityProject


class ContractGenerator(AccessControlEnumerableGenerator):
    CONTRACT_NAME = 'TestContract'
    DEFAULT_ADMIN_ROLE = (0).to_bytes(32, 'big')
    TESTER_ROLE = w3.solidityKeccak(['string'], ['TESTER_ROLE'])

    # ---------- storage ----------
    # --------Initializable--------
    # 0:    _initialized, _initializing;
    # -----ContextUpgradeable------
    # 1:    __gap
    # ...   __gap
    # 50:   __gap
    # ------ERC165Upgradeable------
    # 51:   __gap
    # ...   __gap
    # 100:  __gap
    # --AccessControlUpgradeable---
    # 101:  _roles
    # 102:  __gap
    # ...   __gap
    # 150:  __gap
    # AccessControlEnumerableUpgradeable
    # 151:  _roleMembers
    # 152:  __gap
    # ...   __gap
    # 200:  __gap
    # ----------TestContract----------

    INITIALIZED_SLOT = 0
    ROLES_SLOT = 101
    ROLE_MEMBERS_SLOT = 151

    def __init__(self):
        artifacts_dir = TestSolidityProject.get_artifacts_dir()
        if not isdir(artifacts_dir):
            self._build_contracts()
        artifact_path = join(artifacts_dir, 'contracts', f'{self.CONTRACT_NAME}.sol', f'{self.CONTRACT_NAME}.json')
        contract = self.from_hardhat_artifact(artifact_path)
        super().__init__(bytecode=contract.bytecode)

    @classmethod
    def generate_storage(cls, **kwargs) -> Dict[str, str]:
        default_admin_address = kwargs['default_admin']
        tester_addresses = kwargs['testers']
        storage: Dict[str, str] = {}
        cls._write_uint256(storage, ContractGenerator.INITIALIZED_SLOT, 1)
        rolesSlots = cls.RolesSlots(roles=cls.ROLES_SLOT, role_members=cls.ROLE_MEMBERS_SLOT)
        cls._setup_role(storage, rolesSlots, cls.DEFAULT_ADMIN_ROLE, [default_admin_address])
        cls._setup_role(storage, rolesSlots, cls.TESTER_ROLE, tester_addresses)
        return storage

    # private

    def _build_contracts(self):
        process = run(['yarn', 'install'], capture_output=True, cwd=normpath(join(TestSolidityProject.get_artifacts_dir(), '..')))
        assert process.returncode == 0


class TestAccessControlEnumerableGenerator(TestSolidityProject):
    OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
    TESTER_ADDRESS = '0xd200000000000000000000000000000000000001'
    TESTER2_ADDRESS = '0xD200000000000000000000000000000000000002'
    CONTRACT_ADDRESS = '0xd200000000000000000000000000000000000003'

    def get_test_contract_abi(self):
        return self.get_abi(ContractGenerator.CONTRACT_NAME)

    def prepare_genesis(self):
        test_contract_generator = ContractGenerator()

        return self.generate_genesis(test_contract_generator.generate_allocation(
            self.CONTRACT_ADDRESS,
            default_admin=self.OWNER_ADDRESS,
            testers=[self.TESTER_ADDRESS, self.TESTER2_ADDRESS]))
    
    def test_default_admin_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            test_contract = w3.eth.contract(address=self.CONTRACT_ADDRESS, abi=self.get_test_contract_abi())
            assert test_contract.functions.getRoleMemberCount(ContractGenerator.DEFAULT_ADMIN_ROLE).call() == 1
            assert test_contract.functions.getRoleMember(ContractGenerator.DEFAULT_ADMIN_ROLE, 0).call() == self.OWNER_ADDRESS            
            assert test_contract.functions.hasRole(ContractGenerator.DEFAULT_ADMIN_ROLE, self.OWNER_ADDRESS).call()

    def test_tester_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            test_contract = w3.eth.contract(address=self.CONTRACT_ADDRESS, abi=self.get_test_contract_abi())
            assert test_contract.functions.getRoleMemberCount(ContractGenerator.TESTER_ROLE).call() == 2
            assert test_contract.functions.getRoleMember(ContractGenerator.TESTER_ROLE, 0).call() == self.TESTER_ADDRESS
            assert test_contract.functions.getRoleMember(ContractGenerator.TESTER_ROLE, 1).call() == self.TESTER2_ADDRESS
            assert test_contract.functions.hasRole(ContractGenerator.TESTER_ROLE, self.TESTER_ADDRESS).call()
            assert test_contract.functions.hasRole(ContractGenerator.TESTER_ROLE, self.TESTER2_ADDRESS).call()