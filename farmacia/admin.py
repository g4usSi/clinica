from django.contrib import admin

from .models import Medicamento


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("name", "stock", "price")
    search_fields = ("name",)
