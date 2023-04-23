from django.shortcuts import render
from django.http import HttpResponse
from AppCoder.models import Curso , Profesor
from AppCoder.forms import CursoFormulario, ProfesorFormulario, UserCreationFormCustom, UserEditForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
# Para el loging 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin







def inicio(request):
    return render(request, 'AppCoder/inicio.html')


def cursos(request):
    if request.method == 'POST':
        
        mi_formulario = CursoFormulario(request.POST) # Acá es donde nos llega la información del HTML
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            curso = Curso(nombre=informacion["curso"], camada=informacion["camada"])
            curso.save()
            return render(request, 'AppCoder/inicio.html')
        
    else:
        mi_formulario = CursoFormulario()
        return render(request, 'AppCoder/cursos.html', {"mi_formulario": mi_formulario})

def profesores(request):
    if request.method == 'POST':
        mi_formulario = ProfesorFormulario(request.POST) # Acá es donde nos llega la información del HTML
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            profesor = Profesor(nombre=informacion["nombre"], apellido=informacion["apellido"], email=informacion["email"], profesion=informacion["profesion"])
            profesor.save()
            return render(request, 'AppCoder/inicio.html')
        
    else:
        mi_formulario = ProfesorFormulario()
        return render(request, 'AppCoder/profesores.html', {"mi_formulario": mi_formulario})
        
            
    
    return render(request, 'AppCoder/profesores.html')


def estudiantes(request):
    return render(request, 'AppCoder/estudiantes.html')


def entregables(request):
    return render(request, 'AppCoder/entregables.html')

# def cursos_formulario(request):
#     if request.method == 'POST':
        
#         mi_formulario = CursoFormulario(request.POST) # Acá es donde nos llega la información del HTML
#         if mi_formulario.is_valid():
#             informacion = mi_formulario.cleaned_data
#             curso = Curso(nombre=informacion["curso"], camada=informacion["camada"])
#             curso.save()
#             return render(request, 'AppCoder/inicio.html')
        
#     else:
#         mi_formulario = CursoFormulario()
#         return render(request, 'AppCoder/cursos_formulario.html', {"mi_formulario": mi_formulario})

            
def buscar_camada(request):
    return render(request, "AppCoder/buscar_camada.html")

def buscar(request):
    if request.GET["camada"]:
        camada = request.GET['camada']
        cursos = Curso.objects.filter(camada__icontains=camada)
        
        return render(request, 'AppCoder/resultadosBusqueda.html', {'cursos': cursos, 'camada': camada})
    else:
        respuesta = 'No enviaste datos.'
        return HttpResponse(respuesta)
    
def leer_profesores(request):
    profesores = Profesor.objects.all() # todos los profesores de la base de datos.
    contexto = {"profesores": profesores}
    
    return render(request, "AppCoder/leerProfesores.html", contexto)

def emilinar_profesor(request, profesor_nombre):
    profesor = Profesor.objects.get(nombre=profesor_nombre)
    profesor.delete()
    
    profesores = Profesor.objects.all()  # trae todos los profesores
    contexto = {"profesores": profesores}
    return render(request, "AppCoder/leerProfesores.html", contexto)


def editar_profesor(request, profesor_nombre):

    # Recibe el nombre del profesor que vamos a modificar
    profesor = Profesor.objects.get(nombre=profesor_nombre)

    # Si es metodo POST hago lo mismo que el agregar
    if request.method == 'POST':

        # aquí mellega toda la información del html
        miFormulario = ProfesorFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid():  # Si pasó la validación de Django

            informacion = miFormulario.cleaned_data

            profesor.nombre = informacion['nombre']
            profesor.apellido = informacion['apellido']
            profesor.email = informacion['email']
            profesor.profesion = informacion['profesion']

            profesor.save()

            # Vuelvo al inicio o a donde quieran
            return render(request, "AppCoder/inicio.html")
    # En caso que no sea post
    else:
        # Creo el formulario con los datos que voy a modificar
        miFormulario = ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido': profesor.apellido,
                                                   'email': profesor.email, 'profesion': profesor.profesion})

    # Voy al html que me permite editar
    return render(request, "AppCoder/editarProfesor.html", {"miFormulario": miFormulario, "profesor_nombre": profesor_nombre})


class CursoListView(ListView):
    model = Curso
    context_object_name = "cursos"
    template_name = "AppCoder/cursos_lista.html"     
  
                          
class CursoDetailView(DetailView):
    model = Curso
    template_name = "AppCoder/curso_detalle.html"
   
    
class CursoCreateView(CreateView):
    model = Curso
    template_name = "AppCoder/curso_crear.html"
    success_url = reverse_lazy('ListaCursos')
    fields = ['nombre', 'camada']
    

class CursoUpdateView(UpdateView):
    model = Curso
    template_name = "AppCoder/curso_editar.html"
    success_url = reverse_lazy('ListaCursos')
    fields = ['nombre', 'camada']
    
    
class CursoDeleteView(DeleteView):
    model = Curso
    template_name = "AppCoder/curso_borrar.html"
    success_url = reverse_lazy('ListaCursos')
    

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        

        if form.is_valid():  # Si pasó la validación de Django
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)
            
            login(request, user)
            
            return render(request, "AppCoder/inicio.html", {"mensaje": f'Bienvenido {user.username}'})
    else:
        form = AuthenticationForm()
    return render(request, "AppCoder/login.html", {"form": form})

        
def registro(request):
      if request.method == 'POST':

            form = UserCreationFormCustom(request.POST)
            if form.is_valid():

                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Usuario Creado :)"})

      else:
        form = UserCreationFormCustom()       
        return render(request,"AppCoder/registro.html" ,  {"form":form})

                      

def editarPerfil(request):
    usuario = request.user
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=request.user)
        if miFormulario.is_valid():
            if miFormulario.cleaned_data.get('imagen'):
                usuario.avatar.imagen = miFormulario.cleaned_data.get('imagen')
                usuario.avatar.save()
           
            miFormulario.save()
            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = UserEditForm(initial={'imagen': usuario.avatar.imagen}, instance=request.user)
    return render(request, "AppCoder/editar_perfil.html", {"miFormulario": miFormulario, "usuario": usuario})

class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name = 'AppCoder/cambiar_contrasenia.html'
    success_url = reverse_lazy('EditarPerfil')
    
    
