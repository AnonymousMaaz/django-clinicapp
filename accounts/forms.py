import re
from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if password != password2:
            raise forms.ValidationError("Passwords do not match")

        # Custom validation
        self.validate_password_strength(password)
        self.check_personal_information_similarity(password, username, email, first_name, last_name)

        return cleaned_data

    def validate_password_strength(self, password):
        # Use Django's built-in validators
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)

        if password.isdigit():
            raise forms.ValidationError("Password can't be entirely numeric.")

        # List of commonly used passwords
        common_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123', 'password1']
        if password.lower() in common_passwords:
            raise forms.ValidationError("Password can't be a commonly used password.")

    def check_personal_information_similarity(self, password, username, email, first_name, last_name):
        personal_info = [username, email, first_name, last_name]
        for info in personal_info:
            if info and re.search(r'\b' + re.escape(info) + r'\b', password, re.IGNORECASE):
                raise forms.ValidationError("Password can't be too similar to your personal information.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Set staff status
        if commit:
            user.save()
            # Assign 'staff' role to the user
            staff_group, created = Group.objects.get_or_create(name='staff')
            user.groups.add(staff_group)
        return user
