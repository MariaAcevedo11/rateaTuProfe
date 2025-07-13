
from django.shortcuts import render, redirect
# Create your views here.
from .models import Usuario


from django.contrib import messages

def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombreUsuario']
        password = request.POST['password']

        if Usuario.objects.filter(nombreUsuario=nombre).exists():
            messages.error(request, 'Ese nombre de usuario ya está registrado.')
        else:
            Usuario.objects.create(nombreUsuario=nombre, password=password)
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login_usuario')  # Ajusta la URL según tu flujo

    return render(request, 'registro.html')



def login_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombreUsuario']
        password = request.POST['password']

        try:
            usuario = Usuario.objects.get(nombreUsuario=nombre)
            if usuario.password == password:  # Idealmente usar hash
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombreUsuario
                messages.success(request, f'¡Bienvenido {usuario.nombreUsuario}!')
                return redirect('seleccionar_semestre')  # o donde empieza la navegación
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario no existe.')

    return render(request, 'login.html') 

from .models import Semestre

def seleccionar_semestre(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('registro')

    semestres = Semestre.objects.all().order_by('numeroSemestre')
    return render(request, 'semestres.html', {'semestres': semestres})


from .models import Semestre, Materia

def ver_materias(request, semestre_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('registro')

    semestre = Semestre.objects.get(id=semestre_id)
    materias = semestre.materias.all()  # gracias al related_name en el modelo

    return render(request, 'materias.html', {
        'semestre': semestre,
        'materias': materias
    })

from .models import Materia, Profesor

def ver_profesores(request, materia_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('registro')

    materia = Materia.objects.get(id=materia_id)
    profesores = materia.profesores.all()  # gracias a related_name='profesores'

    return render(request, 'profesores.html', {
        'materia': materia,
        'profesores': profesores
    })


from .models import Profesor, Comentario, Usuario
from django.utils import timezone

def ver_comentarios(request, profesor_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('registro')

    profesor = Profesor.objects.get(id=profesor_id)
    comentarios = profesor.comentarios.all()

    if request.method == 'POST':
        calificacionClaridad = int(request.POST['claridad'])
        calificacionExigencia = int(request.POST['exigencia'])
        calificacionRespeto = int(request.POST['respeto'])
        recomienda = request.POST.get('recomienda') == 'on'
        texto = request.POST.get('texto', '')

        Comentario.objects.create(
            usuario=Usuario.objects.get(id=usuario_id),
            profesor=profesor,
            calificacionClaridad=calificacionClaridad,
            calificacionExigencia=calificacionExigencia,
            calificacionRespeto =calificacionRespeto,
            recomienda=recomienda,
            texto=texto,
            fecha=timezone.now()
        )
        return redirect('ver_comentarios', profesor_id=profesor_id)

    return render(request, 'comentarios.html', {
        'profesor': profesor,
        'comentarios': comentarios,
    })