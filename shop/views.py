from django.shortcuts import render
from .models import Product, Cart, Category, Item, Address_details, Coupon, Order, Governorates, Features, Home_grid_slider
from affiliate.models import Affiliate_profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from .forms import Makeorder
from django.core.paginator import Paginator


def if_login(next, request):
    print(next)
    match next:
        case '/add_to_cart/':
            messages.success(request, 'سجل دخول الان فى اقل من 5 دقائق علشان تقدر تضيف اى منتج تحبه للعربه')
            return redirect('login')
        case '/mycart/':
            messages.success(request, 'سجل دخول الان فى اقل من 5 دقائق علشان تقدر تضيف اى منتج تحبه للعربه')
            return redirect('login')
        case '/add_coupon/':
            messages.success(request, 'سجل دخول الان فى اقل من 5 دقائق علشان تقدر تضيف اى منتج تحبه للعربه')
            return redirect('login')
        case '/delete_item/':
            messages.success(request, 'سجل دخول الان فى اقل من 5 دقائق علشان تقدر تضيف اى منتج تحبه للعربه')
            return redirect('login')
        case '/action_plus/':
            messages.success(request, 'سجل دخول الان فى اقل من 5 دقائق علشان تقدر تضيف اى منتج تحبه للعربه')
            return redirect('login')
        case '/checkout/':
            messages.success(request, 'سجل دخول الان فى اقل من 5 دقائق علشان تقدر تضيف اى منتج تحبه للعربه')
            return redirect('login')
        case _:
            return redirect('home')

def affiliate_only(request):
    try:
        Affiliate_profile.objects.get(user=request.user)
        messages.success(request, f' يجب التسجيل بحساب عادى انت الان تستخدم حساب مسوق ')
        return redirect('affiliate/dashboard')
    except:
        pass


def home(request):
    #################
    if request.GET.get('next'):
        return if_login(request.GET.get('next'), request)
    #################

    context = {}
    products = Product.objects.all().order_by('-id')[:12]
    categorys = Category.objects.all()

    context['imgs'] = Home_grid_slider.objects.all()

    context['products'] = products
    context['categorys'] = categorys
    ############
    try:
        category = Category.objects.get(home_slider='category1')
        context['category1_name'] = category
        context['category1_slug'] = category.slug
        context['category1'] = Product.objects.filter(category=category).order_by('-id')[:6]
    except:
        pass
    #############
    try:
        category = Category.objects.get(home_slider='category2')
        context['category2_name'] = category
        context['category2_slug'] = category.slug
        context['category2'] = Product.objects.filter(category=category).order_by('-id')[:6]
    except:
        pass
    #############
    try:
        category = Category.objects.get(home_slider='category3')
        context['category3_name'] = category
        context['category3_slug'] = category.slug
        context['category3'] = Product.objects.filter(category=category).order_by('-id')[:6]
    except:
        pass
    return render(request, 'shop/home.html', context)


# category page
def category(request, category):
    context = {}
    context['current_category'] = category
    category = Category.objects.get(slug=category)
    products = Product.objects.filter(category=category).order_by('-id')[:12]
    categorys = Category.objects.all()
    if request.GET.get('max') or request.GET.get('min'):
        max = request.GET.get('max')
        min = request.GET.get('min')
        try:
            products = Product.objects.filter(Q(sale_price__gt = 0) & Q(sale_price__lte = max) | Q(price__lte = max) , Q(sale_price__gte = min) | Q(price__gte = min),category=category).order_by('-id')[:12]
        except:
            pass

    if request.GET.get('search'):
        products = Product.objects.filter(Q(title__contains=request.GET.get('search')) | Q(desc__contains=request.GET.get('search'))).order_by('-id') 
    else:
        pass


    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context['products'] = products_page
    context['categorys'] = categorys
    
    return render(request, 'shop/category.html', context)
# end category page

# category page
def all_products(request):
    context = {}
    products = Product.objects.all().order_by('-id')[:12]
    categorys = Category.objects.all()
    if request.GET.get('max') or request.GET.get('min'):
        max = request.GET.get('max')
        min = request.GET.get('min')
        try:
            products = Product.objects.filter(Q(sale_price__gt = 0) & Q(sale_price__lte = max) | Q(price__lte = max) , Q(sale_price__gte = min) | Q(price__gte = min)).order_by('-id')[:12]
        except:
            pass
    if request.GET.get('search'):
        products = Product.objects.filter(Q(title__contains=request.GET.get('search')) | Q(desc__contains=request.GET.get('search'))).order_by('-id') 
    else:
        pass
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context['products'] = products_page
    context['categorys'] = categorys
    context['all_products'] = True
    return render(request, 'shop/category.html', context)
# end category page


def product_page(request,slug):
    context = {}
    product = Product.objects.get(slug=slug)
    products = Product.objects.filter(category=product.category).order_by('-id')[:4]
    descs = product.desc.splitlines()
    x = ''
    for desc in descs:
        x += f"<p>{desc}</p>" 
    context['product'] = product
    context['products'] = products
    context['desc'] = x
    context['features'] = Features.objects.all()
    

    return render(request, 'shop/product-page.html', context)




# add coupon
@login_required(login_url='home')
def add_coupon(request):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon')
        try:
            coupon = Coupon.objects.get(name=coupon_name)
            try:
                Order.objects.get(user=request.user, coupon=coupon) 
                messages.success(request, f' الكوبون مستخدم من قبل ')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                Cart.objects.filter(user=request.user).update(coupon=coupon)
                Cart.objects.filter(user__id=request.user.id).update(affiliate_code='')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            messages.success(request, f' الكوبون خطا ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# add coupon



# item
@login_required(login_url='home')
def delete_item(request):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    if request.method == 'POST':
        if request.POST.get('item'):
            item = Item.objects.get(id=request.POST.get('item'))
            item.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='home')
def add_to_cart(request):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    if request.method == 'POST':
        if request.POST.get('cart') and request.POST.get('product') and int(request.POST.get('quantity')) > 0:
            cart = Cart.objects.get(user__id=request.POST.get('cart'))
            product = Product.objects.get(id=request.POST.get('product'))
            try:
                id = Item.objects.get(cart=cart, product=product).id
                Item.objects.update_or_create(id=id, defaults={'quantity': request.POST.get('quantity'), 'product': product})
                messages.success(request, f' تم اضافه ( {product} )الى العربه  ')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                Item.objects.create(quantity=request.POST.get('quantity'), product=product, cart=cart)
                messages.success(request, f' تم اضافه ( {product} )الى العربه  ')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, f'خطا اقل عدد قطع هو 1 ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='home')
def action_plus(request, id):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    quantity = Item.objects.get(id=id).quantity
    quantity += 1
    Item.objects.update_or_create(id=id, defaults={'quantity': quantity})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='home')
def action_minus(request, id):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    quantity = Item.objects.get(id=id).quantity
    if quantity <= 1: 
        messages.success(request, f' 1 هو اقل عدد قطع ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        quantity -= 1
    Item.objects.update_or_create(id=id, defaults={'quantity': quantity})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# end item


# checkout page
@login_required(login_url='home')
def mycart(request):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################



    return render(request, 'shop/mycart.html')
# checkout page


# checkout page
@login_required(login_url='home')
def checkout(request):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    context = {}
    # get governorates and regions
    cart = Cart.objects.get(user=request.user)
    items = Item.objects.filter(cart=cart)
    if (items.count() == 0):
            messages.success(request, f' يجب اضافه منتجات للعربه اولا ')
            return redirect('mycart')
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
    # end user address

    return render(request, 'shop/checkout.html', context)
# checkout page









# add address
@login_required(login_url='home')
def add_address(request):

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        number1 = request.POST.get('number1')
        number2 = request.POST.get('number2')
        governorate = request.POST.get('governorate')
        region = request.POST.get('region')
        address = request.POST.get('address')
        try:
            shipping = Governorates.objects.get(name=governorate).shipping
        except:
            shipping = 0
        if len(full_name) > 7 and  len(number1) == 11 and  len(governorate) >= 3 and  len(region) >= 3 and  len(address) >= 7 :
            if request.POST.get('title'):
                Address_details.objects.filter(user=request.user).update(active=False)
                title = request.POST.get('title')
                Address_details.objects.filter(user=request.user, title=title).update(user=request.user,full_name=full_name, number1=number1, number2=number2, governorate=governorate, region=region, address=address,shipping=shipping, active=True)
                messages.success(request, f'تم تعديل العنوان بنجاح')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                Address_details.objects.filter(user=request.user).update(active=False)
                id = Address_details.objects.create(user=request.user,full_name=full_name, number1=number1, number2=number2, governorate=governorate, region=region, address=address,shipping=shipping, active=True)
                Address_details.objects.filter(user=request.user, id=id.id).update(title=f"A{id.id+10000}")
                messages.success(request, f'تم اضافه العنوان بنجاح')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'يرجا اكمال البيانات بطريقه صحيحه.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# end add address


# delete address
@login_required(login_url='home')
def delete_address(request, id):


    address = Address_details.objects.get(id=id, user=request.user)
    if address.active is True:
        address.delete()
        try:
            address = Address_details.objects.filter(user=request.user)[0]
            address.active = True
            address.save()
        except:
            pass
    else:
        address.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# end delete address



# activate address
@login_required(login_url='home')
def activate_address(request, id):

    Address_details.objects.filter(user=request.user).update(active=False)
    Address_details.objects.filter(id=id, user=request.user).update(active=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# activate address



# add order page
@login_required(login_url='home')
def add_order(request):
    ##################
    if affiliate_only(request):
        return redirect('affiliate_dashboard')
    ##################

    if request.method == 'POST':
        form = Makeorder(request.POST)
        if request.POST.get('address') == '':
            messages.error(request, 'يجب اضافه عنوان اولا ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if form.is_valid():
            cart = Cart.objects.filter(user__id=request.user.id)


            id = form.save().id
            my_order = Order.objects.filter(id=id)
            my_order.update(order_code=(id+1000), status='جاري تاكيد الطلب')
            messages.error(request, 'شكرا على اتمامك الطلب ستصلك مكالمه تاكيديه فى غضون ساعات للتاكيد ')

            # try:
            #     affiliate_profile = Affiliate_profile.objects.filter(Q(affiliate_coupon = my_order[0].coupon) | Q(affiliate_code = my_order[0].affiliate_code))
            #     if affiliate_profile[0].my_balance != '':          
            #         print(float(my_order[0].earn))
            #         print(float(affiliate_profile[0].my_balance))
            #         affiliate_profile.update( my_balance = (float(my_order[0].earn) + float(affiliate_profile[0].my_balance) ) ) 
            #     else:
            #         affiliate_profile.update( my_balance = my_order[0].earn )
            # except:
            #     pass

            cart.update(coupon='')
            cart.update(affiliate_code='')
            items = Item.objects.filter(cart=cart[0])
            for item in items:
                item.delete()
            return redirect(f'/order-details/{id+1000}')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# add order page



def privacy_policy(request):
    return render(request, 'shop/privacy-policy.html')

def about_us(request):
    return render(request, 'shop/about-us.html')

    