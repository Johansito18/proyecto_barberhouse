from django.shortcuts import render
from .models import Usuarios, Citas, Servicios, Promociones

# Create your views here.

def inicio(request):
    return render(request, 'barberhouse/index.html')


def citas(request):
    c = Citas.objects.all()
    contexto = {'datos': c}
    return render(request, 'barberhouse/citas/listar_citas.html', contexto)
    
    
def servicios(request):
    s = Servicios.objects.all()
    contexto = {'datos': s}
    return render(request, 'barberhouse/servicios/listar_servicios.html', contexto)

def usuarios(request):
    u = Usuarios.objects.all()
    contexto = {'datos': u}
    return render(request, 'barberhouse/usuarios/listar_usuarios.html', contexto)
    
    
def promociones(request):
    p = Promociones.objects.all()
    contexto = {'datos': p}
    return render(request, 'barberhouse/promociones/listar_promociones.html', contexto)


