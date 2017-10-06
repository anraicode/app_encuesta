import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.defaults import page_not_found

from app_encuesta import settings
from cuenta.forms import LoginForm, RegistroForm

UserModel = get_user_model()
def index(request):
    data={'titulo': u'Inicio'}
    return render(request, 'index.html', data)
def logeo(request):
    data={'crud': 'conect', 'ruta':'/', 'titulo': u'Iniciar Sesión',
          'subtitulo':u'Inicio de sesión', 'form':LoginForm()}
    return render(request, 'cuenta/login.html', data)

def conectar(request):
    if request.method == 'POST':
        try:
            f = LoginForm(request.POST)
            if f.is_valid():
                user = authenticate(username=f.cleaned_data['usuario'], password=f.cleaned_data['clave'])
                if user is not None:
                    login(request, user)
                    return HttpResponse(json.dumps({'result': 'ok', 'mensaje': 'Inicio correcto.'}), content_type="application/json")
            return HttpResponse(json.dumps({'result': 'bad', 'mensaje': 'Error al iniciar sesión'}), content_type="application/json")
        except Exception:
            return HttpResponse(json.dumps({'result': 'bad', 'mensaje': 'Error al autentificarse'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'result': 'bad', 'mensaje': 'Metodo Request no es Valido.'}), content_type="application/json")

def desconectar(request):
    logout(request)
    return HttpResponseRedirect("/login")

def restablecer_clave(request, domain_override=None, token_generator=default_token_generator, use_https=True, email_template_name=None):
    data={'titulo': 'Restablecer contraseña', 'subtitulo': 'Restablecer contraseña',
          'crud':'/restablecer/clave', 'ruta':'/login'}
    if request.method == 'POST':
        f=PasswordResetForm(request.POST)
        if f.is_valid():
            context={}
            email_to = f.cleaned_data['email']

            for user in get_users(email_to):
                if not domain_override:
                    current_site = get_current_site(request)
                    site_name = current_site.name
                    domain = current_site.domain
                else:
                    site_name = domain = domain_override
                context = {
                    'email': email_to,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': token_generator.make_token(user),
                    'protocol': 'https' if use_https else 'http',
                }

            asunto = 'Restablecer contraseña'
            mensaje_email = loader.render_to_string(email_template_name, context)
            email_from = settings.EMAIL_HOST_USER

            send_mail(asunto, mensaje_email, email_from, [email_to], fail_silently=False)

        return HttpResponse(json.dumps({'result': 'ok', 'mensaje':'Correo enviado.'}), content_type="application/json")
    else:
        data['form'] = PasswordResetForm()
        return render(request,'cuenta/restablecercontraseña.html', data)

@sensitive_post_parameters()
@never_cache
@deprecate_current_app
def confirmar_clave(request, uidb64=None, token=None, token_generator=default_token_generator, set_password_form=SetPasswordForm):
    assert uidb64 is not None and token is not None  # checked by URLconf

    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = u'Ingrese su nueva contraseña'
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            #si es valido me envia a pagina de succces
            if form.is_valid():
                form.save()
                #response que si es valido
                #return HttpResponseRedirect(post_reset_redirect)
                return HttpResponse(json.dumps({'result': 'ok', 'mensaje': 'correcto.'}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'result': 'bad', 'mensaje': u'%s'%(form._errors)}),
                                    content_type="application/json")

        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = u'Password reset unsuccessful'
    data = {
        'form': form,
        'titulo': title,
        'subtitulo': title,
        'crud': '/restablecer/confirmar%s/%s/'%(uidb64, token),
        'ruta': '/login'
    }
    if validlink:
        return render(request, 'cuenta/password_reset_confirm.html', data)
    else:
        return render(request, 'cuenta/password_reset_confirm.html', data)

def get_users(email):
    active_users = UserModel._default_manager.filter(**{
        '%s__iexact' % User.get_email_field_name(): email,
        'is_active': True,
    })
    return (u for u in active_users if u.has_usable_password())

def registrar(request):
    data = {}
    data['titulo'] = u'Registro'
    data['subtitulo'] = u'Registro de usuario'
    data['crud'] = 'registrar'
    data['ruta'] = '/login'
    data['r'] = True
    if request.method == 'POST':
        f = RegistroForm(request.POST)
        if f.is_valid():
            usuario = User.objects.create_user(
                username=f.cleaned_data['usuario'],
                first_name=f.cleaned_data['nombre'],
                last_name=f.cleaned_data['apellido'],
                email=f.cleaned_data['correo'],
                password=f.cleaned_data['clave']
            )
            usuario.save()
            return HttpResponse(json.dumps({'result':'ok', 'mensaje':'Registro guardado con exito.'}), content_type='application/json')
        return HttpResponse(json.dumps({'result':'bad', 'mensaje':'Error al guardar los datos'}))
    else:
        data['form'] = RegistroForm()
        return render(request, 'cuenta/registro.html', data)

def dato_repetido(request):
    tipo = request.POST['tipo']
    if tipo == 'correo':
        email = request.POST['correo']
        if User.objects.filter(email=email):
            return JsonResponse({'valid': 'false'})
    if tipo == 'usuario':
        usuario = request.POST['usuario']
        if User.objects.filter(username=usuario):
            return JsonResponse({'valid': 'false'})
    return JsonResponse({'valid': 'true'})