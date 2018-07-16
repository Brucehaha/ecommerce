from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from .models import EmailActivation, GuestEmail
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.utils.safestring import mark_safe


User = get_user_model()



class ReactivateEmailForm(forms.Form):
    email       = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = """This email does not exists, would you like to <a href="{link}">register</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class RegisterForm(forms.ModelForm):
	email    = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				"class": "form-control ",
			 	"placeholder": "email"
			 	}
			)
		)
	password = forms.CharField(
			widget=forms.PasswordInput(
				attrs={
					"class": "form-control",
				 	"placeholder": "password"
				 	}
				)

			)
	password2= forms.CharField(
			label = 'Password Confirmation',
			widget=forms.PasswordInput(
				attrs={
					"class": "form-control",
					"placeholder": "Password"
				}
				)
			)

	class Meta:
		model = User
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email is taken")
		return email

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		user.is_active = False #send comfirmation email by signal
		if commit:
			user.save()
		return user


class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password (again)', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email','username']


	def clean_password2(self):
	# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])

		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'is_active', 'admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]



class GuestForm(forms.ModelForm):
	email 	= forms.EmailField(
			widget=forms.EmailInput(
				attrs={
					"class": "form-control",
				 	"placeholder": "email"
				 	}
				)
			)

	class Meta:
		model = GuestEmail
		fields = [
			'email'
		]

	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(GuestForm, self).__init__(*args, **kwargs)

	# def save(self, commit=True):
	# 	obj = super(GuestForm, self).save(commit=False)
	# 	if commit:
	# 		obj.save()
	# 		# request = self.request
	# 		# request.session['guest_email_id'] = obj.id
	# 	return obj


class LoginForm(forms.Form):
	email    = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				"class": "form-control",
			 	"placeholder": "email"
			 	}
			)
		)
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
			 	"placeholder": "password"
			 	}
			)
		)
	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		request = self.request
		cleaned_data = super(LoginForm, self).clean()#or self.cleaned_data
		email = cleaned_data.get("email")
		password = cleaned_data.get("password")
		qs = User.objects.filter(email=email)
		if qs.exists():
			#user is registered, check active
			link = reverse("account:email-reactivate")
			reconfirm_msg = """Go to <a href='{resend_link}'>
			resend confirmation email</a>.
			""".format(resend_link = link)
			not_active=qs.filter(is_active=False)
			if not_active.exists():
				EmailActivation_qs = EmailActivation.objects.filter(email=email)
				is_confirmable = EmailActivation_qs.confirmable().exists()
				if is_confirmable:
					msg1="Please check you email to confirm your account or"+reconfirm_msg
					raise forms.ValidationError(mark_safe(msg1))
				# if if_confirmable = False, validate if the email exits in Email
				#activation object and the actived is False
				is_email_exists = EmailActivation.objects.email_exists(email=email)
				if is_email_exists:
					msg2 = "Email not confirmed, "+reconfirm_msg
					raise forms.ValidationError(mark_safe(msg2))
				if not is_confirmable and is_email_exists:
					raise forms.ValidationError("User is inactive")
		user = authenticate(request, email=email, password=password)
		if user is None:
			raise forms.ValidationError("Invalid user name or password")
		login(request, user)

		self.user=user
		return cleaned_data



# class RegisterForm(forms.Form):
# 	username = forms.CharField(
# 		widget=forms.PasswordInput(
# 			attrs={
# 				"class": "form-control",
# 			 	"placeholder": "username"
# 			 	}
# 			)
# 		)
	# email    = forms.EmailField(
	# 	widget=forms.EmailInput(
	# 		attrs={
	# 			"class": "form-control",
	# 		 	"placeholder": "email"
	# 		 	}
	# 		)
	# 	)
# 	password = forms.CharField(
# 		widget=forms.PasswordInput(
# 			attrs={
# 				"class": "form-control",
# 			 	"placeholder": "password"
# 			 	}
# 			)
#
# 		)
#
# 	password2= forms.CharField(
# 		widget=forms.PasswordInput(
# 			attrs={
# 				"class": "form-control",
# 			 	"placeholder": "Password"
# 			 	}
# 			)
#
# 		)
# 	def clean_username(self):
# 		username = self.cleaned_data.get('username')
# 		qs = User.objects.filter(username=username)
# 		if qs.exists():
# 			raise forms.ValidationError("Username is taken")
# 		return username
#
# 	def clean_email(self):
# 		email = self.cleaned_data.get('email')
# 		qs = User.objects.filter(email=email)
# 		if qs.exists():
# 			raise forms.ValidationError("email is taken")
# 		return email
#
# 	def clean(self):
# 		data = self.cleaned_data
# 		password = self.cleaned_data.get('password')
# 		password2 = self.cleaned_data.get('password2')
#
# 		if password2 != password:
# 			raise forms.ValidationError("Passwords must match.")
# 		return data
