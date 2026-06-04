from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import (
    TipoDocumento,
    MetodoPago,
    Especialidad,
    Medico,
    Paciente,
    Cita,
    Medicamento,
    InventarioMedicamento,
    Tratamiento,
    TratamientoMedicamento,
    Factura,
    DetalleFactura,
    Pago
)

from .serializers import (
    TipoDocumentoSerializer,
    MetodoPagoSerializer,
    EspecialidadSerializer,
    MedicoSerializer,
    PacienteSerializer,
    CitaSerializer,
    MedicamentoSerializer,
    InventarioMedicamentoSerializer,
    TratamientoSerializer,
    TratamientoMedicamentoSerializer,
    FacturaSerializer,
    DetalleFacturaSerializer,
    PagoSerializer
)


class BaseViewSet(viewsets.ModelViewSet):

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Petición exitosa',
            'data': serializer.data
        })

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'success': True,
                'status': 201,
                'message': 'Registro creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'status': 400,
            'message': 'Error al crear el registro',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object())

            return Response({
                'success': True,
                'status': 200,
                'message': 'Petición exitosa',
                'data': serializer.data
            })

        except:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Registro no encontrado',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(
                self.get_object(),
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()

                return Response({
                    'success': True,
                    'status': 200,
                    'message': 'Registro actualizado exitosamente',
                    'data': serializer.data
                })

            return Response({
                'success': False,
                'status': 400,
                'message': 'Error al actualizar',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Registro no encontrado',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.activo = False
            instance.save()

            return Response({
                'success': True,
                'status': 200,
                'message': 'Registro desactivado exitosamente',
                'data': {}
            })

        except:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Registro no encontrado',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)


# ==========================
# CATÁLOGOS
# ==========================

class TipoDocumentoViewSet(BaseViewSet):
    queryset = TipoDocumento.objects.filter(activo=True)
    serializer_class = TipoDocumentoSerializer


class MetodoPagoViewSet(BaseViewSet):
    queryset = MetodoPago.objects.filter(activo=True)
    serializer_class = MetodoPagoSerializer


class EspecialidadViewSet(BaseViewSet):
    queryset = Especialidad.objects.filter(activo=True)
    serializer_class = EspecialidadSerializer


# ==========================
# MÉDICOS Y PACIENTES
# ==========================

class MedicoViewSet(BaseViewSet):
    queryset = Medico.objects.filter(activo=True)
    serializer_class = MedicoSerializer


class PacienteViewSet(BaseViewSet):
    queryset = Paciente.objects.filter(activo=True)
    serializer_class = PacienteSerializer


# ==========================
# CITAS
# ==========================

class CitaViewSet(BaseViewSet):
    queryset = Cita.objects.filter(activo=True)
    serializer_class = CitaSerializer


# ==========================
# MEDICAMENTOS
# ==========================

class MedicamentoViewSet(BaseViewSet):
    queryset = Medicamento.objects.filter(activo=True)
    serializer_class = MedicamentoSerializer


class InventarioMedicamentoViewSet(BaseViewSet):
    queryset = InventarioMedicamento.objects.filter(activo=True)
    serializer_class = InventarioMedicamentoSerializer


# ==========================
# TRATAMIENTOS
# ==========================

class TratamientoViewSet(BaseViewSet):
    queryset = Tratamiento.objects.filter(activo=True)
    serializer_class = TratamientoSerializer


class TratamientoMedicamentoViewSet(BaseViewSet):
    queryset = TratamientoMedicamento.objects.filter(activo=True)
    serializer_class = TratamientoMedicamentoSerializer


# ==========================
# FACTURACIÓN
# ==========================

class FacturaViewSet(BaseViewSet):
    queryset = Factura.objects.filter(activo=True)
    serializer_class = FacturaSerializer


class DetalleFacturaViewSet(BaseViewSet):
    queryset = DetalleFactura.objects.filter(activo=True)
    serializer_class = DetalleFacturaSerializer


class PagoViewSet(BaseViewSet):
    queryset = Pago.objects.filter(activo=True)
    serializer_class = PagoSerializer