from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MailchimpForm
from .models import Mailchimp
from .mixins import CsrfExemptMixin
from .utils import  MailchimpHandler
from django.conf import settings
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse



User = settings.AUTH_USER_MODEL
LIST_ID = getattr(settings, 'MAILCHIMP_LIST_ID', None)


def subscribe(request):
    user = request.user
    form = MailchimpForm(request.POST or None)
    if user.is_authenticated:
        mailchimp_obj, created = Mailchimp.objects.get_or_create(user=user)
    else:
        return redirect('/login/?next=/subscription/')
    if created:
        return rediret('/account')
    else:
        if request.method == 'POST':
            form = MailchimpForm(request.POST, instance = mailchimp_obj)
            print(mailchimp_obj)
            if form.is_valid():
                form.save()
                return redirect('/account')
        else:
            form = MailchimpForm(instance = mailchimp_obj)
        return render(request, 'marketing/subscription.html', {"form":form})


class MarketingPreferenceView(SuccessMessageMixin, UpdateView):
    form_class = MailchimpForm
    template_name = 'marketing/subscription.html'
    success_url ='/account/'
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



"""
POST METHOD
data[merges][LNAME]:
data[merges][EMAIL]: tech@goldenfield.com.au
data[ip_opt]: 203.220.34.84
data[email]: tech@goldenfield.com.au
data[action]: unsub
fired_at: 2018-06-13 03:58:54
data[id]: 71e7c68a8e
data[reason]: manual
data[list_id]: fbe3f0b349
type: unsubscribe
data[email_type]: html
data[web_id]: 42521203
data[merges][FNAME]: Tech
"""
class MailchimpWebhooView(CsrfExemptMixin, View):
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Thanks", status=200)
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(LIST_ID):
            email = data.get('data[email]')
            type = data.get('type')
            response_code, response_data = MailchimpHandler().status_check(email)
            sub_status = response_data['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed == (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed == (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = Mailchimp.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed=is_subbed,
                            mailchimp_subscribed=mailchimp_subbed,
                            messages=str(data)
                            )
        return HttpResponse("Thanks", status=200)

def mailcimp_webhook_view(request):
    data = request.POST
    list_id = data.get('data[list_id]')
    if str(list_id) == str(LIST_ID):
        email = data.get('data[email]')
        type = data.get('type')
        response_code, response_data = MailchimpHandler().status_check(email)
        sub_status = response_data['status']
        is_subbed = None
        mailchimp_subbed = None
        if sub_status == "subscribed":
            is_subbed, mailchimp_subbed == (True, True)
        elif sub_status == "unsubscribed":
            is_subbed, mailchimp_subbed == (False, False)
        if is_subbed is not None and mailchimp_subbed is not None:
            qs = Mailchimp.objects.filter(user__email__iexact=email)
            if qs.exists():
                qs.update(
                        subscribed=False,
                        mailchimp_subscribed=False,
                        messages=str(data)
                        )
    return HttpResponse("Thanks", status=200)
