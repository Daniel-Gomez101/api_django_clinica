from rest_framework import serializers
from .models import (
    TipoDocumento, MetodoPago, Especialidad, Medico, Paciente,
    Cita, Medicamento, InventarioMedicamento, Tratamiento,
    TratamientoMedicamento, Factura, DetalleFactura, Pago
)

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class InventarioMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioMedicamento
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class TratamientoMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TratamientoMedicamento
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class DetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFactura
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']
