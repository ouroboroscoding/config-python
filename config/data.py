# coding=utf8
""" Data

Handles connecting data from one branch to the next
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-05-26"

# Limit exports
__all__ = [ 'Data' ]

# Ouroboros modules
from tools import combine
import undefined

# Python modules
from copy import deepcopy
from typing import Any

class Data(object):
	"""Data

	Class that stands for a point in the config

	Extends:
		object
	"""

	def __init__(self, _data: Any):
		"""Constructor

		Creates a new instance and returns it

		Arguments:
			_data (any): The data this instance points to

		Returns:
			Data
		"""

		# Store the local data
		self.__data = _data

	def __call__(self, _default = None):
		"""Call

		Python magic method that allows the instance to be called

		Returns:
			The current data of the instance
		"""

		# If we have nothing
		if self.__data is undefined:
			return _default
		else:
			if isinstance(_default, dict) and isinstance(self.__data, dict):
				return combine(_default, self.__data)
			else:
				return deepcopy(self.__data)

	def __getattr__(self, __name: str) -> Any:
		"""Get Attribute

		Python magic method to handle any data request

		Arguments:
			__name (str): The name of the attribute to access

		Returns:
			Data
		"""

		# If we have no data, just return ourselves, it makes no difference
		if self.__data is undefined:
			return self

		# If we have the key
		try:
			return Data(self.__data[__name])

		# If the key doesn't exist, or the type isn't a dict
		except (KeyError, TypeError):
			return Data(undefined)

	def __getitem__(self, __name: str) -> Any:
		"""Get Item

		Python magic method to handle any data requests as a key

		Arguments:
			__name (str): The name of the key to access

		Returns:
			Data
		"""

		# If we have no data, just return ourselves, it makes no difference
		if self.__data is undefined:
			return self

		# If we have the key
		try:
			return Data(self.__data[__name])

		# If the key doesn't exist, or the type isn't a dict
		except (KeyError, TypeError):
			return Data(undefined)