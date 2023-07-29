from django.test import TestCase

# Create your tests here.


from django.shortcuts import render
from .models import Image, ImageForm,ImagesForm


# Create your views here.

from functools import wraps
from django.shortcuts import redirect

def hk_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' in request.session:
            # User is authenticated, execute the view function
            return view_func(request, *args, **kwargs)
        else:
            # User is not authenticated, redirect to the login page
            return redirect('/register_user')  # Replace 'login' with the URL name for your login view

    return _wrapped_view

def home(request):
    context = dict()
    if request.method =="POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            context.update({"response": "success"})
        else:
            context.update({"response": "fail"})
    context.update({
        "form":ImageForm(),
        "images":Image.objects.all(),
        })
    return render(request,"home.html",context)


#Upload multiple images
def upload_images(request):
    context = dict()
    if request.method == "POST":
        form = ImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context.update({"response": "success"})
        else:
            context.update({"response": "fail"})
    context.update({
        "form": ImagesForm(),
        "images": Image.objects.all(),
    })
    return render(request, "home.html", context)








def uploaded_images(request):
    context = dict()
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('image')
            for file in files:
                instance = Image(image=file)
                instance.save()
            context.update({"response": "success"})
        else:
            context.update({"response": "fail"})
    context.update({
        "form": ImageForm(),
        "images": Image.objects.all(),
    })
    return render(request, "uploaded_images.html", context)
