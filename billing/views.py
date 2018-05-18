from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse


import stripe
STRIPE_PUBLIC_KEY = getattr(settings, 'STRIPE_PUBLIC_KEY', 'pk_test_G1nt8Wx2P97tG09vDwpkLQjs')
STRIPE_PRIVATE_KEY = getattr(settings, 'STRIPE_PRIVATE_KEY', 'sk_test_KRibT0JWeBwggF5iksBZ6y3j')
stripe.api_key=STRIPE_PRIVATE_KEY

def payment_method(request):
    return render(request, 'billing/card.html', {"publish_key": STRIPE_PUBLIC_KEY})


def payment_method_create(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "Done"})
    return HttpResponse("error", status_code=401)
