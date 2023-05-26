from django.db import models
from django.contrib.auth.models import User
class Hospital(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correoElectronico = models.EmailField(unique=True)  # Dirección del hospital
    telefono = models.CharField(max_length=20) 
    # Otros campos de Hospital
    def __str__(self):
        return self.nombre
class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correoElectronico = models.EmailField(unique=True)
    numero_celular = models.CharField(max_length=20, unique=True)
    ci = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    edad = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    direccion = models.CharField(max_length=200)
    numero_celular = models.CharField(max_length=20, unique=True)
    ci = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
# Create your models here.
class Project(models.Model):
    title= models.CharField(max_length=200)
    description= models.TextField()
    technology=models.CharField(max_length=200)
    created_at= models.DateTimeField(auto_now_add=True)
class Anemia(models.Model):
    genero = models.IntegerField(default=0)
    Hemogobina= models.CharField(max_length=100)
    MCH=models.CharField(max_length=100)
    MCHC=models.CharField(max_length=100)
    MCV=models.CharField(max_length=100)
    Resultado=models.CharField(max_length=100)
    def __str__(self):
        return self.Resultado
class Diabetes(models.Model):
    genero = models.IntegerField(default=0)
    hipertencion=models.CharField(max_length=100)
    cardiopatia=models.CharField(max_length=100)
    fumador=models.CharField(max_length=100)
    MCI=models.CharField(max_length=100)
    nivelesHemoglobina=models.CharField(max_length=100)
    nivelGlucosa=models.CharField(max_length=100)
    edad=models.IntegerField(default=0)
    resultado=models.CharField(max_length=100)
    def __str__(self):
        return self.fumador
class  CancerPulmonar(models.Model):
    edad=models.IntegerField()
    Genero=models.IntegerField()
    ConsumoAlcohol=models.IntegerField()
    AlergiaPolvo=models.IntegerField()
    RegistroGenetico=models.IntegerField()
    EnfermedadPulmonar=models.IntegerField()
    DietaEquilibrada=models.IntegerField()
    Obesidad=models.IntegerField()
    Tabaquismo=models.IntegerField()
    FumadorPasivo=models.IntegerField()
    DolorPecho=models.IntegerField()
    TosConSangre=models.IntegerField()
    fatiga=models.IntegerField()
    PerdidaPeso=models.IntegerField()
    DificultadRespirar=models.IntegerField()
    Sibilancia=models.IntegerField()
    DificultadTragar=models.IntegerField()
    TosSeca=models.IntegerField()
    resultados=models.CharField(max_length=100)
class HistorialPaciente(models.Model):    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    anemia = models.ForeignKey(Anemia, null=True, blank=True, on_delete=models.SET_NULL)
    diabetes = models.ForeignKey(Diabetes, null=True, blank=True, on_delete=models.SET_NULL)
    cancer_pulmonar = models.ForeignKey(CancerPulmonar, null=True, blank=True, on_delete=models.SET_NULL)