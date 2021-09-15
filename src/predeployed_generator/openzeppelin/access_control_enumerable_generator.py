from ..contract_generator import ContractGenerator

class AccessControlEnumerableGenerator(ContractGenerator):

    # private

    def _setup_role(self, roles_slot: int, role_members_slot: int, role: bytes, accounts: [str]):
        role_data_slot = calculate_mapping_value_slot(roles_slot, role, 'bytes32')
        members_slot = role_data_slot
        role_members_value_slot = calculate_mapping_value_slot(role_members_slot, role, 'bytes32')
        values_slot = role_members_value_slot
        indexes_slot = role_members_value_slot + 1
        self._write_uint256(values_slot, len(accounts))
        for i, account in enumerate(accounts):
            members_value_slot = calculate_mapping_value_slot(members_slot, account, 'address')
            self._write_uint256(members_value_slot, 1)
            self._write_address(calculate_array_value_slot(values_slot, i), account)
            self._write_uint256(
                calculate_mapping_value_slot(indexes_slot, int(account, 16), 'uint256'),
                i + 1)