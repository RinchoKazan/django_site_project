from django import forms
from django.contrib.auth.models import User, Group
from django.core import validators

from shopapp.models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'product name',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'product description',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
            }),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'delivery_address', 'products', 'promocode']
        widgets = {
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'cols': 40,
            }),
        }

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(archived=False),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={
          'class': 'form-select',
        })
    )


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']