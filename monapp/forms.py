from django import forms
from .models import Order, Product, ProductItem, ProductAttribute, ProductAttributeValue, Fournisseur

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('price_ttc', 'status')

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = '__all__'

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

class ProductAttributeValueForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('status', )

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['product_id'].widget.attrs['readonly'] = True
        self.fields['fournisseur_id'].widget.attrs['readonly'] = True
        self.fields['prix'].widget.attrs['readonly'] = True
