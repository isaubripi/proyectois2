# coding=utf-8

from django.shortcuts import render

from adm_usuarios.models import Usuario
from django.views.generic import TemplateView
from .models import Rol
from adm_proyectos.models import Proyecto
from adm_proyectos.views import LoginRequiredMixin

# Create your views here.
class RolView(TemplateView):
    '''Esta clase muestra la lista de roles activos.
    Hereda de TemplateView.
    template_name es el archivo html de esta clase.

    '''
    template_name = 'Rol.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y la lista de roles activos.
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        id_proyecto = request.POST['proyecto']
        diccionario['proyecto'] = proyecto_actual

        lista = Rol.objects.filter(activo = True, proyecto=id_proyecto)
        diccionario['lista'] = lista
        return render(request, self.template_name, diccionario)


class CrearRol(LoginRequiredMixin, RolView):
    '''Esta clase crea roles.
    Hereda de RolView.
    template_name es el archivo html de esta clase.

    '''
    template_name = 'CrearRol.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y una lista de usuarios.
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        lista = Usuario.objects.all()
        diccionario['lista_usuarios'] = lista
        return render(request, self.template_name, diccionario)

class CrearRolConfirm(CrearRol):
    '''Esta clase confirma la creacion de un nuevo rol.
       Hereda de CrearRol.
       template_name es el archivo html de esta clase.

    '''
    template_name = 'CrearRolConfirm.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros
        :param request:
        :param args:
        :param kwargs:
        :return: request y el archivo html.
        Si se introduce un nombre de rol existente lanza el error.
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        rol_nombre= request.POST['nombre_rol']
        id_proyecto = request.POST['proyecto']
        if len(Rol.objects.filter(nombre= rol_nombre, activo= True, proyecto=id_proyecto)):
            error = "Nombre del rol ya existe. Intente otro"
            return render(request, super(CrearRolConfirm, self).template_name, {'error':error})
        nuevo_rol = Rol(nombre= rol_nombre)
        nuevo_rol.proyecto = id_proyecto
        nuevo_rol.activo= True

        nuevo_rol.save()
        return render(request, self.template_name, diccionario)


class EditarRol(LoginRequiredMixin, RolView):
    '''Esta clase edita o modifica un rol existente.
    El rol de Scrum Master no se puede modificar.
    Hereda de RolView
    template_name es el archivo html de esta clase
    '''
    template_name = 'EditarRol.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''

        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        rol_actual= Rol.objects.get(id= request.POST['rol'])

        if rol_actual.nombre== 'Scrum Master':
            diccionario['error']= 'Rol: Scrum Master - No se puede modificar'

            return render(request, super(EditarRol, self).template_name, diccionario)
        diccionario['rol']= rol_actual
        return render(request, self.template_name, diccionario)

class EditarRolConfirmar(EditarRol):
    '''Esta clase confirma la modificacion de un rol.
    Hereda de EditarRol.
    template_name es el archivo html de esta clase.

    '''
    template_name = 'EditarRolConfirm.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''

        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual


        roles= Rol.objects.filter(nombre= request.POST['nombre_rol'])
        nuevo_rol_nombre= request.POST['nombre_nuevo_rol']
        for rol_actual in roles:
            rol_actual.nombre= nuevo_rol_nombre
            rol_actual.save()
        return render(request, self.template_name, diccionario)

class EliminarRol(LoginRequiredMixin, RolView):
    '''Esta clase elimina un rol, es decir, pone en estado inactivo el rol.
    El rol de Scrum Master no se puede eliminar.
    Hereda de RolView.
    template_name es el archivo html de esta funcion.

    '''
    template_name = 'EliminarRol.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''


        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        rol_actual= Rol.objects.get(id= request.POST['rol'])

        if rol_actual.nombre== 'Scrum_Master':
            diccionario['error']= 'Rol: Scrum Master - No se puede eliminar'

            return render(request, super(EliminarRol, self).template_name, diccionario)

        if len(Rol.objects.filter(activo=True, proyecto=request.POST['proyecto'])):
            diccionario['error']= 'El rol esta asignado, no se puede eliminar'

            return render(request, super(EliminarRol, self).template_name, diccionario)

        #roles= Rol.objects.filter(nombre= rol_actual.nombre, activo= True)
        #for rol_actual in roles:
        rol_actual.activo= False
        rol_actual.save()

        return render(request, self.template_name, diccionario)

class ConsultarRol(RolView):
    '''Esta clase muestra la lista de los roles activos en el sistema.

    '''
    template_name = 'ConsultarUsuarios.html'
    def post(self, request, *args, **kwargs):
        diccionario={}

        rol_actual= Rol.objects.get(id= request.POST['rol'])

        diccionario['lista_roles']= Rol.objects.filter(nombre=rol_actual.nombre, activo= True)
        return render(request, self.template_name, diccionario)


class AsignarDesasignarPermisos(LoginRequiredMixin, RolView):
    '''
    Esta clase asigna/desasigna permisos a un rol.
    Hereda de RolView.
    template_name es el archivo html de esta funcion.
    '''

    template_name = 'AsignarDesasignarPermisos.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''


        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        rol_actual= Rol.objects.get(id=request.POST['rol'])

        diccionario['rol'] = rol_actual

        return render(request, self.template_name, diccionario)


class AsignarDesasignarPermisosConfirmar(AsignarDesasignarPermisos):
    '''
    Esta clase confirma la asignacion/desasignacion de permisos a un rol.
    Hereda de AsignarDesasignarPermisos.
    template_name es el archivo html de esta funcion.
    '''

    template_name = 'AsignarDesasignarPermisosConfirmar.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''


        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        rol_actual = Rol.objects.get(id = request.POST['nombre_rol'], activo=True)

        if 'crear_proyecto' in request.POST: rol_actual.crear_proyecto= True
        else: rol_actual.crear_proyecto= False
        if 'modificar_proyecto' in request.POST: rol_actual.modificar_proyecto= True
        else: rol_actual.modificar_proyecto= False
        if 'eliminar_proyecto' in request.POST: rol_actual.eliminar_proyecto= True
        else: rol_actual.eliminar_proyecto= False
        if 'cerrar_proyecto' in request.POST: rol_actual.cerrar_proyecto= True
        else: rol_actual.cerrar_proyecto= False
        if 'inicializar_proyecto' in request.POST: rol_actual.inicializar_proyecto= True
        else: rol_actual.inicializar_proyecto= False
        if 'ingresar_proyecto' in request.POST: rol_actual.ingresar_proyecto= True
        else: rol_actual.ingresar_proyecto= False

        if 'crear_usuario' in request.POST: rol_actual.crear_usuario= True
        else: rol_actual.crear_usuario= False
        if 'modificar_usuario' in request.POST: rol_actual.modificar_usuario= True
        else: rol_actual.modificar_usuario= False
        if 'eliminar_usuario' in request.POST: rol_actual.eliminar_usuario= True
        else: rol_actual.eliminar_usuario= False

        if 'agregar_rol' in request.POST: rol_actual.agregar_rol= True
        else: rol_actual.agregar_rol= False
        if 'modificar_rol' in request.POST: rol_actual.modificar_rol= True
        else: rol_actual.modificar_rol= False
        if 'eliminar_rol' in request.POST: rol_actual.eliminar_rol= True
        else: rol_actual.eliminar_rol= False

        if 'generar_reporte' in request.POST: rol_actual.generar_reporte= True
        else: rol_actual.generar_reporte= False
        if 'crear_burndown' in request.POST: rol_actual.generar_burndown= True
        else: rol_actual.generar_burndown= False

        if 'asignar_usuario_inicial' in request.POST: rol_actual.asignar_usuario_inicial= True
        else: rol_actual.asignar_usuario_inicial= False
        if 'asignar_permisos_roles' in request.POST: rol_actual.asignar_permisos_roles= True
        else: rol_actual.asignar_permisos_roles= False
        if 'asignar_roles_usuario' in request.POST: rol_actual.asignar_roles_usuario= True
        else: rol_actual.asignar_roles_usuario= False
        if 'asignar_usuarios_proyecto' in request.POST: rol_actual.asignar_usuarios_proyecto= True
        else: rol_actual.asignar_usuarios_proyecto= False
        if 'asignar_usuarios_flujo' in request.POST: rol_actual.asignar_usuarios_flujo= True
        else: rol_actual.asignar_usuarios_flujo= False
        if 'asignar_equipo' in request.POST: rol_actual.asignar_equipo= True
        else: rol_actual.asignar_equipo= False

        if 'agregar_sprint' in request.POST: rol_actual.agregar_sprint= True
        else: rol_actual.agregar_sprint= False
        if 'modificar_sprint' in request.POST: rol_actual.modificar_sprint= True
        else: rol_actual.modificar_sprint= False
        if 'eliminar_sprint' in request.POST: rol_actual.eliminar_sprint= True
        else: rol_actual.eliminar_sprint= False
        if 'activar_sprint' in request.POST: rol_actual.activar_sprint= True
        else: rol_actual.activar_sprint= False
        if 'ver_sprintbacklog' in request.POST: rol_actual.ver_sprintbacklog= True
        else: rol_actual.ver_sprintbacklog= False

        if 'agregar_historia' in request.POST: rol_actual.agregar_historia= True
        else: rol_actual.agregar_historia= False
        if 'modificar_historia' in request.POST: rol_actual.modificar_historia= True
        else: rol_actual.modificar_historia= False
        if 'eliminar_historia' in request.POST: rol_actual.eliminar_historia= True
        else: rol_actual.eliminar_historia= False
        if 'cargar_horas' in request.POST: rol_actual.cargar_horas= True
        else: rol_actual.cargar_horas= False
        if 'cambiar_actividad_estado' in request.POST: rol_actual.cambiar_actividad_estado= True
        else: rol_actual.cambiar_actividad_estado= False
        if 'ver_historial' in request.POST: rol_actual.ver_historial= True
        else: rol_actual.ver_historial= False
        if 'ver_detalles' in request.POST: rol_actual.ver_detalles= True
        else: rol_actual.ver_detalles= False
        if 'cancelar_historia' in request.POST: rol_actual.cancelar_historia= True
        else: rol_actual.cancelar_historia= False
        if 'asignar_historia' in request.POST: rol_actual.asignar_historia= True
        else: rol_actual.asignar_historia= False
        if 'desasignar_historia' in request.POST: rol_actual.desasignar_historia= True
        else: rol_actual.desasignar_historia= False
        if 'release_historia' in request.POST: rol_actual.release_historia= True
        else: rol_actual.release_historia= False
        if 'finalizar_historia' in request.POST: rol_actual.finalizar_historia= True
        else: rol_actual.finalizar_historia= False
        if 'horas_sprint' in request.POST: rol_actual.horas_sprint=True
        else: rol_actual.horas_sprint= False

        if 'crear_flujo' in request.POST: rol_actual.crear_flujo= True
        else: rol_actual.crear_flujo= False
        if 'modificar_flujo' in request.POST: rol_actual.modificar_flujo= True
        else: rol_actual.modificar_flujo= False
        if 'eliminar_flujo' in request.POST: rol_actual.eliminar_flujo= True
        else: rol_actual.eliminar_flujo= False
        if 'ver_tabla' in request.POST: rol_actual.ver_tabla= True
        else: rol_actual.ver_tabla= False

        if 'crear_actividad' in request.POST: rol_actual.crear_actividad= True
        else: rol_actual.crear_actividad= False
        if 'modificar_actividad' in request.POST: rol_actual.modificar_actividad= True
        else: rol_actual.modificar_actividad= False
        if 'eliminar_actividad' in request.POST: rol_actual.eliminar_actividad= True
        else: rol_actual.eliminar_actividad= False
        if 'establecer_secuencia' in request.POST: rol_actual.establecer_secuencia= True
        else: rol_actual.establecer_secuencia= False
        if 'restablecer_secuencia' in request.POST: rol_actual.restablecer_secuencia= True
        else: rol_actual.restablecer_secuencia= False

        rol_actual.save()

        return render(request, self.template_name, diccionario)




class DesasignarRol(RolView):
    '''Esta clase desasigna un rol de un usuario.
    El rol de Scrum Master no se puede eliminar.

    '''
    template_name = 'DesasignarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}

        rol_actual= Rol.objects.get(id= request.POST['rol'])

        if rol_actual.nombre== 'Scrum Master':
            diccionario['error']= 'Rol: Scrum Master - Operacion No Permitida'

            return render(request, super(DesasignarRol, self).template_name, diccionario)
        rol_actual.activo= False
        rol_actual.save()
        if len(Rol.objects.filter(nombre= rol_actual.nombre))==1:
            diccionario['error']= 'No existe usuarios asignados a dicho rol - Rol Eliminado'

        return render(request, self.template_name, diccionario)

class AsignarRol(RolView):
    '''Esta clase asigna un rol a un usuario.

    '''
    template_name = 'AsignarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}

        rol_actual= Rol.objects.get(id= request.POST['rol'])

        diccionario['rol']= rol_actual
        if rol_actual.nombre== 'Scrum Master':
            diccionario['error']= 'Rol: Scrum Master - Operacion No Permitida'

            return render(request, super(AsignarRol, self).template_name, diccionario)
        usuarios_rol= []    #Usuarios que pertenecen al Rol

        for i in Rol.objects.filter(nombre= rol_actual.nombre, activo= True):
            usuarios_rol.append(i.usuario)
        not_usuarios_rol= []     #Usuarios que no pertenecen al Rol
        for i in Usuario.objects.all():
            if not (i in usuarios_rol): not_usuarios_rol.append(i)
        if not len(not_usuarios_rol):
            diccionario['error']= 'Todos los usuarios tienen asignados este rol'
            diccionario[super(AsignarRol, self).context_object_name]= Rol.objects.filter( activo= True)
            return render(request, super(AsignarRol,self).template_name, diccionario)
        else:
            diccionario['lista_usuarios']= not_usuarios_rol
            return render(request, self.template_name, diccionario)

class AsignarRolConfirm(RolView):
    '''Esta clase confirma la asignación de un rol a un usuario.

    Crear un objeto de rol cuando se asigna a un usuario.
    '''
    template_name = 'AsignarRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}

        rol_actual= Rol.objects.get(id= request.POST['rol'])
        usuario_rol= Usuario.objects.get(username= request.POST['usuario'])

        diccionario['rol']= rol_actual

        nuevo_rol= Rol(
            nombre= rol_actual.nombre,

            usuario= usuario_rol,
            crear_proyecto= rol_actual.crear_proyecto,
            modificar_proyecto= rol_actual.modificar_proyecto,
            eliminar_proyecto= rol_actual.eliminar_proyecto,
            cerrar_proyecto= rol_actual.cerrar_proyecto,
            inicializar_proyecto= rol_actual.inicializar_proyecto,
            ingresar_proyecto= rol_actual.ingresar_proyecto,

            crear_usuario= rol_actual.crear_usuario,
            modificar_usuario= rol_actual.modificar_usuario,
            eliminar_usuario= rol_actual.eliminar_usuario,

            agregar_rol= rol_actual.agregar_rol,
            modificar_rol= rol_actual.modificar_rol,
            eliminar_rol= rol_actual.eliminar_rol,

            generar_resumen_clientes= rol_actual.generar_resumen_clientes,
            generar_burndown= rol_actual.generar_burndown,

            asignar_usuario_inicial= rol_actual.asignar_usuario_inicial,
            asignar_permisos_roles= rol_actual.asignar_permisos_roles,
            asignar_roles_usuario= rol_actual.asignar_roles_usuario,
            asignar_usuarios_proyecto= rol_actual.asignar_usuarios_proyecto,

            agregar_sprint= rol_actual.agregar_sprint,
            modificar_sprint= rol_actual.modificar_sprint,
            eliminar_sprint= rol_actual.eliminar_sprint,
            activar_sprint= rol_actual.activar_sprint,

            agregar_historia= rol_actual.agregar_historia,
            modificar_historia= rol_actual.modificar_historia,
            eliminar_historia= rol_actual.eliminar_historia,
            adjuntar_archivos= rol_actual.adjuntar_archivos,
            cargar_horas= rol_actual.cargar_horas,
            actualizar_estado= rol_actual.actualizar_estado,
            ver_historial= rol_actual.ver_historial,
            validar_historia= rol_actual.validar_historia,

            crear_flujo= rol_actual.crear_flujo,
            modificar_flujo= rol_actual.modificar_flujo,
            eliminar_flujo= rol_actual.eliminar_flujo,
            ver_tabla= rol_actual.ver_tabla,
        )

        nuevo_rol.save()
        return render(request, self.template_name, diccionario)

class UsuarioProyecto(RolView):
    template_name = 'UsuariosProyecto.html'

    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        #Solamente el Administrador del Sistema puede ingresar a la Administracion de Usuarios
        if len(Rol.objects.filter(crear_usuario = True , usuario= usuario_logueado)):

            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permisos para ver los usuarios del proyecto'

            return render(request, super(UsuarioProyecto, self).template_name, diccionario)


class AsignarRolesProyecto(LoginRequiredMixin, RolView):
    template_name = 'AsignarRolesProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        id_proyecto = request.POST['proyecto']
        usuario_logueado = Usuario.objects.get(id = request.POST['login'])
        diccionario['logueado'] = usuario_logueado
        usuario_actual = Usuario.objects.get(id = request.POST['usuario'])
        diccionario['usuario_actual'] = usuario_actual
        lista = usuario_actual.roles.filter(proyecto= id_proyecto)
        diccionario['roles_asignados'] = lista
        lista1 = Rol.objects.filter(proyecto=id_proyecto)

        diccionario['no_asignados'] = lista1
        return render(request, self.template_name, diccionario)


class AsignarRolesConfirmProyecto(AsignarRolesProyecto):
    template_name = 'AsignarRolesConfirmProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        id_proyecto = request.POST['proyecto']
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        usuario_actual = Usuario.objects.get(id = request.POST['user'])
        lista2 = usuario_actual.roles.filter(proyecto= id_proyecto)
        lista3 = Rol.objects.filter(proyecto=id_proyecto)
        for rol in lista2:
            if rol.nombre not in request.POST:
                usuario_actual.roles.remove(rol)
        for r in lista3:
            if r.nombre in request.POST:
                usuario_actual.roles.add(r)
        usuario_actual.save()
        return render(request, self.template_name, diccionario)