from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MailchimpForm
from .models import Mailchimp
from django.conf import settings


User = settings.AUTH_USER_MODEL


def subscription(request):
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
        else:
            form = MailchimpForm(instance = mailchimp_obj)
        return render(request, 'marketing/subscription.html', {"form":form})
