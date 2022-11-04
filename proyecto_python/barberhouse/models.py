from django.db import models

# Create your models here.
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol
    
class Usuarios(models.Model):
    cedula_usuario = models.IntegerField(primary_key = True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    correo = models.EmailField()
    clave = models.CharField(max_length=20)
    rol = models.ForeignKey(Rol, on_delete= models.DO_NOTHING, default=3)
    foto = models.ImageField(upload_to = 'barberhouse/fotos', default = 'barberhouse/fotos/default.png')

    
    def __str__(self):          
        return f"{self.nombre}"
    
class Promociones(models.Model):
    nombre_promocion = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    
    def __str__(self):
        return f"{self.nombre_promocion}"
    
class Servicios(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    precio = models.IntegerField()
    promocion = models.ForeignKey(Promociones, on_delete= models.DO_NOTHING)
    empleado = models.ForeignKey(Usuarios, on_delete= models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.nombre_servicio}"
    
class Citas(models.Model):
    fecha_cita = models.DateTimeField()
    usuarioCliente = models.ForeignKey(Usuarios, on_delete= models.DO_NOTHING, related_name = "usuarioCliente")
    usuarioEmpleado = models.ForeignKey(Usuarios, on_delete= models.DO_NOTHING, related_name = "usuarioEmpleado")
    
    
    def __str__(self):
        return f"{self.id} - {self.fecha_cita}"

class ServiciosCitas(models.Model):
    servicio = models.ForeignKey(Servicios, on_delete= models.DO_NOTHING)
    cita = models.ForeignKey(Citas, on_delete= models.DO_NOTHING)

    def __str__(self):
        return f"serv: {self.servicio} cita: {self.cita}"