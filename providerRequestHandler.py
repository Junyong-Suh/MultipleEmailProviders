'''
Class ProviderRequestHandler
Purpose: Handle Provider requests

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: August 28th, 2014
'''
import requests
import json

class ProviderRequestHandler:

	def _sendRequest(self, payload, providerInfo):
		# 3.1 compose payload for the provider
		composedPayload = self._composePayload(payload, providerInfo)
		if not composedPayload:
			return 500, "failed to compose payload"
		providerEndpoint = self._getProviderEndpoint(providerInfo)
		if not providerEndpoint:
			return 500, "unable to get provider endpoint"

		# 3.2 send requests and get the response
		try:
			providerName = self._getValueFromDict("name", providerInfo)
			timeout = self._getValueFromDict("timeout", providerInfo)
			supports_delayed_delivery = self._getValueFromDict("supports_delayed_delivery", providerInfo)

			# only mandrill and mailgun support delayed delivery
			if self._isDelayedDelivery(payload):
				if self._str2bool(supports_delayed_delivery):
					if providerName == "mailgun":
						api_user = self._getValueFromDict("api_user", providerInfo)
						api_key = self._getValueFromDict("api_key", providerInfo)
						r = requests.post(providerEndpoint, auth=(api_user, api_key), data=composedPayload, timeout=timeout)
					else:
						r = requests.post(providerEndpoint, data=composedPayload, timeout=timeout)
			else:
				if providerName == "mailgun":
					api_user = self._getValueFromDict("api_user", providerInfo)
					api_key = self._getValueFromDict("api_key", providerInfo)
					r = requests.post(providerEndpoint, auth=(api_user, api_key), data=composedPayload, timeout=timeout)
				else:
					r = requests.post(providerEndpoint, data=composedPayload, timeout=timeout)
		except (requests.exceptions.Timeout) as error:
			return 408, str(error)
		except (requests.exceptions.InvalidSchema, requires.exceptions.SSLError) as error:
			return 503, str(error)

		# 3.3 return the result (status, text)
		return r.status_code, r.text

	def _getProviderEndpoint(self, providerInfo):
		return self._getValueFromDict("endpoint", providerInfo) + self._getValueFromDict("api_send", providerInfo)

	# ToDo: find smarter way to do this -- with template json schema per provider
	def _composePayload(self, payload, providerInfo):
		providerName = self._getValueFromDict("name", providerInfo)

		composedPayload = {}
		if providerName == "sendgrid":
			# credentials
			composedPayload["api_user"] = self._getValueFromDict("api_user", providerInfo)
			composedPayload["api_key"] = self._getValueFromDict("api_key", providerInfo)

			# payload
			# https://sendgrid.com/docs/API_Reference/Web_API/mail.html
			composedPayload["to"] = self._getValueFromDict("to", payload)
			composedPayload["toname"] = self._getValueFromDict("to_name", payload)
			composedPayload["subject"] = self._getValueFromDict("subject", payload)
			composedPayload["html"] = self._getValueFromDict("body", payload)
			composedPayload["text"] = self._getValueFromDict("safeBody", payload)
			composedPayload["from"] = self._getValueFromDict("from", payload)
			composedPayload["fromname"] = self._getValueFromDict("from_name", payload)
			composedPayload["Reply-To"] = self._getValueFromDict("from", payload)
			return composedPayload
		elif providerName == "mailgun":
			# requires Auth instead of credentials over payload
			# http://documentation.mailgun.com/quickstart-sending.html#send-via-api
			composedPayload["to"] = self._getValueFromDict("to_name", payload) + " <"+ self._getValueFromDict("to", payload) + ">"
			composedPayload["subject"] = self._getValueFromDict("subject", payload)
			composedPayload["html"] = self._getValueFromDict("body", payload)
			composedPayload["text"] = self._getValueFromDict("safeBody", payload)
			composedPayload["from"] = self._getValueFromDict("from_name", payload) + " <"+ self._getValueFromDict("from", payload) + ">"

			send_at = self._getValueFromDict("send_at", payload)
			if send_at:
				composedPayload["o:deliverytime"] = send_at
			return composedPayload
		elif providerName == "mandrill":
			# credentials
			composedPayload["key"] = self._getValueFromDict("api_key", providerInfo)

			# payload
			# https://mandrillapp.com/api/docs/messages.JSON.html#method-send
			composedPayload["message"] = {}
			composedPayload["message"]["html"] = self._getValueFromDict("body", payload)
			composedPayload["message"]["text"] = self._getValueFromDict("safeBody", payload)
			composedPayload["message"]["subject"] = self._getValueFromDict("subject", payload)
			composedPayload["message"]["from_email"] = self._getValueFromDict("from", payload)
			composedPayload["message"]["from_name"] = self._getValueFromDict("from_name", payload)
			composedPayload["message"]["to"] = {}
			composedPayload["message"]["to"][0] = {}
			composedPayload["message"]["to"][0]["email"] = self._getValueFromDict("to", payload)
			composedPayload["message"]["to"][0]["name"] = self._getValueFromDict("to_name", payload)
			composedPayload["message"]["to"][0]["type"] = "to"
			composedPayload["message"]["headers"] = {}
			composedPayload["message"]["headers"]["Reply-To"] = self._getValueFromDict("from", payload)
			send_at = self._getValueFromDict("send_at", payload)
			if send_at:
				composedPayload["o:deliverytime"] = send_at
			return json.dumps(composedPayload)
		else:
			return None

	def _isDelayedDelivery(self, payload):
		return self._getValueFromDict("send_at", payload)

	# ToDo: move this to proper util or helper class
	def _str2bool(self, v):
		return v.lower() in ("yes", "true", "t", "1")

	# ToDo: move this to proper util or helper class
	def _getValueFromDict(self, key, payload):
		if key in payload:
			return payload[key]
		else:
			return None
