from django.shortcuts import render,redirect
from django.core.mail import send_mail,BadHeaderError
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'account was created for ' + user)

            return redirect('login.html')
    context = {'form': form}
    return render(request,'register.html',context)
def loginPage(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'username or password is incorrect')

    context = {}
    return render(request,'login.html',context)
def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url="login")

def index(request):
    return render(request,'index.html',{})
@login_required(login_url="login")
def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        #send Email
        send_mail(
        #subject
        'message from' + message_name,
        #message
        message,
        #from email
        message_email,
#to email
        ['fairydental123@gmail.com'],
        )
        return render(request,'contact.html',{'message_name':message_name})
    else:
        return render(request,'contact.html',{})
@login_required(login_url="login")
def about(request):
    return render(request,'about.html')
@login_required(login_url="login")
def pricing(request):
    return render(request,'pricing.html',{})
@login_required(login_url="login")
def service(request):
    return render(request,'service.html',{})
@login_required(login_url="login")
def appointment(request):
    if request.method == "POST":
        your_name = request.POST['your-name']
        your_phone =request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_scheldule = request.POST['your-scheldule']
        your_date = request.POST['your-date']
        your_message = request.POST['your-message']

        appointment = "Name:" + your_name







        return render(request,'appointment.html',{
        'your_name':your_name,
        'your_phone':your_phone,
        'your_email': your_email,
        'your_address':your_address,
        'your_scheldule':your_scheldule,
        'your_date': your_date,
        'your_message':your_message,



        })
    else:
        return render(request,'index.html',{})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
