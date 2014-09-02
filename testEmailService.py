#
# class EmailServiceTestCase
# unit test for the service
#
# author: Junyong Suh
# last updated: September 1st, 2014
#

import emailService
import unittest
from configLoader import ConfigLoader
from emailRequestHandler import EmailRequestHandler
from providerRequestHandler import ProviderRequestHandler
from payloadValidationHelper import PayloadValidationHelper

class EmailServiceTestCase(unittest.TestCase):

	def setUp(self):
		emailService.app.config['TESTING'] = True
		self.app = emailService.app.test_client()
		self.config = ConfigLoader()
		emailService.app.config['ENV'] = self.config.getEnv()

	def tearDown(self):
		# nothing to do yet
		pass

	'''
	configLoader.py testing
	'''

	def test_configLoader_getPayloadValidationVersion(self):
		assert self.config.getPayloadValidationVersion()

	def test_configLoader_getPayloadValidationConfig(self):
		assert self.config.getPayloadValidationConfig()

	def test_configLoader_getEmailServiceVersion(self):
		assert self.config.getEmailServiceVersion()

	def test_configLoader_getSplunkLogPath(self):
		assert self.config.getSplunkLogPath()

	def test_configLoader_getLogPath(self):
		assert self.config.getLogPath()

	def test_configLoader_isLoaded(self):
		assert self.config.isLoaded() is True

	def test_configLoader_getEnv(self):
		assert self.config.getEnv() in ('prod', 'dev')

	'''
	emailService.py testing
	'''

	def test_root(self):
		rv = self.app.get('/')
		assert "{\"message\": \"Please check API documentation\"}" in rv.data
		rv = self.app.post('/')
		assert "405 Method Not Allowed" in rv.data
		rv = self.app.put('/')
		assert "405 Method Not Allowed" in rv.data
		rv = self.app.delete('/')
		assert "405 Method Not Allowed" in rv.data

	def test_test(self):
		emailService.app.config['ENV'] = "prod"
		if emailService.app.config['ENV'] is "prod":
			rv = self.app.get('/test/')
			assert "{\"message\": \"Page not allowed to access\"}" in rv.data
			rv = self.app.post('/test/')
			assert "405 Method Not Allowed" in rv.data
			rv = self.app.put('/test/')
			assert "405 Method Not Allowed" in rv.data
			rv = self.app.delete('/test/')
			assert "405 Method Not Allowed" in rv.data
		emailService.app.config['ENV'] = "dev"
		if emailService.app.config['ENV'] is "dev":
			rv = self.app.get('/test/')
			assert "<p>Just for testing</p>" in rv.data
			rv = self.app.post('/test/')
			assert "405 Method Not Allowed" in rv.data
			rv = self.app.put('/test/')
			assert "405 Method Not Allowed" in rv.data
			rv = self.app.delete('/test/')
			assert "405 Method Not Allowed" in rv.data

	def test_email(self):
		pass

	'''
	emailRequestHandler.py testing
	'''

	def test_email_request_handler(self):
		pass

	'''
	payloadValidationHelper.py testing
	'''

	def test_payload_validation_helper(self):
		pass

	'''
	providerRequestHandler.py testing
	'''

	def test_provider_request_handler(self):
		pass

if __name__ == '__main__':
	unittest.main()
