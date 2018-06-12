from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MailchimpForm
from .models import Mailchimp
from django.conf import settings
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin


User = settings.AUTH_USER_MODEL


def subscribe(request):
    user = request.user
    form = MailchimpForm(request.POST or None)
    if user.is_authenticated:
        mailchimp_obj, created = Mailchimp.objects.get_or_create(user=user)
    else:
        return redirect('/login/?next=/subscription/')
    if created:
        return rediret('/')
    else:
        if request.method == 'POST':
            form = MailchimpForm(request.POST, instance = mailchimp_obj)
            print(mailchimp_obj)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = MailchimpForm(instance = mailchimp_obj)
        return render(request, 'marketing/subscription.html', {"form":form})


class MarketingPreferenceView(SuccessMessageMixin, UpdateView):
    form_class = MailchimpForm
    template_name = 'marketing/subscription.html'
    success_url ='/subscription/'
    success_message = "{calculated_field}" # replace the method by % below
    # success_message = "%(calculated_field)" #

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login/?next=/subscription/')
        return super(MarketingPreferenceView, self).dispatch(*args, **kwargs)

    def get_success_message(self, cleaned_data):
        sub_status = cleaned_data['subscribed']
        msg = "Thank you for updating your email preference!"
        if sub_status:
            msg = "Thank you for opt-in"
        else:
            msg = "We will miss you so much!"
        print(cleaned_data)
        # return self.success_message % dict(
        #     cleaned_data,
        #     calculated_field=msg,
        # )
        return self.success_message.format(calculated_field=msg)# replace the method by % above
    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email opt-in'
        return context

    def get_object(self):
        user = self.request.user
        mailchimp_obj, created = Mailchimp.objects.get_or_create(user=user)
        return mailchimp_obj
