from django import forms


class AccessForm(forms.Form):
    email = forms.EmailField(
        label="CBS email address",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "name@gsb.columbia.edu",
            }
        ),
    )
    access_code = forms.CharField(
        label="Class access code",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Enter the class access code",
            }
        ),
    )

