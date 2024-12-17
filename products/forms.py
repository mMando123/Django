from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'availability']
        labels = {
            'name': 'اسم المنتج',
            'price': 'السعر',
            'description': 'الوصف',
            'image': 'صورة المنتج',
            'availability': 'حالة التوفر',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المنتج'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'أدخل السعر'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'أدخل وصف المنتج'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
        }
