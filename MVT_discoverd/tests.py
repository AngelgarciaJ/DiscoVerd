from django.test import TestCase

# Create your tests here.

# FILE: MVT_discoverd/tests.py


from django.test import TestCase
from django.urls import reverse
from MVT_discoverd.models import CustomUser  # Importa el modelo de usuario personalizado

class LoginTests(TestCase):

    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='12345')

    def test_login_usuario(self):
        # Datos de inicio de sesión
        data = {
            'email': 'testuser@example.com',
            'password': '12345'
        }
        # Enviar una solicitud POST para iniciar sesión
        response = self.client.post(reverse('login_estudiantes'), data)
        # Verificar que el inicio de sesión fue exitoso
        self.assertEqual(response.status_code, 302)  # Redirección después de iniciar sesión
        self.assertTrue(response.wsgi_request.user.is_authenticated)