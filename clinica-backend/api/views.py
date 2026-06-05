from io import BytesIO
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from openpyxl import Workbook
import logging

from .permissions import IsAdminOrReadOnly
from .models import (
    TipoDocumento, MetodoPago, Especialidad, Medico, Paciente, 
    Cita, Medicamento, InventarioMedicamento, Tratamiento, 
    TratamientoMedicamento, Factura, DetalleFactura, Pago
)
from .serializers import (
    TipoDocumentoSerializer, MetodoPagoSerializer, EspecialidadSerializer, 
    MedicoSerializer, PacienteSerializer, CitaSerializer, 
    MedicamentoSerializer, InventarioMedicamentoSerializer, 
    TratamientoSerializer, TratamientoMedicamentoSerializer, 
    FacturaSerializer, DetalleFacturaSerializer, PagoSerializer, 
    CitaDetalleSerializer, TratamientoMedicamentoDetalleSerializer, 
    DetalleFacturaDetalleSerializer
)

# Logger configurado para mostrar actividad en consola
logger = logging.getLogger('django')

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({'success': True, 'status': 200, 'message': 'Petición exitosa', 'data': serializer.data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'success': True, 'status': 201, 'message': 'Registro creado exitosamente', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'status': 400, 'message': 'Error al crear el registro', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # --- MÉTODO PARA AUDITORÍA (ÍTEM 8) ---
    def perform_create(self, serializer):
        serializer.save(usuario_creacion=self.request.user)
        logger.info(f"Usuario {self.request.user} creó un registro en {self.queryset.model.__name__}")

    def perform_update(self, serializer):
        serializer.save(usuario_modificacion=self.request.user)
        logger.info(f"Usuario {self.request.user} modificó un registro en {self.queryset.model.__name__}")

    # --- MÉTODO DE EXPORTACIÓN DIRECTA (DESCARGA) ---
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar_excel(self, request):
        nombre_modelo = self.queryset.model.__name__.lower()
        wb = Workbook()
        ws = wb.active
        ws.title = f"Reporte {nombre_modelo.capitalize()}"
        campos = [campo.name for campo in self.queryset.model._meta.fields]
        ws.append(campos) 
        queryset_filtrado = self.filter_queryset(self.get_queryset())
        for objeto in queryset_filtrado:
            fila = []
            for campo in campos:
                valor = getattr(objeto, campo, '')
                if hasattr(valor, 'id'): valor = valor.id
                elif hasattr(valor, 'strftime'): valor = valor.strftime('%Y-%m-%d %H:%M')
                fila.append(valor)
            ws.append(fila)
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="reporte_{nombre_modelo}.xlsx"'
        return response

# --- VIEWSETS ESPECÍFICOS ---
class TipoDocumentoViewSet(BaseViewSet):
    queryset = TipoDocumento.objects.filter(activo=True)
    serializer_class = TipoDocumentoSerializer

class MetodoPagoViewSet(BaseViewSet):
    queryset = MetodoPago.objects.filter(activo=True)
    serializer_class = MetodoPagoSerializer

class EspecialidadViewSet(BaseViewSet):
    queryset = Especialidad.objects.filter(activo=True)
    serializer_class = EspecialidadSerializer

class MedicoViewSet(BaseViewSet):
    queryset = Medico.objects.filter(activo=True)
    serializer_class = MedicoSerializer

class PacienteViewSet(BaseViewSet):
    queryset = Paciente.objects.filter(activo=True)
    serializer_class = PacienteSerializer

class CitaViewSet(BaseViewSet):
    queryset = Cita.objects.filter(activo=True)
    serializer_class = CitaSerializer
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']: return CitaDetalleSerializer
        return super().get_serializer_class()

class MedicamentoViewSet(BaseViewSet):
    queryset = Medicamento.objects.filter(activo=True)
    serializer_class = MedicamentoSerializer

class InventarioMedicamentoViewSet(BaseViewSet):
    queryset = InventarioMedicamento.objects.filter(activo=True)
    serializer_class = InventarioMedicamentoSerializer

class TratamientoViewSet(BaseViewSet):
    queryset = Tratamiento.objects.filter(activo=True)
    serializer_class = TratamientoSerializer

class TratamientoMedicamentoViewSet(BaseViewSet):
    queryset = TratamientoMedicamento.objects.filter(activo=True)
    serializer_class = TratamientoMedicamentoSerializer
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']: return TratamientoMedicamentoDetalleSerializer
        return super().get_serializer_class()

class FacturaViewSet(BaseViewSet):
    queryset = Factura.objects.filter(activo=True)
    serializer_class = FacturaSerializer

class DetalleFacturaViewSet(BaseViewSet):
    queryset = DetalleFactura.objects.filter(activo=True)
    serializer_class = DetalleFacturaSerializer
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']: return DetalleFacturaDetalleSerializer
        return super().get_serializer_class()

class PagoViewSet(BaseViewSet):
    queryset = Pago.objects.filter(activo=True)
    serializer_class = PagoSerializer