# visualizacion_expedientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from gestdocu.models import TipoDocumento, Documento, Caso, Expediente, Tiene
from accounts.models import Cliente, User # Asegúrate de importar User y Cliente
from .serializers import TipoDocumentoSerializer, DocumentoSerializer, TieneSerializer
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
# --- Vistas para TipoDocumento ---

@permission_classes([IsAuthenticated])
def tipo_documento_list(request):
    tipos_documento = TipoDocumento.objects.all()
    context = {'tipos_documento': tipos_documento}
    return render(request, 'visualizacion_expedientes/tipo_documento_list.html', context)

@permission_classes([IsAuthenticated])
def tipo_documento_create(request):
    if request.method == 'POST':
        serializer = TipoDocumentoSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Tipo de documento creado exitosamente.')
            return redirect('tipo_documento_list')
        else:
            messages.error(request, 'Error al crear el tipo de documento. Verifique los datos.')
    else:
        serializer = TipoDocumentoSerializer()
    
    context = {'serializer': serializer, 'form_title': 'Crear Tipo de Documento'}
    return render(request, 'visualizacion_expedientes/tipo_documento_form.html', context)

@permission_classes([IsAuthenticated])
def tipo_documento_update(request, pk):
    tipo_documento = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == 'POST':
        serializer = TipoDocumentoSerializer(tipo_documento, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Tipo de documento actualizado exitosamente.')
            return redirect('tipo_documento_list')
        else:
            messages.error(request, 'Error al actualizar el tipo de documento. Verifique los datos.')
    else:
        serializer = TipoDocumentoSerializer(tipo_documento)
    
    context = {'serializer': serializer, 'form_title': 'Editar Tipo de Documento'}
    return render(request, 'visualizacion_expedientes/tipo_documento_form.html', context)

@permission_classes([IsAuthenticated])
def tipo_documento_delete(request, pk):
    tipo_documento = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == 'POST':
        try:
            tipo_documento.delete()
            messages.success(request, 'Tipo de documento eliminado exitosamente.')
            return redirect('tipo_documento_list')
        except ProtectedError:
            messages.error(request, 
                           f'No se puede eliminar el tipo de documento "{tipo_documento.nombre}" '
                           'porque tiene documentos asociados. Primero reasigne o elimine los documentos relacionados.')
            return redirect('tipo_documento_list') # O puedes redirigir de nuevo a la página de confirmación con el error
    context = {'tipo_documento': tipo_documento}
    return render(request, 'visualizacion_expedientes/tipo_documento_confirm_delete.html', context)

# --- Vistas para Documento ---

@permission_classes([IsAuthenticated])
def documento_list(request):
    documentos = Documento.objects.all()
    context = {'documentos': documentos}
    return render(request, 'visualizacion_expedientes/documento_list.html', context)

@permission_classes([IsAuthenticated])
def documento_create(request):
    if request.method == 'POST':
        # CORRECCIÓN: Combina POST y FILES en un solo diccionario
        data = request.POST.copy()  # Crea una copia mutable
        data.update(request.FILES)  # Añade los archivos al diccionario
        
        serializer = DocumentoSerializer(data=data)
        if serializer.is_valid():
            # Asignar el usuario actual como 'creado_por'
            serializer.save(creado_por=request.user)
            messages.success(request, 'Documento creado exitosamente.')
            return redirect('documento_list')
        else:
            messages.error(request, 'Error al crear el documento. Verifique los datos.')
    else:
        serializer = DocumentoSerializer()
    
    context = {
        'serializer': serializer, 
        'form_title': 'Crear Documento',
        'expedientes': Expediente.objects.all(), # Necesario para el selector de expediente
        'tipos_documento': TipoDocumento.objects.all(), # Necesario para el selector de tipo
    }
    return render(request, 'visualizacion_expedientes/documento_form.html', context)


@permission_classes([IsAuthenticated])
def documento_update(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        # CORRECCIÓN: Combina POST y FILES en un solo diccionario
        data = request.POST.copy()  # Crea una copia mutable
        data.update(request.FILES)  # Añade los archivos al diccionario
        
        serializer = DocumentoSerializer(documento, data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Documento actualizado exitosamente.')
            return redirect('documento_list')
        else:
            messages.error(request, 'Error al actualizar el documento. Verifique los datos.')
    else:
        serializer = DocumentoSerializer(documento)
    
    context = {
        'serializer': serializer, 
        'form_title': 'Editar Documento',
        'expedientes': Expediente.objects.all(),
        'tipos_documento': TipoDocumento.objects.all(),
    }
    return render(request, 'visualizacion_expedientes/documento_form.html', context)

@permission_classes([IsAuthenticated])
def documento_delete(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        documento.delete()
        messages.success(request, 'Documento eliminado exitosamente.')
        return redirect('documento_list')
    context = {'documento': documento}
    return render(request, 'visualizacion_expedientes/documento_confirm_delete.html', context)


# --- Vistas para Tiene (Relación Caso-Cliente) ---

@permission_classes([IsAuthenticated])
def tiene_list(request):
    relaciones_tiene = Tiene.objects.all()
    context = {'relaciones_tiene': relaciones_tiene}
    return render(request, 'visualizacion_expedientes/tiene_list.html', context)

@permission_classes([IsAuthenticated])
def tiene_create(request):
    if request.method == 'POST':
        serializer = TieneSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Relación Caso-Cliente creada exitosamente.')
            return redirect('tiene_list')
        else:
            messages.error(request, 'Error al crear la relación. Verifique los datos.')
    else:
        serializer = TieneSerializer()
    
    context = {
        'serializer': serializer, 
        'form_title': 'Crear Relación Caso-Cliente',
        'casos': Caso.objects.all(),      # Necesario para el selector de caso
        'clientes': Cliente.objects.all(), # Necesario para el selector de cliente
    }
    return render(request, 'visualizacion_expedientes/tiene_form.html', context)

@permission_classes([IsAuthenticated])
def tiene_update(request, pk):
    tiene_instance = get_object_or_404(Tiene, pk=pk)
    if request.method == 'POST':
        serializer = TieneSerializer(tiene_instance, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Relación Caso-Cliente actualizada exitosamente.')
            return redirect('tiene_list')
        else:
            messages.error(request, 'Error al actualizar la relación. Verifique los datos.')
    else:
        serializer = TieneSerializer(tiene_instance)
    
    context = {
        'serializer': serializer, 
        'form_title': 'Editar Relación Caso-Cliente',
        'casos': Caso.objects.all(),
        'clientes': Cliente.objects.all(),
    }
    return render(request, 'visualizacion_expedientes/tiene_form.html', context)

@permission_classes([IsAuthenticated])
def tiene_delete(request, pk):
    tiene_instance = get_object_or_404(Tiene, pk=pk)
    if request.method == 'POST':
        tiene_instance.delete()
        messages.success(request, 'Relación Caso-Cliente eliminada exitosamente.')
        return redirect('tiene_list')
    context = {'tiene_instance': tiene_instance}
    return render(request, 'visualizacion_expedientes/tiene_confirm_delete.html', context)

# --- Tu vista de visualización jerárquica ---
@login_required
def expedientes_jerarquicos(request):
    """
    Vista para mostrar expedientes en estructura jerárquica:
    Cliente → Caso → Expediente → Documentos
    """
    
    clientes_con_casos = []
    
    for cliente in Cliente.objects.all():
        casos_del_cliente = []
        
        for caso in cliente.casos.all():
            expedientes_del_caso = []
            
            for expediente in caso.expedientes.all():
                documentos_del_expediente = expediente.documentos.all()
                
                expedientes_del_caso.append({
                    'expediente': expediente,
                    'documentos': documentos_del_expediente,
                    'total_documentos': documentos_del_expediente.count()
                })
            
            casos_del_cliente.append({
                'caso': caso,
                'expedientes': expedientes_del_caso,
                'total_expedientes': len(expedientes_del_caso),
                'total_documentos': sum(exp['total_documentos'] for exp in expedientes_del_caso)
            })
        
        if casos_del_cliente:
            clientes_con_casos.append({
                'cliente': cliente,
                'casos': casos_del_cliente,
                'total_casos': len(casos_del_cliente)
            })
    
    context = {
        'clientes_con_casos': clientes_con_casos,
        'total_clientes': len(clientes_con_casos)
    }
    
    return render(request, 'visualizacion_expedientes/expedientes_jerarquicos.html', context)