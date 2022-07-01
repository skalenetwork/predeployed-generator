import os
from src.predeployed_generator.tools import ArtifactsHandler

hardhat_artifacts_path = os.getenv('OZ_PATH')
package_artifacts_path = os.getenv('ARTIFACTS_DIR')


def main():
    handler = ArtifactsHandler(hardhat_artifacts_path, package_artifacts_path)
    handler.prepare_artifacts('ProxyAdmin')
    handler.prepare_artifacts('TransparentUpgradeableProxy')


if __name__ == '__main__':
    main()
