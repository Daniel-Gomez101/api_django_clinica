
# Create your models here.
# ================================================================
#  CLÍNICA – models.py
#  Schema: clinica  |  Patrón: igual al proyecto tienda
#  Django 4.x +
# ================================================================

from django.db import models


# ================================================================
# 0. CATÁLOGOS
# ================================================================

class TipoDocumento(models.Model):
    codigo      = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=80)
    activo      = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."tipos_documento"'

    def __str__(self):
        return f"{self.codigo} – {self.descripcion}"


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    activo      = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."metodos_pago"'

    def __str__(self):
        return self.nombre


# ================================================================
# 1. ESPECIALIDADES
# ================================================================

class Especialidad(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo      = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."especialidades"'

    def __str__(self):
        return self.nombre


# ================================================================
# 2. MÉDICOS
# ================================================================

class Medico(models.Model):
    especialidad    = models.ForeignKey(
                        Especialidad, on_delete=models.PROTECT,
                        db_column='especialidad_id')
    nombres         = models.CharField(max_length=100)
    apellidos       = models.CharField(max_length=100)
    numero_licencia = models.CharField(max_length=50, unique=True)
    email           = models.CharField(max_length=150, unique=True, blank=True, null=True)
    telefono        = models.CharField(max_length=20,  blank=True, null=True)
    activo          = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."medicos"'

    def __str__(self):
        return f"Dr. {self.nombres} {self.apellidos}"


# ================================================================
# 3. PACIENTES
# ================================================================

SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]

TIPO_SANGRE_CHOICES = [
    ('A+','A+'), ('A-','A-'), ('B+','B+'), ('B-','B-'),
    ('AB+','AB+'), ('AB-','AB-'), ('O+','O+'), ('O-','O-'),
]

class Paciente(models.Model):
    numero_historia  = models.CharField(max_length=20, unique=True)
    tipo_documento   = models.ForeignKey(
                         TipoDocumento, on_delete=models.PROTECT,
                         db_column='tipo_documento_id')
    numero_documento = models.CharField(max_length=30, unique=True)
    nombres          = models.CharField(max_length=100)
    apellidos        = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo             = models.CharField(max_length=1, choices=SEXO_CHOICES)
    email            = models.CharField(max_length=150, blank=True, null=True)
    telefono         = models.CharField(max_length=20,  blank=True, null=True)
    direccion        = models.TextField(blank=True, null=True)
    tipo_sangre      = models.CharField(
                         max_length=5, choices=TIPO_SANGRE_CHOICES,
                         blank=True, null=True)
    alergias         = models.TextField(blank=True, null=True)
    activo           = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."pacientes"'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.numero_documento})"


# ================================================================
# 4. CITAS
# ================================================================

ESTADO_CITA_CHOICES = [
    ('programada',  'Programada'),
    ('confirmada',  'Confirmada'),
    ('en_curso',    'En Curso'),
    ('completada',  'Completada'),
    ('cancelada',   'Cancelada'),
    ('no_asistio',  'No Asistió'),
]

class Cita(models.Model):
    paciente         = models.ForeignKey(
                         Paciente, on_delete=models.PROTECT,
                         db_column='paciente_id')
    medico           = models.ForeignKey(
                         Medico, on_delete=models.PROTECT,
                         db_column='medico_id')
    fecha_hora       = models.DateTimeField()
    duracion_minutos = models.IntegerField(default=30)
    motivo           = models.TextField(blank=True, null=True)
    estado           = models.CharField(
                         max_length=20,
                         choices=ESTADO_CITA_CHOICES,
                         default='programada')
    notas            = models.TextField(blank=True, null=True)
    activo           = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."citas"'

    def __str__(self):
        return f"Cita #{self.pk} – {self.paciente} con {self.medico} ({self.fecha_hora:%Y-%m-%d %H:%M})"


# ================================================================
# 5. MEDICAMENTOS
# ================================================================

class Medicamento(models.Model):
    nombre_comercial = models.CharField(max_length=150)
    nombre_generico  = models.CharField(max_length=150, blank=True, null=True)
    presentacion     = models.CharField(max_length=100, blank=True, null=True)
    concentracion    = models.CharField(max_length=50,  blank=True, null=True)
    unidad           = models.CharField(max_length=30,  blank=True, null=True)
    precio_unitario  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    requiere_receta  = models.BooleanField(default=True)
    activo           = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."medicamentos"'

    def __str__(self):
        return f"{self.nombre_comercial} ({self.concentracion})"


# ================================================================
# 5b. INVENTARIO DE MEDICAMENTOS
# ================================================================

TIPO_MOVIMIENTO_CHOICES = [
    ('entrada', 'Entrada'),
    ('salida',  'Salida'),
    ('ajuste',  'Ajuste'),
]

class InventarioMedicamento(models.Model):
    medicamento      = models.ForeignKey(
                         Medicamento, on_delete=models.PROTECT,
                         db_column='medicamento_id')
    tipo_movimiento  = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad         = models.IntegerField()
    stock_resultante = models.IntegerField()
    motivo           = models.CharField(max_length=200, blank=True, null=True)
    referencia       = models.CharField(max_length=100, blank=True, null=True)
    activo           = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."inventario_medicamentos"'

    def __str__(self):
        return f"{self.tipo_movimiento} – {self.medicamento} ({self.cantidad})"


# ================================================================
# 6. TRATAMIENTOS
# ================================================================

ESTADO_TRATAMIENTO_CHOICES = [
    ('activo',      'Activo'),
    ('completado',  'Completado'),
    ('suspendido',  'Suspendido'),
]

class Tratamiento(models.Model):
    cita        = models.ForeignKey(
                    Cita, on_delete=models.PROTECT,
                    db_column='cita_id')
    diagnostico = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField(blank=True, null=True)
    estado       = models.CharField(
                     max_length=20,
                     choices=ESTADO_TRATAMIENTO_CHOICES,
                     default='activo')
    activo       = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."tratamientos"'

    def __str__(self):
        return f"Tratamiento #{self.pk} – {self.diagnostico[:40]}"


# ================================================================
# 7. TRATAMIENTO_MEDICAMENTOS  (N:M con atributos de prescripción)
# ================================================================

class TratamientoMedicamento(models.Model):
    tratamiento        = models.ForeignKey(
                           Tratamiento, on_delete=models.CASCADE,
                           db_column='tratamiento_id',
                           related_name='prescripciones')
    medicamento        = models.ForeignKey(
                           Medicamento, on_delete=models.PROTECT,
                           db_column='medicamento_id')
    dosis              = models.CharField(max_length=100)
    frecuencia         = models.CharField(max_length=100, blank=True, null=True)
    duracion_dias      = models.IntegerField(blank=True, null=True)
    cantidad_prescrita = models.IntegerField(default=1)
    instrucciones      = models.TextField(blank=True, null=True)
    activo             = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."tratamiento_medicamentos"'
        unique_together = [('tratamiento', 'medicamento')]

    def __str__(self):
        return f"{self.medicamento} → {self.tratamiento}"


# ================================================================
# 8. FACTURAS
# ================================================================

ESTADO_FACTURA_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('pagada',    'Pagada'),
    ('parcial',   'Parcial'),
    ('anulada',   'Anulada'),
    ('vencida',   'Vencida'),
]

class Factura(models.Model):
    paciente         = models.ForeignKey(
                         Paciente, on_delete=models.PROTECT,
                         db_column='paciente_id')
    cita             = models.ForeignKey(
                         Cita, on_delete=models.SET_NULL,
                         null=True, blank=True,
                         db_column='cita_id')
    numero_factura   = models.CharField(max_length=30, unique=True)
    fecha_emision    = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    subtotal         = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto         = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total            = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado           = models.CharField(
                         max_length=20,
                         choices=ESTADO_FACTURA_CHOICES,
                         default='pendiente')
    notas            = models.TextField(blank=True, null=True)
    activo           = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."facturas"'

    def __str__(self):
        return f"{self.numero_factura} – {self.paciente} (${self.total})"


# ================================================================
# 9. DETALLE_FACTURAS
# ================================================================

TIPO_DETALLE_CHOICES = [
    ('consulta',      'Consulta'),
    ('procedimiento', 'Procedimiento'),
    ('medicamento',   'Medicamento'),
    ('laboratorio',   'Laboratorio'),
    ('otro',          'Otro'),
]

class DetalleFactura(models.Model):
    factura         = models.ForeignKey(
                        Factura, on_delete=models.CASCADE,
                        db_column='factura_id',
                        related_name='detalles')
    descripcion     = models.CharField(max_length=200)
    tipo            = models.CharField(max_length=20, choices=TIPO_DETALLE_CHOICES, default='consulta')
    cantidad        = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_linea = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # subtotal_linea es calculado en BD (GENERATED ALWAYS), solo lectura en Django
    subtotal_linea  = models.DecimalField(
                        max_digits=10, decimal_places=2,
                        editable=False, blank=True, null=True)
    activo          = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."detalle_facturas"'

    def __str__(self):
        return f"{self.descripcion} x{self.cantidad} = ${self.subtotal_linea}"


# ================================================================
# 10. PAGOS
# ================================================================

class Pago(models.Model):
    factura        = models.ForeignKey(
                       Factura, on_delete=models.PROTECT,
                       db_column='factura_id',
                       related_name='pagos')
    metodo_pago    = models.ForeignKey(
                       MetodoPago, on_delete=models.PROTECT,
                       db_column='metodo_pago_id')
    fecha_pago     = models.DateTimeField()
    monto          = models.DecimalField(max_digits=12, decimal_places=2)
    referencia     = models.CharField(max_length=100, blank=True, null=True)
    notas          = models.TextField(blank=True, null=True)
    activo         = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True,     db_column='fecha_modificacion')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."pagos"'

    def __str__(self):
        return f"Pago #{self.pk} – {self.factura.numero_factura} (${self.monto})"