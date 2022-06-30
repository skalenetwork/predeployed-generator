#!/usr/bin/env bash

set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$(dirname "$0")/.."
ARTIFACTS_DIR="src/predeployed_generator/openzeppelin/artifacts/"
OPENZEPPELIN_DIR="openzeppelin-contracts"
if [[ ! -d "openzeppelin-contracts" ]]
then
    git clone --branch "v$(cat OPENZEPPELIN_CONTRACTS_VERSION)" https://github.com/OpenZeppelin/openzeppelin-contracts.git $OPENZEPPELIN_DIR
    cd $OPENZEPPELIN_DIR
    npm install
    cd ..
fi

ARTIFACTS_DIR=$ARTIFACTS_DIR OZ_PATH="$OPENZEPPELIN_DIR/artifacts/contracts/proxy/transparent/" python $SCRIPT_DIR/generate_meta.py
