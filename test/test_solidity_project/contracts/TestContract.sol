// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity ^0.8.7;

import "@openzeppelin/contracts-upgradeable/access/AccessControlEnumerableUpgradeable.sol";

contract TestContract is AccessControlEnumerableUpgradeable {
    bytes32 public constant TESTER_ROLE = keccak256("TESTER_ROLE");
}