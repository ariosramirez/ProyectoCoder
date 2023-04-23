from django.urls import path
from AppCoder import views
from django.contrib.auth.views import LogoutView

# Para las imagenes
from django.conf import settings
from django.conf.urls.static import static
from ProyectoCoder.settings import  MEDIA_URL, MEDIA_ROOT



urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('cursos/', views.cursos, name="Cursos"),
    path('profesores/',views.profesores, name="Profesores"),
    path('estudiantes/',views.estudiantes, name="Estudiantes"),    
    path('entregables/',views.entregables, name="Entregables"),   
    # path('cursosFormulario/',views.cursos_formulario, name="Cursos formulario"),   
    path('buscarCamada/',views.buscar_camada, name="Burcar Camada"),
    path('buscar/', views.buscar, name="buscar"),
    path('leerProfesores/', views.leer_profesores, name="LeerProfesores"),
    path('eliminarProfesor/<profesor_nombre>/', views.emilinar_profesor, name= "EliminarProfesor"),
    path('editarProfesor/<profesor_nombre>/', views.editar_profesor, name="EditarProfesor"),
    
    
    path('cursos/lista', views.CursoListView.as_view(), name = "ListaCursos"),
    path('cursos/nuevo', views.CursoCreateView.as_view(), name = "NuevoCurso"),
    path('cursos/<pk>', views.CursoDetailView.as_view(), name = "DetalleCurso"),
    path('cursos/<pk>/editar', views.CursoUpdateView.as_view(), name = "EditarCurso"),
    path('cursos/<pk>/borrar', views.CursoDeleteView.as_view(), name = "BorrarCurso"),
    # Loging y logout
    path('login/', views.login_request, name="Login"),
    path('registro/', views.registro, name="Registro"),
    path('logout/', LogoutView.as_view(template_name='AppCoder/logout.html'), name='Logout'),
    path('editarPerfil/', views.editarPerfil, name="EditarPerfil"),
    path('cambiarContrasenia', views.CambiarContrasenia.as_view(), name="CambiarContrasenia"),

]

urlpatterns+= static(MEDIA_URL, document_root=MEDIA_ROOT)
