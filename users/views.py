from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail

# Create your views here.
def register(request):
    
    if request.method =="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['user_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username =user_name).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            
            elif User.objects.filter(email = email).exists():
                messages.info(request,'Email Exists')
                return redirect('register')
            else:
                send_mail(
                    'Welcoming to Alumini association',
                    'Congratulations!!, You have successfully registered into Alumini Association. Stay in contact , share your blogs. Enjoy our services. Thanking You , regards Government College of Engineering Aurangabad ',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently = False
                )
                user = User.objects.create_user(username = user_name,first_name = first_name,last_name = last_name,email= email, password = password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Wrong Password')
            return redirect('register')
    else:
        return render(request,'users/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        user = auth.authenticate(username = username ,password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'users/signin.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html',context)
