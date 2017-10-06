from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset_confirm

from cuenta.views import *

urlpatterns = [
    url(r'^login$', logeo, name='login'),
    url(r'^conect$', conectar, name='conect'),
    url(r'^logout$', desconectar, name='logout'),
    url(r'^registrar$', registrar, name='registrar'),
    url(r'^registro/datoValidacion/$', dato_repetido, name='validar_dato'),
    url(r'^restablecer/clave$', restablecer_clave,
        {'email_template_name':'cuenta/password_reset_email.html'},
        name='password_reset'),
    url(r'^restablecer/confirmar(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        confirmar_clave, name='password_reset_confirm'),
    url(r'', login_required(index), name='index')
]