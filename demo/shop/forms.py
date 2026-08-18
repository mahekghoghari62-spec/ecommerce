import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address, CustomerProfile


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomerProfile
        fields = ["phone"]
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields["email"].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if self.user is not None:
            self.user.email = self.cleaned_data["email"]
            if commit:
                self.user.save()
        return profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line1", "address_line2", "city", "state", "pincode", "address_type", "is_default"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "pincode": forms.TextInput(attrs={"class": "form-control"}),
            "address_type": forms.Select(attrs={"class": "form-select"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CustomerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your full name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "10-digit mobile number"}),
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "phone", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Choose a username"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Create a password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm your password"})

    # ---------- Full Name ----------
    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()

        if len(full_name) < 3:
            raise forms.ValidationError("Full name must be at least 3 characters long.")

        if not re.match(r"^[A-Za-z ]+$", full_name):
            raise forms.ValidationError("Full name can only contain letters and spaces.")

        # collapse multiple spaces (e.g. "Mahek   Ghoghari" -> "Mahek Ghoghari")
        return re.sub(r"\s+", " ", full_name)

    # ---------- Email ----------
    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    # ---------- Phone ----------
    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain digits only.")

        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")

        if not re.match(r"^[6-9]\d{9}$", phone):
            raise forms.ValidationError("Enter a valid 10-digit Indian mobile number.")

        if CustomerProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("An account with this phone number already exists.")

        return phone

    # ---------- Username ----------
    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long.")

        if not re.match(r"^[A-Za-z0-9_]+$", username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores.")

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")

        return username

    # ---------- Password ----------
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        if not re.search(r"[A-Z]", password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"[0-9]", password1):
            raise forms.ValidationError("Password must contain at least one number.")

        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data["full_name"].strip()
        parts = full_name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            CustomerProfile.objects.create(user=user, phone=self.cleaned_data["phone"])
        return user