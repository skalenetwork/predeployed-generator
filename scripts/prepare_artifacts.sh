#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."
ARTIFACTS_DIR="src/predeployed_generator/openzeppelin/artifacts/"
OPENZEPPELIN_DIR="openzeppelin-contracts"
if [[ ! -d "openzeppelin-contracts" ]]
then
    git clone --branch "v$(cat OPENZEPPELIN_CONTRACTS_VERSION)" git@github.com:OpenZeppelin/openzeppelin-contracts.git $OPENZEPPELIN_DIR
    cd $OPENZEPPELIN_DIR
    npm install
    cd ..
fi
cp -v "$OPENZEPPELIN_DIR/artifacts/contracts/proxy/transparent/ProxyAdmin.sol/ProxyAdmin.json" $ARTIFACTS_DIR
cp -v "$OPENZEPPELIN_DIR/artifacts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol/TransparentUpgradeableProxy.json" $ARTIFACTS_DIR
