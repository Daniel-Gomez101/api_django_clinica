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

from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Clinica API",
      default_version='v1',
      description="API para la gestion clinica",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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

urlpatterns = [
    path('', include(router.urls)),

    #swagger

    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'
    ),

    
]