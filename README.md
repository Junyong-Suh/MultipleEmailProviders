MultipleEmailProviders
======================

## Overview
A service abstraction between two (or more) different email service providers. This way, if one of the services goes down, you can quickly failover to a different provider without affecting your customers.

## Technical Design Documentation
Find it [here](https://github.com/Junyong-Suh/MultipleEmailProviders/blob/master/docs/TechDesignDoc.md)

## Requirements
1. Python v2.7.x
2. Flask v0.10.0 or higher
3. requests v2.3.0 or higher

## How to setup

* Install Python v2.7 or higher - [https://www.python.org/downloads/](https://www.python.org/downloads/)

* Install pip (or something else if you would prefer) - [http://pip.readthedocs.org/en/latest/installing.html]

* Install Flask v0.10.x or higher

```
pip install Flask
```
* Install requests v2.3.0 or higher
```
pip install requests
```

## Credentials for mail providers
You should have proper api user and api keys in [email providers configuration file](https://github.com/Junyong-Suh/MultipleEmailProviders/blob/master/config/emailProviders.json)

## Run
```
python emailService.py
```

#### Sample call
```
curl -X POST http://127.0.0.1:5000/email/ \
-H "Content-Type:application/json" \
-d @./test/sample.json -v
```
```
curl -X POST http://127.0.0.1:5000/email/ \
-H "Content-Type:application/x-www-form-urlencoded" \
-d body="<h1>Hello</h1><p>from Uber</p>" \
-d from_name="Uber" \
-d from="no-reply@uber.com" \
-d to="junyongsuh@gmail.com" \
-d to_name="Junyong Suh" \
-d safeBody="Hello from Uber" \
-d subject="Your Monday evening trip with Uber" -v
```

#### Test page (only in [dev](https://github.com/Junyong-Suh/MultipleEmailProviders/blob/master/config/configuration.json#L4) mode)
```
http://127.0.0.1:5000/test/
```

#### Delayed delivery for Mandrill and Mailgun
* to request relayed delivery, set parameter 'send_at' no further than 3 days from current time in payload
* Mailgun expects the following format for 'send_at'
```
Thu, 13 Oct 2011 18:02:00 GMT
```
* Mandrill expects the following format for 'send_at'
```
UTC timestamp in YYYY-MM-DD HH:MM:SS format
```
* To do further is have one 'send_at' format from client then transform for each mail provider.

#### Constraints for Mandrill delayed delivery
* Mandrill requires payment for delayed delivery
```
when this message should be sent as a UTC timestamp in YYYY-MM-DD HH:MM:SS format.
If you specify a time in the past, the message will be sent immediately.
An additional fee applies for scheduled email,
and this feature is only available to accounts with a positive balance.
```
* Mandrill returns this response when no positive balance.
```
{
	"status":"error",
	"code":10,
	"name":"PaymentRequired",
	"message":"Email scheduling is only available for accounts with a positive balance."
}
```

## Test (covers ~10%)
```
python testEmailService.py
```

#### Which language and/or microframework you chose and why
Python and Flask due to it's easiness to implement web service as well as it's used in Uber. Although this is the first service / program that I wrote in Python other than scripts, had fun working with Python and Flask. (Of cource, a lot of headaches too!)

#### Tradeoffs you might have made
* Keep a record of emails passing through the service in queryable form of data storage - logging to a log file instead of database
* Database would get too large soon assuming we will handle tremendous traffics. If we'd like to store in the database, I would construct a) database logging web endpoint in seperate service and b) seperate database servers. So in this service, we would simply call that logging service and move on.
* Also lack of time to work on. :-(
* Two log files - one for general log and the other one for Splunk to consume (key=value pair log)

#### Anything you left out
* Test automation - need to familiar with unittest which needs more time. Current test covers ~10% of the service, more likely to refactor or even reconstruct the service as I get familiar with Python and Flask.
* Webhooks for Mandrill and Mailgun for email opens and click. Recieve those webhook POST requests and store that information in some form of data storage. -- Webhooks require to have running server to get POST requests from email providers. Would spin up EC2 server with Elastic IP to work on if I have more time.

#### What you might do differently if you were to spend additional time on the project
* I would construct a class for each mail provider to deal with specific providers
* If we have dedicated client side SDK, I would add signatre and timestamp to authenticate only valid users to make requests to avoid abusing of the system.
* I would implement the service in multi-threaded system since there is HTTP I/O from 3rd party which takes a significant time to wait.
* I would look for a way to protect system from too many requests. a) track a list of ID and # of requests sent in the last 10 minutes and/or b) create a queue to hold the request to process, and response 408 Request Timeout if the request is hold for more than certain period. This may result in slow services in busy time but prevent the service to down.
* Spin up EC2 server with Elastic IP to implement webhook
* Clean up the code, refactor, modulize, more Pythonic configuration reading and testing
