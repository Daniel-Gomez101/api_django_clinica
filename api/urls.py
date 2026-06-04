from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'tipos-documento', TipoDocumentoViewSet)
router.register(r'metodos-pago', MetodoPagoViewSet)
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'inventario-medicamentos', InventarioMedicamentoViewSet)
router.register(r'tratamientos', TratamientoViewSet)
router.register(r'tratamiento-medicamentos', TratamientoMedicamentoViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'detalle-facturas', DetalleFacturaViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]