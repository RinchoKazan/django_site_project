from django import forms
from django.contrib.auth.models import User
from django.core import validators

from shopapp.models import Product, Order


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         label='Product description',
#         widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}),
#         validators=[validators.RegexValidator(
#             regex=r'greate',
#             message='Field must contain word "greate"',
#         )],
#     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount']

class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(archived=False),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'promocode', 'user', 'products']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }