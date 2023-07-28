from django.db import models
from django import forms
# Create your models here.

class Image(models.Model):
    photo = models.ImageField(upload_to="uploaded_images")
    generated = models.DateTimeField(auto_now_add=True)


#craete models form
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        labels = {"photo":''}
