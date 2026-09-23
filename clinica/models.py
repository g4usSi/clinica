from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Usuario del sistema.

    Reemplaza la tabla `user` del SQL original.
    Django ya proporciona:
    - username
    - password
    - email
    - is_active
    - is_staff
    - is_superuser
    - date_joined
    """

    name = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["username"]

    def __str__(self):
        return self.username


class Pacient(models.Model):
    """
    Paciente.
    """

    GENDER_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]

    no = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, blank=True,)

    day_of_birth = models.DateField(null=True, blank=True,  )

    email = models.EmailField(
        max_length=255,
        blank=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    phone = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.CharField(
        max_length=255,
        blank=True,
    )

    sick = models.TextField(
        max_length=500,
        blank=True,
    )

    medicaments = models.TextField(
        max_length=500,
        blank=True,
    )

    alergy = models.TextField(
        max_length=500,
        blank=True,
    )

    is_favorite = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "pacient"
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["lastname", "name"]

    def __str__(self):
        return f"{self.name} {self.lastname}"


class Category(models.Model):
    """
    Categoría de médicos.
    """

    name = models.CharField(
        max_length=200,
    )

    class Meta:
        db_table = "category"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Medic(models.Model):
    """
    Médico.
    """

    GENDER_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]

    no = models.CharField(
        max_length=50,
        blank=True,
    )

    name = models.CharField(
        max_length=50,
    )

    lastname = models.CharField(
        max_length=50,
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
    )

    day_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        max_length=255,
        blank=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    phone = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="medics",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "medic"
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ["lastname", "name"]

    def __str__(self):
        return f"Dr. {self.name} {self.lastname}"


class Status(models.Model):
    """
    Estado de una reserva.

    Valores originales:
    1 - Pendiente
    2 - Aplicada
    3 - No asistió
    4 - Cancelada
    """

    name = models.CharField(
        max_length=100,
    )

    class Meta:
        db_table = "status"
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Payment(models.Model):
    """
    Estado del pago.

    Valores originales:
    1 - Pendiente
    2 - Pagado
    3 - Anulado
    """

    name = models.CharField(
        max_length=100,
    )

    class Meta:
        db_table = "payment"
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """
    Reserva / cita médica.
    """

    class StatusChoices(models.IntegerChoices):
        PENDIENTE = 1, "Pendiente"
        APLICADA = 2, "Aplicada"
        NO_ASISTIO = 3, "No asistió"
        CANCELADA = 4, "Cancelada"

    class PaymentChoices(models.IntegerChoices):
        PENDIENTE = 1, "Pendiente"
        PAGADO = 2, "Pagado"
        ANULADO = 3, "Anulado"

    title = models.CharField(
        max_length=100,
    )

    note = models.TextField(
        blank=True,
    )

    message = models.TextField(
        blank=True,
    )

    date_at = models.DateField(
        null=True,
        blank=True,
    )

    time_at = models.TimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    pacient = models.ForeignKey(
        Pacient,
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    symtoms = models.TextField(
        blank=True,
    )

    sick = models.TextField(
        blank=True,
    )

    medicaments = models.TextField(
        blank=True,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    medic = models.ForeignKey(
        Medic,
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    is_web = models.BooleanField(
        default=False,
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name="reservations",
        default=1,
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="reservations",
        default=1,
    )

    class Meta:
        db_table = "reservation"
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-date_at", "-time_at"]

        indexes = [
            models.Index(
                fields=["date_at", "time_at"],
                name="reservation_date_time_idx",
            ),
            models.Index(
                fields=["pacient"],
                name="reservation_pacient_idx",
            ),
            models.Index(
                fields=["medic"],
                name="reservation_medic_idx",
            ),
            models.Index(
                fields=["status"],
                name="reservation_status_idx",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.pacient}"


class Setting(models.Model):
    """
    Configuraciones generales del sistema.
    """

    KIND_CHOICES = [
        (1, "Texto"),
        (2, "Número"),
        (3, "Booleano"),
        (4, "JSON"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    label = models.CharField(
        max_length=255,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=1,
    )

    val = models.TextField(
        blank=True,
    )

    cfg_id = models.IntegerField(
        default=1,
    )

    class Meta:
        db_table = "setting"
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"
        ordering = ["name"]

    def __str__(self):
        return f"{self.label}: {self.val}"