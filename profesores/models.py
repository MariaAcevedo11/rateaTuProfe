from django.db import models
from django.db.models import Avg
# Create your models here.

class Usuario(models.Model):
    nombreUsuario = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10, null = False, blank = False)

    def __str__(self):
        return self.nombreUsuario

class Semestre(models.Model):
    numeroSemestre = models.PositiveIntegerField()

    def __str__(self):
        return f"Semestre {self.numeroSemestre}"

class Materia(models.Model):
    nombreMateria = models.CharField(max_length=100)
    semestreEnQueSeCursa = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='materias')

    def __str__(self):
        return self.nombreMateria
    
class Profesor(models.Model):
    nombreProfesor = models.CharField(max_length=100)
    materiasQueDa = models.ManyToManyField('Materia', related_name='profesores')

    def __str__(self):
        return self.nombreProfesor

    def promedioClaridad(self):
        return self.comentarios.aggregate(avg=Avg('calificacionClaridad'))['avg'] or 0

    def promedioExigencia(self):
        return self.comentarios.aggregate(avg=Avg('calificacionExigencia'))['avg'] or 0

    def promedioRespeto(self):
        return self.comentarios.aggregate(avg=Avg('calificacionRespeto'))['avg'] or 0

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField(blank=True)
    calificacionClaridad = models.PositiveIntegerField()
    calificacionExigencia = models.PositiveIntegerField()
    calificacionRespeto = models.PositiveIntegerField()
    recomienda = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario} sobre {self.profesor}"
