from django.db import models
from django.conf import settings

# ================================================================
# MODELO BASE DE AUDITORÍA (Ítem 8)
# ================================================================

class ModeloBaseAuditoria(models.Model):
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="%(class)s_creador"
    )
    usuario_modificacion = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="%(class)s_modificador"
    )

    class Meta:
        abstract = True

# ================================================================
# CATÁLOGOS
# ================================================================

class TipoDocumento(ModeloBaseAuditoria, models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=80)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."tipos_documento"'

    def __str__(self):
        return self.codigo


class MetodoPago(ModeloBaseAuditoria, models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."metodos_pago"'

    def __str__(self):
        return self.nombre


# ================================================================
# ESPECIALIDADES, MÉDICOS Y PACIENTES
# ================================================================

class Especialidad(ModeloBaseAuditoria, models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."especialidades"'

    def __str__(self):
        return self.nombre


class Medico(ModeloBaseAuditoria, models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_licencia = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."medicos"'

    def __str__(self):
        return f"Dr. {self.nombres} {self.apellidos}"


class Paciente(ModeloBaseAuditoria, models.Model):
    numero_historia = models.CharField(max_length=20, unique=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    numero_documento = models.CharField(max_length=30, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    tipo_sangre = models.CharField(max_length=5, blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."pacientes"'

    def __str__(self):
        return self.nombres


# ================================================================
# CITAS, MEDICAMENTOS Y TRATAMIENTOS
# ================================================================

class Cita(ModeloBaseAuditoria, models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField()
    duracion_minutos = models.IntegerField(default=30)
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, default='programada')
    notas = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."citas"'


class Medicamento(ModeloBaseAuditoria, models.Model):
    nombre_comercial = models.CharField(max_length=150)
    nombre_generico = models.CharField(max_length=150, blank=True, null=True)
    concentracion = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."medicamentos"'


class InventarioMedicamento(ModeloBaseAuditoria, models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    stock_resultante = models.IntegerField()
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."inventario_medicamentos"'


class Tratamiento(ModeloBaseAuditoria, models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.PROTECT)
    diagnostico = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='activo')
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."tratamientos"'


class TratamientoMedicamento(ModeloBaseAuditoria, models.Model):
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dosis = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."tratamiento_medicamentos"'


# ================================================================
# FACTURACIÓN Y PAGOS
# ================================================================

class Factura(ModeloBaseAuditoria, models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    numero_factura = models.CharField(max_length=30, unique=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, default='pendiente')
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."facturas"'


class DetalleFactura(ModeloBaseAuditoria, models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_linea = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."detalle_facturas"'


class Pago(ModeloBaseAuditoria, models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    fecha_pago = models.DateTimeField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, db_column='fecha_modificacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = '"clinica"."pagos"'