import json
from os.path import join, isdir, normpath
from subprocess import run
from typing import Dict
from web3.auto import w3

from src.predeployed_generator.openzeppelin.access_control_enumerable_generator import AccessControlEnumerableGenerator
from .test_solidity_project import TestSolidityProject

class CustomContractGenerator(AccessControlEnumerableGenerator):
    CONTRACT_NAME = 'TestContract'
    DEFAULT_ADMIN_ROLE = (0).to_bytes(32, 'big')
    TESTER_ROLE = w3.solidity_keccak(['string'], ['TESTER_ROLE'])

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
    # 201:  shortString
    # 202:  longString
    # 203:  bytes32Value
    # 204:  testers

    INITIALIZED_SLOT = 0
    ROLES_SLOT = 101
    ROLE_MEMBERS_SLOT = 151
    SHORT_STRING_SLOT = 201
    LONG_STRING_SLOT = AccessControlEnumerableGenerator.next_slot(SHORT_STRING_SLOT)
    BYTES32_VALUE_SLOT = AccessControlEnumerableGenerator.next_slot(LONG_STRING_SLOT)
    TESTERS_SLOT = AccessControlEnumerableGenerator.next_slot(BYTES32_VALUE_SLOT)

    def __init__(self):
        artifacts_dir = TestSolidityProject.get_artifacts_dir()
        if not isdir(artifacts_dir):
            self._build_contracts()
        artifact_path = join(artifacts_dir, 'contracts', f'{self.CONTRACT_NAME}.sol', f'{self.CONTRACT_NAME}.json')
        meta_path = self._get_meta_path()
        contract = self.from_hardhat_artifact(artifact_path, meta_path)
        super().__init__(bytecode=contract.bytecode, abi=contract.abi, meta=contract.meta)

    @classmethod
    def generate_storage(cls, **kwargs) -> Dict[str, str]:
        default_admin_address = kwargs['default_admin']
        tester_addresses = kwargs['testers']
        storage: Dict[str, str] = {}
        cls._write_uint256(storage, CustomContractGenerator.INITIALIZED_SLOT, 1)
        rolesSlots = cls.RolesSlots(roles=cls.ROLES_SLOT, role_members=cls.ROLE_MEMBERS_SLOT)
        cls._setup_role(storage, rolesSlots, cls.DEFAULT_ADMIN_ROLE, [default_admin_address])
        cls._setup_role(storage, rolesSlots, cls.TESTER_ROLE, tester_addresses)
        cls._write_string(storage, cls.SHORT_STRING_SLOT, "short string")
        cls._write_string(storage, cls.LONG_STRING_SLOT, ' '.join(['very'] * 32) + ' long string')
        cls._write_bytes32(storage, cls.BYTES32_VALUE_SLOT, cls.TESTER_ROLE)
        cls._write_addresses_array(storage, cls.TESTERS_SLOT, tester_addresses)
        return storage

    # private

    def _build_contracts(self):
        process = run(['yarn', 'install'], capture_output=True, cwd=normpath(join(TestSolidityProject.get_artifacts_dir(), '..')))
        assert process.returncode == 0

    def _get_meta_path(self):
        artifacts_dir = TestSolidityProject.get_artifacts_dir()
        dbg_path = join(artifacts_dir, 'contracts', f'{self.CONTRACT_NAME}.sol', f'{self.CONTRACT_NAME}.dbg.json')
        with open(dbg_path) as dbg_file:
            dbg_info = json.loads(dbg_file.read())
            build_info_path = dbg_info['buildInfo']
        return join(artifacts_dir, 'contracts', f'{self.CONTRACT_NAME}.sol', build_info_path)
