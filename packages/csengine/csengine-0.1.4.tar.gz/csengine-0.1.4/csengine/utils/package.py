from typing import Dict

import pkg_resources


def get_packages() -> Dict[str, str]:
    installed_packages = pkg_resources.working_set
    return [(i.key, i.version) for i in installed_packages]
