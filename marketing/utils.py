from django.conf import settings
import requests
import json
import hashlib
import re


MAILCHIMP_API = getattr(settings, 'MAILCHIMP_API', None)
LIST_ID = getattr(settings, 'MAILCHIMP_LIST_ID', None)
DC = getattr(settings, 'MAILCHIMP_DC', None)


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
		self.api_key = MAILCHIMP_API
		self.list_id = LIST_ID
		self.dc = DC # data centre
		self.endpoints = "https://{}.api.mailchimp.com/3.0/lists/".format(self.dc)

	def get_member_endpoints(self):
		return self.endpoints+self.list_id +"/members"

	def change(self, email, status='unsubscribed'):
		#data
		#endpoint
		#auth
		email = check_email(email)
		email = email.encode()
		email = get_hash_email(email)
		endpoints= "{endpoints}/{email}".format(endpoints=self.get_member_endpoints(),email=email)
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
		r = requests.post(self.get_member_endpoints(), auth=('', self.api_key), json=data)
		return r.status_code, r.json()

	def status_check(self, email):
		email = check_email(email)
		email = email.encode()
		email = get_hash_email(email)
		endpoints= "{endpoints}/{email}".format(endpoints=self.get_member_endpoints(), email=email)
		r = requests.get(endpoints, auth=('', self.api_key))
		return r.status_code, r.json()

	def subscribe(self, email):
		return self.change(email, status="subscribed")

	def unsubscribe(self, email):
		return self.change(email, status="unsubscribed")

	def pending(self, email):
		return self.change(email, status="pending")
