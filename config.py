from sublime import load_settings
from functools import lru_cache

_OSX_NODE_PATH = "/usr/local/bin/node"
_OSX_TNS_PATH = "/usr/local/bin/nativescript"


@lru_cache(maxsize=1)
def _load_config():
    settings = load_settings("nativescript.sublime-settings")
    osx_node_path = settings.get("node_osx_path") or _OSX_NODE_PATH
    osx_tns_path = settings.get("nativescript_osx_path") or _OSX_TNS_PATH,
    return {
        "osx_node_path": osx_node_path,
        "osx_nativescript_path": osx_tns_path,
        "linux_node_path": settings.get("linux_node_path") or "",
        "linux_nativescript_path": settings.get("linux_nativescript_path") or "",
        "win_node_name": "node",
        "win_nativescript_name": "nativescript"
    }


def get_config(name):
    return _load_config()[name]
