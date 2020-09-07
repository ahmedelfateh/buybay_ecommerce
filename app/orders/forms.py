from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (("S", "Stripe"), ("P", "PayPal"))


class CheckoutForm(forms.Form):
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Street Address", "id": "address"})
    )
    apartment_address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Apartment or suite", "id": "address-2"}
        ),
    )
    country = CountryField(blank_label="(select country)").formfield(
        widget=CountrySelectWidget(
            attrs={
                "class": "custom-select d-block w-100",
            }
        )
    )
    zip = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "zip"})
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )