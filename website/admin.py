from django.contrib import admin
from models import Protein

class ProteinAdmin(admin.ModelAdmin):
	pass

admin.site.register(Protein, ProteinAdmin)
