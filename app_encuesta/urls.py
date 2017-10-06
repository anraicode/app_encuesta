
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('cuenta.urls', namespace='cuenta')),
    url(r'^encuesta', include('encuesta.urls', namespace='encuesta')),
]
