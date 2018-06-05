ENDPONITS = "https://us17.api.mailchimp.com/3.0/lists/fbe3f0b349/members"
MAILCHIMP_API = "5c8c60927437848799641dfee1289c0c-us17"
STATUS = ["subscribed", "unsubscribed", "cleaned", "pending"]

def get_hash_email(email):
	email = email.lower()
	md5=hashlib.md5(email)
	return md5.hexdigest()
def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email

class Mailchimp():
	def __init__(self):
		self.endpoints = ENDPONITS
		self.api_key = MAILCHIMP_API

	def get_list(self):
		r=requests.get(self.endpoints, auth=('', MAILCHIMP_API))
		return r.json()

	def subscribe(self, email):
		data = {
			"email_address":email,
			"status":"subscribed"
		}
		r = requests.post(self.endpoints, auth=('', MAILCHIMP_API), json=data)
		return r.status_code, r.json()

	def unsubscribe(self, email):
		email = check_email(email)
		email = email.encode()
		email = get_hash_email(email)
		data = {
			"status":"unsubscribed"
		}
		endpoints= "{endpoints}/{email}".format(endpoints=self.endpoints,email=email)
		r = requests.patch(endpoints, auth=('', MAILCHIMP_API), json=data)
		return r.status_code, r.json()
