'''contract_generator.py

The module is used to generate predeployed smart contracts in genesis block

Functions:
    to_even_length
    add_0x
    calculate_mapping_value_slot
    calculate_array_value_slot
    next_slot

Classes:
    ContractGenerator
'''

from __future__ import annotations

import json
from web3.auto import w3


def to_even_length(hex_string: str) -> str:
    '''Modify hex string to have even amount of digits.

    For example:
        "0x0" becomes "0x00"
        "0x123 becomes "0x0123"
        "0x12" stays "0x12"
    '''
    assert hex_string.startswith('0x')
    if len(hex_string) % 2 != 0:
        return "0x0" + hex_string[2:]
    return hex_string


def add_0x(bytes_string: str) -> str:
    '''Add "0x" prefix to the string'''
    if bytes_string.startswith('0x'):
        return bytes_string
    return '0x' + bytes_string


def calculate_mapping_value_slot(slot: int, key: any, key_type: str) -> int:
    '''Calculate slot in smart contract storage where value of the key in mapping is stored'''
    if key_type == 'address':
        return calculate_mapping_value_slot(slot, int(key, 16).to_bytes(32, 'big'), 'bytes32')
    return int.from_bytes(w3.solidityKeccak([key_type, 'uint256'], [key, slot]), 'big')


def calculate_array_value_slot(slot: int, index: int) -> int:
    '''Calculate slot in smart contract storage where value of the array in the index is stored'''
    return int.from_bytes(w3.solidityKeccak(['uint256'], [slot]), 'big') + index


def next_slot(previous_slot: int) -> int:
    '''Return next slot in smart contract storage'''
    return previous_slot + 1


class ContractGenerator:
    '''Generate smart contract allocation in a genesis block'''
    def __init__(self, bytecode: str, balance: int = 0, nonce: int = 0):
        self.bytecode = bytecode
        self.balance = balance
        self.nonce = nonce
        self.storage = {}

    @staticmethod
    def from_hardhat_artifact(
            artifact_filename: str,
            balance: int = 0,
            nonce: int = 0) -> ContractGenerator:
        '''Create ContractGenerator from the artifact file built by hardhat'''
        with open(artifact_filename, encoding='utf-8') as artifact_file:
            contract = json.load(artifact_file)
            return ContractGenerator(contract['deployedBytecode'], balance, nonce)

    def generate(self) -> dict:
        '''Produce smart contract allocation object.

        It consists of fields 'code', 'balance', 'nonce' and 'storage'
        '''
        assert isinstance(self.bytecode, str)
        assert isinstance(self.storage, dict)
        assert isinstance(self.balance, int)
        assert isinstance(self.nonce, int)
        return {
            'code': self.bytecode,
            'balance': hex(self.balance),
            'nonce': hex(self.nonce),
            'storage': self.storage
        }

    # private

    def _write_address(self, slot: int, address: str) -> None:
        self.storage[to_even_length(hex(slot))] = address.lower()

    def _write_bytes32(self, slot: int, data: bytes) -> None:
        assert len(data) <= 32
        self.storage[to_even_length(hex(slot))] = to_even_length(add_0x(data.hex()))

    def _write_uint256(self, slot: int, value: int) -> None:
        self.storage[to_even_length(hex(slot))] = to_even_length(add_0x(hex(value)))

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

    def _write_addresses_array(self, slot: int, values: list) -> None:
        self._write_uint256(slot, len(values))
        for i, address in enumerate(values):
            address_slot = calculate_array_value_slot(slot, i)
            self._write_address(address_slot, address)

    def _write_string(self, slot: int, value: str) -> None:
        binary = value.encode()
        length = len(binary)
        if length < 32:
            binary += (2 * length).to_bytes(32 - length, 'big')
            self._write_bytes32(slot, binary)
        else:
            self._write_uint256(slot, 2 * length + 1)

            def chunks(size, source):
                for i in range(0, len(source), size):
                    yield source[i:i + size]

            for index, data in enumerate(chunks(32, binary)):
                if len(data) < 32:
                    data += int(0).to_bytes(32 - len(data), 'big')
                self._write_bytes32(calculate_array_value_slot(slot, index), data)
