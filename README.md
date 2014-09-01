MultipleEmailProviders
======================

## Overview
A service that abstraction between two (or more) different email service providers. This way, if one of the services goes down, you can quickly failover to a different provider without affecting your customers.

## Technical Design Documentation
Find it [here](https://github.com/Junyong-Suh/MultipleEmailProviders/blob/master/docs/TechDesignDoc.md)

## Requirements
1. Python v2.7.x
2. Flask v0.10.0 or higher
3. requests v2.3.0 or higher

## How to setup (assuming you have [Git](http://git-scm.com/book/en/Getting-Started-Installing-Git) installed)
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

### Sample call
'''
curl -X POST http://127.0.0.1:5000/email/ -H "Content-Type:application/json" -d @./test/sample.json -v
'''
'''
curl -X POST http://127.0.0.1:5000/email/ -H "Content-Type:application/x-www-form-urlencoded" -d body="<h1>Hello</h1><p>from Uber</p>" -d from_name="Uber" -d from="no-reply@uber.com" -d to="junyongsuh@gmail.com" -d to_name="Junyong Suh" -d safeBody="Hellofrom Uber" -d subject="Your Monday evening trip with Uber" -v
'''

## Test (coming soon)
```
make test
```

## Which language and/or microframework you chose and why
Python and Flask due to it's easiness to implement web service as well as it's used in Uber.

## Tradeoffs
#### You might have made
1. Adding email providers in configuration - priority as index vs provider name as index
- Implemented provider name as index to have better readability and less hassle when adding them
2. Logging to a log file instead of database
- Implemented logging to a file to have less failure points. Log in JSON format to be used in ETL in the future.
- Database would get too large soon assuming we will handle tremendous traffics. If we'd like to store in the database, I would construct a) database logging web endpoint in seperate service and b) seperate database servers. So in this service, we would simply call that logging service and move on.

#### Anything you left out
1. Test automation - keep adding on
2. Keep a record of emails passing through the service in queryable form of data storage
- using log files instead of data storage
3. Webhooks for Mandrill and Mailgun for email opens and click. Recieve those webhook POST requests and store that information in some form of data storage.
4. Delayed delivery for Mandrill and Mailgun

#### What you might do differently if you were to spend additional time on the project
1. If we have dedicated client side SDK, I would add signatre and timestamp to authenticate only valid users to make requests to avoid abusing of the system.
2. I would implement the service in multi-threaded system since there is HTTP I/O from 3rd party which takes a significant time to wait.
3. I would look for a way to protect system from too many requests. a) track a list of ID and # of requests sent in the last 10 minutes and/or b) create a queue to hold the request to process, and response 408 Request Timeout if the request is hold for more than certain period. This may result in slow services in busy time but prevent the service to down.
4. I would construct a class for each mail provider to deal with specific providers
5. Extend payloadValidationHandler to read static JSON schema file on local, and handle the validation as needed. In this way, adding new provider will be done by adding configuration.
