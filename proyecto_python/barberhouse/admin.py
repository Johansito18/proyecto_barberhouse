from django.contrib import admin
from .models import Rol, ServiciosCitas,Usuarios,Promociones,Citas,Servicios

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rol')

@admin.register(Usuarios)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('cedula_usuario', 'nombre', 'apellido','correo','clave', 'rol', 'foto', 'verFoto')
    
    def verFoto(self, obj):
        #generar código html en el admin
        from django.utils.html import format_html
        foto = obj.foto.url
        return format_html(f"<a href='{foto}' target='_blank'><img src='{foto}' width='20%' /></a>")
        
    def rol(self,obj):
        return obj.rol.nombre_rol
    
@admin.register(Promociones)
class PromocionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_promocion')
    
@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_servicio', 'precio', 'promocion', 'empleado')    

    def promocion(self,obj):
        return obj.promocion.nombre_promocion
    
    def empleado(self,obj):
        return obj.empleado.nombre
    
        
@admin.register(Citas)
class CitasAdmin(admin.ModelAdmin):
    list_display = ('id','fecha_cita','cliente','empleado')

    def cliente(self,obj):
        return obj.usuarioCliente.nombre

    def empleado(self,obj):
        return obj.usuarioEmpleado.nombre


@admin.register(ServiciosCitas)
class ServiciosCitasAdmin(admin.ModelAdmin):
    list_display = ('id','servicio','cita','citaId')

    def servicio(self,obj):
        return obj.servicio.nombre_servicio

    def citaId(self,obj):
        return obj.cita.id

    
    
