# coding=utf8
""" Conf

Loads configuration from ./config.json merged with ./config.`hostname`.json
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-05-26"

# Limit exports
__all__ = [ 'Conf' ]

# Ouroboros modules
import jsonb
from tools import merge
import undefined

# Python modules
from copy import copy
import platform
import sys
from typing import Any

# Project modules
from . import data

class Conf(object):
	"""Conf

	Class that can only be instantiated once

	Extends:
		object
	"""

	_exists = False
	"""Used to flag any attempt to create multiple instances of itself"""

	def __init__(self):
		"""Constructor

		Creates a new instance and returns it

		Returns:
			Conf
		"""

		# If we already exist, fuck shit up
		if self._exists:
			raise RuntimeError(
				'config-oc.config.Conf can not be instantiated twice'
			)
		self._exists = True

		# Init the list of reload callbacks
		self._callbacks = [ ]

		# Load the config
		self._load()

	def __call__(self):
		"""Call

		Python magic method that allows the instance to be called

		Returns:
			The current data of the instance
		"""

		return copy(self.__data)

	def __getattr__(self, __name: str) -> Any:
		"""Get Attribute

		Python magic method to handle any data request as an attribute

		Arguments:
			__name (str): The name of the attribute to access

		Returns:
			data.Data
		"""

		# If we have the name in the top level of the data
		try:
			return data.Data(self.__data[__name])
		except KeyError:
			return data.Data(undefined)

	def __getitem__(self, __name: str) -> Any:
		"""Get Item

		Python magic method to handle any data requests as a key

		Arguments:
			__name (str): The name of the key to access

		Returns:
			data.Data
		"""

		# If we have the name in the top level of the data
		try:
			return data.Data(self.__data[__name])
		except KeyError:
			return data.Data(undefined)

	def _load(self):
		"""Load (private)

		Loads the data from the files into memory

		Returns:
			None
		"""

		# Init the data
		self.__data = { }

		# Load the primary file
		try:
			self.__data = jsonb.load('config.json')
		except FileNotFoundError:
			sys.stderr.write('config-oc.config unable to load config.json\n')

		# Load the hostname file on top of the base file
		try:
			merge(
				self.__data,
				jsonb.load('config.%s.json' % platform.node())
			)
		except FileNotFoundError:
			sys.stderr.write(
				'config-oc unable to load config.%s.json\n' % platform.node()
			)

	def reload(self):
		"""Reload

		Called to reload the config files from memory
		"""

		# Call the load method again
		self._load()

		# Call each reload callback
		for f in self._callbacks:
			f()

	def on_reload(self, callback: callable):
		"""On Reload

		Attachs a functhon/method to be called if the config is reloaded

		Arguments:
			callback (Callable): The function to call on reload
		"""

		# If the function does not already exist
		if callback not in self._callbacks:
			self._callbacks.append(callback)