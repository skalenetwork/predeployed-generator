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
from typing import Dict, List, Union

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


class ContractGenerator:
    '''Generate smart contract allocation in a genesis block'''
    def __init__(self, bytecode: str, balance: int = 0, nonce: int = 0):
        self.bytecode = bytecode
        self.balance = balance
        self.nonce = nonce

    @staticmethod
    def from_hardhat_artifact(
            artifact_filename: str,
            balance: int = 0,
            nonce: int = 0) -> ContractGenerator:
        '''Create ContractGenerator from the artifact file built by hardhat'''
        with open(artifact_filename, encoding='utf-8') as artifact_file:
            contract = json.load(artifact_file)
            return ContractGenerator(contract['deployedBytecode'], balance, nonce)

    def generate(self, **initial_values) -> Dict[str, Union[str, Dict[str, str]]]:
        '''Generate smart contract

        Returns an object in format:
        {
            'balance': ... ,
            'nonce': ... ,
            'code': ... ,
            'storage': ...
        }
        '''
        return self._generate(self.generate_storage(**initial_values))

    def generate_allocation(self, contract_address: str, **args) -> Dict[
                                                                        str,
                                                                        Dict[
                                                                            str,
                                                                            Union[
                                                                                str,
                                                                                Dict[str, str]
                                                                            ]
                                                                        ]
                                                                    ]:
        '''Generate smart contract allocation

        Returns an object in format:
        {
            "0xd2...": {
                'balance': ... ,
                'nonce': ... ,
                'code': ... ,
                'storage': ...
            }
        }
        '''
        return {contract_address: self._generate(self.generate_storage(**args))}

    @classmethod
    def generate_storage(cls, **_) -> Dict[str, str]:
        '''Generate smart contract storage layout
        based on initial values provided in args
        '''
        return {}

    # private

    def _generate(self, storage: Dict[str, str] = None) -> Dict[
                                                            str,
                                                            Union[
                                                                str,
                                                                Dict[str, str]
                                                            ]
                                                        ]:
        '''Produce smart contract allocation object.

        It consists of fields 'code', 'balance', 'nonce' and 'storage'
        '''
        assert isinstance(self.bytecode, str)
        assert isinstance(self.balance, int)
        assert isinstance(self.nonce, int)
        assert isinstance(storage, dict) or storage is None
        return {
            'code': self.bytecode,
            'balance': hex(self.balance),
            'nonce': hex(self.nonce),
            'storage': storage if storage is not None else {}
        }

    @staticmethod
    def _write_address(storage: Dict[str, str], slot: int, address: str) -> None:
        storage[to_even_length(hex(slot))] = address.lower()

    @staticmethod
    def _write_bytes32(storage: Dict[str, str], slot: int, data: bytes) -> None:
        assert len(data) <= 32
        storage[to_even_length(hex(slot))] = to_even_length(add_0x(data.hex()))

    @staticmethod
    def _write_uint256(storage: Dict[str, str], slot: int, value: int) -> None:
        storage[to_even_length(hex(slot))] = to_even_length(add_0x(hex(value)))

    @classmethod
    def _write_addresses_array(cls, storage: Dict[str, str], slot: int, values: List[str]) -> None:
        cls._write_uint256(storage, slot, len(values))
        for i, address in enumerate(values):
            address_slot = cls.calculate_array_value_slot(slot, i)
            cls._write_address(storage, address_slot, address)

    @classmethod
    def _write_string(cls, storage: Dict[str, str], slot: int, value: str) -> None:
        binary = value.encode()
        length = len(binary)
        if length < 32:
            binary += (2 * length).to_bytes(32 - length, 'big')
            cls._write_bytes32(storage, slot, binary)
        else:
            cls._write_uint256(storage, slot, 2 * length + 1)

            def chunks(size, source):
                for i in range(0, len(source), size):
                    yield source[i:i + size]

            for index, data in enumerate(chunks(32, binary)):
                if len(data) < 32:
                    data += int(0).to_bytes(32 - len(data), 'big')
                cls._write_bytes32(
                    storage,
                    cls.calculate_array_value_slot(slot, index),
                    data)

    @classmethod
    def calculate_mapping_value_slot(
            cls,
            slot: int,
            key: Union[bytes, str, int],
            key_type: str) -> int:
        '''Calculate slot in smart contract storage where value of the key in mapping is stored'''

        if key_type == 'bytes32':
            assert isinstance(key, bytes)
        elif key_type == 'address':
            assert isinstance(key, str)
            return cls.calculate_mapping_value_slot(
                slot,
                int(key, 16).to_bytes(32, 'big'),
                'bytes32')
        elif key_type == 'uint256':
            assert isinstance(key, int)
        else:
            raise TypeError(f'{key_type} is unknown key type')

        return int.from_bytes(w3.solidityKeccak([key_type, 'uint256'], [key, slot]), 'big')


    @staticmethod
    def calculate_array_value_slot(slot: int, index: int) -> int:
        '''Calculate slot in smart contract storage
        where value of the array in the index is stored
        '''
        return int.from_bytes(w3.solidityKeccak(['uint256'], [slot]), 'big') + index


    @staticmethod
    def next_slot(previous_slot: int) -> int:
        '''Return next slot in smart contract storage'''
        return previous_slot + 1
