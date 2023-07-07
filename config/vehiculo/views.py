from django.shortcuts import render, redirect
from .forms import VehiculoForm
from .models import Vehiculo 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import permission_required

# Create your views here.



#======================================index=============================================

def index(request):
    return render(request, 'index.html')

#================= FUNCIONES DE AUTENTICACION ==============================
def login_view(request):
    print('llego a login?')
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Iniciaste sesion como: {username}")
                return HttpResponseRedirect("/")
            else:
                messages.error(request,"Invalido username o password")
                return HttpResponseRedirect("/")
    else:
        messages.error(request,"Invalido username o password")
        form = AuthenticationForm()
    return render(request=request, template_name="login.html",context={"login_form":form})

#RegistrO

def registro_view(request):
    if request.method == "POST":

        form = RegistroUsuarioForm(request.POST)
        print(f'form es valido: {form.is_valid()}')
        if form.is_valid():
            user = form.save()

            login(request,user)
            print(f"request: {request}")
            print(f"user: {user}")
            messages.success(request, "Registrado Satisfactoriamente." )
            return HttpResponseRedirect('/') 
        messages.error(request, "Registro invalido. Algunos datos ingresados no son correctos")
    print('FALLO POST')
    form = RegistroUsuarioForm()   
    return render (request=request, template_name="registro.html", context={"register_form":form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

#======================================Funcion para add vehiculo=============================================
@permission_required('vehiculo.add_vehiculomodel', raise_exception=True)
def add_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            print('form valido')
            form.save()
            return redirect('index')  # Redirigir a la página de inicio o a otra URL después de guardar el vehículo
    else:
        form = VehiculoForm()
        
    
    context = {'form': form}
    return render(request, 'add_vehiculo.html', context)

#==================================Funcion para listar vehiculos===========================

@permission_required('vehiculo.visualizar_catalogo', raise_exception=True)
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()

    # Asignar condiciones de precios a los vehículos

    for vehiculo in vehiculos:
        if vehiculo.precio <= 10000:
            vehiculo.condicion_precio = "Bajo"
        elif vehiculo.precio > 10000 and vehiculo.precio <= 30000:
            vehiculo.condicion_precio = "Medio"
        else:
            vehiculo.condicion_precio = "Alto"

    return render(request, 'lista_vehiculos.html', {'vehiculos': vehiculos})
