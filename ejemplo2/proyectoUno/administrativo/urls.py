"""
    Manejo de urls para la aplicación
    administrativo
"""
from django.urls import path, include
# se importa las vistas de la aplicación
from administrativo import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'numerosts', views.NumeroTelefonicoViewSet)


urlpatterns = [
        path('', views.index, name='index'),
        path('estudiante/<int:id>', views.obtener_estudiante,
            name='obtener_estudiante'),
        path('crear/estudiante', views.crear_estudiante,
            name='crear_estudiante'),
        path('editar_estudiante/<int:id>', views.editar_estudiante,
            name='editar_estudiante'),
        path('eliminar/estudiante/<int:id>', views.eliminar_estudiante,
            name='eliminar_estudiante'),
        # numeros telefonicos
        path('crear/numero/telefonico', views.crear_numero_telefonico,
            name='crear_numero_telefonico'),
        path('editar/numero/telefonico/<int:id>', views.editar_numero_telefonico,
            name='editar_numero_telefonico'),
        path('crear/numero/telefonico/estudiante/<int:id>',
            views.crear_numero_telefonico_estudiante,
            name='crear_numero_telefonico_estudiante'),
        path('saliendo/logout/', views.logout_view, name="logout_view"),
        path('entrando/login/', views.ingreso, name="login"),
        path('api/', include(router.urls)),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

 ]
