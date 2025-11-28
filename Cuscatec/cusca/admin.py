from .models import PerfilUsuario, StudentNews
from django.contrib import admin

admin.site.register(PerfilUsuario)


class StudentNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información de la Noticia', {
            'fields': ('title', 'content')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Metadatos', {
            'fields': ('author', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva noticia
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(StudentNews, StudentNewsAdmin)
