'''
Class PayloadValidationHelper
Purpose: Validate payload

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: August 28th, 2014
'''
from configLoader import ConfigLoader
import re

class PayloadValidationHelper:

	def __init__(self):
		self.config = ConfigLoader()
		self.payloadValidationSchema = self.config.getPayloadValidationConfig()

	def _getValidatedPayload(self, request):
		# 1-1. Check if the payload is valid JSON
		# http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
		payload = request.get_json(force=False, silent=False, cache=True)

		# 1-2. Check if the payload has all keys and values
		if not self._hasRequiredFields(payload):
			return None

		# 1-3. Check if mail addresses are valid (syntax validation)
		if not self._hasValidEmailAddresses(payload):
			return None

		return payload

	def _hasRequiredFields(self, payload):
		# 1-2. Check if the payload has all required keys and values
		for keySchema in self.payloadValidationSchema:
			# ToDo: "keyName" should be guaranteed
			keyName = self._getValueFromDict("keyName", keySchema)
			keyValue = payload[keyName]
			for option in keySchema:
				optionValue = keySchema[option]
				# required check
				if option == "required" and self._str2bool(optionValue):
					if not keyValue:
						# value missing
						return False
		return True

	def _hasValidEmailAddresses(self, payload):
		# 1-3. Check if mail addresses are valid (syntax validation)
		# basic email syntax validation
		EMAIL_REGEX = re.compile("^[a-zA-Z0-9_]+[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,6}$")

		# check email types only
		for keySchema in self.payloadValidationSchema:
			# ToDo: "keyName" should be guaranteed
			keyName = self._getValueFromDict("keyName", keySchema)
			keyValue = payload[keyName]
			for option in keySchema:
				optionValue = keySchema[option]
				if option == "type" and optionValue == "email":
					r = EMAIL_REGEX.match(keyValue)
					if r is None:
						return False
		return True

	# ToDo: move this to proper util or helper class
	def _str2bool(self, v):
		return v.lower() in ("yes", "true", "t", "1")

	# ToDo: move this to proper util or helper class
	def _getValueFromDict(self, key, payload):
		if key in payload:
			return payload[key]
		else:
			return None
