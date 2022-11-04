from unicodedata import name
from django.urls import path

from . import views

app_name = "barberhouse"

urlpatterns = [
    path('', views.inicio, name="inicio"),

    
    #contraseña
    
    
    
    
    #Roles
    path('roles/', views.roles, name="listarRoles"),
    path('crear_rol/', views.formularioRol, name="crear_Rol"),
    path('Guardar_rol/', views.guardarRol, name="guardar_Rol"),
    path('editar_rol/<int:id>', views.editarRol, name="editar_Rol"),
    path('actualizar_rol/', views.actualizarRol, name="actualizar_Rol"),
    path('eliminar:rol/<int:id>', views.eliminarRol, name="eliminar_Rol"),
    path('BuscarRol/',views.rolesBuscar, name="Buscar_rol"),


    #Login
    path('loginForm/',views.loginForm, name="loginForm"),
    path('login/',views.login, name="login"),
    path('loginCerrar/',views.loginCerrar, name="login_cerrar"),
    
    #Email
    path('enviarMail/',views.sendMail, name="Send_mail"),
    

    #usuarios
    path('usuarios/', views.usuarios, name="listarUsuarios"),
    path('crear_usuarios/', views.usuariosFormulario, name="crear_usuario"),
    path('crear_usuarios/', views.usuariosFormulario, name="registrar_cliente"),
    path('guardar_usuarios/', views.usuariosGuardar, name="guardar_usuario"),
    path('guardar_clientes/', views.clientesGuardar, name="guardar_cliente"),
    path('editar_usuarios/<int:id>', views.usuariosEditar, name="editar_usuario"),
    path('actualizar_usuarios/', views.usuariosActualizar, name="actualizar_usuario"),
    path('eliminar_usuarios/<int:id>', views.usuariosEliminar, name="eliminar_usuario"),
    path('BuscarUsuario/',views.usuariosBuscar, name="Buscar_usuario"),
    path('Perfil/',views.perfil, name="Perfil_Usuario"),
    path('ActualizarPerfil/',views.actualizarPerfil, name="actualizar_perfil"),

    #servicios
    path('servicios/', views.servicios, name="listarServicios"),
    path('crear_servicios/', views.serviciosFormulario, name="crear_servicio"),
    path('guardar_servicios/', views.serviciosGuardar, name="guardar_servicio"),
    path('editar_servicios/<int:id>', views.serviciosEditar, name="editar_servicio"),
    path('actualizar_servicios/', views.serviciosActualizar, name="actualizar_servicio"),
    path('eliminar_servicios/<int:id>', views.serviciosEliminar, name="eliminar_servicio"),
    
    #Citas
    path('citas/', views.citas, name="listarCitas"),
    path('crear_citas/', views.citasFormulario, name="crear_cita"),
    path('guardar_citas/', views.citasGuardar, name="guardar_cita"),
    path('editar_citas/<int:id>', views.citasEditar, name="editar_cita"),
    path('actualizar_citas/', views.citasActualizar, name="actualizar_cita"),
    path('eliminar_citas/<int:id>', views.citasEliminar, name="eliminar_cita"),
    
    #Promociones
    path('promociones/', views.promociones, name="listarPromociones"),
    path('crear_promociones', views.promocionesFormulario, name="crear_promocion"),
    path('guardar_promociones', views.promocionesGuardar, name="guardar_promocion"),
    path('editar_promociones/<int:id>', views.promocionesEditar, name="editar_promocion"),
    path('actualizar_promociones/', views.promocionesActualizar, name="actualizar_promocion"),
    path('eliminar_promociones/<int:id>', views.promocionesEliminar, name="eliminar_promocion"),

]
