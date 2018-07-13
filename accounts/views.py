from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView,FormView,DetailView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm
from carts.models import Cart
from .models import GuestEmail
from .signals import user_logged_in
from django.utils.safestring import mark_safe
from .models import EmailActivation




class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                  if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)


class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

@login_required
def account_home_view(request): #accounts/login/?next=/some/path
	return render(request, "home.html", {})


class AccountHomeView(LoginRequiredMixin, DetailView):
	template_name='accounts/home.html'

	def get_object(self):
		return self.request.user
#
# class LoginRequiredMixin(object):
# 	@method_decorator(login_required)
# 	def dispatch(self, *args, **kwargs):
# 		return super(LoginRequiredMixin, self).dispatch(self, *args, **kwargs)

def guest_register(request):
	form = GuestForm(request.POST or None)
	context = {
		"form": form
	}
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		email = form.cleaned_data.get("email")
		new_guest_email = GuestEmail.objects.get_or_create(email=email)
		request.session['guest_email_id'] = email
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			redirect("/register/")
	return redirect("/register/")


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
	form_class = LoginForm
	success_url = '/'
	template_name = 'accounts/login.html'

	def form_valid(self, form):
		request = self.request
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, email=email, password=password)
		if user is not None:
			if not user.is_active:
				message.error(request, "This user is inactive")
				return super(LoginView, self).form_invalid(form)
			login(request, user)
			user_logged_in.send(user.__class__, instance=user, request=request)
			## retrive the cart and cart items number
			try:
				del request.session['guest_email_id']
			except KeyError:
				pass
			Cart.objects.load_cart(request)
			next_path= self.get_next_url()
			return redirect(next_path)
		return super(LoginView, self).form_invalid(form)



class RegisterView(SuccessMessageMixin,CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'
    success_message ='Activation link has been sent to you email, please check'
    # success_message = 'Please check your email and active you account'


# def login(request):
# 	form = LoginForm(request.POST or None)
# 	context = {
# 		"form": form
# 	}
#
# 	next_ = request.GET.get('next')
# 	next_post = request.POST.get('next')
# 	redirect_path = next_ or next_post or None
#
# 	if form.is_valid():
# 		username = form.cleaned_data.get("username")
# 		password = form.cleaned_data.get("password")
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			auth_login(request, user)
# 			## retrive the cart and cart items number
# 			try:
# 				del request.session['guest_email_id']
# 			except KeyError:
# 				pass
#
# 			Cart.objects.load_cart(request)
# 			if is_safe_url(redirect_path, request.get_host()):
# 				return redirect(redirect_path)
# 			else:
# 				return redirect("/")
# 		else:
# 			print("Error")
# 	return render(request, "login.html", context)
# # def register(request):
# 	form = RegisterForm(request.POST or None)
# 	context = {
# 		"form": form
# 	}
#
# 	if form.is_valid():
# 		print(form.cleaned_data)
# 		email = form.cleaned_data.get("email")
# 		password = form.cleaned_data.get("password")
#
# 		new_user = User.objects.create_user(email, password)
# 		print(new_user)
# 	return render(request, "register.html", context)
