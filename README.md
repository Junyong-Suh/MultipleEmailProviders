MultipleEmailProviders
======================

## Overview
A service that abstraction between two (or more) different email service providers. This way, if one of the services goes down, you can quickly failover to a different provider without affecting your customers.

## Requirements
1. Python v2.7.x
2. Flask v0.10.x or higher
3. requests v2.3.0 or higher

## How to setup
* Install Python v2.7 or higher - [https://www.python.org/downloads/](https://www.python.org/downloads/)

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

## Test (coming soon)
```
make test
```

## Deploy (coming soon)
```
make
```

## Which language and/or microframework you chose and why
I chose Python and Flask due to it's easiness to implement web service as well as it's used in Uber.

## Tradeoffs
* You might have made
* Anything you left out
* What you might do differently if you were to spend additional time on the project
