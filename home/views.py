from django.shortcuts import render
from .models import Image, ImageForm


# Create your views here.
def home(request):
    context = dict()
    if request.method =="POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    context.update({
        "form":ImageForm(),
        "images":Image.objects.all(),
        "response": "success",
        })
    return render(request,"home.html",context)
