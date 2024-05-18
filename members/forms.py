from django import forms
from .models import Students
from django.contrib.auth.hashers import check_password

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model=Students
        fields = ["name", "email", "password"]
        widgets = {
            'password' : forms.PasswordInput
        }

class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                student = Students.objects.get(email=email)
                if not check_password(password, student.password):
                    raise forms.ValidationError("Invalid email or password")
            except Students.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
        return cleaned_data