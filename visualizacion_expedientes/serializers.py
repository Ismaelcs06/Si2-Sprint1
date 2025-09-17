# visualizacion_expedientes/serializers.py
from rest_framework import serializers
from gestdocu.models import TipoDocumento, Documento, Caso, Expediente ,Tiene# Importar Expediente
from accounts.models import User, Cliente

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    # Asegúrate de que los querysets apunten a los modelos correctos
    creado_por = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False) # created_by se asigna en la vista, no en el formulario
    expediente = serializers.PrimaryKeyRelatedField(queryset=Expediente.objects.all()) # ¡CORRECCIÓN AQUÍ!
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())

    class Meta:
        model = Documento
        fields = '__all__'

class TieneSerializer(serializers.ModelSerializer):
    # Asegúrate de que Caso y Cliente estén importados y que el queryset sea correcto
    caso = serializers.PrimaryKeyRelatedField(queryset=Caso.objects.all()) # ¡CORRECCIÓN AQUÍ!
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())

    class Meta:
        model = Tiene
        fields = '__all__'