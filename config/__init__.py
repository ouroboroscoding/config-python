# coding=utf8
""" Config

Loads configuration from ./config.json merged with ./config.`hostname`.json
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-05-26"

# Limit exports
__all__ = [ 'config', 'Data' ]

# Project modules
from .conf import Conf
from .data import Data

# The one instance we export
config = Conf()