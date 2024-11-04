from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, LivroViewSet
from django.urls import path, include
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'livros', LivroViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('livros/estatisticas/',EstatisticaLivrosView.as_view(), name='estatisticas_livros'),
]