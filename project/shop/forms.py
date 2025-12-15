from django import forms
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)