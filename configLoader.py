'''
Class ConfigLoader
Purpose: Read configuration settings

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: August 28th, 2014
'''
import json

class ConfigLoader:

	def __init__(self):
		# general configuration
		try:
			path = "./config/configuration.json"
			self.config = json.loads(open(path).read())
			if self.config["env"]:
				self.env = self.config["env"]
			if self.config["provider"]:
				self.provider = self.config["provider"]
			if self.config["payloadValidationVersion"]:
				self.payloadValidationVersion = self.config["payloadValidationVersion"]
		except (ValueError, KeyError, TypeError) as error:
			print path +" is invalid"
			print error
		except (IOError) as error:
			print error

		# payload validation configuration
		try:
			path = "./config/payloadValidationConfig.json"
			payloadValidationConfig = json.loads(open(path).read())
			v = self.getPayloadValidationVersion()
			if v in payloadValidationConfig:
				self.payloadValidationSchema = payloadValidationConfig[v]
		except (ValueError, KeyError, TypeError) as error:
			print path + " is invalid"
			print error
		except (IOError) as error:
			print error

		# email provider configurations
		try:
			# path = "./config/emailProviders.json"
			path = "./config/emailProviders.override.json"	# for dev
			emailProviderConfig = json.loads(open(path).read())
			self.providerConfigsInPriority = {}
			for emailProvider in emailProviderConfig:
				providerInfo = emailProviderConfig[emailProvider]
				for key in providerInfo:
					if key == "priority":
						self.providerConfigsInPriority[providerInfo[key]] = providerInfo
		except (ValueError, KeyError, TypeError) as error:
			print path + " is invalid"
			print error
		except (IOError) as error:
			print error

	def getPayloadValidationVersion(self):
		return self.payloadValidationVersion

	def getPayloadValidationConfig(self):
		return self.payloadValidationSchema

	def getEnv(self):
		return self.env

	def getProviderConfigsInPriority(self):
		return self.providerConfigsInPriority
