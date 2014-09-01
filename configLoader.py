'''
Class ConfigLoader
Purpose: Read configuration settings

Author: Junyong Suh (junyongsuh@gmail.com)
Last updated: August 28th, 2014
'''
import json
import os.path

class ConfigLoader:

	def __init__(self):
		# general configuration
		path = "./config/configuration.json"
		if os.path.isfile(path):
			try:
				config = json.loads(open(path).read())
				if config["env"]:
					self.env = config["env"]
				if config["payloadValidationVersion"]:
					self.payloadValidationVersion = config["payloadValidationVersion"]
				if config["emailServiceVersion"]:
					self.emailServiceVersion = config["emailServiceVersion"]
				if config["splunkLogPath"]:
					self.splunkLogPath = config["splunkLogPath"]
				if config["logPath"]:
					self.logPath = config["logPath"]
				configurationIsLoaded = True
			except (ValueError, KeyError, TypeError) as error:
				print path +" is invalid"
				print error
			except (IOError) as error:
				print error

		# payload validation configuration
		path = "./config/payloadValidationConfig.json"
		if os.path.isfile(path):
			try:
				payloadValidationConfig = json.loads(open(path).read())
				v = self.getPayloadValidationVersion()
				if v in payloadValidationConfig:
					self.payloadValidationSchema = payloadValidationConfig[v]
				payloadValidationConfigIsLoaded = True
			except (ValueError, KeyError, TypeError) as error:
				print path + " is invalid"
				print error
			except (IOError) as error:
				print error

		# email provider configurations
		path = "./config/emailProviders.override.json"	# for dev
		if not os.path.isfile(path):
			path = "./config/emailProviders.json"

		try:
			emailProviderConfig = json.loads(open(path).read())
			self.providerConfigsInPriority = {}
			for emailProvider in emailProviderConfig:
				providerInfo = emailProviderConfig[emailProvider]
				for key in providerInfo:
					if key == "priority":
						self.providerConfigsInPriority[providerInfo[key]] = providerInfo
			emailProvidersIsLoaded = True
		except (ValueError, KeyError, TypeError) as error:
			print path + " is invalid"
			print error
		except (IOError) as error:
			print error

		# All configuration is loaded?
		if configurationIsLoaded and payloadValidationConfigIsLoaded and emailProvidersIsLoaded:
			self.isLoadedSuccessfully = True
		else:
			self.isLoadedSuccessfully = False

	def getEmailServiceVersion(self):
		return self.emailServiceVersion

	def getPayloadValidationVersion(self):
		return self.payloadValidationVersion

	def getPayloadValidationConfig(self):
		return self.payloadValidationSchema

	def getEnv(self):
		return self.env

	def getProviderConfigsInPriority(self):
		return self.providerConfigsInPriority

	def getEmailServiceVersion(self):
		return self.emailServiceVersion

	def getSplunkLogPath(self):
		return self.splunkLogPath

	def getLogPath(self):
		return self.logPath

	def isLoaded(self):
		return self.isLoadedSuccessfully
