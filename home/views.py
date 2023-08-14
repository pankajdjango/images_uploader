from django.shortcuts import render,redirect
from .models import Image, ImageForm, ImagesForm, UserAccountForm,LoginForm,UserAccount, DocsForm,Docs
from django.contrib import messages
from .authentication import hk_required,already_login,hk_or_login_required,admin_required
import os
# Create your views here.

@hk_or_login_required
def home(request):
    context = dict()
    user_id=request.session.get("user_id",1)
    user_obj = UserAccount.objects.get(user_id=user_id)
    if request.method =="POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            file = request.FILES.getlist('photo')[0]
            name, extension = os.path.splitext(file.name)
            image_name = name + extension
            duplicate = True if (Image.objects.filter(name=image_name).exists()) else False
            obj = Image(photo=file,name=image_name,duplicate=duplicate,user_id=user_obj)
            obj.save()
            context.update({"response": "success"})
        else:
            context.update({"response": "fail"})
    if UserAccount.objects.filter(user_id=user_id,is_staff=True).exists():
        images = Image.objects.filter().order_by('-id')
    else:
        images = Image.objects.filter(user_id=user_obj,active=True).order_by('-id')
    context.update({
        "form":ImageForm(),
        "images":images,
        })
    return render(request,"home.html",context)

#Upload multiple images
@admin_required
def upload_images(request):
    context = dict()
    user_id=request.session.get("user_id",1)
    user_obj = UserAccount.objects.get(user_id=user_id)
    if request.method == "POST":
        form = ImagesForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('photo')
            for file in files:
                name, extension = os.path.splitext(file.name)
                image_name = name + extension
                duplicate = True if (Image.objects.filter(name=image_name).exists()) else False
                obj = Image(photo=file,name=image_name,duplicate=duplicate,user_id=user_obj)
                obj.save()
            context.update({"response": "success"})
        else:
            context.update({"response": "fail"})
    context.update({
        "form": ImagesForm(),
        "images":Image.objects.all().order_by('-id'),
    })
    return render(request, "uploaded_images.html", context)

@hk_or_login_required
def delete(request):
    id = request.GET.get("id")
    super_user = UserAccount.objects.filter(user_id=request.session.get("user_id"),is_staff=True).exists()
    try:
        if super_user:
                image = Image.objects.get(id=id)
                image.delete()
        else:
            document = Image.objects.get(id=id)
            document.active = False
            document.save()
            return redirect("/")
    except Exception as e:
        pass
    
    return redirect("/upload")

@already_login
def register_user(request):
    context = dict()
    form = UserAccountForm()
    login_form = LoginForm()
    if request.method == 'POST':
        if "login" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.cleaned_data['mobile_or_email']
                password = login_form.cleaned_data['password']
                if user is not None and user.check_password(password):
                    request.session["username"] = f"{user.first_name} {user.last_name}"
                    request.session["user_id"]=user.user_id
                    messages.success(request, 'You have loggedin successfully.')
                    return redirect("/")
            else:
                messages.error(request, "Invalid Email/Mobile and Password!")
            context.update({"login":True})
        else:
            # form = UserAccountForm(request.POST, request=request)
            form = UserAccountForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User account created successfully.')
                return redirect('/')  # Replace 'login' with the URL name for your login view
    context.update({"form" : form,"login_form" : login_form})
    return render(request, 'register.html', context)

@hk_or_login_required
def logout(request):
    request.session.clear()
    return redirect("/login")


@hk_or_login_required
def docs(request):
    context = {}
    user_id = request.session.get("user_id", 1)

    if request.method == "POST":
        form = DocsForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['upload_file']
            name, extension = os.path.splitext(file.name)
            file_name = name + extension
            duplicate = Docs.objects.filter(name=file_name).exists()
            obj = Docs(upload_file=file, name=file_name, duplicate=duplicate, user_id_id=user_id)
            obj.save()
            context["response"] = "success"
        else:
            context["response"] = "fail"
    if UserAccount.objects.filter(user_id=user_id, is_staff=True).exists():
        docs = Docs.objects.all().order_by('-id')
    else:
        docs = Docs.objects.filter(user_id_id=user_id, active=True).order_by('-id')
    context.update({"form": DocsForm(), "docs": docs})
    return render(request, "docs.html", context)


@hk_or_login_required
def delete_file(request):
    try:
        file = Docs.objects.get(id=request.GET.get("id"))
        file.delete()
    except Docs.DoesNotExist:
        pass
    return redirect("/docs")