import json
import os
from os.path import normpath, join, dirname, basename

dbg_path = os.getenv('DBG_PATH')
package_artifacts_path = os.getenv('ARTIFACTS_DIR')


def get_build_info_path():
    with open(dbg_path) as dbg_file:
        dbg = json.loads(dbg_file.read())
        return normpath(join(dirname(dbg_path), dbg['buildInfo']))


def main():
    name = basename(dbg_path).split('.')[0]
    build_info_path = get_build_info_path()
    with open(build_info_path) as info_file:
        info = json.loads(info_file.read())
        meta_data = {
            'name': name,
            'solcVersion': info['solcVersion'],
            'solcLongVersion': info['solcLongVersion'],
            'input': info['input']
        }
    print(join(package_artifacts_path, f'{name}.meta.json'))
    with open(join(package_artifacts_path, f'{name}.meta.json'), 'w') as meta:
        meta.write(json.dumps(meta_data, indent=4))


if __name__ == '__main__':
    main()
