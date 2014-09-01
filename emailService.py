from flask import Flask, request, Response, render_template
from emailRequestHandler import EmailRequestHandler
from configLoader import ConfigLoader
import os.path
app = Flask(__name__)

# ToDo: Make a landing page
@app.route("/")
def home():
	response = Response(
		"{\"message\": \"Please check API documentation\"}",
		status=400,
		mimetype='application/json'
		)
	return response

@app.route("/email/", methods=['POST'])
def email():
	handler = EmailRequestHandler()
	response = handler.process(request)
	return response

# For Dev purpose only
@app.route("/test/", methods=['GET'])
def test():
	f = open('./test/test.html', 'r')
	content = f.read()
	return Response(content, mimetype="text/html")

# Main Service
if __name__ == "__main__":
	config = ConfigLoader()
	try:
		env = config.getEnv()
		print "Environment: "+ env
		if env == "prod":
			app.run()
		elif env == "dev":
			app.run(debug=True)
	except (AttributeError):
		print "Unable to determine the environment. Can't start the Service."
