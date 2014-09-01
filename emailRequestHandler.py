'''
Class EmailRequestHandler
Purpose: Handle emails requests

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: September 1st, 2014
'''
from providerRequestHandler import ProviderRequestHandler
from payloadValidationHelper import PayloadValidationHelper
from flask import Response, Markup
import re
import json

class EmailRequestHandler:

	def __init__(self, config):
		self.config = config
		self.payloadValidationSchema = self.config.getPayloadValidationConfig()
		# a list of provider info sorted by priority
		self.providerConfigsInPriority = self.config.getProviderConfigsInPriority()

	def process(self, request):
		# 1. Validates the payload
		payloadValidationHelper = PayloadValidationHelper(self.config)
		payload = payloadValidationHelper._getValidatedPayload(request)
		if not payload:
			return self._responseFailure(400, "payload invalid.", payload, request)

		# 2. Convert the 'body' HTML to a plain text version to send along to the email provider.
		self._updateBodyHTMLsafe(payload)

		# 3. Send email via providers (try each if fails)
		# 4. Log the requests and responses
		providerRequestHandler = ProviderRequestHandler()
		for priority in self.providerConfigsInPriority:
			providerInfo = self.providerConfigsInPriority[priority]
			statusCode, response = providerRequestHandler._sendRequest(payload, providerInfo)
			if statusCode == 200:
				return self._responseSuccess(statusCode, response, payload, request)
			else:
				# ToDo: this will log twice for the last failure
				self._log("Log", statusCode, response, payload, request)

		if statusCode == 200:
			return self._responseSuccess(statusCode, response, payload, request)
		else:
			return self._responseFailure(statusCode, response, payload, request)

	def _updateBodyHTMLsafe(self, payload):
		body = self._getValueFromDict("body", payload)
		if body:
			payload["safeBody"] = Markup(body).striptags()	# remove HTML tags
			# payload["safeBody"] = Markup.escape(body)		# escape HTML tags

	def _responseSuccess(self, statusCode, response, payload, request):
		self._log("Log", statusCode, response, payload, request)
		response = Response(
			"{\"message\": \"Mail has sent successfully.\", \"response\": "+ response +"}",
			status=statusCode,
			mimetype='application/json'
		)
		return response

	def _responseFailure(self, statusCode, response, payload, request):
		self._log("Log", statusCode, response, payload, request)
		response = Response(
			"{\"message\": \"Error while processing the request\", \"response\": "+ response +"}",
			status=statusCode,
			mimetype='application/json'
		)
		return response

	# ToDo: move this to proper util or helper class
	# ToDo: dump to a file
	def _log(self, level, statusCode, response, payload, request):
		env = self.config.getEnv()
		emailServiceVersion = self.config.getEmailServiceVersion()
		ip = request.remote_addr
		userAgent = request.headers["User-Agent"]

		print "logType="+ level +", v="+ emailServiceVersion +", env="+ env +", statusCode="+ str(statusCode) +", response="+ response +", ip="+ ip +", userAgent="+ userAgent +", payload="+ json.dumps(payload)

	# ToDo: move this to proper util or helper class
	def _getValueFromDict(self, key, payload):
		if key in payload:
			return payload[key]
		else:
			return None
