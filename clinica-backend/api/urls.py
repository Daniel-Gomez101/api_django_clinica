from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    TipoDocumentoViewSet, 
    MetodoPagoViewSet, 
    EspecialidadViewSet,
    MedicoViewSet, 
    PacienteViewSet, 
    CitaViewSet,
    MedicamentoViewSet,
    InventarioMedicamentoViewSet,
    TratamientoViewSet,
    TratamientoMedicamentoViewSet,
    FacturaViewSet,
    DetalleFacturaViewSet,
    PagoViewSet
)

# 1. El router se encarga de tus endpoints clínicos
router = DefaultRouter()

router.register(r'tipos_documento', TipoDocumentoViewSet)
router.register(r'metodos_pago', MetodoPagoViewSet)
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'inventario_medicamentos', InventarioMedicamentoViewSet)
router.register(r'tratamientos', TratamientoViewSet)
router.register(r'tratamiento_medicamentos', TratamientoMedicamentoViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'detalle_facturas', DetalleFacturaViewSet)
router.register(r'pagos', PagoViewSet)

# 2. Solo exportamos las rutas del router
urlpatterns = [
    path('', include(router.urls)),
]