from django.core.validators import MinValueValidator
from django.db import models


class Medicamento(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "farmacia_medicamento"
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ["name"]

    def __str__(self):
        return self.name
