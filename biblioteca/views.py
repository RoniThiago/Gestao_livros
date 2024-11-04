from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import generics
from .models import Autor, Livro 
from .serializers import AutorSerializer, LivroSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from django.utils import timezone
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Count


class AutorViewSet (viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    
    def create(self, request, *args, **kwargs):
        if Autor.objects.filter(nome=request.data.get('nome')).exists():
            return Response({"detail": "Autor já existe."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
class LivroViewSet (viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'autor_nome']
    
    @action(detail=True, methods=['patch'])
    def atualizar_titulo(self, request, pk=None):
           livro = self.get_object()
           livro.titulo = request.data.get('titulo')
           livro.save()
           return Response({'status': 'Título atualizado!'})
    
    def get_queryset(self):
         um_ano_atras = timezone.now() - timezone.timedelta(days=365)
         return Livro.objects.filter(data_publicacao_gte=um_ano_atras)
     


class LivroPagination(PageNumberPagination):
    page_size = 10 

class LivroListView(generics.ListAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    pagination_class = LivroPagination
    
class EstatisticasLivrosView(APIView):
    def get(self, request):
        total_livros = livro.objects.count()
        livros_por_autor = Livro.objects.values('autor_nome').annotate(total=Count('id'))
        return Response ({
                'total_livros':total_livros,
                'livros_por_autor': list(livros_por_autor),
            })
             
    
