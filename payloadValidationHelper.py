'''
Class PayloadValidationHelper
Purpose: Validate payload

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: September 1st, 2014
'''
import re

class PayloadValidationHelper:

	def __init__(self, config):
		self.config = config
		self.payloadValidationSchema = self.config.getPayloadValidationConfig()

	def _getValidatedPayload(self, request):
		# 1-1. Check if the payload is valid JSON
		# http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
		payload = self._getPayload(request)
		if payload is None:
			return None

		# 1-2. Check if the payload has all keys and values
		if not self._hasRequiredFields(payload):
			return None

		# 1-3. Check if mail addresses are valid (syntax validation)
		if not self._hasValidEmailAddresses(payload):
			return None

		return payload

	def _getPayload(self, request):
		cotentType = self._getValueFromDict('content-type', request.headers)
		cotentType = cotentType.lower()

		if cotentType == "application/json":
			payload = request.get_json(force=False, silent=False, cache=True)
		elif request.form:
			args = request.form
			payload = {}
			for key in args:
				payload[key] = args[key]

		return payload

	def _hasRequiredFields(self, payload):
		# 1-2. Check if the payload has all required keys and values
		for keySchema in self.payloadValidationSchema:
			keyName = self._getValueFromDict("keyName", keySchema)
			if keyName is None:
				return False

			keyValue = self._getValueFromDict(keyName, payload)
			if keyValue is None:
				return False

			for option in keySchema:
				optionValue = self._getValueFromDict(option, keySchema)
				if optionValue is None:
					return False
				# required check
				if option == "required" and self._str2bool(optionValue):
					if keyValue is None:
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
