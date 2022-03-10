from django.forms import ModelForm
from django import forms
from .models import Item, Address_details, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class makeitem(ModelForm):
    class Meta():
        model = Item
        fields = ['product', 'quantity', 'cart']


class makeuser(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class Makeaddress(ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'يفضل ان يكون الاسم ثلاثي'}))
    number1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'مثال : 01234567890'}))
    number2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'مثال : 01234567890'}), required=False)
    region = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'مثال : شارع كلية آداب - برج طيبة - عمارة 7 - الدور الخامس'}))
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'مثال : انا غير متواجد يوم الجمعة بالعنوان المذكور بالأعلى ولاكنى متواجد طوال الأسبوع من السبت الى الخميس'}), required=False)

    class Meta():
        model = Address_details
        fields = ['user', 'full_name', 'number1', 'number2',
                  'governorate', 'region', 'address', 'active']


class Makeorder(ModelForm):
    full_name = forms.CharField(widget=forms.TextInput())
    number1 = forms.CharField(widget=forms.TextInput())
    number2 = forms.CharField(widget=forms.TextInput(), required=False)
    governorate = forms.CharField(widget=forms.TextInput())
    region = forms.CharField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())
    notes = forms.CharField(widget=forms.Textarea(), required=False)
    items = forms.CharField(widget=forms.Textarea())

    class Meta():
        model = Order
        fields = ['user', 'full_name', 'number1', 'number2', 'governorate', 'region', 'address', 'notes', 'items', 'coupon', 'coupon_discount', 'payable', 'total','earn','affiliate_code', 'shipping']
