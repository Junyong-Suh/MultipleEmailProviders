'''
Class EmailRequestHandler
Purpose: Handle emails requests

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: August 28th, 2014
'''
from configLoader import ConfigLoader
from providerRequestHandler import ProviderRequestHandler
from payloadValidationHelper import PayloadValidationHelper
from flask import Response, Markup
import re
import json

class EmailRequestHandler:

	def __init__(self):
		self.config = ConfigLoader()
		self.payloadValidationSchema = self.config.getPayloadValidationConfig()
		# a list of provider info sorted by priority
		self.providerConfigsInPriority = self.config.getProviderConfigsInPriority()

	def process(self, request):
		# 1. Validates the payload
		payloadValidationHelper = PayloadValidationHelper()
		payload = payloadValidationHelper._getValidatedPayload(request)
		if not payload:
			return self._responseFailure(400, "payload invalid.")

		# 2. Convert the 'body' HTML to a plain text version to send along to the email provider.
		self._updateBodyHTMLsafe(payload)

		# 3. Send email via providers (try each if fails)
		# 4. Log the requests and responses
		providerRequestHandler = ProviderRequestHandler()
		for priority in self.providerConfigsInPriority:
			providerInfo = self.providerConfigsInPriority[priority]
			statusCode, response = providerRequestHandler._sendRequest(payload, providerInfo)
			if statusCode == 200:
				return self._responseSuccess(statusCode, response, payload)
			else:
				# ToDo: this will log twice for the last failure
				self._log("Log", statusCode, response, payload)

		if statusCode == 200:
			return self._responseSuccess(statusCode, response, payload)
		else:
			return self._responseFailure(statusCode, response, payload)

	def _updateBodyHTMLsafe(self, payload):
		body = self._getValueFromDict("body", payload)
		if body:
			payload["safeBody"] = Markup(body).striptags()	# remove HTML tags
			# payload["safeBody"] = Markup.escape(body)		# escape HTML tags

	def _responseSuccess(self, statusCode, response, payload):
		self._log("Log", statusCode, response, payload)
		response = Response(
			"{\"message\": \"Mail has sent successfully.\", \"response\": \""+ response +"\"}",
			status=statusCode,
			mimetype='application/json'
		)
		return response

	def _responseFailure(self, statusCode, response, payload):
		self._log("Log", statusCode, response, payload)
		response = Response(
			"{\"message\": \"Error while processing the request\", \"response\": \""+ response +"\"}",
			status=statusCode,
			mimetype='application/json'
		)
		return response

	# ToDo: move this to proper util or helper class
	# ToDo: dump to a file
	def _log(self, level, statusCode, response, payload):
		env = self.config.getEnv()
		print "logType="+ level +", v="+ self.emailServiceVersion() +", env="+ env +", statusCode="+ str(statusCode) +", response="+ response +", payload="+ json.dumps(payload)

	# ToDo: move this to proper util or helper class
	def _getValueFromDict(self, key, payload):
		if key in payload:
			return payload[key]
		else:
			return None
