from django.shortcuts import render,redirect , HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import CreateView
from .models import Doctor, Patient , CustomUser
from .forms import DoctorForm ,PatientForm
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm




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

# Create your views here.


def login(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_approve == False:
                    return HttpResponse("noora")
                else:
                    auth.login(request,user)
                    return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})
    
# @login_excluded('/')
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user= auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             print("dnoobboboobboboboboone")
#             return redirect("/")
#         else:
#             messages.warning(request, 'Invalid Credentails')
#             return redirect("login")
#     return render(request,"login.html")
    
@login_excluded('/')
def registration(request):
    # if request.method == 'POST':
    #     first_name = request.POST['first_name']
    #     last_name = request.POST['last_name']
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     c_password = request.POST['c_password']
    #     if password == c_password:
    #         if User.objects.filter(username=username).exists():
    #             messages.warning(request ,f' Username {username} Already Exists!! ')
    #         elif User.objects.filter(email=email).exists():
    #             messages.warning(request ,f'{email} Already Exists!! ')
    #         else:
    #             user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email , password=password)
    #             user.save()
    #             # username = user.cleaned_data.get('username')
    #             messages.success(request , f'Account Created Sucessfully for {username}!')
    #             return redirect('login')
    #     else:
    #         messages.warning(request ,f'Password did not match!! ')

    return render(request,"registration.html")

# where name is the name of the method to be decorated.
# or in case of few decorators:
# decorators = [never_cache, login_required]
# @method_decorator(decorators, name='dispatch')
# class YourClassBasedView(TemplateView):

@method_decorator(login_excluded('/'), name='dispatch')
class doctor_register(CreateView):
    model = CustomUser
    form_class = DoctorForm
    template_name = "doctor_register.html"

    def form_valid(self, form):
        user = form.save()
        return HttpResponse (" you need approvement from admin noob admi")

        
@method_decorator(login_excluded('/'), name='dispatch')
class patient_register(CreateView):
    model = CustomUser
    form_class = PatientForm
    template_name = "patient_register.html"

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect("/")


