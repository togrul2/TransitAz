from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import validate_password, ValidationError
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

            path = request.GET.get('next', 'main')
            if path == '':
                path = 'main'
            return redirect(path)
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

        try:
            validate_password(password1)
        except ValidationError as VeMessage:
            messages.error(request, *VeMessage)

        if password1 != password2:
            messages.error(request, 'Şifrələr eyni deyillər')
            has_error = True

        if not validate_email(email):
            messages.error(request, 'Həqiqi olan bir mail ünvanı daxil edin, hansınaki daxil ola bilərsiniz')
            has_error = True

        if User.objects.filter(username=username).exists():
            messages.error(request, 'İstifadəçi adı artıq islənir, başqasını seçin')
            return render(request, 'auth/register.html', context={'data': request.POST})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email adresi artıq işlənir, başqasını seçin')
            return render(request, 'auth/register.html', context={'data': request.POST})

        if agreed != 'on':
            messages.error(request, 'Qaydaları qəbul etməlisiniz')
        if has_error:
            return render(request, 'auth/register.html', context={'data': request.POST})

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()

        if not has_error:
            send_activation_email(request, user)
            messages.success(request, 'Təsdiq məktubu e-poçtunuza göndərildi')
            return redirect('activation_request')

    return render(request, template_name='auth/register.html')


def logoutUser(request):
    path = request.GET.get('next', 'main')

    if path == '':
        path = 'main'
    logout(request)
    return redirect(path)


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
        messages.success(request, 'Təbriklər! Hesab təsdiqləndi')
        return render(request, 'auth/activation_success.html')
    return render(request, 'auth/activate_failed.html', context={'user': user})


def my_profile(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'my-profile.html', context={'path': 'my_profile'})


def add_phone(request):
    if request.method == 'POST':
        text = request.POST.get('phone-number')
        user = User.objects.get(username=request.user)
        user.phone_number = '+994' + text
        user.save()

    return redirect(request.GET.get('next', 'my_profile'))


def change_password(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(request.GET.get('next', 'main'))

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        has_authenticated = authenticate(request, username=user, password=old_password)

        if has_authenticated is None:
            messages.error(request, 'Mövcud şifrə yanlışdır')
            return render(request, 'auth/change-password.html', status=401)

        try:
            validate_password(password1)
        except ValidationError as vex:
            messages.error(request, *vex)
            return render(request, 'auth/change-password.html', status=400)

        if password1 != password2:
            messages.error(request, "Şifrələr eyni deyil")
            return render(request, 'auth/change-password.html', status=400)

        profile = User.objects.get(username=user)
        profile.set_password(password1)
        profile.save()
        messages.success(request, 'Şifrəniz uğurla dəyişildi')
        return redirect('my-profile')
    return render(request, 'auth/change-password.html')


def edit_profile(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        username = request.POST.get('username')
        if not username[0].isalpha() or len(username) < 4:
            messages.error(request, 'Istifadəçi adı yararlı deyil')
            return render(request, 'edit_profile.html', context={'user': user}, status=400)

        user.username = username
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return redirect('my_profile')

    return render(request, 'edit_profile.html', context={'user': user})
