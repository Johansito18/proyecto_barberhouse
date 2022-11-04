from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import ServiciosCitas, Usuarios, Citas, Servicios, Promociones, Rol

# Mensajes tipo Cookie temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError

#Paginador
from django.core.paginator import Paginator

#Buscar
from django.db.models import Q

from .crypt import claveEncriptada
from django.core.mail import send_mail



#Almacenamiento y gestión de archivos o fotos
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from os import remove, path 
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

def inicio(request):
    return render(request, 'barberhouse/index.html')


def loginForm(request):
    return render(request,'barberhouse/login/login.html')

def login(request):
    try:
        correo = request.POST["correo"]
        clave = request.POST["clave"]

        # r = Rol.objects.all(nombre_rol = nombre_rol)
        
        u = Usuarios.objects.get(correo = correo, clave = clave)

        request.session["logueo"] = [u.cedula_usuario, u.nombre, u.apellido, u.rol.nombre_rol]

        return redirect('barberhouse:inicio')
    except:
        messages.warning(request,"no se han enviado datos")
        return redirect('barberhouse:inicio')

def loginCerrar(request):
    try:
        del request.session["logueo"]
        messages.success(request, "session cerrada")
    except Exception as e:
        messages.warning(request, "ocurrio un error: ", e)
    return redirect('barberhouse:inicio')

def perfil(request):
    login = request.session.get('logueo', False)
    q = Usuarios.objects.get(pk = login[0])

    contexto = {"perfil": q}

    return render(request, 'barberhouse/usuarios/perfil.html', contexto)

def actualizarPerfil(request):
    if request.method == "POST":
        try:
            login = request.session.get('logueo', False)
            q = Usuarios.objects.get(pk = login[0])
            q.cedula_usuario = request.POST["cedula"]
            q.nombre = request.POST["nombre"]
            q.apellido = request.POST["apellido"]
            q.fecha_nacimiento = request.POST["fecha"]

            if q.correo != request.POST["correo"]:
                try:
                    c = Usuarios.objects.get(correo = request.POST["correo"])
                    raise Exception("Este correo ya existe")
                except Usuarios.DoesNotExist:
                    messages.debug(request, "--El resultado de la consulta es: OK--")
                    q.correo = request.POST["correo"]
            else:
                messages.debug(request, "--No hay cambios en el correo --")
                q.correo = request.POST["correo"]

            if request.POST["clave"] != "":
                q.clave = claveEncriptada(request.POST["clave"])
            q.save()
        except Usuarios.DoesNotExist:
            messages.error(request, "No existe el usuario...")    
        except Exception as e:
            messages.error(request, f'Error: {e}')
    else:
        messages.warning(request, "No Envio datos")

    return redirect('barberhouse:Perfil_Usuario')


# enviar correos
def sendMail(request):
    try:
        send_mail(
            'Mi coshi',
            'Mi muñeca hermosa, sabes que te amo tanto mi bebe y estoy tan orgulloso de ti, de ver la mujer ta luchadora que tengo a mi lado, de versad te felicito por estar cumpliendo tus metas, TE AMO MI FLAcA',
            'd4v1d1521@gmail.com',
            ['alexandraarenas0213@gmail.com'],
            fail_silently=False,
        )
        messages.info(request, "correo de prueba enviado con exito")
    except Exception as e:
        messages.error(request, f"error: {e}")
    return redirect('barberhouse:loginForm')
    


#Roles
def roles(request):
    
    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        r = Rol.objects.all()
    
        p = Paginator(r,3 )
    
        page_number = request.GET.get('page')

        r = p.get_page(page_number)

        contexto = {'datos': r}
        return render(request, 'barberhouse/roles/listar_roles.html', contexto)
    else:
        if login and (login[3] != "Admin"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')

    

def rolesBuscar(request):
    if request.method == "POST":

        q = roles.objects.filter(
            Q(nombre_rol__icontains = request.POST["buscar"])
        )

        p = Paginator(q, 20)
        p_number = request.GET.get('page')

        u = p.get_page(p_number)

        contexto = {'page_obj': u, 'Datos': request.POST["buscar"]}

        return render(request,'barberhouse/roles/listar_roles_ajax.html',contexto)
    else:
        messages.warning(request,"no se han enviado datos")
        return redirect('barberhouse:listarRoles')


def formularioRol(request):

    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        return render(request, 'barberhouse/roles/crear_roles.html')
    else:
        if login and (login[3] != "Admin"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')

def guardarRol(request):
    try:
        if request.method == "POST":
            r = Rol(
                nombre_rol = request.POST["Nombre"] 
            )
            r.save()
            messages.success(request, "Rol agregado correctamente")
            return redirect('barberhouse:listarRoles')
        else:
            messages.warning(request, "No se enviaron datos")   
    except Exception as e:
        messages.error(request,"Error: " + str(e))
        return redirect('barberhouse:listarRoles')


def editarRol(request,id):
    
    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        e = Rol.objects.get(pk = id)
        contexto = {"datos": e}
        return render(request, 'barberhouse/roles/editar_roles.html', contexto)

    else:
        if login and (login[3] != "Admin"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')


def actualizarRol(request):
    try:
        if request.method == "POST":
            r = Rol.objects.get(pk = request.POST["id"])

            r.nombre_rol = request.POST["Nombre"]

            r.save()

            messages.success(request, "Rol actualizado")
            return redirect('barberhouse:listarRoles')
        else:
            messages.warning(request,"No se enviaron datos")
            return redirect('barberhouse:listarRoles')
    except Exception as e:
        messages.error(request, "error: " + str(e))
        return redirect('barberhouse:listarRoles')

def eliminarRol(request,id):
    try:
        p = Rol.objects.get(pk = id)
        p.delete()
        
        return HttpResponseRedirect(reverse('barberhouse:listarRoles'))
    except Rol.DoesNotExist:
        return HttpResponse('ERROR: Rol no existe')
    except Exception as e:
        return HttpResponse(f'error: {e}')


        

#Usuarios
def usuarios(request):
    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        u = Usuarios.objects.all()

        p = Paginator(u, 2)
        
        p_number = request.GET.get('page')

        u = p.get_page(p_number)

        contexto = {'datos': u}
        return render(request, 'barberhouse/usuarios/listar_usuarios.html', contexto)
    else:
        if login and login[3] != "Admin":
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')

def usuariosBuscar(request):
    if request.method == "POST":

        q = Usuarios.objects.filter(
            Q(cedula__icontains = request.POST["buscar"])|
            Q(nombre__icontains = request.POST["buscar"])|
            Q(apellido__icontains = request.POST["buscar"])|
            Q(rol__icontains = request.POST["buscar"])
            )

        p = Paginator(q, 20)
        p_number = request.GET.get('page')

        u = p.get_page(p_number)

        contexto = {'page_obj': u, 'Datos': request.POST["buscar"]}

        return render(request,'barberhouse/usuarios/listar_usuario_ajax.html',contexto)
    else:
        messages.warning(request,"no se han enviado datos")
        return redirect('barberhouse:usuarios')


def usuariosFormulario(request):

    login = request.session.get('logueo', False)
    if login == False:
        
        return render(request, 'barberhouse/usuarios/registrar_cliente.html')

    elif login and (login[3] == "Admin"):

        r = Rol.objects.all()
        contexto = {'datos': r}
        return render(request, 'barberhouse/usuarios/crear_usuarios.html',contexto)
    
    else:
        if login and (login[3] != "Admin"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')



def usuariosGuardar(request):
    try:
        if request.method == "POST":
            print(request.FILES)
            if request.FILES:
                #Crear instancia de File System Storage
                fss = FileSystemStorage()
                #Capturar la foto del formulario
                f = request.FILES["foto"]
                #Cargar archivo al servidor
                file = fss.save("barberhouse/fotos/" + f.name, f)
                print("Si foto--------------------")
            else:
                print("No foto.......................")
                file = "barberhouse/fotos/default.png"

            u = Usuarios(
                cedula_usuario = request.POST["cedula_usuario"],
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                fecha_nacimiento = request.POST["fecha_nacimiento"],
                rol = Rol.objects.get(pk = request.POST["rol"]),
                foto = file,
                correo = request.POST["correo"],
                clave = claveEncriptada(request.POST["clave"]),
            )
            u.save()

            messages.success(request, "Usuario guardado correctamente!")
            return redirect('barberhouse:listarUsuarios')
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarUsuarios')
    except Exception as e:
        
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarUsuarios')

def clientesGuardar(request):
    try:
        if request.method == "POST":
            print(request.FILES)
            if request.FILES:
                #Crear instancia de File System Storage
                fss = FileSystemStorage()
                #Capturar la foto del formulario
                f = request.FILES["foto"]
                #Cargar archivo al servidor
                file = fss.save("barberhouse/fotos/" + f.name, f)
                print("Si foto--------------------")
            else:
                print("No foto.......................")
                file = "barberhouse/fotos/default.png"

            u = Usuarios(
                cedula_usuario = request.POST["cedula_usuario"],
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                fecha_nacimiento = request.POST["fecha_nacimiento"],
                foto = file,
                correo = request.POST["correo"],
                clave = request.POST["clave"],
            )
            u.save()

            messages.success(request, "Usuario guardado correctamente!")
            return redirect('barberhouse:listarUsuarios')
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarUsuarios')
    except Exception as e:
        
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarUsuarios')
        
def usuariosEditar(request,id):
    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        u = Usuarios.objects.get(pk = id)
        r = Rol.objects.all()
        
        contexto = {"usuario": u, "roles": r}
        return render(request, 'barberhouse/usuarios/editar_usuarios.html',contexto)
    else:
        if login and login[3] != "Admin":
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')

    

def usuariosActualizar(request):
    try:
        if request.method == "POST":
            u = Usuarios.objects.get(pk = request.POST["cedula_usuario"])

            if request.FILES:
                ruta_foto = str(BASE_DIR) + str(u.foto.url)
                if path.exists(ruta_foto):
                    if u.foto.url != "/uploads/barberhouse/fotos/default.png":
                        remove(ruta_foto)
                else:
                    raise Exception("La foto no existe o no se encuentra.")

                fss = FileSystemStorage()
                f = request.FILES["foto"]
                file = fss.save("territorio/fotos/" + f.name, f)
                
                u.foto = file

            else:
                print("El usuario no seleccionó foto nueva")


            u.nombre = request.POST["nombre"]
            u.apellido = request.POST["apellido"]
            u.fecha_nacimiento = request.POST["fecha_nacimiento"]
            u.rol = Rol.objects.get(pk = request.POST["rol"])
            u.correo = request.POST["correo"]
            u.clave = claveEncriptada(request.POST["clave"])

            u.save()
            
            messages.success(request, "Usuario actualizado correctamente!")
            return redirect('barberhouse:listarUsuarios') 
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarUsuarios') 
        
    except Exception as e:    
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarUsuarios')

def usuariosEliminar(request, id):
    try:
        u = Usuarios.objects.get(pk = id)
        u.delete()
        return HttpResponseRedirect(reverse('barberhouse:listarUsuarios'))
    except Usuarios.DoesNotExist:
        messages.warning(request, 'Usted no envió datos')
        return redirect('barberhouse:listarUsuarios') 
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarUsuarios') 



#Promociones    
def promociones(request):
    
    login = request.session.get('logueo', False)
    if login:

        p = Promociones.objects.all()

        pag = Paginator(p, 10)

        pag_number = request.GET.get('page')

        p = pag.get_page(pag_number)

        contexto = {'datos': p}
        return render(request, 'barberhouse/promociones/listar_promociones.html', contexto)
    else:
        
        messages.warning(request, "Debe iniciar sesión primero...")
        return redirect('barberhouse:loginForm')

def promocionesFormulario(request):
    
    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        return render(request, 'barberhouse/promociones/crear_promociones.html')
    else:
        if login and (login[3] != "Admin"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm') 

def promocionesGuardar(request):
    try:
        if request.method == "POST":
            p = Promociones(
                nombre_promocion = request.POST["nombre_promocion"],
                fecha_inicio = request.POST["fecha_inicio"],
                fecha_fin = request.POST["fecha_fin"],
            )
            p.save()

            messages.success(request, "Promocion guardado correctamente!")
            return redirect('barberhouse:listarPromociones')
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarPromociones')

    except Exception as e:
        
        messages.error(request, "Error: " + str(e))

        return redirect('barberhouse:listarPromociones')

def promocionesEditar(request,id):

    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        p = Promociones.objects.get(pk = id)
    
        contexto = {"datos": p}
        return render(request, 'barberhouse/promociones/editar_promociones.html',contexto)
       
    else:
        if login and (login[3] != "Admin"):

            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')


def promocionesActualizar(request):
    try:
        if request.method == "POST":
            p = Promociones.objects.get(pk = request.POST["id"])
            
            p.nombre_promocion = request.POST["nombre_promocion"]
            p.fecha_inicio = request.POST["fecha_inicio"]
            p.fecha_fin = request.POST["fecha_fin"]
            
            p.save()

            messages.success(request, "Promocion actualizada correctamente!")

            return redirect('barberhouse:listarPromociones') 
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarPromociones')


    except Exception as e:
        
        messages.error(request, "Error: " + str(e))

        return redirect('barberhouse:listarPromociones')

def promocionesEliminar(request,id):
    try:
        p = Promociones.objects.get(pk = id)
        p.delete()

        return HttpResponseRedirect(reverse('barberhouse:listarPromociones'))
    except Promociones.DoesNotExist:
        messages.warning(request, 'ERROR: Promocion no existe')
        return redirect('barberhouse:listarPromociones') 
        
    except Exception as e:
        messages.error(request, 'ERROR: ' + str(e))
        return redirect('barberhouse:listarPromociones') 


#Servicios    
def servicios(request):
    
    login = request.session.get('logueo', False)
    if login:

        s = Servicios.objects.all()
        p = Paginator(s,5)
        p_number = request.GET.get('page')
        s = p.get_page(p_number)
        contexto = {'datos': s}
        return render(request, 'barberhouse/servicios/listar_servicios.html', contexto)
    else:
            
        messages.warning(request, "Debe iniciar sesión primero...")
        return redirect('barberhouse:loginForm')

def serviciosFormulario(request):

    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin"):

        p = Promociones.objects.all()
        e = Usuarios.objects.all()

        contexto = {'promocion': p, 'empleado': e}
        return render(request, 'barberhouse/servicios/crear_servicios.html', contexto)
    else:
        if login and (login[3] != "Admin"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')  

def serviciosGuardar(request):
    try:
        if request.method == "POST":
            s = Servicios(
                nombre_servicio = request.POST["nombre_servicio"],
                precio = request.POST["precio"],
                promocion = Promociones.objects.get(pk = request.POST["promocion"]),
                empleado = Usuarios.objects.get(pk = request.POST["empleado"]),
            )
            s.save()
        
            messages.success(request, "Servicio guardado correctamente!")
            return redirect('barberhouse:listarServicios') 
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarServicios') 
      
    except Exception as e:    
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarServicios')

def serviciosEditar(request, id):
    login = request.session.get('logueo', False)
    if login:

        s = Servicios.objects.get(pk = id)
        p = Promociones.objects.all()
        e = Usuarios.objects.all()

        contexto = {"servicio": s, "promocion": p, "empleado": e}
        return render(request, 'barberhouse/servicios/editar_servicios.html', contexto)
    else:
            
        messages.warning(request, "Debe iniciar sesión primero...")
        return redirect('barberhouse:loginForm')
    

    

def serviciosActualizar(request):
    try:
        if request.method == "POST":
            s = Servicios.objects.get(pk = request.POST["id"])

            s.nombre_servicio = request.POST["nombre_servicio"]
            s.precio = request.POST["precio"]
            s.promocion = Promociones.objects.get(pk = request.POST["promocion"])
            s.empleado = Usuarios.objects.get(pk = request.POST["empleado"])
            
            s.save()
        
            messages.success(request, "Servicio actualizado correctamente!")
            return redirect('barberhouse:listarServicios') 
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarServicios') 
      
    except Exception as e:    
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarServicios')
        

def serviciosEliminar(request, id):
    try:
        s = Servicios.objects.get(pk = id)
        s.delete()

        return HttpResponseRedirect(reverse('barberhouse:listarServicios'))
    except Servicios.DoesNotExist:
        messages.warning(request, 'ERROR: Servicio no existe')
        return redirect('barberhouse:listarServicios')
        
    except Exception as e:
        messages.error(request, 'ERROR: ' + str(e))
        return redirect('barberhouse:listarServicios')
        

#ServiciosCitas
def citas(request):
    login = request.session.get('logueo', False)
    #cookie = request.session.get('serviCookie')

    if login:

        
        c = ServiciosCitas.objects.all()
        #s = Servicios.objects.filter(cita = c)

        #print(cookie)

        p = Paginator(c,3 )
        
        page_number = request.GET.get('page')

        c = p.get_page(page_number)
        
        contexto = {'datos': c}
        return render(request, 'barberhouse/citas/listar_citas.html', contexto)
    else:
        
        messages.warning(request, "Debe iniciar sesión primero...")
        return redirect('barberhouse:loginForm')

    

def citasFormulario(request):
    
    login = request.session.get('logueo', False)
    if login:

        e = Usuarios.objects.all()
        s = Servicios.objects.all() 

        contexto = {'empleado': e, 'cliente':e, 'servicio': s}
        return render(request, 'barberhouse/citas/crear_citas.html', contexto)
    else:
        
        messages.warning(request, "Debe iniciar sesión primero...")
        return redirect('barberhouse:loginForm')  

def citasGuardar(request):
    try:
        if request.method == "POST":

            cita = Citas(
                fecha_cita = request.POST["fecha_cita"],
                usuarioCliente = Usuarios.objects.get(pk = request.POST["cliente"]),
                usuarioEmpleado = Usuarios.objects.get(pk = request.POST["empleado"]),
                
            )
            cita.save()

            servicioCita = ServiciosCitas(
                servicio = Servicios.objects.get(pk = request.POST["servicio"]),
                cita = cita,
            )
            """ serviciosxcita = []
            
            serviciosxcita.append(servicioCita.servicio)
            print(serviciosxcita)

            request.session["serviCookie"] = [servicioCita.servicio.nombre_servicio] """

            servicioCita.save()


        
            messages.success(request, "Cita guardada correctamente!")
            return redirect('barberhouse:listarCitas') 
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarCitas') 

    except Exception as e:    
        """ messages.error(request, "Error: " + str(e)) """
        print(e)
        """ return redirect('barberhouse:listarCitas') """ 
        return HttpResponse(e)
        

def citasEditar(request, id):
    
    login = request.session.get('logueo', False)
    if login and (login[3] == "Admin") or (login[3]=="Barbero") or (login[3]=="Cliente"):

        c = Citas.objects.get(pk = id)
        e = Usuarios.objects.all()
        s = Servicios.objects.all()

        contexto = {"cita": c, "empleado": e, "servicio": s}
        return render(request, 'barberhouse/citas/editar_citas.html', contexto)
    else:
        if login and (login[3] != "Admin") or (login[3]!="Barbero") or (login[3]!="Cliente"):
            messages.warning(request, "Usted no está autorizado para éste módulo...")
            return redirect('barberhouse:inicio')
        else:
            messages.warning(request, "Debe iniciar sesión primero...")
            return redirect('barberhouse:loginForm')

def citasActualizar(request):
    try:
        if request.method == "POST":
            c = Citas.objects.get(pk = request.POST["id"])
            
            c.fecha_cita = request.POST["fecha_cita"]
            c.cliente = Usuarios.objects.get(pk = request.POST["cliente"])
            c.servicio = Servicios.objects.get(pk = request.POST["servicio"])
            
            c.save()
        
            messages.success(request, "Cita actualizada correctamente!")
            return redirect('barberhouse:listarCitas') 
        else:
            messages.warning(request, 'Usted no envió datos')
            return redirect('barberhouse:listarCitas') 

    except Exception as e:    
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarCitas') 

def citasEliminar(request, id):
    try:
        c = Citas.objects.get(pk = id)
        c.delete()

        return HttpResponseRedirect(reverse('barberhouse:listarCitas'))
    except Servicios.DoesNotExist:
        messages.warning(request, 'ERROR: Cita no existe')
        return redirect('barberhouse:listarCitas') 
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('barberhouse:listarCitas') 
