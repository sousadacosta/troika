"""Hook system to perform custom actions"""

import logging

from .components import discover_modules
from . import hooks
from .hooks.base import Hook
from .hooks.base import at_startup, pre_submit, at_exit  # re-export

_logger = logging.getLogger(__name__)


def setup_hooks(config, site):
    """Set up the hooks according to site configuration

    Parameters
    ----------
    config: `troika.config.Config`
        Configuration object
    site: str
        Site name
    """
    site_config = config.get_site_config(site)
    for _ in discover_modules(hooks, what="hook"):
        pass  # importing the modules is enough
    for spec in Hook.registered_hooks.values():
        req = site_config.get(spec.name, [])
        spec.instantiate(req)
        if req:
            _logger.debug("Enabled %s hooks: %s", spec.name, ", ".join(req))
