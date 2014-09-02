Specifications
======================

## Overview
HTTP service that accepts POST requests with JSON data to a ‘/email’ endpoint with the following parameters:
####
	* ‘to’ ­ The email address to send to
	* ‘to_name’ ­ The name to accompany the email
	* ‘from’ ­ The email address in the from and reply fields
	* ‘from_name’ ­ the name to accompany the from/reply emails
	* ‘subject’ ­ The subject line of the email
	* ‘body’ ­ the HTML body of the email

Example Request Payload:
```
{
	“to”: “fake@example.com”,
	“to_name”: “Ms. Fake”,
	“from”: “noreply@uber.com”,
	“from_name”: “Uber”,
	“subject”: “A Message from Uber”,
	“body”: “<h1>Your Bill</h1><p>$10</p>”
}
```
## Email providers
#### Sendgrid
	* Main Website: www.sendgrid.com
	* Signup: www.sendgrid.com/user/signup
	* Simple Send Documentation: https://sendgrid.com/docs/API_Reference/Web_API/mail.html
#### Mailgun
	* Main Website: www.mailgun.com
	* Simple Send Documentation: http://documentation.mailgun.com/quickstart.html#sending­messages
#### Mandrill
	* Main Website: www.mandrillapp.com
	* Simple Send Documentation: https://mandrillapp.com/api/docs/messages.JSON.html#method­send

## Good to haves
* [Implemented](https://github.com/Junyong-Suh/MultipleEmailProviders/blob/master/config/emailProviders.json) Instead of relying on a configuration change for choosing which email provider to use, dynamically select a provider based on their error responses. For instance, if Mailgun started to timeout or was returning errors, automatically switch to Mandrill.
* [Implemented](https://github.com/Junyong-Suh/MultipleEmailProviders/blob/master/emailRequestHandler.py#L27) Keep a record of emails passing through your service in some queryable form of data storage.
* [Implemented](https://github.com/Junyong-Suh/MultipleEmailProviders#delayed-delivery-for-mandrill-and-mailgun) Both services offer delayed delivery. Implement a delivery date / time parameter for POST requests to your service.
* Both Mandrill and Mailgun have webhooks for email opens and clicks. Implement endpoints on your service to receive those webhook POST requests and store that information in some form of data storage.
