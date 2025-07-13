from django.contrib import admin

# Register your models here.

from .models import Usuario, Semestre, Materia, Profesor, Comentario

admin.site.register(Usuario)
admin.site.register(Semestre)
admin.site.register(Materia)
admin.site.register(Profesor)
admin.site.register(Comentario)