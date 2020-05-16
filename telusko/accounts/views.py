from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import CustomPreferences
from .forms import ExtendedUserCreationForm, CustomPreferencesForm

# Create your views here.


def login(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')    

def register(request):

    if request.method == 'POST':
        form=ExtendedUserCreationForm(request.POST,request.FILES)
        custom_form=CustomPreferencesForm(request.POST,request.FILES)
        

        if form.is_valid() and custom_form.is_valid():
            user=form.save()
            
            custom=custom_form.save(commit=False)
            custom.user=user
            
            custom.save()

            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=auth.authenticate(username=username,password1=password)
            return redirect('login/')
            
            """username=request.POST.get('username')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            email=request.POST.get('email')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email Taken')
                    return redirect('register')
                else: 
                     cu_user=CustomPreferences()
                     cu_user.preferences=request.POST.get('preferences')
                     cu_user.save()  
                     user2 = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                     user2.save()
                     print('user created')
                     return redirect('login/')

            else:
                 messages.info(request,'password not matching..')    
                 return redirect('register')
                 """
            

            #return redirect('/')

    else:
        form=ExtendedUserCreationForm()

        custom_form=CustomPreferencesForm()

    context={'form':form,'custom_form':custom_form}

    return render(request,'register.html',context)


    """ first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        preferences=request.POST['preferences']
        

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name,preferences=preferences)
                user.save()
                print('user created')
                return redirect('login/')

        else:
            messages.info(request,'password not matching..')    
            return redirect('register')
        return redirect('/')
        
    else:
        return render(request,'register.html')
    """



def logout(request):
    auth.logout(request)
    return redirect('/')       