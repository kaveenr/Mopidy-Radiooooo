import logging
import pathlib

import pkg_resources

from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-Radiooooo").version

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-Radiooooo"
    ext_name = "radiooooo"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        # schema["display_enabled"] = config.String()
        # schema["password"] = config.Secret()
        return schema

    def setup(self, registry):
        # You will typically only implement one of the following things
        # in a single extension.

        from .frontend import RadioooooFrontend
        registry.add("frontend", RadioooooFrontend)

        from .backend import RadioooooBackend
        registry.add("backend", RadioooooBackend)
