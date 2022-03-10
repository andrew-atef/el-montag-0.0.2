from asyncio.windows_events import NULL
from .models import Category, Coupon, Item, Cart, Address_details
from affiliate.models import Affiliate_profile
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def message_processor(request):
        context = {}
        ###################
        try:
                Affiliate_profile.objects.get(user=request.user)
                context['is_affiliate'] = True
        except:
                pass
        try:
                categorys = Category.objects.all()
                context['categorys'] = categorys
        except:
                pass
        ###################

        ###################
        try:
                total = 0
                earn = 0
                cart = Cart.objects.get(user=request.user)
                if request.GET.get('a'):
                        try:
                                coupon = Cart.objects.get(user=request.user).coupon
                                if coupon is not None:
                                        pass
                                else:
                                        cart.affiliate_code = request.GET.get('a')
                                        cart.save()
                        except:
                                pass
                context['affiliate_code'] = cart.affiliate_code
                items = Item.objects.filter(cart=cart)
                for item in items:
                        earn += item.product.affiliate_earn
                        if item.product.sale_price > 0 :
                                total += float(item.quantity) * float(item.product.sale_price)
                        else:
                                total += float(item.quantity) * float(item.product.price)

                context['items'] = items
        except:
                pass
        ###################

        ###################
        try:
                shipping = Address_details.objects.get(user=request.user, active=True).shipping
        except:
                shipping = 0

        context['shipping'] = shipping
        ###################

        ###################
        try:
                addressActive = Address_details.objects.get(user=request.user, active=True)
                context['addressActive'] = addressActive
        except:
                pass

        ###################


        ###################
        try:
                coupon = Cart.objects.get(user=request.user).coupon
                if coupon is not None:
                        discount = 0
                        for item in items:
                                discount += float(item.product.coupon_discount) * float(item.quantity)
                        payable = float(total + shipping) - float(discount)
                else:
                        discount = 0
                        payable = total + shipping
        except:
                coupon = False
                discount = 0
                payable = total + shipping
        context['coupon'] = coupon
        context['discount'] =  discount
        context['payable'] = payable
        context['earn'] = earn

        context['total'] = total
        return context


