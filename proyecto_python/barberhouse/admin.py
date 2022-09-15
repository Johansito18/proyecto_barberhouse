from django.contrib import admin
from .models import Rol,Usuarios,Promociones,Citas,Servicios

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rol')

@admin.register(Usuarios)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('cedula_usuario', 'nombre', 'apellido', 'rol')
    
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
    list_display = ('id','fecha_cita','cliente','servicio')

    def cliente(self,obj):
        return obj.cliente.nombre
    
    def servicio(self,obj):
        return obj.servicio.nombre_servicio
    

    
    
