from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """ 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

    
@login_excluded('/')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("done")
            return redirect("/")
        else:
            messages.warning(request, 'Invalid Credentails')
            return redirect("login")
    return render(request,"login.html")
    
@login_excluded('/')
def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password == c_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request ,f' Username {username} Already Exists!! ')
            elif User.objects.filter(email=email).exists():
                messages.warning(request ,f'{email} Already Exists!! ')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email , password=password)
                user.save()
                # username = user.cleaned_data.get('username')
                messages.success(request , f'Account Created Sucessfully for {username}!')
                return redirect('login')
        else:
            messages.warning(request ,f'Password did not match!! ')

    return render(request,"registration.html")

def logout(request):
    auth.logout(request)
    return redirect("/")


