from django.contrib import admin
from .models import Anemia
from .models import Diabetes,CancerPulmonar,Paciente,Medico,Hospital
# Register your models here.
admin.site.register(Anemia)
admin.site.register(Diabetes)
admin.site.register(CancerPulmonar)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Hospital)