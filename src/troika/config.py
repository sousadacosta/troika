"""Configuration file handling"""

from collections import UserDict
import logging
import os
import yaml

from . import ConfigurationError, InvocationError

_logger = logging.getLogger(__name__)


class Config(UserDict):
    """Configuration mapping"""

    def get_site_config(self, name):
        """Get the configuration associated with the given site

        Parameters
        ----------
        name: str
            Name of the requested site

        Raises
        ------
        `ConfigurationError`
            if the configuration does not define a 'sites' object
        `KeyError`
            if the requested site is not defined
        """
        try:
            sites = self.data['sites']
        except KeyError:
            raise ConfigurationError(f"No 'sites' defined in configuration")

        return sites[name]


def get_config(configfile=None):
    """Read a configuration file

    If configfile is None, the path is read from the ``TROIKA_CONFIG_FILE``
    environment variable.

    Parameters
    ----------
    configfile: None, path-like or file-like

    Returns
    -------
    `Config`
    """

    if configfile is None:
        configfile = os.environ.get("TROIKA_CONFIG_FILE")
        if configfile is None:
            raise InvocationError("No configuration file found")

    try:
        path = os.fspath(configfile)
    except TypeError: # not path-like
        pass
    else:
        configfile = open(path, "r")

    config_fname = configfile.name if hasattr(configfile, 'name') \
                                   else repr(configfile)
    _logger.debug("Using configuration file %s", config_fname)

    try:
        return Config(yaml.safe_load(configfile))
    except yaml.parser.ParserError as e:
        raise ConfigurationError(str(e))
