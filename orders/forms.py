from django import forms
from orders.models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address', 'city', 'zip_code', 'country']


class OrderForm(forms.Form):
    full_name = forms.CharField(label="Full name", max_length=100)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", max_length=20)
    address = forms.CharField(label="Delivery Address", widget=forms.Textarea)
    alt_recipient = forms.CharField(label="Alternate recipient name", max_length=100, required=False)
    payment_method = forms.ChoiceField(choices=[
        ("card", "Credit/Debit Card"),
        ("paypal", "PayPal"),
        ("cod", "Cash on Delivery"),
    ])
    installments = forms.IntegerField(min_value=1, max_value=12, initial=1, label="Number of payments")
    note = forms.CharField(widget=forms.Textarea, required=False, label="Additional notes")
