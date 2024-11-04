from django.contrib import admin
from .models import Autor, Livro

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ['nome']
    
class LivroAdmin(admin.ModelAdmin):
    # Método para restringir a edição apenas aos superusuários
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

admin.site.register(Livro, LivroAdmin)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_play = ('id', 'titulo', 'autor', 'data_publicacao', 'numero_paginas')
    search_fields = ['titulo']
    list_filter = ['autor', 'data_publicacao']
    
    
