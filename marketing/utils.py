import requests
import json
import hashlib
import re


ENDPONITS = "https://us15.api.mailchimp.com/3.0/lists/a0006a84d5/members"
MAILCHIMP_API = "23d1f136c6c659e8a7dc89b2206ba84d-us15"


def get_hash_email(email):
	email = email.lower()
	md5=hashlib.md5(email)
	return md5.hexdigest()
def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email


#STATUS = ["subscribed", "unsubscribed", "cleaned", "pending"]
class MailchimpHandler():
	def __init__(self):
		self.endpoints = ENDPONITS
		self.api_key = MAILCHIMP_API

	def change(self, email, status='unsubscribed'):
		#data
		#endpoint
		#auth
		email = check_email(email)
		email = email.encode()
		email = get_hash_email(email)
		endpoints= "{endpoints}/{email}".format(endpoints=self.endpoints,email=email)
		status = status
		data = {
			"status":status
		}
		r = requests.put(endpoints, auth=('', self.api_key), json=data)
		return r.status_code, r.json()

	def add(self, email):
		email = email
		data = {
			"email_address":email,
			"status": "subscribed"
		}
		r = requests.post(self.endpoints, auth=('', self.api_key), json=data)
		return r.status_code, r.json()

	def status_check(self, email):
		email = check_email(email)
		email = email.encode()
		email = get_hash_email(email)
		endpoints= "{endpoints}/{email}".format(endpoints=self.endpoints,email=email)
		r = requests.get(endpoints, auth=('', self.api_key))
		return r.status_code, r.json()

	def subscribe(self, email):
		return self.change(email, status="subscribed")

	def unsubscribe(self, email):
		return self.change(email, status="unsubscribed")

	def pending(self, email):
		return self.change(email, status="pending")
