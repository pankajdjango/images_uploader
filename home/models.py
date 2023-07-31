from django.db import models
from django import forms
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from multiupload.fields import MultiFileField
import os


# Create your models here.
class UserAccount(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    mobile_no = models.CharField(max_length=10,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    generated = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def check_password(self,password):
        if self.password == password:
            return True
        else :
            return False


def uploaded_images(instance, filename):
    if not (Image.objects.filter(name=instance.name).exists()) :
        root, ext = os.path.splitext(filename)
        return os.path.join("uploaded_images", f"{root}{ext}")
    else:
        return os.path.join("uploaded_images", "duplicate", filename)


class Image(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to=uploaded_images)
    generated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    duplicate = models.BooleanField(default=False)
    source = models.CharField(max_length=50, default="image server")
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super(Image, self).delete(*args, **kwargs)


#craete models form
class ImagesForm(forms.ModelForm):
    photo = MultiFileField(min_num=1, max_num=50, max_file_size=1024*1024*5)  # Limiting to 5 files, each up to 5 MB.for multiupload
    class Meta:
        model = Image
        fields = ('photo',)
        labels = {"photo": ''}

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('photo',)
        labels = {"photo":''}


class UserAccountForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super().__init__(*args, **kwargs)
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'mobile_no', 'email', 'password', 'confirm_password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data['mobile_no']
        if not (mobile_no.startswith('6') or mobile_no.startswith('7') or mobile_no.startswith('8') or mobile_no.startswith('9')):
            raise forms.ValidationError('Invalid mobile number.')
        if not len(mobile_no) == 10 or not mobile_no.isdigit():
            raise forms.ValidationError('Mobile number must be 10 digits.')
        return mobile_no

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            # messages.error(self.request, "Passwords do not match.")
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    mobile_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile or Email'}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),)

    def clean_mobile_or_email(self):
        mobile_or_email = self.cleaned_data['mobile_or_email']
        try:
            if mobile_or_email.isdigit():
                user = UserAccount.objects.get(mobile_no=mobile_or_email)  # Try to find the user by mobile number
            else:
                user = UserAccount.objects.get(email=mobile_or_email)  # Try to find the user by email
        except UserAccount.DoesNotExist:
            raise ValidationError(_('Invalid mobile or email address.'))
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        if password and 'mobile_or_email' in cleaned_data:
            user = cleaned_data['mobile_or_email']
            if not user.check_password(password):
                raise ValidationError(_('Incorrect password.'))
        return cleaned_data
