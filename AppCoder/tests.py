from django.test import TestCase, Client

from django.urls import reverse
from django.contrib.auth.models import User

from models import Profesor



class RegistrarTestCase(TestCase):
    def setUp(self):
       self.profesor = Profesor.objects.create(nombre="Juan", apellido="Perez", email="juan@gmail.com", profesion="Ingeniero")
       self.url = reverse('EliminarProfesor', args=[self.profesor.nombre])
       
    def test_eliminar_profesor(self):
        respuesta = self.client.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        
        self.assertTemplateUsed(respuesta, 'AppCoder/leerProfesores.html')
        self.assertQuerysetEqual(Profesor.objects.all(), [])

 
