from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from shop.models import Order, Cart, Address_details, Governorates
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect



# Create your views here.
def loginn(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            try:
                email = request.POST['email']
                username = User.objects.get(email=email).username
                password = request.POST['password1']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except:
                messages.success(request, f'خطا فى البيانات')
    return render(request, 'user/login.html')



@login_required(login_url='home')
def logout_v(request):
    logout(request)  
    return redirect('home')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            try:
                first_name = request.POST.get('first_name')
                email = request.POST.get('email')
                password1 = request.POST.get('password1')
                if len(first_name) < 5:
                    messages.success(request, f'خطا فى الاسم')
                    return redirect('signup')
                if len(password1) < 8:
                    messages.success(request, f'يجب ان تكون كلمه المرور مكونه من 8 حروف او ارقام على الاقل')
                    return redirect('signup')
                new_user = User.objects.create_user(email, email, password1)
                new_user.first_name = first_name
                try:
                    Cart.objects.create(user=new_user)
                except:
                    pass
                new_user.save()
                user = authenticate(username=email, password=password1)
                login(request, user)
                return redirect('home')
            except:
                messages.success(request, f'خطا فى البيانات')
                return redirect('signup')
        else:
            pass
    return render(request, 'user/register.html')


@login_required(login_url='home')
def profile(request):
    context = {}
    # get governorates and regions
    try:
        governorates = Governorates.objects.all()
        regions = ''
        for governorate in governorates:
            for x in governorate.region.splitlines():
                try:
                    id = request.POST.get('address_id')
                    instance = Address_details.objects.get(id=id)
                    if x == instance.region:
                        regions += f'''<option data-ref="{x}" data-belong="{governorate}" selected value="{x}" >{x}</option>''' 
                    else:
                        regions += f'''<option data-ref="{x}" data-belong="{governorate}" value="{x}" >{x}</option>''' 
                except:
                    regions += f'''<option data-ref="{x}" data-belong="{governorate}" value="{x}" >{x}</option>''' 

        context['governorates'] = governorates
        context['regions'] = regions
    except:
        pass
    # end governorates and regions

    # get user address
    try:
        addresses = Address_details.objects.filter(user=request.user.id, hidden=False)
        context['addresses'] = addresses
    except:
        pass
    return render(request, 'user/profile.html', context)

# update address
@login_required(login_url='home')
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                u = User.objects.get(id=request.user.id)
                user = authenticate(request, username=u.username, password=current_password)
                if user is not None:
                    u.set_password(request.POST.get('password1'))
                    u.save()
                    return redirect('home')
                else:
                    messages.success(request, f' حدث خطا ')
            except:
                messages.success(request, f' حدث خطا ')  
        else:
            messages.success(request, f' حدث خطا ') 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# end update address


# update address
@login_required(login_url='home')
def update_profile(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            number1 = request.POST.get('number1')
            email = request.POST.get('email')
            if len(first_name) < 5:
                messages.success(request, f' خطا فى الاسم ')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if len(number1) != 11 :
                messages.success(request, f' خطا فى الرقم ')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            User.objects.filter(id=request.user.id).update(first_name=first_name, last_name=number1, username=email, email=email)
        except:
            messages.success(request, f' حدث خطا ')   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# end update address


@login_required(login_url='home')
def my_orders(request):
    context = {}
    try:
        orders = Order.objects.filter(user=request.user).order_by('-id')
        context['orders'] = orders
    except:
        pass
    return render(request, 'user/my_orders.html', context)



@login_required(login_url='home')
def order_details(request, code):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, order_code=code)
        except:
            return redirect('home')
    return render(request, 'user/order-details.html', {'order': order})
