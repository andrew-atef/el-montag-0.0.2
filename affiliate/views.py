from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from shop.models import Cart, Coupon, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Affiliate_profile, Billing
from django.db.models import Q
# Create your views here.
def start(request):
    return render(request, 'affiliate/affiliate-start.html')

def loginn(request):
    try:
        Affiliate_profile.objects.get(user=request.user)
        return redirect('affiliate_dashboard')
    except:
        pass
    if request.method == 'POST':
        try:
            email = request.POST['email']
            username = User.objects.get(email=email).username
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('affiliate_dashboard')
            else:
                messages.success(request, f'خطا فى البيانات')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            messages.success(request, f'خطا فى البيانات')
    return render(request, 'affiliate/login.html')



@login_required(login_url='home')
def logout_v(request):
    logout(request)  
    return redirect('home')


def signup(request):
    try:
        Affiliate_profile.objects.get(user=request.user)
        return redirect('affiliate_dashboard')
    except:
        pass
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            number1 = request.POST.get('number1')
            email = request.POST.get('email')
            notes = request.POST.get('notes')
            password1 = request.POST.get('password1')

            if len(first_name) < 5:
                messages.success(request, f'خطا فى الاسم')
                return redirect('signup')
            if len(number1) != 11:
                messages.success(request, f'خطا فى الرقم')
                return redirect('signup')
            if len(password1) < 8:
                messages.success(request, f'يجب ان تكون كلمه المرور مكونه من 8 حروف او ارقام على الاقل')
                return redirect('signup')

            new_user = User.objects.create_user(email, email, password1)
            new_user.first_name = first_name
            new_user.last_name = number1
            new_user.save()
            try:
                profile = Affiliate_profile.objects.create(user=new_user, notes=notes)
                Coupon.objects.create(name=profile.affiliate_coupon)
            except:
                pass
            user = authenticate(username=email, password=password1)
            login(request, user)
            try:
                Cart.objects.create(user=user)
            except:
                pass
            return redirect('affiliate_dashboard')
        except:
            messages.success(request, f'خطا فى البيانات')
            return redirect('signup')
    else:
        pass
    return render(request, 'affiliate/register.html')



def dashboard(request):
    context = {}
    try:
        context['dashboard'] = True
        profile = Affiliate_profile.objects.get(user=request.user)
        context['profile'] = profile


        try:
            my_orders =  Order.objects.filter(Q(coupon=profile.affiliate_coupon) &  Q(status='تم التوصيل') | Q(affiliate_code=profile.affiliate_code) & Q(status='تم التوصيل'))
            print(my_orders)
            total_sales = 0
            earn = 0
            for order in my_orders:
                total_sales += float(order.total)
                earn += float(order.earn)
            context['total_sales'] = total_sales
            context['my_earn'] = earn
            try:
                context['Orders_Delivered'] = Order.objects.filter(Q(coupon=profile.affiliate_coupon) &  Q(status='تم التوصيل') | Q(affiliate_code=profile.affiliate_code) &  Q(status='تم التوصيل')).count()
            except:
                pass
            try:
                context['all_Orders'] = Order.objects.filter(Q(coupon=profile.affiliate_coupon) &  Q(status='جاري تاكيد الطلب') | Q(status='جاري تجهيز الطلب') | Q(status='قيد التوصيل') | Q(status='تعليق التوصيل') | Q(status='تم إلغاء أو رفض الطلب') | Q(affiliate_code=profile.affiliate_code) &  Q(status='جاري تاكيد الطلب') | Q(status='جاري تجهيز الطلب') | Q(status='قيد التوصيل') | Q(status='تعليق التوصيل') | Q(status='تم إلغاء أو رفض الطلب')).count()
            except:
                pass
        except:
            context['total_sales'] = 0
            context['my_earn'] = 0
            context['Orders_Delivered'] = 0
            context['all_Orders'] = 0
            pass


    except:
        return redirect('start')
    return render(request, 'affiliate/dashboard.html', context)



def customer_orders(request):
    context = {}
    try:
        context['customer_orders'] = True
        profile = Affiliate_profile.objects.get(user=request.user)
        context['profile'] = profile
        try:
            my_orders =  Order.objects.filter(Q(coupon=profile.affiliate_coupon) | Q(affiliate_code=profile.affiliate_code))
            context['orders'] = my_orders
        except:
            pass


    except:
        return redirect('start')
    return render(request, 'affiliate/customer_orders.html', context)



def billing(request):
    context = {}
    context['billing'] = True
    try:
        profile = Affiliate_profile.objects.get(user=request.user)
        context['profile'] = profile
        try:
            my_orders =  Order.objects.filter(Q(coupon=profile.affiliate_coupon) & Q(status='تم التوصيل') | Q(affiliate_code=profile.affiliate_code) & Q(status='تم التوصيل'))
            earn = 0
            for order in my_orders:
                earn += float(order.earn)
            context['my_earn'] = float(earn) - float(profile.withdrawn)
        except:
            pass

        my_billis = Billing.objects.filter(user=request.user)
        context['billis'] = my_billis

    except:
        return redirect('start')
    return render(request, 'affiliate/billing.html', context)

def add_billing(request):
    context = {}
    if request.method == 'POST':
        transfer_amount = request.POST.get('transfer_amount')
        number1 = request.POST.get('number1')
        try:
            Billing.objects.create(user=request.user, status='قيد المراجعه', transfer_amount=transfer_amount, number1=number1 )
            profile = Affiliate_profile.objects.filter(user=request.user)
            profile.update(withdrawn = float(transfer_amount)) 
        except:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))