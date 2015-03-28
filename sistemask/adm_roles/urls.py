__author__ = 'isidro'

from django.conf.urls import patterns, include, url
from .views import RolView, CrearRol, CrearRolConfirm, EditarRol, EditarRolConfirmar, EliminarRol,AsignarRol, AsignarRolConfirm, DesasignarRol, ConsultarRol

urlpatterns= patterns('',
    url(r'^inicio/rol/$', RolView.as_view(), name='rol'),
    url(r'^inicio/rol/crear/$', CrearRol.as_view(), name='crear_rol'),
    url(r'^confirmar/$', CrearRolConfirm.as_view(), name='crear_rol_confirmar'),
    url(r'^editar/$', EditarRol.as_view(), name='editar_rol'),
    url(r'^editar/confirmar/$', EditarRolConfirmar.as_view(), name='editar_rol_confirmar'),
    url(r'^eliminar/$', EliminarRol.as_view(), name='eliminar_rol'),
    url(r'^consultar_usuarios/$', ConsultarRol.as_view(), name='consultar_rol'),
    url(r'^desasignar/$', DesasignarRol.as_view(), name='desasignar_rol'),
    url(r'^asignar/$', AsignarRol.as_view(), name='asignar_rol'),
    url(r'^asignar/confirmar/$', AsignarRolConfirm.as_view(), name='asignar_rol_confirmar'),
)