from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Cart, Entry
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from django.conf import settings
from .forms import EntryForm, EntryFormSet, inlineFormSet

import stripe


STRIPE_PUBLIC_KEY = getattr(settings, 'STRIPE_PUBLIC_KEY', 'pk_test_G1nt8Wx2P97tG09vDwpkLQjs')
STRIPE_PRIVATE_KEY = getattr(settings, 'STRIPE_PRIVATE_KEY', 'sk_test_KRibT0JWeBwggF5iksBZ6y3j')
stripe.api_key=STRIPE_PRIVATE_KEY


# with intermediate table-----------------------------start
# TEST FORMSET VIEW FOR ORDER---FAILD
def entry_update(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    formset = inlineFormSet(instance=cart_obj)
    if request.method == 'POST':
        formset = inlineFormSet(request.POST,
                               instance=cart_obj)
        if formset.is_valid():
            formset.save()
            return redirect("cart:entry")
    return render(request, 'carts/cart.html', {'formset': formset})

# def entry_update(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     formset = EntryFormSet(queryset=cart_obj.entry_set.all())
#     if request.method == 'POST':
#         formset = EntryFormSet(request.POST,
#                                queryset=cart_obj.entry_set.all())
#         if formset.is_valid():
#             formset.save()
#             return redirect("cart:entry")
#     return render(request, 'carts/home.html', {'formset': formset})

# SUCESSFULL CREATED
def cart_update(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj is not None:
        product_qs = Entry.objects.filter(cart=cart_obj, product=product)
        if product_qs.exists():
            product_obj = product_qs.first()
            product_obj.delete()
            added = False
        else:
            Entry.objects.create(cart=cart_obj, product=product)
            added = True
        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "itemCount": cart_obj.products.count(),
            }
            return JsonResponse(json_data)
        return redirect("cart:home")
# with intermediate table-----------------------------end

# order cart without intermediate table---------------start
def cart_refresh(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()

    products_array = [{"url":x.get_absolute_url(), "name":x.title, "price":x.price, "id":x.id} for x in products]
    return JsonResponse({"products": products_array,"subtotal":cart_obj.subtotal, "total":cart_obj.total})


def cart_page(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, "carts/home.html", {'cart':cart_obj })

# def cart_page(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     entrys = Entry.objects.filter(cart=cart_obj)
#     return render(request, "carts/home.html", {'cart':cart_obj, "entrys":entrys})


# has been disabled
def cart_update_old_remove(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj is not None:
        if product in cart_obj.products.all():
            cart_obj.products.remove(product)
            added = False
        else:
            cart_obj.products.add(product)
            added = True

        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "itemCount": cart_obj.products.count(),
            }
            return JsonResponse(json_data)
        return redirect("carts:cart")
# order cart without intermediate table---------------end


def check_out(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    order_obj = None
    form = LoginForm(request=request)
    address_form = AddressForm()
    guest_form = GuestForm(request=request)
    shipping_address_id = request.session.get('shipping_address_id')
    billing_address_id = request.session.get('billing_address_id')
    address_qs = None

    if new_cart or cart_obj.products.count() == 0:
        return redirect("carts:cart")
    else:
        pass

    billing_profile, new_billing_profile = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, oder_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if shipping_address_id is not None:
            shipping_address_obj = Address.objects.get(id=shipping_address_id)
            order_obj.shipping_address = shipping_address_obj
            del request.session['shipping_address_id']

        if billing_address_id is not None:
            print(billing_address_id)
            billing_address_obj = Address.objects.get(id=billing_address_id)
            order_obj.billing_address = billing_address_obj
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        '''
        update order_obj to done, "paid"
        del request.session['card_id']
        redirect "success"
        '''
    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            billing_profile.charge(order_obj)
            order_obj.mark_paid()
            cart_obj.cart_checkout()
            ##delete session card id after check_ou
            del request.session['cart_id']
            ##delete cart no. with remove cart items.
            del request.session['cart_items']
            if not billing_profile.user:
                billing_profile.deactivate_card()
                try:
                    ## delete the session of guest email check out
                    del request.session['guest_email_id']
                except KeyError:
                    pass

            return redirect("carts:success")

    context={
        "order_obj" : order_obj,
        "billing_profile" : billing_profile,
        "form":form,
        "guest_form" : guest_form,
        "address_form" : address_form,
        "address_qs" : address_qs,
        "public_token":STRIPE_PUBLIC_KEY,

    }
    return render(request, "carts/checkout.html", context)




def success(request):
    return render(request, "carts/success.html")
