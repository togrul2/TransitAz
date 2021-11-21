from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User
from .utils import generate_token
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from validate_email import validate_email
from django.conf import settings
import threading
# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Account activation'
    email_body = render_to_string('auth/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    # Email object
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user.email]
    )

    # Instead of email.send()
    EmailThread(email).start()


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request,  username=username, password=password)

        if user is not None:
            if not user.is_verified:
                messages.error(request, "Sizin hesabınız təsdiqlənməyib, email poçtunuzu yoxlayın!")

            login(request, user)
            if remember_me == 'remember_me':
                request.session.set_expiry(0)

            return redirect(request.GET.get('next', 'main'))
        else:
            messages.error(request, "İstifadəçi adı və ya şifrə yanlışdır!")

    return render(request, 'auth/login.html')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        has_error = False
        context = {'data': request.POST}
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        agreed = request.POST.get('accepted')

        if len(password1) < 6:
            messages.error(request, 'Şifrə ən azı 6 simvoldan ibarət olmalıdır')
            has_error = True

        if password1 != password2:
            messages.error(request, 'Şifrələr eyni deyillər')
            has_error = True

        if not validate_email(email):
            messages.error(request, 'Həqiqi olan bir mail ünvanı daxil edin, hansınaki daxil ola bilərsiniz')
            has_error = True

        if User.objects.filter(username=username).exists():
            messages.error(request, 'İstifadəçi adı artıq islənir, başqasını seçin')
            return render(request, 'auth/register.html', context={'data': context})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email adresi artıq islənir, başqasını seçin')
            return render(request, 'auth/register.html', context={'data': context})

        if agreed != 'on':
            messages.error(request, 'Qaydaları qəbul etməniz lazım')
        if has_error:
            return render(request, 'auth/register.html', context={'data': request.POST})

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()

        if not has_error:
            send_activation_email(request, user)
            messages.success(request, 'We sent you an email to verify your account')
            return redirect('activation_request')

    return render(request, template_name='auth/register.html')


def logoutUser(request):
    logout(request)
    return redirect(request.GET.get('next', 'main'))


def main(request):
    return render(request, 'main.html', context={'path': 'main'})


def activation_request(request):
    return render(request, 'auth/activation_requested.html')


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Email is verified')
        return render(request, 'auth/activation_success.html')
    return render(request, 'auth/activate_failed.html', context={'user': user})
