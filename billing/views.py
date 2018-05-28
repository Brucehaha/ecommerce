from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import BillingProfile, Card
from django.utils.http import is_safe_url
import json

import stripe
STRIPE_PUBLIC_KEY = getattr(settings, 'STRIPE_PUBLIC_KEY', 'pk_test_G1nt8Wx2P97tG09vDwpkLQjs')
STRIPE_PRIVATE_KEY = getattr(settings, 'STRIPE_PRIVATE_KEY', 'sk_test_KRibT0JWeBwggF5iksBZ6y3j')
stripe.api_key=STRIPE_PRIVATE_KEY

def payment_method(request):
    return render(request, 'billing/card.html', {"public_token": STRIPE_PUBLIC_KEY})


def payment_method_create(request):
    if request.method == "POST" and request.is_ajax():
        token = request.POST.get('token')
        next_= request.POST.get("next_URL")

        billing_obj, created = BillingProfile.objects.new_or_get(request)
        if not billing_obj:
            return JsonResponse({'message': "Please register or login"}, status=401)
        elif token:
            customer = stripe.Customer.retrieve(billing_obj.customer_id)
            card_info = customer.sources.create(source=token)
            card = Card.objects.new_or_get(billing_obj,card_info, token)
            if is_safe_url(next_, request.get_host()):
                next_URL = next_
            return JsonResponse({
                "message": "Card is successfully Created!",
                "nextURL":next_URL,
                })

        else:
            return HttpResponse({"message": "Please Create Create Stripe Customer"}, status=401)
    return HttpResponse("error", status=401)
