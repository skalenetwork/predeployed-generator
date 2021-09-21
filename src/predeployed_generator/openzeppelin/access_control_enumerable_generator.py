'''access_control_enumerable_generator.py

Module for generation of contracts that are AccessControlEnumerable

classes:
    AccessControlEnumerableGenerator
'''

from typing import List

from ..contract_generator import ContractGenerator

class AccessControlEnumerableGenerator(ContractGenerator):
    '''Generates AccessControlEnumerable
    '''

    # private

    @classmethod
    def _setup_role(
            cls,
            storage: dict,
            roles_slot: int,
            role_members_slot: int,
            role: bytes,
            accounts: List[str]
            ) -> None:
        role_data_slot = cls.calculate_mapping_value_slot(
            roles_slot,
            role,
            'bytes32')
        members_slot = role_data_slot
        role_members_value_slot = cls.calculate_mapping_value_slot(
            role_members_slot,
            role,
            'bytes32')
        values_slot = role_members_value_slot
        indexes_slot = role_members_value_slot + 1
        cls._write_uint256(storage, values_slot, len(accounts))
        for i, account in enumerate(accounts):
            members_value_slot = cls.calculate_mapping_value_slot(
                members_slot,
                account,
                'address')
            cls._write_uint256(storage, members_value_slot, 1)
            cls._write_address(
                storage,
                cls.calculate_array_value_slot(values_slot, i),
                account)
            cls._write_uint256(
                storage,
                cls.calculate_mapping_value_slot(
                    indexes_slot,
                    int(account, 16),
                    'uint256'),
                i + 1)
