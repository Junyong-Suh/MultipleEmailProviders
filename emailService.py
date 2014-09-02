from flask import Flask, request, Response, render_template
from configLoader import ConfigLoader
from emailRequestHandler import EmailRequestHandler
import os.path
app = Flask(__name__)

@app.route("/")
def home():
	response = Response("{\"message\": \"Please check API documentation\"}", status=400, mimetype='application/json')
	return response

@app.route("/email/", methods=['POST'])
def email():
	emailHandler = EmailRequestHandler(config)
	response = emailHandler.process(request)
	return response

# For Dev purpose only
@app.route("/test/", methods=['GET'])
def test():
	if app.config["ENV"] == "dev":
		f = open('./test/test.html', 'r')
		content = f.read()
		return Response(content, status=200, mimetype="text/html")
	else:
		return Response("{\"message\": \"Page not allowed to access\"}", status=404)

# Main Service
if __name__ == "__main__":
	config = ConfigLoader()
	if config.isLoaded():
		# get environment
		app.config["ENV"] = config.getEnv()
		print "Environment: "+ app.config["ENV"].upper()
		if app.config["ENV"].lower() == "prod":
			app.run()
		elif app.config["ENV"].lower() == "dev":
			app.run(debug=True)
	else:
		print "Failed to load the config. Can't start the Service."
