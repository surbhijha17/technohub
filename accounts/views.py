from django.contrib import messages
from articles.models import Category
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from .forms import UserLoginForm,UserSignUpForm
from django.http import HttpResponseRedirect,HttpResponse ,JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def signup_view(request):
    categories = Category.objects.all()
    if request.method =='POST':
        form=UserSignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()

            login(request,user)
            return redirect('home')
    else:
        form=UserSignUpForm()
    return render(request,'accounts/signup.html',{'categories':categories,'form':form,})


def login_view(request):
    categories = Category.objects.all()
    if request.method =='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if'next'in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
    else:
        form= AuthenticationForm()
    return render(request,'accounts/login.html',{'categories':categories, 'form':form})

#def login_view(request):
    if request.method =='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active():
                    login(request,user)
                    return HttpResponseRedirect(reverse('articles:list'))
                else:
                    return HttpResponse("User is not active")
    else:
        form=UserLoginForm()
        return render(request,'accounts/login.html',{'categories':categories,'form':form})
    #            if'next'in request.POST:
    #                return redirect(request.POST.get('next'))
    #            else:
    #                return redirect('articles:list')
    #    else:
    #        form= AuthenticationForm()
    #    return render(request,'accounts/login.html',{'form':form})

def logout_view(request):

    if request.method=='POST':
        logout(request)
        return redirect('home')
