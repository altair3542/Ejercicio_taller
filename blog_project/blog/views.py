from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import PostForm

# Create your views here.

def lista_publicaciones(request):
    query = request.GET.get('q')
    categoria = request.GET.get('categoria')
    fecha_publicacion = request.GET.get('fecha_publicacion')
    publicaciones = Post.objects.all()

    if query:
        publicaciones = publicaciones.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query)
        )

    if categoria:
        publicaciones = publicaciones.filter(categoria__icontains=categoria)

    if fecha_publicacion:
        publicaciones = publicaciones.filter(fecha_publicacion=fecha_publicacion)


    paginator = Paginator(publicaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/lista_publicaciones.html', {
        'page_obj': page_obj,
        'query': query,
        'categoria': categoria,
        'fecha_publicacion': fecha_publicacion,
        })

def detalle_publicacion(request,pk):
    publicacion = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detalle_publicacion.html', {'publicacion': publicacion})

def crear_publicacion(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_publicaciones')
    else:
        form = PostForm
    return render(request, 'blog/crear_publicacion.html', {'form': form})


def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=publicacion)
        if form.is_valid():
            publicacion = form.save()
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        form = PostForm(instance=publicacion)
    return render(request, 'blog/editar_publicacion.html', {'form': form, 'publicacion': publicacion})
