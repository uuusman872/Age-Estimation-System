from django.shortcuts import render,redirect , HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import CreateView
from .models import Doctor, Patient , CustomUser,SomeLocationModel
from .forms import DoctorForm ,PatientForm ,ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from .forms import LocationForm
from django.core.mail import EmailMessage
from django.views.generic import View
from django import forms
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utilts import account_activation_token


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
                    messages.warning(request,"Wait for Account Approval!")
                else:
                    auth.login(request,user)
                    return redirect('/')
            else:
                messages.warning(request,"Invalid username or password")
        else:
                messages.warning(request,"Invalid username or password")
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
    mymap = LocationForm()
    extra_context={'mymap': mymap}
    template_name = "doctor_register.html"

    

    def form_valid(self, form):
        user = form.save()
        # mmmap = SomeLocationModel.objects.create(user=user)
        # mmmap.location = form.cleaned_data.get('location')
        # mmmap.save()
        # if self.request.method == 'POST':
        #     mmmap= SomeLocationModel.objects.create(user=user)
        #     mmmap.location = self.form.cleaned_data.get('location')
        #     mmmap.save()

        uidb64=urlsafe_base64_encode(force_bytes(user.pk))

        domain= get_current_site(self.request).domain

        link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
        
        activate_url='http://'+domain+link         

        email_body='Hi' + user.username + " Please use this link to verify account\n "+ activate_url
        
        email_subject="Activate your account"

        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@example.com',
            [user.email],
        )


        email.send(fail_silently=False)
        messages.warning(self.request,"Account Successfully Created!")
        return redirect('login')

class VerificationView(View):
    def get(self,request,uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                messages.warning(request, 'User already activated!' )
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully!\n Please wait for admin approval.' )
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

        
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


def profile(request):
    user= request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form= ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    context = { 'form' : form}
    return render(request,"doctor/profile.html" ,context)
